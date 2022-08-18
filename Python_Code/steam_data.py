from __future__ import unicode_literals
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from scipy.stats import pearsonr
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import datetime as dt
import plotly.express as px
import plotly
import json




connection_string = ('Driver={ODBC Driver 17 for SQL Server};Server=tcp:unstructured-data-server.database.windows.net,1433;Database=unstructured-data;Uid=project-admin;Pwd={password22$};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
connection_url = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string})
engine = create_engine(connection_url, fast_executemany=True)

connection = engine.raw_connection()
cursor = connection.cursor()
steam_data = pd.read_sql('SELECT * FROM steam_source_data', engine)

#Make sure data types are correct
steam_data[['appid', 'average_playtime', 'positive_ratings', 'negative_ratings']] = steam_data[['appid', 'average_playtime', 'positive_ratings', 'negative_ratings']].apply(pd.to_numeric)
steam_data ['price'] = steam_data['price'].astype('float64')

#converting GBP to USD
steam_data['price'] = round(steam_data['price'] * 1.22, 2)

#convert playtime to hours
steam_data['average_playtime'] = round(steam_data['average_playtime']/60, 2)
steam_data = steam_data.rename(columns={'average_playtime': 'average_playtime(hours)'})

#Separate ';' separated string into a ',' list
steam_data['categories'] = steam_data['categories'].apply(lambda x: x[0:].split(';'))
steam_data['platforms'] = steam_data['platforms'].apply(lambda x: x[0:].split(';'))
steam_data['genres'] = steam_data['genres'].apply(lambda x: x[0:].split(';'))
steam_data['developer'] = steam_data['developer'].apply(lambda x: x[0:].split(';'))
steam_data['publisher'] = steam_data['publisher'].apply(lambda x: x[0:].split(';'))

#Split columns that are lists into thier own df
categories_df = steam_data.filter(items=['appid', 'categories'])
platforms_df = steam_data.filter(items=['appid', 'platforms'])
genres_df = steam_data.filter(items=['appid', 'genres'])
developers_df = steam_data.filter(items=['appid', 'developer'])
publisher_df = steam_data.filter(items=['appid', 'publisher'])


#https://stackoverflow.com/questions/50729552/split-column-containing-lists-into-different-rows-in-pandas
#Separate out the lists to perform analysis
broken_out_genres_df = genres_df.set_index(['appid'])['genres'].apply(pd.Series).stack().reset_index(level=1, drop=True)
broken_out_genres_df = broken_out_genres_df.reset_index()
broken_out_genres_df.columns = ['appid', 'genres']

broken_out_publishers_df = publisher_df.set_index(['appid'])['publisher'].apply(pd.Series).stack().reset_index(level=1, drop=True)
broken_out_publishers_df = broken_out_publishers_df.reset_index()
broken_out_publishers_df.columns = ['appid', 'publisher']

broken_out_developers_df = developers_df.set_index(['appid'])['developer'].apply(pd.Series).stack().reset_index(level=1, drop=True)
broken_out_developers_df = broken_out_developers_df.reset_index()
broken_out_developers_df.columns = ['appid', 'developer']

#get top most listed genres
top_ten_listed_genres = broken_out_genres_df['genres'].value_counts()
top_ten_listed_genres = top_ten_listed_genres[0:10]
top_ten_listed_genres = top_ten_listed_genres.reset_index()
top_ten_listed_genres = pd.DataFrame(top_ten_listed_genres, columns=['Genre', 'Count'])
top_ten_listed_genres.to_sql('Top_Ten_Listed_Genres', engine, if_exists='replace', index=False)

#Highest average playtime on game by genre
playtime_df = steam_data.filter(items=['appid', 'average_playtime(hours)'])
most_played_genres = broken_out_genres_df.merge(playtime_df, on='appid')
most_played_genres = most_played_genres.loc[most_played_genres.groupby('genres')['average_playtime(hours)'].idxmax()]
most_played_genres = most_played_genres.sort_values('average_playtime(hours)', ascending=False)
top_hundred_most_played_genres = most_played_genres[0:100]
plt.title('Top Ten Genres with the Highest Average Playtime')
plt.xlabel('Genre')
plt.ylabel('Playtime(hours)')
scatter = sns.scatterplot(x='genres', y='average_playtime(hours)', data=top_hundred_most_played_genres)
scatter.set_xticklabels(top_hundred_most_played_genres['genres'], rotation=90)
plt.savefig('Img/scatterplot.png')
top_hundred_most_played_genres.to_sql('Top_Hundred_Most_Played_Genres', engine, if_exists='replace', index=False)


