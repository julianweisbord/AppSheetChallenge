'''
Created on July 1st, 2018
author: Julian Weisbord
description: Recommend n similar movies for a given movie, using the MovieLens data set.
'''
import sys
import math
import pandas as pd

DATASET = './ml-latest-small'
DEFAULT_MOVIEID = 1
LIKE_MOVIE_THRESH = 3.75
MAX_RATING = 5
SIMILAR_N = 5
SIMILARITY_RANGE = .5


def get_input_movie(movieId, movies_tbl, ratings_tbl):
    '''
    Description: Given an input movie id, this function determines the average user rating and genres.
    Input: movieId <int> the movies unique identifier, movies_tbl <Pandas DataFrame> dataframe of
               movies.csv file, ratings_tbl <Pandas DataFrame> dataframe of ratings_tbl file.
    Return: avg_rating <float> the average rating for movieId, total_ratings <int> total number
            of ratings for movieId, genres <list of strings> all the movieId genres.
    '''
    ratings_sum = ratings_tbl[ratings_tbl['movieId'] == movieId]['rating'].sum()
    total_ratings = len(ratings_tbl[ratings_tbl['movieId'] == movieId])
    avg_rating = ratings_sum / total_ratings
    if avg_rating < LIKE_MOVIE_THRESH:
        print("Movie rating is less than {}/5, no one liked the movie, exiting...".format(LIKE_MOVIE_THRESH))
        exit()

    # Get genres of input movie
    genres = list(movies_tbl[movies_tbl['movieId'] == movieId]['genres'])[0].split('|')
    if 'IMAX' in genres:  # Remove IMAX because that isn't really a genre and it isn't in the README as a genre.
        genres.remove('IMAX')
    return avg_rating, total_ratings, genres

def calc_similarity(input_rating_genre, movies_tbl, ratings_tbl):
    '''
    Description: Manipulates input data to create a table of movies that users rated similarly to the input
                     movie and also have the same genres.
    Input: input_rating_genre <list of movieId, avg_rating, total_ratings, genre_list>, movies_tbl <Pandas DataFrame>
               dataframe of movies.csv file, ratings_tbl <Pandas DataFrame> dataframe of ratings_tbl file.
    '''
    movieId_inp, avg_rating_inp, total_ratings_inp, genres_list = input_rating_genre
    # Create a table of all users who liked input movie (>= LIKE_MOVIE_THRESH) and all the other movies
    # they rated +/-.SIMILARITY_RANGE with the same genres.
    users_liked_movie = list(ratings_tbl[ratings_tbl['movieId'] == movieId_inp][ratings_tbl['rating'] >= LIKE_MOVIE_THRESH]['userId'])
    rating_range = [avg_rating_inp - SIMILARITY_RANGE, avg_rating_inp + SIMILARITY_RANGE]
    # List of movie entries where the users liked the movie and gave it a rating within +/- .5 of the input movie
    user_tbl = ratings_tbl.loc[ratings_tbl['userId'].isin(users_liked_movie)][ratings_tbl['rating'] >= rating_range[0]]
    user_tbl = user_tbl[ratings_tbl['rating'] <= rating_range[1]]
    possible_movies = list(user_tbl['movieId'])

    # Create table based on user_tbl where each movieId has same genres ase input genre_list
    mv_frame = movies_tbl.loc[movies_tbl['movieId'].isin(possible_movies)][['genres', 'movieId']]
    mv_frame = mv_frame.reset_index(drop=True)
    drop_idx = 0
    for idx, row in mv_frame.iterrows():
        genre_check = True
        for genre in genres_list:
            if genre not in row['genres']:
                genre_check = False
                break
        if genre_check == False:
            mv_frame = mv_frame.drop(mv_frame.index[drop_idx])  # Drop tables that don't contain the same genres.
            mv_frame = mv_frame.reset_index(drop=True)
            drop_idx -= 1
        drop_idx += 1
    similar_movieIds = list(mv_frame['movieId'])
    if movieId_inp in similar_movieIds:
        similar_movieIds.remove(movieId_inp)

    similar_tbl = ratings_tbl.loc[ratings_tbl['movieId'].isin(similar_movieIds)]

    similar_movies = []  # similar_movies Type = [(movieId, num_rating_>=_4.0, avg_rating), ...]
    for movieId in similar_movieIds:
        num_ratings = len(similar_tbl[similar_tbl['movieId'] == movieId])
        avg_rating = similar_tbl[similar_tbl['movieId'] == movieId]['rating'].sum() / num_ratings
        similar_movies.append([movieId, num_ratings, avg_rating])

    # Create a matrix of weighted euclidean distance of the previous table compared to input movie
    input_movie_ratings = [movieId_inp, total_ratings_inp, avg_rating_inp]
    print("\ninput movie: ", input_movie_ratings)
    euclid_dists = weighted_euclidean(input_movie_ratings, similar_movies)

    # Return most similar by taking the min n movies of this matrix
    top_n_tup = sorted(euclid_dists, key=lambda tup: tup[1], reverse=False)[:SIMILAR_N]
    if len(top_n_tup) < SIMILAR_N:
        print("Did not find {} similar movies based on movies with the same genre and rating +/- {}".format(SIMILAR_N, SIMILARITY_RANGE))
    print("\n Top n Movies, (Movie Id, Similarity score):", top_n_tup)

def euclid_norm(a, b, max_val):
    '''
    Description: Helper function that calculate norm of a and b.
    '''
    norm = (a - b) / max_val
    return norm

def weighted_euclidean(input_movie_ratings, similar_movies):
    '''
    Description: Calculates the euclidean distance between the input movie and the list of
                    of similar movies that users also liked. The euclidean parameters are
                    rating similarity and popularity similarity, they are weighted 6:1.
    Input: input_movie_ratings <list of tuples (movieId, num_rating, avg_rating)>,
               similar_movies <list of tuples (movieId, num_rating, avg_rating)>
    Return: euclid_dists <list of tuples (movieId, int)> the movieIds and euclidean distances
                measured as differences from the input movie.
    '''
    euclid_dists = []
    max_num_ratings = max(map(lambda x: x[1], similar_movies))  # For normalization

    for mov_pos, movie in enumerate(similar_movies):
        euclid_dists.append(
            (movie[0], math.sqrt((euclid_norm(input_movie_ratings[1], similar_movies[mov_pos][1], max_num_ratings))**2
                                 + 6 *(euclid_norm(input_movie_ratings[2], similar_movies[mov_pos][2], MAX_RATING))**2)))
    return euclid_dists

def main():

    movieId = DEFAULT_MOVIEID
    if len(sys.argv) == 2:
        movieId = int(sys.argv[1])
        print("input movie id: ", movieId)

    movies_tbl = pd.read_csv(DATASET + '/movies.csv')
    ratings_tbl = pd.read_csv(DATASET + '/ratings.csv')
    avg_rating, total_ratings, genre_list = get_input_movie(movieId, movies_tbl, ratings_tbl)
    input_rating_genre = [movieId, avg_rating, total_ratings, genre_list]
    calc_similarity(input_rating_genre, movies_tbl, ratings_tbl)

if __name__ == '__main__':
    main()
