# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 20:35:24 2021

@author: Emmanuel
"""

#Import Libraries

import pandas as pd
from bs4 import BeautifulSoup
import requests
import smtplib
import time
import datetime
import csv



#Connect to Amazon website-page

url = "https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
page = requests.get(url, headers= headers)


#Pulling contents from the webpage

soup1 = BeautifulSoup(page.content, "html.parser")
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
title = soup2.find(id='productTitle').get_text()
price = soup2.find(id= 'priceblock_ourprice').get_text()
brand = soup2.find(id= 'bylineInfo').get_text()


#Cleaning up the data pulled a little bit

title = title.strip()
price = float(price.strip()[1:])
brand = brand.strip()[7:]
print(title)
print(price)
print(brand)


#Create date stamp

today = datetime.datetime.now()
print(today)


# Create Amazon web scrapper.csv document and write headers and data into the document

doc_header = ['Product Name', 'Price', 'Brand', 'Date-Time']
doc_data = [title, price, brand, today]

with open('Amazon Web Scrapper Dataset.csv', 'w', newline=(''), encoding=('UTF8')) as f:
    writer = csv.writer(f)
    writer.writerow(doc_header)
    writer.writerow(doc_data)
    
    
#Display our Amazon web scrapper.csv doc

pd.set_option('display.max_columns', None)
print(pd.read_csv('Amazon Web Scrapper Dataset.csv'))  


#Appending data to the csv document

with open('Amazon Web Scrapper Dataset.csv', 'a+', newline=(''), encoding=('UTF8')) as f:
     writer = csv.writer(f)
     writer.writerow(doc_data)  
     


#Function for sending myself an email whenever the product price goes below $15

def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    #server.starttls()
    server.ehlo()
    server.login('agholoremma@gmail.com','xxxxxxxxxxxxxx')
    
    subject = "Your Fav Shirt is now below $15"
    body = "Emmanuel, If you are getting this mail it means the mission was successful, the future is safe and the shirt of your dreams is now below $15. Don't mess it up! buy it now!!! Link here: https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data+analyst+tshirt&qid=1626655184&sr=8-3"
   
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(
        'agholoremma@gmail.com',
        msg
     
    )     



#Combine all of the above code into one function in order to keep recording data from the amazon webpage

def amazon_price():
    from bs4 import BeautifulSoup
    import requests
    import smtplib
    import time
    import datetime
    import csv
    
    url = "https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    page = requests.get(url, headers= headers)
    
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    title = soup2.find(id='productTitle').get_text()
    price = soup2.find(id= 'priceblock_ourprice').get_text()
    brand = soup2.find(id= 'bylineInfo').get_text()
    
    title = title.strip()
    price = float(price.strip()[1:])
    brand = brand.strip()[7:]
   
    today = datetime.datetime.now()
    
    doc_header = ['Product Name', 'Price', 'Brand', 'Date-Time']
    doc_data = [title, price, brand, today]
    
        
    with open('Amazon Web Scrapper Dataset.csv', 'a+', newline=(''), encoding=('UTF8')) as f:
         writer = csv.writer(f)
         writer.writerow(doc_data) 
         
    if(price < 15):
        send_mail()
         

#Automatically run amazon_price funtion, record the price of the shirt daily in the csv file 
#and then send a mail whenever the price of the shirt is below $15
         
while(True):
    amazon_price()
    time.sleep(86400)
    