#Highiest total average playtime by genre
playtime_df = steam_data.filter(items=['appid', 'average_playtime(hours)'])
most_total_played_genres = broken_out_genres_df.merge(playtime_df, on='appid').drop(columns=['appid'])
most_total_played_genres = most_total_played_genres.groupby('genres', as_index=False).agg(average_playtime_total=('average_playtime(hours)', 'sum'))
most_total_played_genres = most_total_played_genres.sort_values('average_playtime_total', ascending=False)
top_ten_total_played_genres = most_total_played_genres[0:10]
top_ten_total_played_genres.to_sql('Top_Ten_Total_Played_Genres', engine, if_exists='replace', index=False)


#Which publishers have the game with the highest average playtime
playtime_df = steam_data.filter(items=['appid', 'average_playtime(hours)'])
most_played_publishers = broken_out_publishers_df.merge(playtime_df, on='appid')
most_played_publishers = most_played_publishers.sort_values('average_playtime(hours)', ascending=False)
top_ten_played_publishers = most_played_publishers[0:10]
top_ten_played_publishers.to_sql('Top_Ten_Played_Publishers', engine, if_exists='replace', index=False)


#Which developers have the game with the highest average playtime
playtime_df = steam_data.filter(items=['appid', 'average_playtime(hours)'])
most_played_developers = broken_out_developers_df.merge(playtime_df, on='appid')
most_played_developers = most_played_developers.sort_values('average_playtime(hours)', ascending=False)
top_ten_played_developers = most_played_developers[0:10]
top_ten_played_developers.to_sql('Top_Ten_Played_Developers', engine, if_exists='replace', index=False)
plt.title('Top Ten Developers with the Highest Average Playtime')
plt.xlabel('Developer')
plt.ylabel('Playtime(hours)')
bar = sns.barplot(x='developer', y='average_playtime(hours)', data=top_ten_played_developers)
bar.set_xticklabels(top_ten_played_developers['developer'], rotation=45)
plt.savefig('Img/barplot.png')
developer = pd.get_dummies(top_ten_played_developers['developer'])
playtime = top_ten_played_developers['average_playtime(hours)']
df = pd.concat([developer, playtime], axis=1)
plt.matshow(df.corr())
cb = plt.colorbar()
plt.title('Correlation Matrix')
plt.savefig('Img/correlationmatrix.png')
df.to_sql('Developers_Correlation_Matrix', engine, if_exists='replace', index=False)
#print(df.corr(method='pearson'))


#Do reviews affect average playtime?
good_reviews = steam_data[steam_data['positive_ratings'] != 0][0:6000]
good_reviews = good_reviews['positive_ratings']
bad_reviews = steam_data[steam_data['negative_ratings'] != 0][0:6000]
bad_reviews = bad_reviews['negative_ratings']
playtime = steam_data[steam_data['average_playtime(hours)'] != 0][0:6000]
playtime = playtime['average_playtime(hours)']
gr_corr, _ = pearsonr(good_reviews, playtime)
br_corr, _ = pearsonr(bad_reviews, playtime)
# print(f'The correlation between good reviews and the average playtime in hours is {round(gr_corr,2)}')
# print(f'The correlation between bad reviews and the average playtime in hours is {round(br_corr,2)}')

#Developer # of Games released by year
steam_data['release_date'] = pd.to_datetime(steam_data['release_date'])
dates = steam_data.filter(items=['appid', 'release_date'])
merged_df = pd.merge(broken_out_developers_df, dates, on='appid')
merged_df['release_year'] = pd.DatetimeIndex(merged_df['release_date']).year
merged_df = merged_df.drop(columns=['release_date','appid'])
counts = merged_df.groupby(['developer', 'release_year'], as_index=False).size()
counts.reset_index()
counts = pd.DataFrame(counts)
counts = counts.rename(columns={'size': 'Count'})
counts = counts.sort_values(['release_year', 'Count'], ascending=[True,False])
counts['total'] = counts.groupby(['developer'])['Count'].transform('count')
counts = counts[counts['total'] > 9]
plt.title('Games Released By Year')
plt.xlabel('Year')
plt.ylabel('Number of Games')
sns.lineplot(x='release_year', y='Count', hue='developer', data=counts)
plt.savefig('Img/lineplot.png')
counts.to_sql('Developer_Released_Games_By_Year', engine, if_exists='replace', index=False)