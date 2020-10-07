from sqlalchemy.ext.declarative import declarative_base
from models import Claro, ClaroProductPrice
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base
import math
import csv
import requests
from extract_xml import getFecha, loadXML, extractSkus   

engine = create_engine("sqlite:///db.sqlite")
Session = sessionmaker(bind=engine)
session = Session()

def clean_percentage(data):
    return int(100-(data['data']['sale_price']*100/data['data']['price']))

def clean_url(item, data):
    return "https://www.claroshop.com/producto/" + str(item) + "/" + data['data']['title_seo']

def clean_category(cats):
    category = ""
    for count,cat in enumerate(cats):
        if (count+1)%2 and ((count) < len(cats)-1):
            category += cat['name'] 
        else:
            category += '|' + cat['name']
    return category

def parseItems(items):

    for item in items:
        url = "https://csapi.claroshop.com/producto/" + str(item)
        resp = requests.get(url)
        my_json = resp.json()

        claro = Claro()
        claro = (
            session.query(Claro)
            .filter_by(sku=my_json['data']['sku'])
            .first()
        )
        #Check if the Product already exists
        if claro is None:
            claro = Claro(sku=my_json['data']['sku'])
        
        claro.sku = my_json['data']['sku']
        claro.name = my_json['data']['title']
        claro.category = clean_category(my_json['data']['categories'][0])
        claro.seller = my_json['data']['store']['name']
        claro.description = my_json['data']['description']
        claro.brand = my_json['data']['attributes']['marca']
        claro.image_url = my_json['data']['images'][0]['link']
        claro.url = clean_url(item, my_json)
        
        session.add(claro)
        session.commit()

        #Check if the BranchProduct already exists
        price_product = (
            session.query(ClaroProductPrice)
            .filter_by(claro=claro, price=my_json['data']['price'])
            .first()
        )

        if price_product is None:
            price_product = ClaroProductPrice(claro=claro, price=my_json['data']['price'])

        price_product.stock = my_json['data']['stock']
        price_product.price = my_json['data']['price']
        price_product.discount = my_json['data']['sale_price']
        price_product.percentage = clean_percentage(my_json)
        price_product.date = getFecha()

        session.add(price_product)
        session.commit()

def main():
    #Load XML
    date = loadXML()

    #Pasamos al xml
    items = extractSkus(date + '.xml')
    print(len(items))
    
    #Parse items
    parseItems(items)
    
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    main()