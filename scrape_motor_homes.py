# Import modules
import re
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs

#########################################################################################################################################################################################

def scrape_data(url, fuel_type):
    '''
     A function that gets the items in the given url
     
     Args:
         parse_url: url for the page to scrape
    '''
      
    # list to hold extracted data
    df_list = [] 
    
    # Iterate through all pages (20 pages)
    for i in range(1, 21): 
        page_url = url + '?page=' + str(i)  
        response = rq.get(page_url)
        parse_page = bs(response.text, 'lxml')
        search_body = parse_page.find('div', {'id': 'content-search__body'}) # Get the section with container frames
        container_frames = re.findall('id="pagination_container_\w+"', str(search_body)) # regular expression to find all item containers
        
        # loop through each container item and get required details
        for i in range(1, len(container_frames) + 1, 1):
            item_url_short = parse_page.find('div', {'id': 'pagination_container_'+str(i)}).find('div', {'class':'product-btns'}).find_all('a', {'clas':''})[1]['href']
            item_url_full = 'https://rv.campingworld.com' + str(item_url_short) # url to item details
            response_item = rq.get(item_url_full)
            parse_item = bs(response_item.text, 'lxml')
            tab_content = parse_item.find('div', {'class':'tab-content'}).find_all('div', {'class':'oneSpec clearfix'}) # Get tab container with specifications
            specifications_1 = [spec.find('h4').text for spec in tab_content] # list cont
            specifications_2 = [spec.find('h5').text for spec in tab_content] # list containing specifications of each item
            specifications = dict(zip(specifications_1, specifications_2))
            
            # Get vehicle details if it meets gas type specification
            # Exception handling to skip items with missing fuel type in their specifications
            try:
                if fuel_type == specifications['FUEL TYPE']:
                    vehicle_name =  parse_item.find('div', {'class':'card__title'}).find('h1', {'itemprop': 'name'}).text.replace(' ', '', 31)
                    stock_number = parse_item.find('div', {'class':'stock-num-prod-details'}).text.split(' ')[2]
                    status = parse_item.find('div', {'class':'product-card-line'}).find('h1', {'id': '#used-or-new'}).text
                    location = parse_item.find('span', {'class':'stock-results'}).find('b').text + ', ' + list(parse_item.find('span', {'class':'stock-results'}).stripped_strings)[1]
                    price_low = parse_item.find('span', {'class':'price-info low-price'}).text[1:].replace(',', '')
                    if int(price_low) > 300000:
                        horse_power = specifications['HORSEPOWER']
                    else:
                        horse_power = ''
                    fuel = fuel_type
                    sleeps = specifications['SLEEPS']
                    length = specifications['LENGTH'][:5]

                    #append extracted data to list of dictionaries
                    df_list.append({'vehicle_name': vehicle_name,
                                    'stock_number': stock_number,
                                    'status': status,
                                    'location': location,
                                    'fuel_type': fuel_type,
                                    'sleeps': int(sleeps),
                                    'length (inches)': float(length),
                                    'price_low ($)': float(price_low)})
            except:
                continue
    
    # transform extracted data into a data frame
    df = pd.DataFrame(df_list, columns = ['vehicle_name', 'stock_number', 'status', 'location','fuel_type', 'sleeps',
                                          'length', 'price_low ($)', 'horse_power'])
    
    # drop duplicates from the data set if exists
    df.drop_duplicates(inplace = True)
    
    # save dataframe as csv
    df.to_csv(fuel_type + '_RV_Motors.csv', index = False) 
    
    return df

########################################################################################################################################################################################


# Inputs
# url = https://rv.campingworld.com/rvclass/motorhome-rvs
# fuel_type = Diesel

url = str(input('Enter url: '))
fuel_type = str(input('Enter fuel type: '))

# Run program
scrape_data(url, fuel_type)
