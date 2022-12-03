from typing import List
import requests as rq
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def GamesInGenre(genre): #returns dataframe 
    response = rq.get("http://steamspy.com/api.php?request=genre&genre="+genre)
    data = (
        response.json()
    )  # based on this https://atcoordinates.info/2019/09/24/examples-of-using-the-census-bureaus-api-with-python/
    #print(data)
    df = pd.DataFrame(data)
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


#ReceptionByGenre("Early+Access")