# Import modules
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs


def get_page(url):
    '''
    A function to get the next url file as lxml using BeautifulSoup
    
    Args:
        url: The url address of the page to be scrapped
    '''
    response = rq.get(url)
    parse_page = bs(response.text, 'lxml')
    return parse_page


def next_page(parse_page):
    '''
     A function that gets the url for the next page
     
     Args:
         file: A parsed HTML of a webpage.
    '''
    
    pagination = parse_page.find('div', {'class': 'pagination-wrap'})
    if pagination.find('li', {'class': 'active'}):
        new_url = pagination.find('a', {'id': 'page_next'})['href']
        return new_url
    else:
        return


def scrape_data(parse_page, url, fuel_type):
    '''
     A function that gets the items in the given url
     
     Args:
         parse_url: url for the page to scrape
    '''
      
    url_list = [url, ]
    df_list = [] # list to contain details
    
    
    for i in range(1, 21):
        try: # Exception handling to handle the error when the url returned is 'None'
            page = get_page(url)
            url = next_page(page)
            if not url:
                break
            url_list.append(url)

        except:
            print(f'End of file. No URL returned!!!')  

    
    # iterate though products in the page to check if vehicle uses diesel
    for url in url_list:
        for i in range(1, 21):
            item_url_short = parse_page.find('div', {'id': 'pagination_container_'+str(i)}).find('div', {'class':'product-btns'}).find_all('a', {'clas':''})[1]['href']
            item_url_full = 'https://rv.campingworld.com'+str(item_url_short)
            response_item = rq.get(item_url_full)
            parse_item = bs(response_item.text, 'lxml')
            fuel = parse_item.find('div', {'class':'tab-content'}).find_all('div', {'class':'oneSpec clearfix'})[1].find('h5').text

            # Get vehicle details if it meets gas type specification
            if fuel_type == fuel:
                vehicle_name =  parse_item.find('div', {'class':'card__title'}).find('h1', {'itemprop': 'name'}).text.split(' ', 1)[1]
                #print(vehicle_name)
                stock_number = parse_item.find('div', {'class':'stock-num-prod-details'}).text.split(' ')[2]
                status = parse_item.find('div', {'class':'product-card-line'}).find('h1', {'id': '#used-or-new'}).text
                location = parse_item.find('span', {'class':'stock-results'}).find('b').text + ', ' + list(parse_item.find('span', {'class':'stock-results'}).stripped_strings)[1]
                fuel_type = parse_item.find('div', {'class':'tab-content'}).find_all('div', {'class':'oneSpec clearfix'})[1].find('h5').text
                sleeps = parse_item.find('div', {'class':'tab-content'}).find_all('div', {'class':'oneSpec clearfix'})[3].find('h5').text
                length = parse_item.find('div', {'class':'tab-content'}).find_all('div', {'class':'oneSpec clearfix'})[2].find('h5').text[:5]
                price_low = parse_item.find('span', {'class':'price-info low-price'}).text[1:].replace(',', '')
                if int(price_low) > 300000:
                    horse_power = parse_item.find('div', {'class':'tab-content'}).find_all('div', {'class': 'oneSpec clearfix'})[6].find('h5').text
                else:
                    horse_power = ''
                horse_power = parse_item.find('div', {'class':'tab-content'}).find_all('div', {'class':'oneSpec clearfix'})

                #append details to list of fictionaries
                df_list.append({'vehicle_name': vehicle_name,
                                'stock_number': int(stock_number),
                                'status': status,
                                'location': location,
                                'fuel_type': fuel_type,
                                'sleeps': int(sleeps),
                                'length': float(length),
                                'price_low ($)': float(price_low)})
            else:
                continue

    # transform extracted data into a data frame
    df = pd.DataFrame(df_list, columns = ['vehicle_name', 'stock_number', 'status', 'location','fuel_type', 'sleeps',
                                                  'length', 'price_low ($)', 'horse_power'])
    return df
    