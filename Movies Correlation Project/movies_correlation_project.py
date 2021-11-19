# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 21:20:22 2021

@author: Emmanuel
"""

#Import Libraries

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.pyplot import figure


matplotlib.rcParams['figure.figsize'] = (12,8) #Adjusts the config of the plot


#Import our dataset

df = pd.read_csv('movies.csv')
pd.set_option('display.max_columns', None) #Set our display to show all columns when printed
print(df)



#check the datatypes

print(df.dtypes)


#Check for missing data
#loop through the data and see if there is anything missing

for col in df.columns:
    percent_missing = np.mean(df[col].isnull())
    print('{} - {}%'.format(col, percent_missing))
    


#Fill all missing data with mean for numeric and 'N/A' for Objects

df['budget'] = df['budget'].fillna(np.mean(df['budget']))
df['gross'] = df['gross'].fillna(np.mean(df['gross']))
df['score'] = df['score'].fillna(np.mean(df['score']))
df['votes'] = df['votes'].fillna(np.mean(df['votes']))
df['runtime'] = df['runtime'].fillna(np.mean(df['runtime']))
df['rating'] = df['rating'].fillna('N/A')
df['writer'] = df['writer'].fillna('N/A')
df['star'] = df['star'].fillna('N/A')
df['country'] = df['country'].fillna('N/A')
df['company'] = df['company'].fillna('N/A')
df['released'] = df['released'].fillna('N/A')



#change datatypes of columns to what we need

df['budget'] = df['budget'].astype('int64')
df['gross'] = df['gross'].astype('int64')


print(df)


#create a release date column containing only dates without the extra text 

df['release_date'] = df['released'].astype(str).str.split("(" , expand=True)[0]


#create a year only column from the released date column

df['year_correct'] = df['release_date'].astype(str).str[-5:]


#Order our table by Gross Earnings

df.sort_values(by=['gross'], inplace=False, ascending=False)


#check for duplicates

pd.set_option('display.max_rows', None)
print(df.duplicated().any())


#Correlation Insights

#Scatter plot of Budget vs Gross

plt.scatter(df['budget'], df['gross'])
plt.title('Budget Vs Gross Earnings')
plt.xlabel('Budget')
plt.ylabel('Gross Earnings')
plt.legend()
plt.show()


#Seaborn Regplot of Budget vs Gross

sns.regplot(df['budget'], df['gross'], df, scatter_kws={'color':'red'},
            line_kws={'color':'Blue'})
    


#Check for Correlation among numeric columns

df.corr(method = 'pearson')


#Visualize Correlations with Seaborn Heatmap 

correlation_matrix = df.corr(method = 'pearson')
sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix For Movie Features')
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.show()


#Check for Correlation among both object and numeric columns

#Firstly, Convert Objects to Category and Encode them

df_encoded = df.copy()
for col_name in df_encoded.columns:   
    if(df_encoded[col_name].dtype == 'object'):
        df_encoded[col_name] = df_encoded[col_name].astype('category')
        df_encoded[col_name] = df_encoded[col_name].cat.codes
        
        
#check for correlation with all Encoded category and numeric data

df_encoded.corr(method='pearson')


#Visualize Correlations with Seaborn Heatmap 

correlation_matrix2 = df_encoded.corr(method = 'pearson')
sns.heatmap(correlation_matrix2, annot=True)
plt.title('Correlation Matrix For Movie Features')
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.show()


#Filter Correlation Insights

correlation_encoded = df_encoded.corr(method='pearson')
correlation_pairs = correlation_encoded.unstack()
print(correlation_pairs)

sorted_corr_pairs = correlation_pairs.sort_values()
print(sorted_corr_pairs)


#Show data-points with the Highest Correlations

high_correlation = sorted_corr_pairs[((sorted_corr_pairs) >= 0.5) & ((sorted_corr_pairs) < 1.0)  ]
print(high_correlation)


#In summary Votes and Budget have the highest correlation to Gross Earnings
#Company name has a low Correlation with Gross Earnings
        
        
        
    






