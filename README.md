# Ruppenthal Scraper V1.0 Documentation

## Overview
This Python script, called "Ruppenthal Scraper V1.0," is designed to scrape data from a website and update a Google Sheets document with the scraped information. It uses the Selenium library to interact with the website and BeautifulSoup for parsing. The script is primarily intended for handling a particular website, ruppenthal.com/shop, and it performs actions to gather data and update a Google Sheets document with the relevant information.

## Requirements
- Python 3.x
- Chrome browser
- Selenium library
- Chromedriver autoinstaller
- BeautifulSoup library
- pygsheets library
- Google API credentials (credentials.json) for accessing the Google Sheets document

## Usage
1. Before running the script, make sure to install the required libraries:
```bash
pip install selenium chromedriver_autoinstaller beautifulsoup4 pygsheets
```

2. Ensure you have the Google API credentials (credentials.json) in the same directory as the script. This file is necessary to access the Google Sheets document.

3. Update the `email` and `password` variables in the script with the correct login credentials for the ruppenthal.com/shop website.

4. The script will read item codes from a Google Sheets document named "products." It will search for each item code on the ruppenthal.com/shop website, extract relevant information, and update the Google Sheets document with the scraped data.

5. Execute the script:
```bash
python ruppenthal_scraper.py
```

6. After running the script, it will log the time taken to complete the scraping process in the "time_logs.txt" file.

## Script Functionality
1. The script begins by displaying a start screen with the script's name and version.

2. The `log_time_to_file` function logs the time taken to complete the script's execution in minutes to the "time_logs.txt" file.

3. The `main` function is the entry point of the script.

4. The script uses Selenium and Chromedriver to interact with the ruppenthal.com/shop website, login, and search for item codes.

5. It utilizes BeautifulSoup to parse the website's HTML and extract relevant data.

6. The script uses pygsheets to authenticate and open the Google Sheets document for updating.

7. It iterates through the item codes in the "products" sheet and updates the Google Sheets document with the item's information if it exists on the website. If an item is not found, it logs it as a non-existing item.

8. After processing all item codes, the script switches the website's shop using a button and repeats the process for the non-existing items.

## Note
- Ensure you have a stable internet connection while running the script, as it relies on web scraping and interacting with external websites.

- Make sure to comply with the website's terms of service and avoid overloading their servers with too many requests. Use the script responsibly and with proper authorization.

- The script can be adapted to work with other websites by modifying the specific locators and elements according to the new website's structure.

- It is recommended to run the script in a virtual environment to avoid conflicts with existing packages and dependencies.

- Before updating any data in the Google Sheets document, make sure to thoroughly test the script on a small set of data to avoid any unintended modifications.

- Please refer to the ruppenthal.com/shop website's robots.txt or terms of service to ensure you are allowed to scrape data from the site.

- This script was last tested with Python 3.x and Chrome browser. If you encounter any issues, consider checking for updates and compatibility with the required libraries.

- The script assumes that the Google Sheets document contains a "products" sheet with the item codes in the third column (C) and additional columns for relevant information. Ensure the sheet layout matches the script's assumptions.

## Disclaimer
Use this script responsibly and at your own risk. The author is not responsible for any misuse or unintended consequences resulting from the use of this script. Always review and comply with the website's terms of service and legal guidelines before scraping data.
