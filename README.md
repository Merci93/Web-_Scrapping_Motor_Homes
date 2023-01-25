# Scraping Camping World
## Description

A web scraping task to collect nationwide listings of "Motorhomes for Sale" that are running on Diesel. The script, developed with Selenium (a web automation tool) and BeatufulSoup, crawls through the [Camping World](https://rv.campingworld.com/rvclass/motorhome-rvs) web page collecting details of Motorhomes that meet specific criteria, in this case: Motor homes that are running on Diesel. The script is developed such that it is straightforward to change and collect data for a different fuel type by changing the `click XPATH` for the fuel type selection. The automated script runs through the pages, scanning each RV Motorhome, and collecting the required information.

Selenium `click` method is employed in switching between pages until the last page. A `try except` method was applied to handle `KeyError` and `NoSuchElementException` for Motorhomes with prices above $300,000 with missing horse power data, and for breaking out of the loop at the last page, respectively.

## Data
The data captured include:
- Vehicle name
- Stock number
- Status (New or Used)
- Dealership location
- Sleeps (Number of sleeps)
- Sales price (USD)
- Horse power (for MotorHomes with sales price above $300,000)

## Requirements:
- regular expression: install with _pip install re_ in command line or _!pip install re_ in jupyter notebook
- pandas
- selenium
- time
- BeautifulSoup (bs4)
- chromedriver executable

## Files description
- **scrape (.py and .ipynb)**: Scrapes the above listed information about RV motors from the webpage. The _.py_ file can be run via anaconda command line interface (in Windows) or terminal (in Linux/Ubuntu), and the _.ipynb_ file on jupyter notebook or jupyter lab.
- **chromedriver.exe**: A tool for automated testing of webapps, with capabilities for page navigations and user input execution. [Download Chrome Webdriver](https://sites.google.com/chromium.org/driver/downloads?authuser=0).
>NOTE: The chromedriver.exe should be downloaded and stored in any location of your choice, preferably same location as the scripts (.py and .ipynb) and the path copied into `driver_path` in the scripts. The driver helps for speedy execution and collection of data. The section `driver = webdriver.Chrome()` performs same task as the chromedriver.exe, but with lengthy execution time.

## Approach
- Main function _scrape_data_ taking one argument: `url`.
- Instantiate the chrome webdriver
- Created an empty list to hold extracted data.
- Created a `while loop` to iterate through all the pages available. In this case, there are 51 pages. Selenium `click` method was employed to click on the `next page` item after all the data in the current page are collected. The loop breaks at the end of the page when the `NoSuchElementException` is encountered.
- Container frames in each page are collected.
- A `for loop` is used to iterate through the container frames collecting the data for each MotorHome: name, status, price, location, length, sleeps and stock number.
- For MotorHomes with price above $300,000, the `view details` is clicked and the MotorHome horse power is collected from the motor specifications.
- Once the container on a current page is exhausted, the loop moves to the next page. This process continues until the last page when the loop terminates. The collected data is transformed into a dataframe using `pandas.DataFrame` method, duplicates dropped and finally saved as a `csv` file using the `.to_csv` pandas method. The file is saved in the same location as the script.

>PS: This approach can work for any web scraping activity but the codes in the scripts provided has been tailored to suit the web page being scraped and also the requirements of the task. Also the time taken to complete extracting, transforming, loading data and saving CSV file is dependent on the number of pages to scrape, data to be collected, and system capacity.

>The total data collected were about 1000 rows (from 51 pages). Duplicates were dropped and resulting data were about 400 rows. Though there were still multiple listings of MotorHomes with the same name, location, price, length and sleeps, but with different stock number. These were left with the assumption that they are same type of MotorHomes in the same location, thus the different stock number as serves as their separate listings.
