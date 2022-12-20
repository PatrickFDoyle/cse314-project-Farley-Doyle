This function takes in one input. A dataframe. (Note this dataframe must contain the columns positive_ratings, and negative_ratings)
It returns a list where the first item is the total of postive reviews for all of the given games, and the second item is the total of negative reviews for all those games.

Example
Input
games = pd.Dataframe({"positive_ratings":[2,3]},{"negative_ratings":[3,4]})
SumReviews(games)

Return
[5,7]