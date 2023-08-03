from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import re


def display_start_screen():
    design = '''
==================================
  Ruppenthal Scraper V1.0
==================================

Welcome to the script! Running Now...
'''
    print(design)

# Call the function to display the start screen
display_start_screen()


def log_time_to_file(file_path, time_taken):
    with open(file_path, 'a') as file:
        file.write(f"{time_taken} minutes\n\n")

def main():
    # File path to store the time logs
    file_path = "time_logs.txt"

    # Measure the start time
    start_time = time.time()




    def extract_numbers(text):
        number = re.findall(r'\d+(?:,\d+)?', text)
        numbers = '\n'.join(number)
        return numbers

    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)


    driver.get("https://ruppenthal.com/shop")

    username_input = driver.find_element(By.NAME, 'username')
    username_input.send_keys("ruppenthal@daniel-abt.de")

    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys("60Diamanten60")

    login_button = driver.find_element("xpath", "//button[contains(@class, 'uk-float-left') and contains(@class, 'btn-primary') and contains(@class, 'btn-block')]")
    login_button.click()

    import pygsheets

    # Authenticate and open the Google Sheets document
    gc = pygsheets.authorize(service_file='credentials.json')
    doc_url = 'https://docs.google.com/spreadsheets/d/114bor0O_M5Y_FXdcZUsXd0zIeT_ULvsmrmMIzabNaSU/edit#gid=573685590'
    doc = gc.open_by_url(doc_url)

    # Select the desired sheet by name
    sheet_name = 'products'
    sheet = doc.worksheet_by_title(sheet_name)

    # Get all values in the second column "rupid"
    column_values = sheet.get_col(3, include_tailing_empty=False)[1:]

    # Filter out empty values and convert to item codes
    item_codes = [value for value in column_values if value]
    existing_items = []
    non_existing_items = []

    for item_code in item_codes:
        search_input = driver.find_element(By.ID, 'searchField')
        search_input.clear()
        search_input.send_keys(item_code)

        search_button = driver.find_element(By.CSS_SELECTOR, 'span.searchGo')
        action = ActionChains(driver)
        action.move_to_element(search_button).click().perform()
        time.sleep(5)
        image_urls = []
        try:
            item_element = driver.find_element(By.CSS_SELECTOR, '.item.shop-1.uk-first-column')
            item_id = item_element.get_attribute("data-id")
            fullstockname = "span.inventoryAmount-" + str(item_id)
            stock_quantity = driver.find_element(By.CSS_SELECTOR, fullstockname).text
            print(f"Item {item_code} exists")
            existing_items.append(item_code)
            image_elements = driver.find_elements(By.CSS_SELECTOR, ".imgbox.ratio-productimg.uk-width-1-1.uk-inline-clip a")
            for image_element in image_elements:
                image_url = image_element.get_attribute("href")
                image_urls.append(image_url)
            image_urls_string = ", ".join(image_urls)
            price_element = driver.find_element(By.CSS_SELECTOR, ".pricebox.uk-box-shadow-small.pricebox-article.inventTyp")

            element_name = driver.find_element(By.CSS_SELECTOR, "h3.uk-margin-remove.testh3")
            name_text = element_name.text

            prices = []
            price_elements = price_element.find_elements(By.CSS_SELECTOR, ".price")
            print(price_element)
            print(price_elements)
            for price_element in price_elements:
                price = extract_numbers(price_element.text)
                print(price)
                price = price.replace(",", ".")
                prices.append(float(price))
            minimumprice = str(min(prices)).replace(".", ",")
            real_value = minimumprice
            try:
                descript = driver.find_element(By.CSS_SELECTOR, 'div.uk-margin-small-top p[data-attribname="descript"]')
                descript_attribute = descript.text
            except NoSuchElementException:
                descript_attribute = ''

            span_elements = driver.find_elements(By.CSS_SELECTOR, "p span.additionalData")
            for span_element in span_elements:
                attrib_name = span_element.get_attribute("data-attribname")

                cell = next((cell for cell in sheet.find(item_code)), None)
                row, col = cell.row, cell.col if cell else (None, None)
                header_values = sheet.get_row(1, include_tailing_empty=False)

                if attrib_name == "ZUSATZ1":
                    zusatz1 = span_element.text
                    print(zusatz1)
                    zusatz1_index = header_values.index("zusatz1") + 1
                    sheet.update_value((row, zusatz1_index), zusatz1)
                if attrib_name == "GROSBEZ":
                    grosbez = span_element.text
                    print(grosbez)
                    grosbez_index = header_values.index("grosbez") + 1
                    sheet.update_value((row, grosbez_index), grosbez)
                if attrib_name == "FARBE":
                    farbe = span_element.text
                    print(farbe)
                    farbe_index = header_values.index("farbe") + 1
                    sheet.update_value((row, farbe_index), farbe)
                if attrib_name == "REINHTXT":
                    reinhtxt = span_element.text
                    print(reinhtxt)
                    reinhtxt_index = header_values.index("reinhtxt") + 1
                    sheet.update_value((row, reinhtxt_index), reinhtxt)
                if attrib_name == "size":
                    size = span_element.text
                    print(size)
                    size_index = header_values.index("size") + 1
                    sheet.update_value((row, size_index), size)
                if attrib_name == "ZUSATZ2":
                    zusatz2 = span_element.text
                    print(zusatz2)
                    zusatz2_index = header_values.index("zusatz2") + 1
                    sheet.update_value((row, zusatz2_index), zusatz2)


            print(name_text)
            cells = sheet.find(item_code)
            if cells:
                for cell in cells:
                    row = cell.row
                    column_name = 'rupimg'
                    rupprice = 'rupprice'
                    rupname = 'rupname'
                    descript_column = 'descript'
                    stock_quantity_column = 'stock_quantity'
                    sshop = 'sshop'
                    header_values = sheet.get_row(1, include_tailing_empty=False)

                    column_index = header_values.index(column_name) + 1
                    rupprice_index = header_values.index(rupprice) + 1
                    rupname_index = header_values.index(rupname) + 1
                    descript_index = header_values.index(descript_column) + 1
                    stock_quantity_index = header_values.index(stock_quantity_column) + 1
                    sshop_index = header_values.index(sshop) + 1

                    sheet.update_value((row, column_index), image_urls_string)
                    sheet.update_value((row, rupprice_index), real_value)
                    sheet.update_value((row, rupname_index), name_text)
                    sheet.update_value((row, descript_index), descript_attribute)
                    sheet.update_value((row, stock_quantity_index), stock_quantity)
                    sheet.update_value((row, sshop_index), "Ruppenthal")



        except NoSuchElementException:
            print(f"Item {item_code} does not exist")
            non_existing_items.append(item_code)



        search_input.clear()
        image_urls = []




    print("Existing items:", existing_items)
    print("Non-existing items:", non_existing_items)
    # Find the button element using CSS selector
    button = driver.find_element(By.CSS_SELECTOR, 'a.btn.only-icon.btn-ernst-stein.changeShop')

    # Click the button
    button.click()
    not_existing = []
    time.sleep(5)
    for non_existing_item in non_existing_items:
        search_input = driver.find_element(By.ID, 'searchField')
        search_input.clear()
        search_input.send_keys(non_existing_item)

        search_button = driver.find_element(By.CSS_SELECTOR, 'span.searchGo')
        action = ActionChains(driver)
        action.move_to_element(search_button).click().perform()
        time.sleep(5)
        try:
            item_element = driver.find_element(By.CSS_SELECTOR, '.item.shop-2.uk-first-column')
            item_id = item_element.get_attribute("data-id")
            fullstockname = "span.inventoryAmount-" + str(item_id)
            stock_quantity = driver.find_element(By.CSS_SELECTOR, fullstockname).text
            print(f"Item {non_existing_item} exists")
            not_existing.append(non_existing_item)
            image_elements = driver.find_elements(By.CSS_SELECTOR, ".imgbox.ratio-productimg.uk-width-1-1.uk-inline-clip a")
            for image_element in image_elements:
                image_url = image_element.get_attribute("href")
                image_urls.append(image_url)
            image_urls_string = ", ".join(image_urls)
            price_element = driver.find_element(By.CSS_SELECTOR, ".pricebox.uk-box-shadow-small.pricebox-article.inventTyp")

            element_name = driver.find_element(By.CSS_SELECTOR, "h3.uk-margin-remove.testh3")
            name_text = element_name.text

            prices = []
            price_elements = price_element.find_elements(By.CSS_SELECTOR, ".price")
            print(price_element)
            print(price_elements)
            for price_element in price_elements:
                price = extract_numbers(price_element.text)
                print(price)
                price = price.replace(",", ".")
                prices.append(float(price))
            minimumprice = str(min(prices)).replace(".", ",")
            real_value = minimumprice
            try:
                descript = driver.find_element(By.CSS_SELECTOR, 'div.uk-margin-small-top p[data-attribname="descript"]')
                descript_attribute = descript.text
            except NoSuchElementException:
                descript_attribute = ''

            span_elements = driver.find_elements(By.CSS_SELECTOR, "p span.additionalData")
            for span_element in span_elements:
                attrib_name = span_element.get_attribute("data-attribname")

                cell = next((cell for cell in sheet.find(non_existing_item)), None)
                row, col = cell.row, cell.col if cell else (None, None)
                header_values = sheet.get_row(1, include_tailing_empty=False)

                if attrib_name == "ZUSATZ1":
                    zusatz1 = span_element.text
                    print(zusatz1)
                    zusatz1_index = header_values.index("zusatz1") + 1
                    sheet.update_value((row, zusatz1_index), zusatz1)
                if attrib_name == "GROSBEZ":
                    grosbez = span_element.text
                    print(grosbez)
                    grosbez_index = header_values.index("grosbez") + 1
                    sheet.update_value((row, grosbez_index), grosbez)
                if attrib_name == "FARBE":
                    farbe = span_element.text
                    print(farbe)
                    farbe_index = header_values.index("farbe") + 1
                    sheet.update_value((row, farbe_index), farbe)
                if attrib_name == "REINHTXT":
                    reinhtxt = span_element.text
                    print(reinhtxt)
                    reinhtxt_index = header_values.index("reinhtxt") + 1
                    sheet.update_value((row, reinhtxt_index), reinhtxt)
                if attrib_name == "size":
                    size = span_element.text
                    print(size)
                    size_index = header_values.index("size") + 1
                    sheet.update_value((row, size_index), size)
                if attrib_name == "ZUSATZ2":
                    zusatz2 = span_element.text
                    print(zusatz2)
                    zusatz2_index = header_values.index("zusatz2") + 1
                    sheet.update_value((row, zusatz2_index), zusatz2)


            print(name_text)
            cells = sheet.find(non_existing_item)
            if cells:
                for cell in cells:
                    row = cell.row
                    column_name = 'rupimg'
                    rupprice = 'rupprice'
                    rupname = 'rupname'
                    descript_column = 'descript'
                    stock_quantity_column = 'stock_quantity'
                    sshop = 'sshop'
                    header_values = sheet.get_row(1, include_tailing_empty=False)

                    column_index = header_values.index(column_name) + 1
                    rupprice_index = header_values.index(rupprice) + 1
                    rupname_index = header_values.index(rupname) + 1
                    descript_index = header_values.index(descript_column) + 1
                    stock_quantity_index = header_values.index(stock_quantity_column) + 1
                    sshop_index = header_values.index(sshop) + 1

                    sheet.update_value((row, column_index), image_urls_string)
                    sheet.update_value((row, rupprice_index), real_value)
                    sheet.update_value((row, rupname_index), name_text)
                    sheet.update_value((row, descript_index), descript_attribute)
                    sheet.update_value((row, stock_quantity_index), stock_quantity)
                    sheet.update_value((row, sshop_index), "Ernst Stein")



        except NoSuchElementException:
            print(f"Item {non_existing_item} does not exist")


    end_time = time.time()

    # Calculate the time taken in minutes
    time_taken = (end_time - start_time) / 60

    # Log the time taken to the file
    log_time_to_file(file_path, time_taken)

if __name__ == '__main__':
    main()