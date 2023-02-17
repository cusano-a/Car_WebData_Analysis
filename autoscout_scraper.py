from bs4 import BeautifulSoup, SoupStrainer
import argparse
import urllib.request
import json
from datetime import datetime
import regex as re
import os
import pandas as pd
from dotenv import load_dotenv

#Load the url of the used cars website
load_dotenv()
used_cars_website = os.environ.get('USED_CARS_WEBSITE')

#Dict of countries supported by the website
countries = {"Germany": "D",
             "Austria": "A",
             "Belgium" : "B",
             "Spain": "E",
             "France": "F",
             "Italy": "I",
             "Luxembourg": "L",
             "Netherlands": "NL"}

#Regex for manufacturer data and vendor location data
pattern_manufacturer = re.compile(r'\"makeId\":(.*?),\"modelOrModelLineId\":(.*?),\"make\":"?(.*?)"?,\"model\":"?(.*?)"?,\"modelVersionInput\":"?(.*?)"?,')
pattern_vendor_location = re.compile('"location":{"countryCode":"?(.*?)"?,"zip":"?(.*?)"?,"city":"?(.*?)"?,\"street\":"?(.*?)"?,')

def initWS():
    if not used_cars_website:
        print('Used cars website URL not found')
        exit()
    if not os.path.isdir("data"):
        os.mkdir("data")
    path_to_visited_urls = os.path.join("data", "visited_urls.json")
    if not os.path.isfile(path_to_visited_urls):
        with open(path_to_visited_urls,"w") as file:
            json.dump([],file)

def get_car_URLs(country, numpages, offsetpag, db=False):
    car_URLs = []
    #Iterating all the Web Pages within the search results
    for page in range(1+offsetpag,1+offsetpag+numpages):
        try:
            url = used_cars_website+'/lst?sort=age&desc=1&ustate=N%2CU&size=20&page='+str(page)+ '&cy=' + countries[country] +'&atype=C'
            only_a_tags = SoupStrainer("a")
            soup = BeautifulSoup(urllib.request.urlopen(url).read(),'lxml', parse_only=only_a_tags)
        except Exception as e:
            if db: print(f"Error page {page}: " + str(e) +" "*50, end="\r")
            pass
        for link in soup.find_all("a"):
            if r"/annunci/" in str(link.get("href")):
                car_URLs.append(link.get("href"))
    return car_URLs

def get_car_dict(URL, db=False):
    car_dict = {}
    car_dict["country"] = country
    car_dict["date"] = str(datetime.now())
    car = BeautifulSoup(urllib.request.urlopen(used_cars_website+URL).read(),'lxml')

    #Manufacturer data
    manufacturer_res = re.findall(pattern_manufacturer, car.find(id="__NEXT_DATA__").text)
    if manufacturer_res:
        car_dict["makeId"], car_dict["modelOrModelLineId"], car_dict["maker"], car_dict["model"], car_dict["modelVersionInput"] = manufacturer_res[0]
    else:
        car_dict["makeId"], car_dict["modelOrModelLineId"], car_dict["maker"], car_dict["model"], car_dict["modelVersionInput"] = ('NaN', 'NaN', 'NaN', 'NaN', 'NaN')
        if db: print(f'Not found manufacturer in URL {URL}')

    #Main data attributes
    for key, value in zip(car.find_all("dt"),car.find_all("dd")):
        if value.find_all("li"): #concatenate list of item
            car_dict[key.text.replace("\n","")] = ";".join([itm.text.replace("\n","") for itm in value.find_all("li")])
        else:
            car_dict[key.text.replace("\n","")] = value.text.replace("\n","")

    car_dict["dealer"] = car.find("div",attrs={"class":"cldt-vendor-contact-box","data-vendor-type":"dealer"}) != None
    car_dict["privateSeller"] = car.find("div",attrs={"class":"cldt-vendor-contact-box","data-vendor-type":"privateseller"}) != None
    car_dict["price"] =  car.find("span",attrs={"class":"StandardPrice_price__X_zzU"}).text

    #Vendor Location Data
    location_res =  re.findall(pattern_vendor_location, car.find(id="__NEXT_DATA__").text)
    if location_res:
        car_dict["countryCode"], car_dict["zip"], car_dict["city"], car_dict["street"] = location_res[0]
    else:
        car_dict["countryCode"], car_dict["zip"], car_dict["city"], car_dict["street"] = ('NaN', 'NaN', 'NaN', 'NaN')
        if db: print(f'Not found vendor location in URL {URL}')

    return car_dict


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--country', '-c', dest='country',
                        help='Country where to search cars', default='Italy',
                        choices=countries.keys())
    parser.add_argument('--numpages', '-n', dest='numpages',
                        help='Number of pages to retrieve', type=int, default=20)
    parser.add_argument('--offsetpag', '-o', dest='offsetpag',
                        help='Number of pages to skip', type=int,  default=0)
    parser.add_argument('--debug', '-d', dest='debug',
                        help='Enable debug mode', action='store_true')
    args = parser.parse_args()

    country = args.country
    numpages = args.numpages
    offsetpag = args.offsetpag
    db = args.debug

    #Check/Create folders for results
    initWS()
    path_to_visited_urls = os.path.join("data", "visited_urls.json")

    #In Debug mode not skip already processed cars
    if db:
        visited_urls = []
        filesavename = re.sub("[.,:,-, ]","_",str(datetime.now()))+"_db.csv"
    else:
        with open(path_to_visited_urls) as file:
            visited_urls = json.load(file)
        filesavename = re.sub("[.,:,-, ]","_",str(datetime.now()))+".csv"

    #Results container
    multiple_cars_dict = {}
    fullsavename = os.path.join('data', filesavename)

    #Getting car detail URL from all pages
    car_URLs = get_car_URLs(country, numpages, offsetpag, db)
    car_URLs_unique = [car for car in list(set(car_URLs)) if car not in visited_urls]
    print(f'{len(car_URLs_unique)} cars to be processed.')

    #Iterating cars detail Web Pages
    for ii, URL in enumerate(car_URLs_unique):
        if((ii+1)%20==0): print(f'Processing car {ii+1}', end='\r')
        try:
            car_dict = get_car_dict(URL, db)
            multiple_cars_dict[URL] = car_dict
            visited_urls.append(URL)
        except Exception as e:
            if db: print(f"Error car {ii+1}: " + str(e) +" "*10)
    print("\nAll cars processed")

    #Saving results
    if len(multiple_cars_dict)>0:
        df = pd.DataFrame(multiple_cars_dict).T
        df.to_csv(fullsavename, sep=";",index_label="url")
        if not db:
            with open(path_to_visited_urls, "w") as file:
                json.dump(visited_urls, file)
