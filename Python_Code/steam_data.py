import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 


steam_data = pd.read_csv('C:/Users/625320/OneDrive - BOOZ ALLEN HAMILTON/Desktop/Project/BAH-TEDE-Project/Data/steam.csv')

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

#Highest average playtime on game by genre
playtime_df = steam_data.filter(items=['appid', 'average_playtime(hours)'])
most_played_genres = broken_out_genres_df.merge(playtime_df, on='appid')
most_played_genres = most_played_genres.loc[most_played_genres.groupby('genres')['average_playtime(hours)'].idxmax()]
most_played_genres = most_played_genres.sort_values('average_playtime(hours)', ascending=False)

#Highiest total average playtime by genre
playtime_df = steam_data.filter(items=['appid', 'average_playtime(hours)'])
most_total_played_genres = broken_out_genres_df.merge(playtime_df, on='appid').drop(columns=['appid'])
most_total_played_genres = most_total_played_genres.groupby('genres', as_index=False).agg(average_playtime_total=('average_playtime(hours)', 'sum'))
most_total_played_genres = most_total_played_genres.sort_values('average_playtime_total', ascending=False)


#Which publishers have the game with the highest average playtime
playtime_df = steam_data.filter(items=['appid', 'average_playtime(hours)'])
most_played_publishers = broken_out_publishers_df.merge(playtime_df, on='appid')
most_played_publishers = most_played_publishers.sort_values('average_playtime(hours)', ascending=False)
top_ten_played_publishers = most_played_publishers[0:10]

#Which developers have the game with the highest average playtime
playtime_df = steam_data.filter(items=['appid', 'average_playtime(hours)'])
most_played_developers = broken_out_developers_df.merge(playtime_df, on='appid')
most_played_developers = most_played_developers.sort_values('average_playtime(hours)', ascending=False)
top_ten_played_developers = most_played_developers[0:10]
#Do reviews affect average playtime?
good_reviews = steam_data['positive_ratings']
bad_reviews = steam_data['negative_ratings']


#which genres have the most playtime

