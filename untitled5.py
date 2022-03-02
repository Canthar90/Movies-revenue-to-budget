# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tHGrw1nkZ9rZUi75veWhxSS5b3l1VRK2
"""

import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt
from scipy import misc # contain a immage of racoon
from PIL import Image # for reading image files
import pandas as pd

import seaborn as sns

from sklearn.linear_model import LinearRegression

costs_df = pd.read_csv("cost_revenue_dirty.csv")
costs_df.shape

costs_df.columns

costs_df.head()

costs_df.isnull().values.any()

costs_df.duplicated().values.any()

costs_df.dtypes

costs_df.USD_Production_Budget = costs_df.USD_Production_Budget.astype(str).str.replace('$',"")
costs_df.USD_Production_Budget = costs_df.USD_Production_Budget.astype(str).str.replace(',',"")
costs_df.USD_Production_Budget = pd.to_numeric(costs_df.USD_Production_Budget)
costs_df.USD_Production_Budget

costs_df.USD_Worldwide_Gross = costs_df.USD_Worldwide_Gross.astype(str).str.replace('$',"")
costs_df.USD_Worldwide_Gross = costs_df.USD_Worldwide_Gross.astype(str).str.replace(',',"")
costs_df.USD_Worldwide_Gross = pd.to_numeric(costs_df.USD_Worldwide_Gross)
costs_df.USD_Worldwide_Gross

costs_df.USD_Domestic_Gross = costs_df.USD_Domestic_Gross.astype(str).str.replace('$','')
costs_df.USD_Domestic_Gross = costs_df.USD_Domestic_Gross.astype(str).str.replace(',','')
costs_df.USD_Domestic_Gross = pd.to_numeric(costs_df.USD_Domestic_Gross)
costs_df.USD_Domestic_Gross

costs_df.Release_Date = pd.to_datetime(costs_df.Release_Date)

costs_df.head()

costs_df.USD_Domestic_Gross.mean()

costs_df.USD_Domestic_Gross.max()

costs_df.USD_Production_Budget.mean()

costs_df.USD_Worldwide_Gross.min()

costs_df.USD_Domestic_Gross.min()

costs_df.shape

5391 * 0.25

costs_lower25 = costs_df.nsmallest(1347, "USD_Worldwide_Gross")

costs_lower25.USD_Production_Budget.mean()

costs_lower25.USD_Worldwide_Gross.mean()

costs_lower25

costs_df.describe()

costs_no_rev = costs_df[costs_df.USD_Domestic_Gross==0]
costs_no_rev.sort_values('USD_Production_Budget', ascending=False)

costs_no_rev.USD_Production_Budget.max()

costs_no_rev.USD_Worldwide_Gross.max()

costs_no_rev_Ww = costs_df[costs_df.USD_Worldwide_Gross==0]
costs_no_rev_Ww.sort_values('USD_Production_Budget', ascending=False)

costs_no_rev_Ww.USD_Production_Budget.max()

x = costs_df.USD_Production_Budget.min()
costs_df[costs_df.USD_Production_Budget==x]

international_releases = costs_df.loc[(costs_df.USD_Domestic_Gross == 0)&(costs_df.USD_Worldwide_Gross!=0)]
international_releases

international_releases = costs_df.query('USD_Domestic_Gross == 0 and USD_Worldwide_Gross != 0')
international_releases.tail()

date = pd.Timestamp('2018-5-1')
not_released = costs_df[costs_df.Release_Date>=date]
not_released

data_clean = costs_df.drop(not_released.index)

data_clean.shape

fail_movies = data_clean[data_clean.USD_Production_Budget > (data_clean.USD_Worldwide_Gross)]
fail_movies

failed_num = fail_movies.shape[0]
failed_num
movies_num = data_clean.shape[0]
movies_num
(failed_num/movies_num)*100

plt.figure(figsize=(8,4), dpi=200)

with sns.axes_style('darkgrid'):
  ax = sns.scatterplot(data=data_clean,
                  x='USD_Production_Budget',
                  y='USD_Worldwide_Gross',
                  hue='USD_Worldwide_Gross', #colour of dots
                  size='USD_Worldwide_Gross') #size of dots)
  ax.set(ylim=(0,3000000000),
        xlim=(0,450000000),
        ylabel='Revenue $ in Billions',
        xlabel='Budget in 100$ milions')
  plt.show()

plt.figure(figsize=(8,4), dpi=200)

with sns.axes_style('darkgrid'):

  ax=sns.scatterplot(data=data_clean,
        x='Release_Date',
        y='USD_Production_Budget',
        hue='USD_Worldwide_Gross',
        size='USD_Worldwide_Gross')
  
  ax.set(ylim=(0,450000000),
         xlim=(data_clean.Release_Date.min(), data_clean.Release_Date.max()),
        #  htitle='USD Wordlwide Gross in Bilons', 
         ylabel='Budget in 100$ milions',
         xlabel='Date of Release')
  plt.legend(title='USD Worldwide Gross in Billions')
  plt.show()

dt_index = pd.DatetimeIndex(data_clean.Release_Date)
years = dt_index.year
years

decades = years//10*10
data_clean["Decades"] = decades
data_clean.head()

old_films = data_clean[data_clean.Decades<1970]
old_films

old_films.sort_values('USD_Production_Budget', ascending=False)

new_films = data_clean[data_clean.Decades>=1970]
new_films

plt.figure(figsize=(8,4),dpi=200)
  
with sns.axes_style('whitegrid'):
  sns.regplot(data=old_films,
              x='USD_Production_Budget',
              y='USD_Worldwide_Gross',
              scatter_kws = {'alpha': 0.4},
              line_kws = {'color': 'black'})
  
  plt.show()

plt.figure(figsize=(8,4),dpi=200)
  
with sns.axes_style('whitegrid'):
  ax = sns.regplot(data=new_films,
              x='USD_Production_Budget',
              y='USD_Worldwide_Gross',
              scatter_kws = {'alpha': 0.4,
                             'color': '#2f4b7c'},
              line_kws = {'color': '#ff7c43'})
  ax.set(ylabel='Revenue in $ billions',
         xlabel='Budget in 100$ millions')
  
  plt.show()

regression = LinearRegression()
x = pd.DataFrame(new_films, columns=['USD_Production_Budget'])

y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])

regression.fit(x,y)

regression.intercept_

regression.coef_

regression.score(x,y)

x1 = pd.DataFrame(old_films, columns=['USD_Production_Budget'])

y1 = pd.DataFrame(old_films, columns=['USD_Worldwide_Gross'])

old_r = regression.fit(x1,y1)
old_r

old_r.intercept_

old_r.coef_

old_r_score = regression.score(x1,y1)
old_r_score

regression.fit(x,y)
budget = 350000000
revenue_estimatu = regression.intercept_[0] + regression.coef_[0,0] * budget
revenue_estimatu = round(revenue_estimatu, -6)

print(f"The revenue estimate for a movie with a budget of: {budget} in $ is: {revenue_estimatu}")