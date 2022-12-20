from typing import List
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from ast import literal_eval

def GamesFromPublisher(publisher): #returns dataframe of games by publisher 
    df = pd.read_csv('./clean_games.csv')
    df.publisher = df.publisher.apply(literal_eval)
    mask = df.publisher.apply(lambda x: publisher in x) # taken from https://stackoverflow.com/questions/41518920/python-pandas-how-to-query-if-a-list-type-column-contains-something
    games =df[mask]
    return games
def GenresOfPublisher(publisher):
    games = GamesFromPublisher(publisher)
    games.genres = games.genres.apply(literal_eval)
    genredict={}
    cleanedgenres=[]
    genres=(games.genres.values.tolist())
    for genre_list in genres:
        for genre in genre_list:
            cleanedgenres.append(genre)
    for genre in cleanedgenres:
        num=cleanedgenres.count(genre)
        genredict[genre]=cleanedgenres.count(genre)
    labels = genredict.keys()
    plt.title("Kinds of games " + publisher + " publishes")
    plt.pie(genredict.values(),labels=labels)
    plt.xticks(fontsize=14,rotation = 90)
    plt.show()


def GamesInGenre(genre): #returns dataframe 
    
    df = pd.read_csv('clean_games.csv')
    mask = df.genres.apply(lambda x: genre in x) # taken from https://stackoverflow.com/questions/41518920/python-pandas-how-to-query-if-a-list-type-column-contains-something
    games =df[mask]
    return games
def SumReviews(games):
    pos=games.positive_ratings.sum()
    neg = games.negative_ratings.sum()
    return [pos,neg]
def ReceptionByGenre(genre):
    games=GamesInGenre(genre)
    reviews=SumReviews(games)
    data = np.array(reviews)
    sentiment=["Positive","Negative"]
    plt.title("Sentiments of "+genre+" Games")
    plt.pie(data, labels = sentiment,autopct='%1.1f%%')
    plt.show()
def Top100(): #returns the top 100 steam games of all time
    df = pd.read_csv('./clean_games.csv')
    return df.nlargest(100,'total_ratings')
def PublisherGraph():
    games=Top100()
    games.publisher = games.publisher.apply(literal_eval) #https://stackoverflow.com/questions/32742976/how-to-read-a-column-of-csv-as-dtype-list-using-pandas
    publisherdict={}
    #publisherdict['other']=0
    publishers=(games.publisher.values.tolist())
    cleanedpubs=[]
    for pub_list in publishers:
        for publisher in pub_list:
            cleanedpubs.append(publisher)
    for publisher in cleanedpubs:
        num=cleanedpubs.count(publisher)
        if(num>1):
            publisherdict[publisher]=cleanedpubs.count(publisher)
        #else:
        #    publisherdict['other']+=1
    uniquepublishers = publisherdict.keys()
    plt.title("Publishers frequency in top 100 steam games")
    plt.bar(uniquepublishers,publisherdict.values())
    plt.xticks(fontsize=14,rotation = 90)
    plt.show()

def playtimeByGenre(genre): #we are using playtime of two weeks because using forever playtime massively skews the data towards outliers, and we get ridculous results like the average playtime being 300 hours.
    games=GamesInGenre(genre)
    games['median_playtime']=pd.to_numeric(games["median_playtime"])
    average_playtime_twoweeks=games.median_playtime.mean()
    return average_playtime_twoweeks
def cleanGames():
    df = pd.read_csv('./steam.csv')
    #clean genres
    cleanedgenres=[]
    genres=(df.genres.values.tolist())
    for genre in genres:
        tempcleaned=[]
        cleaned=genre.split(';')
        for values in cleaned:
            tempcleaned.append(values)
        cleanedgenres.append(tempcleaned)
    df.drop('genres',axis=1)
    df['genres']=cleanedgenres
    #clean tags
    cleanedtags=[]
    tags =df.steamspy_tags.values.tolist()
    for tag in tags:
        tempcleaned=[]
        cleaned = tag.split(';')
        for values in cleaned:
            tempcleaned.append(values)
        cleanedtags.append(tempcleaned)
    df.drop('steamspy_tags',axis=1)
    df['tags']=cleanedtags
    #clean developers
    cleaneddevs=[]
    developer=(df.developer.values.tolist())
    for dev in developer:
        tempcleaned=[]
        cleaned=dev.split(';')
        for values in cleaned:
            tempcleaned.append(values)
        cleaneddevs.append(tempcleaned)
    df.drop('developer',axis=1)
    df['developer']=cleaneddevs
    #clean publisher
    cleanedpubs=[]
    publisher=(df.publisher.values.tolist())
    for pub in publisher:
        tempcleaned=[]
        cleaned=pub.split(';')
        for values in cleaned:
            values = values.removesuffix("(Mac)")
            values = values.removesuffix("(Linux)")
            tempcleaned.append(values)
        tempcleaned=[*set(tempcleaned)]
        cleanedpubs.append(tempcleaned)
    df.drop('publisher',axis=1)
    df['publisher']=cleanedpubs
    
    #clean platforms
    cleanedplat=[]
    platform=(df.platforms.values.tolist())
    for plat in platform:
        tempcleaned=[]
        cleaned=plat.split(';')
        for values in cleaned:
            tempcleaned.append(values)
        cleanedplat.append(tempcleaned)
    df.drop('platforms',axis=1)
    df['platforms']=cleanedplat
    #clean categories
    cleanedcat=[]
    categories=(df.categories.values.tolist())
    for cat in categories:
        tempcleaned=[]
        cleaned=cat.split(';')
        for values in cleaned:
            tempcleaned.append(values)
        cleanedcat.append(tempcleaned)
    df.drop('categories',axis=1)
    df['categories']=cleanedcat
    #add review ratio
    ratio =df['positive_ratings']/(df['positive_ratings']+df['negative_ratings'])
    df['review_ratio']=ratio
    df['total_ratings']=df['positive_ratings']+df['negative_ratings']
    df.to_csv('clean_games.csv',index=False)