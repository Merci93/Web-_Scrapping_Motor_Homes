# Web Scraping

A web scraping task to collect nationwide listings of "Motorhomes for Sale" that are running on Diesel. The script, developed with python, crawls through the web page (https://rv.campingworld.com/rvclass/motorhome-rvs) collecting details of Motorhomes that meet specific criteria, in this case: Motor homes that are running on Diesel. The script is developed such that it is straightforward to change the script and collect data for a different fuel type by inputting the fuel type when propmted. The script modifies itself and crawls through it page, scanning through each RV Motorhome type on each page and getting the details for the Motorhomes that meet the required fuel type. A _try except_ method was used to handle the exception for Motorhomes with missing fuel specifications, thus skipping to the next iteration.

The data captured include:
- Vehicle name
- Stock number
- Status (New or Used)
- Dealership location
- Fuel type
- Sleeps (Number of sleeps)
- Sales price ($)
- Horse power (for Motor homes with sales price above $300,000)

The collected data is saved as a csv file using the fuel type and the string 'RV motors'.

## Modules:
- regular expression: install with _pip install re_ in command line or _!pip install re_ in jupyter notebook
- pandas
- requests
- BeautifulSoup (bs4)

## Files description
- **scrape (.py and .ipynb)**: Scrapes the above listed information about RV motors from the webpage using the defined fuel type. The _.py_ file can be run via anaconda command line interface (in Windows) or terminal (in Linux/Ubuntu), and the _.ipynb_ file on jupyter notebook or jupyter lab.

## Approach
- A function _scrape_data_ taking two arguments: _url_ and _fuel type_.
- Created an empty list to hold extracted data.
- _For loop_ iterating through the pages, in this case, there are 20 pages numbered from 1 to 20. The loop modifies the page by changing the page number, hence advancing to the next page.
- Page data is collected using _python request get_ method and parsed as _lxml_ file using _BeautifulSoup_.
- From the page data, get pagination container holding the RV Motorhomes and their details. This was implemented using regular expression. The result is a list containing the containers for each RV Motorhomes in the page.
- Iterate through the list of containers collecting their _view details url_ and checking the specifications which contains the fuel type, and other details including name, sales price, horse power, sleeps, stock number, dealership location and length.
- The details above are collected using list encapsulation, zipped and converted into a dictionary.
- The dictionary key _FUEL TYPE_ is checked for equality with the input fuel type. If true, the details of the RV motor is appended as a dictionary to the empty list created earlier. A _try except_ method is also implemented here to handle situations where the _FUEL TYPE_ is missing from the item, thus skipping it and moving to the next item. For Motorhomes meeting the set specifications (fuel type), exception handlers (_try except_) were used in skipping missing data and replacing them with 'N/A'.
- Once the container on a current page is exhausted, the loop moves to the next page. This process continues until the last page when the loop exits. The collected data is transformed into a dataframe using _pandas.DataFrame_ method and finally saved as a _csv_ file using the _.to_csv_ pandas method. The file is saved in the same location as the script.
- The dataframe is returned if jupyter notebook or jupyter Lab was used to run the .ipynb script. If run on command line with the .py script, the saved csv file will be accessible in the same location as the script.

#### PS: This approach can work for any web scraping activity but the codes in the scripts provided has been tailored to suit the web page being scraped and also the requirements of the task.