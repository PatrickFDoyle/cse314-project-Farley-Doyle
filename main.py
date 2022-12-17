from typing import List
import requests as rq
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def GamesInGenre(genre): #returns dataframe 
    response = rq.get("http://steamspy.com/api.php?request=genre&genre="+genre)
    print(response)
    data = (
        response.json()
    )  # based on this https://atcoordinates.info/2019/09/24/examples-of-using-the-census-bureaus-api-with-python/
    #print(data)
    df = pd.DataFrame(data)
    print(df)
    return df
def SumReviews(games):
    pos=games.loc['positive'].sum()
    neg = games.loc['negative'].sum()
    return [pos,neg]
def ReceptionByGenre(genre):
    games=GamesInGenre(genre)
    reviews=SumReviews(games)
    #positive=reviews[0]
    #negative=reviews[1]
    data = np.array(reviews)
    sentiment=["Positive","Negative"]
    plt.title("Sentiments of "+genre+" Games")
    plt.pie(data, labels = sentiment,autopct='%1.1f%%')
    plt.show()
def Top100(): #returns the top 100 steam games of all time
    response = rq.get("http://steamspy.com/api.php?request=top100forever")
    data = (
        response.json()
    )  # based on this https://atcoordinates.info/2019/09/24/examples-of-using-the-census-bureaus-api-with-python/
    #print(data)
    df = pd.DataFrame(data)
    #print(df.index)
    #publishers = (df.loc['publisher'].unique())
    #print(len(publishers))
    return df
def PublisherGraph(games):
    #publishers = (games.loc['publisher'].unique())
    publishers=(games.loc['publisher']).values.tolist()
    cleanedpubs=[]
    for publisher in publishers:
        cleaned=publisher.split(',')
        for values in cleaned:
            cleanedpubs.append(values)
    #print(cleanedpubs)
    publisherdict={}
    #publisherdict['other']=0
    for publisher in cleanedpubs:
        num=cleanedpubs.count(publisher)
        if(num>1):
            publisherdict[publisher]=cleanedpubs.count(publisher)
        #else:
        #    publisherdict['other']+=1
    if ' Inc.' in publisherdict:
        publisherdict.pop(' Inc.')
    if ' Ltd.' in publisherdict:
        publisherdict.pop(' Ltd.')
    uniquepublishers = publisherdict.keys()
    plt.title("Publishers frequency in top 100 steam games")
    plt.bar(uniquepublishers,publisherdict.values())
    plt.xticks(fontsize=14,rotation = 90)
    plt.show()

def playtimeByGenre(genre): #we are using playtime of two weeks because using forever playtime massively skews the data towards outliers, and we get ridculous results like the average playtime being 300 hours.
    print(genre)
    games=GamesInGenre(genre)
    print(games.index)
    average_playtime_twoweeks=games.loc['average_2weeks'].mean()
    return average_playtime_twoweeks
def graphPlaytimeOfGenres():
    genres = ["Action","Strategy","RPG","Indie","Adventure","Sports","Simulation","Early+Access","Ex+Early+Access","MMO","Free"]
    playtimes =[]
    for genre in genres:
        print(genre)
        time = playtimeByGenre(genre)
        print("THE TIME IS", time)
        playtimes.append(playtimeByGenre(genre))
    print(playtimes)
print(playtimeByGenre("Early+Access"))
#graphPlaytimeOfGenres()