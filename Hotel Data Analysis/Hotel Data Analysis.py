# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 18:01:27 2021

@author: Emmanuel
"""

#We want to understand the relationship between Average daily rate for hotels and the lead time before booking



#Import Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress


#Import Datasets 

df1 = pd.read_excel('C:/Users/Emmanuel/Documents/Data science/PROJECTS/SPYDER PROJECTS/Hotel Data Analysis Report/hotel_revenue_historical_full.xlsx', sheet_name='2018')
df2 = pd.read_excel('C:/Users/Emmanuel/Documents/Data science/PROJECTS/SPYDER PROJECTS/Hotel Data Analysis Report/hotel_revenue_historical_full.xlsx', sheet_name='2019')
df3 = pd.read_excel('C:/Users/Emmanuel/Documents/Data science/PROJECTS/SPYDER PROJECTS/Hotel Data Analysis Report/hotel_revenue_historical_full.xlsx', sheet_name='2020')


#concatenate all three datasets into one dataset

df = pd.concat([df1,df2,df3], ignore_index=True)
df.info()


#Set our console display to show all columns when printed

pd.set_option('display.max_columns', None)


#Analyze the percentage of reservation bookings that were cancelled within the 3 years

print(df['is_canceled'].value_counts(normalize=True))


#Isolate and Filter out the reservations that were cancelled from our dataset
#This will enable us to run analysis on only the hotel reservation bookings that were not cancelled

df_main = df[df['is_canceled']!=1]
print(df_main.info())


#Univiarate  analysis/visualization of the average daily booking rate for the hotel 

sns.distplot(df_main['adr'],kde_kws={'color':'red'})
plt.title('Average Daily Booking Rate Analysis')
adr_mean = df_main['adr'].mean()
plt.axvline(adr_mean, color='black', linestyle = '--', label = 'City Mean')
plt.show()
#from the distplot we can see that the avarage daily rate peaks at 100 dollars


#Univiarate analysis/visualization of the average daily booking rate by Hotel types

sns.distplot(df_main[df_main['hotel']=='City Hotel']['adr'], label=('City Hotel'))
sns.distplot(df_main[df_main['hotel']=='Resort Hotel']['adr'], label=('Resort Hotel'))
resort_mean = df_main[df_main['hotel']=='Resort Hotel']['adr'].mean()
city_mean = df_main[df_main['hotel']=='City Hotel']['adr'].mean()
plt.axvline(resort_mean, color='black', linestyle = '--', label = 'Resort Mean')
plt.axvline(city_mean, color='red', linestyle = '--', label = 'City Mean')
plt.title('Average Daily Booking Rate By Hotel Types')
plt.legend()
plt.show()
#from the distplot we can see that the ADR for city hotel is higher than resort hotel
#the ADR mean for city hotel is also larger than resort hotel


#Univiarate analysis/visualization of the booking lead time 

sns.distplot(df_main['lead_time'],kde_kws={'color':'red'})
plt.title('Booking Lead Time Analysis')
plt.show()
#From the distplot we can see that the peak booking lead time is 0-14 days
#i.e majority of people make reservations 0 - 14 days before the actual check-in date


#Booking Lead time analysis per the two types of hotels

sns.violinplot(data=df_main,y='lead_time', x='hotel')
plt.title('Booking Lead Time Analysis By Various Hotel Types')
plt.show()
#from the violinplot we can see that there is a bigger distribution of lead time for the resort hotel than the city hotel
#This is probably because resort hotel gets booked easier than city hotels



#Bivariate analysis of lead time and ADR

sns.regplot(data= df_main, x='lead_time', y='adr', line_kws={'color':'red'})
plt.title('Regression Plot of Lead_time vs ADR')
plt.show()
#from the Distplot we can see that as lead time goes up ADR comes down
#therefore it is cheaper to book early


#To visualize both the distribution and the regplot we will use a jointplot

sns.jointplot(data= df_main, x='lead_time', y='adr', kind='reg', joint_kws={'line_kws':{'color':'red'}})
plt.title('Joint Plot of Lead_time vs ADR')
plt.show()


#Linear Regression

linregress(df_main['lead_time'], df_main['adr'])
slope = linregress(df_main['lead_time'], df_main['adr'])[0]
intercept = linregress(df_main['lead_time'], df_main['adr'])[1]
rvalue = linregress(df_main['lead_time'], df_main['adr'])[2]

#create a dataframe for the regression values so we can bring it into Power BI

regression_table = pd.DataFrame({'Name': ['Slope', 'Intercept', 'R_value'],
                                'Values': [slope, intercept, rvalue]})


#We can then use python scripting to load these analysis, tables and visuals into Power BI and then build our report and interactive dashboard.





























