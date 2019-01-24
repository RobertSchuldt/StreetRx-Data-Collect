# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:43:14 2019

@author: Robert Schuldt
@Email: rfschuldt@uams.edu

Street RX is a website dedicated to allowing people to post the prices of their
drugs that they purchased. I would like to be able to grab their exposed JSON 
data to see if I can track prices for opioids to get a better idea of the street
price of these drugs across the country. Possibly target spots that are going
to see higher demand for heroin b/c of higher opioid pill prices. 
"""
import requests
import json
import csv
from pprint import pprint
 
# attempt to get most recent 2 weeks of data
streetrx = requests.get("https://streetrx.com/search.php")
 
# check the status code of the request
if (streetrx.status_code != 200):
    print('streetRx currently unavailable')
    quit()
 
# save the data using requests built in json converter
data = streetrx.json()
 
# remove unwanted keys
removableKeys = ['allProductMatches', 'point', 'productMatches', 'quoteTable', 'subsetProductMatches']
for key in removableKeys:
    data.pop(key)
 
# uncomment the below if you'd like to see the data in the command line
pprint(data)
 
# create new CSV file for writing
# newline='' is required so a blank row isn't inserted
# between each entry
street_rx_data = open('C:\\Users\\3043340\\Documents\\Street RX\\streetrx.csv', 'w', newline='')
 
with street_rx_data as file:
    # here's the columns we're interested in
    columns = ['date', 'place_name', 'product_name', 'price', 'unit', 'quote_id']
    # set these as our columns and write the header row
    w = csv.DictWriter(file, columns)
    w.writeheader()
    # each index (?) for the data, to get past the 1st layer
    # i'm not sure what the number means, probably some sort
    # of internal id that we don't need to worry about.
    for item in data.values():
        # each one is unique to a location however, so we get the object
        # stored within each one of those for processing.
        for location_data in item.values():
            place_name = location_data['place_name']
            # each location has multiple quotes for different
            # substances. we can set the place_name initially
            # then loop through each quote belonging to that
            # place.
            for quote in location_data['quote']:
                # replace an html tag that's in the date
                # with a comma (bad design by streetrx)
                date         = quote['date'].replace('<br />', ', ')
                # then just copy over the rest of the fields
                product_name = quote['product_name']
                price        = quote['price']
                unit         = quote['unit']
                quote_id     = quote['quote_id']
                # write the row
                # note: it's able to place each item under the correct
                #       column due to setting the column names earlier.
                #       it uses the object key to map to the correct
                #       column.
                w.writerow({
                    'date': date,
                    'place_name': place_name,
                    'product_name': product_name,
                    'price': price,
                    'unit': unit,
                    'quote_id': quote_id})
            

      