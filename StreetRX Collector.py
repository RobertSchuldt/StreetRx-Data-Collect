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
import requests as rq
import urllib.request
import json as js
import csv


#start by checking that the API is accesible
streetrx = rq.get("https://streetrx.com/search.php")

print(streetrx.status_code)

## we get status code 200 should all should be well. Now we need to  just do a 
#test to see if we can pull in some data


print(streetrx.content)

'''
Now that I know I can grab some content it is time to convert this chunk of
JSON into something I can actually interpret. I will be attempting to create
a program that can run in regular intervals to download this data and store
the information as they only keep information in 2 week intervals on this site
'''

url = "https://streetrx.com/search.php"
x = urllib.request.urlopen(url)
street_data = x.read()

encoding = x.info().get_content_charset('utf8')
#The above is JSON default

print(street_data)

data = js.loads(street_data.decode(encoding))
print(data)



del data['allProductMatches']
del data['point']
del data['productMatches']
del data[ 'quoteTable']
del data[ 'subsetProductMatches']

print(type(data['markers']))

for key,values in data.items():
    for k,v in values.items():
        for k1, v1 in v.items():
            keys= v.keys()
            print(keys)
            
'''
Now I want to write this data into a CSV that I can analyze. I want to set
this program up to eventually auto push into the CSV file the new data over the
coming months but we will just do a single push to test the feasibility
'''

#create the file to write to
street_rx_data = open('C:\\Users\\3043340\\Documents\\Street RX\\streetrx_1.csv', 'w')

#now I create my writer
with street_rx_data as f:
    for key,values in data.items():
        for k,v in values.items():
            for k1, v1 in v.items():
                w = csv.DictWriter(f, v.keys())
                w.writeheader()
                w.writerow(v)
                 
                 
    
    
    