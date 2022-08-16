
from logging import lastResort
import requests
from torch import le

big_array = []
last_row = 0
last_row2 = 0
page_number = 500

print(f"Wait {page_number * 3} seconds")

for i in range(1,page_number):
    if last_row!=0:
        last_row =len(big_array) 
    if last_row2!=0:
        last_row2 =len(big_array)     
        
    page = requests.get(f"https://www.pakwheels.com/used-cars/search/-/?page={i}")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup((page.content), features="html.parser")

    prices = soup.find_all('div', {'class': 'price-details generic-dark-grey'});
    price_array=[]
    for p in prices:
        p=p.text.replace(" ", "")
        if '.' in p:
            x = p.split(".")
            x = len(x[1].replace("lacs","").replace("crore",""))-1
            if x == 1:
                p=p.replace("lacs", "0000").replace("crore", "00000")
            else:
                p=p.replace("lacs", "000").replace("crore", "0000")
            
        else:
            p=p.replace("lacs", "00000").replace("crore", "000000")
            
    
        p=p.replace("PKR", "").replace(".",",")
        # print(p)

        price_array.append(p)
            

    price_array=list(map(str.strip,price_array))

    car_name = soup.find_all('a', {'class': 'car-name ad-detail-path'});
    name_array=[]
    for name in car_name:
    
        name = name.text.replace("for Sale", "")
        name_array.append(name)

    name_array=list(map(str.strip,name_array))


    main_data = soup.find_all('ul', {'class': 'search-vehicle-info-2'})
    main_array = []

    for data in main_data:
        data = data.text
        main_array.append(data)

    main_array = list(map(str.strip,main_array))
    
    for m in main_array:
        m = m.split('\n')  
        big_array.append(m)

    for p1 in price_array:        
        big_array[last_row].append(p1)
        last_row+=1 

    for n in name_array:        
        big_array[last_row2].append(n)
        last_row2+=1        

# print(big_array)
# print(len(big_array))

# import numpy
# a = numpy.array(big_array)
# numpy.savetxt("foo.csv", a, delimiter=',', header="Year,KM,FuelType,Engine,Drive,price,CarName", comments="")


# , columns=['Year', 'KM','FuelType','Engine','Drive','Price','CarName']

import pandas as pd
cities = pd.DataFrame(big_array)
cities.to_csv('vehicel_data_new.csv', index=False) 


