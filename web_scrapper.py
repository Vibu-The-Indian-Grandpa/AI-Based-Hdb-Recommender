
from selenium import webdriver # import webdriver
from selenium.webdriver.common.by import By # import By class
from selenium.webdriver.chrome.service import Service as ChromeService #import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller
import numpy as np
import pandas as pd

import numpy as np
# create driver object
options=webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")
options.add_experimental_option("detach", True)


driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
driver.get("https://homes.hdb.gov.sg/home/finding-a-flat") # link for search tool

driver.find_element("xpath",'//a[@class="alert-bar-close js-alert-bar-close"]').click()
driver.find_element("xpath",'//div[@class="row"]').find_element("xpath",'//app-flat-cards-categories[@class="col-12 col-sm-6 col-xl-4"]').click()
driver.implicitly_wait(10)
select = Select(driver.find_element("xpath",'//div[@class="col-12 new-flat-title"]').find_element("xpath",'//select[@aria-label="sortByResult"]'))
select.select_by_visible_text('50')


property_addr=[]
flat_type_list=[]
floor_area_list=[]
resale_price_list=[]

while True:

    
    web_frame=driver.find_elements("xpath",'//div[@class="row"]')[4]
    listings=web_frame.text.split("\n")



    for i in range(0,len(listings),5):
        print(listings)
        property_addr.append(listings[i+1])
        flat_type_list.append(listings[i+2].split(":")[1].strip())
        floor_area_list.append(listings[i+3].split(":")[1].strip())
        resale_price_list.append(listings[i+4])
    
 
    try:
    
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']"))))
        driver.find_element("xpath","//a[@aria-label='Next']").click()
        print("Navigating to Next Page")
        
    except (TimeoutException, WebDriverException) as e:
        print("Last page reached")
        break
    
    
data_list=[property_addr,flat_type_list,floor_area_list,resale_price_list]
print("Total Property lenght:", len(property_addr))
property_df=pd.DataFrame(data=np.array(data_list).T,columns=["Address","flat_type","floor_area_list","resale_price_list"])
property_df.to_csv("property_list.csv",index=False) 
driver.quit()

# # URL of the web page you want to scrape
# url = 'https://homes.hdb.gov.sg/home/finding-a-flat'

# # params = {
# #      'Mode of sale': 'Resale',
# #       'page':2
    
# #      # Add other filter parameters as needed
# #  }
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Send a GET request to the web page with headers
# response = requests.get(url, headers=headers)


    


# # Check if the request was successful (status code 200)
# if response.status_code == 200:
    
#     # Parse the HTML content of the page
#     soup = BeautifulSoup(response.content, 'html.parser')
#     #print(soup)

#     first_layer = soup.find('app-root')
#     print(first_layer)
#     # for listing in list_of_cards:
#     #     print("Hello")
        
#     #     address = listing.find('h2', class_='h6').get_text()
#     #     #Extract the flat type
#     #     flat_type = listing.find('p', class_='small mb-1').get_text().replace('Flat type: ', '')

#     #     # Extract the floor area
#     #     floor_area = listing.find('p', class_='small mb-6').get_text().replace('Floor area: ', '')

#     #     # Extract the price
#     #     price = listing.find('p', class_='text-right mb-0').get_text()
#     #     break
#     #     # print('Address:', address)
#     #     # print('Flat type:', flat_type)
#     #     # print('Floor area:', floor_area)
#     #     # print('Price:', price)
        
# else:
#     print('Failed to retrieve the web page. Status code:', response.status_code)
