'''
Created on July 1st, 2018
author: Julian Weisbord
description: Determine the n highest rated movies for each genre in the MovieLens data set.
'''
import time
import pandas as pd
from collections import defaultdict
from operator import itemgetter

N_HIGHEST = 5
DATASET = './ml-latest-small'


def top_n(n_highest):
    '''
    Description: Compute a dictionary of movie genre keys and movie rating tuples as values. Each tuple
                    contains: (Movie ID, Number of Ratings, Rating). At the end, this function prints the
                    top rated movies for each genre.
    Input: n_highest <int> the number of movies to print for each genre
    '''
    # Get columns of movieid, genre, and rating from ratings.csv and movies.csv
    ratings_tbl = pd.read_csv(DATASET + '/ratings.csv')
    movies_tbl = pd.read_csv(DATASET + '/movies.csv')
    # Create a set of all the different movie genres
    genres = [genre for genre_str in movies_tbl[['movieId', 'genres']]['genres'] for genre in genre_str.split('|')]
    genres = set(genres)
    if 'IMAX' in genres:  # Remove IMAX because that isn't really a genre and it isn't in the README as a genre.
        genres.remove('IMAX')

    # Create a dictionary of average rating values of all movies that contain that genre in their list of genres.
        # Only choose movies that have received greater/equal to 4.25/5 recommendation for consideration.
    best_movies = set(ratings_tbl[ratings_tbl['rating'] >= 4.25]['movieId'])
    best_movies_tbl = movies_tbl.loc[movies_tbl['movieId'].isin(best_movies)]
    best_movies_tbl = best_movies_tbl.reset_index(drop=True)

    avg_movie_ratings = defaultdict(list)  # Type: {genre: [(movieId, num_movie_ratings, avg_rating)]}

    for genre in genres:
        for idx, movieId in enumerate(best_movies_tbl['movieId']):
            genre_str = best_movies_tbl[best_movies_tbl['movieId'] == movieId]['genres'][idx]
            if genre in genre_str:

                movie_ratings = 0
                num_movie_ratings = len(ratings_tbl[ratings_tbl['movieId'] == movieId]['rating'])
                if num_movie_ratings == 0:
                    continue  # No ratings for this movie so move to next movie
                movie_ratings = ratings_tbl[ratings_tbl['movieId'] == movieId]['rating'].sum()
                avg_rating = movie_ratings / num_movie_ratings
                avg_movie_ratings[genre].append((movieId, num_movie_ratings, avg_rating))
            else:
                continue
    # Return the 5 highest values for each genre
    print("Output Format: [(Movie ID, Number of Ratings, Rating)] ->")
    for genre in genres:
        tie_breaker(genre, avg_movie_ratings)

def tie_breaker(genre, avg_movie_ratings):
    '''
    Description: Selects N_HIGHEST rated movies for a genre, if ther is an n way tie, prioritize the
                     movies with the most ratings.
    Input: genre <string> A single movie genre, avg_movie_ratings <dict of <string:list of tuples>>
               is a structure that stores info about each movie within a genre.
    '''
    max_rating = max(avg_movie_ratings[genre], key=itemgetter(2))[2]
    max_list = [tup for tup in avg_movie_ratings[genre] if tup[2] == max_rating]
    max_list.sort(key=lambda tup: tup[1], reverse=True)
    top_n_tup = max_list[:N_HIGHEST]

    if len(max_list) < N_HIGHEST:  # Case where there isn't a tie
        top_n_tup = sorted(avg_movie_ratings[genre], key=lambda tup: tup[2], reverse=True)[:N_HIGHEST]

    print("\nGenre: ", genre)
    print(top_n_tup)

def main():
    start_time = time.time()
    top_n(N_HIGHEST)
    end_time = time.time() - start_time
    print("Took {} seconds".format(end_time))

if __name__ == '__main__':
    main()
