import re
import lxml
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs

def scrape_data(url):
    """
    Scrapes data from the given url.

    Keyword Arguments:
    url: URL to the webpage to be scraped.
    """
    #driver = webdriver.Chrome()
    #driver_path = 'Add the path to chrome driver here'
    driver_path = 'C:/Users/David Ugochi Asogwa/Documents/Folders/GitHub/Web_Scrapping_Motor_Homes/chromedriver.exe'
    driver = webdriver.Chrome(service = Service(driver_path))

    # Get URL
    # Select RV class and fuel type: Diesel
    driver.get(url)
    rv_class = driver.find_element(By.XPATH, '//*[@id="rv_class"]/fieldset/div[1]').click()
    time.sleep(1)
    fuel_type = driver.find_element(By.XPATH, '//*[@id="classAFuel"]/div[3]/label').click()

    # List to hold extracted data.
    df_list = []

    # Loop through pages till end.
    # Get current page source and container frames.
    # loop through all item in the contaimer frames collecting required data.

    while True:

        time.sleep(1)
        search_body = bs(driver.page_source, 'lxml')
        container_frames = re.findall('id="pagination_container_\w+"', str(search_body))

        for container in container_frames:
            time.sleep(1)
            vehicle_name = driver.find_element(By.XPATH, '//*[@' + str(container)
                                               + ']/div/div[3]/div[1]/div[1]/a/span').text
            status = driver.find_element(By.XPATH, '//*[@' + str(container)
                                         + ']/div/div[3]/div[1]/div[1]/span').text.capitalize()
            location = driver.find_element(By.XPATH, '//*[@' + str(container) + ']/div/div[3]/div[1]/div[2]/span[1]').text
            stock_number = driver.find_element(By.XPATH, '//*[@'
                                               + str(container)
                                               + ']/div/div[3]/div[1]/div[2]/span[2]').text.split(' ')[2]
            length = driver.find_element(By.XPATH, '//*[@' + str(container) + ']//div[@class="specs"]').text.split('\n')[1]
            sleeps = driver.find_element(By.XPATH, '//*[@' + str(container)
                                         + ']//div[@class="specs"][2]').text.split('\n')[1]
            try:
                sales_price = driver.find_element(By.XPATH, '//*[@'
                                                  + str(container) 
                                                  + ']//span[@class="price-info low-price "]').text[1:].replace(',', '')
            except NoSuchElementException:
                sales_price = driver.find_element(By.XPATH, '//*[@'
                                                  + str(container)
                                                  + ']//span[@class="price-info low-price"]').text[1:].replace(',', '')

            try:
                if int(sales_price) > 300000:
                    get_details = driver.find_element(By.XPATH, '//*[@'+str(container)+']/div/div[3]/div[4]/a[2]').click()
                    time.sleep(2)
                    get_page_source = bs(driver.page_source, 'lxml')
                    tab_content = get_page_source.find('div', {'class':'tab-content'}).find_all('div',
                                                                                         {'class':'oneSpec clearfix'})
                    specifications_1 = [spec.find('h4').text for spec in tab_content]
                    specifications_2 = [spec.find('h5').text for spec in tab_content]
                    specifications = dict(zip(specifications_1, specifications_2))
                    horse_power = specifications['HORSEPOWER']
                    back_to_results = driver.find_element(By.ID, 'back-link').get_attribute('href')
                    driver.get(back_to_results)

                else:
                    horse_power = 'N/A'

            except KeyError:
                horse_power = 'N/A'

                # Return to search results.
                time.sleep(1)
                back_to_results = driver.find_element(By.ID, 'back-link').get_attribute('href')
                driver.get(back_to_results)

            # Append extracted data to list of dictionaries.
            df_list.append({'vehicle_name': vehicle_name,
                            'stock_number': stock_number,
                            'status': status,
                            'location': location,
                            'sleeps': sleeps,
                            'length': length,
                            'sales_price (USD)': int(sales_price),
                            'horse_power': horse_power})

        # Go to next page.
        try:
            next_page = driver.find_element(By.XPATH, '//*[@id="page_next"]').click()
        except NoSuchElementException:
            break         # Break at the end of the page.

    driver.close()

    return df_list


def create_df(list_dict):
    """
    A function that creates a dataframe from list of dictionary

    Keyword arguments:
    dataframe_dict: A list containing dictionary of items
    """

    # Transform extracted data into a data frame.
    df = pd.DataFrame(list_dict, columns = ['vehicle_name', 'stock_number', 'status', 'location','fuel_type', 'sleeps',
                                          'length', 'sales_price (USD)', 'horse_power'])

    df.to_csv('RV_MotorHomes_with_possible_duplicates.csv', index = False)

    # Drop duplicates from the data set.
    df.drop_duplicates(inplace = True)

    # Save dataframe as CSV.
    df.to_csv('RV_MotorHomes.csv', index = False)


if __name__ == '__main__':
    #url = 'https://rv.campingworld.com/rvclass/motorhome-rvs'
    url = str(input('Enter URL: '))
    create_df(scrape_data(url))
