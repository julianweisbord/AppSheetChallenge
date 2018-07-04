## Results:
1.) Write a program that prints out the top-5 highest-rated movies for each genre. 

Usage: python3 highest_ranked.py

To do this, I considered the different ways that this app would define highest-rated movies. I chose the literal definition, taking the movies with the highest average rating but I imagine that in other rating systems, the highest rated movies might be weighted by the number of people that rated them (I.e a movie with an average rating of 4.5 with 10,000 ratings would be considered better than a 5.0 movie with 2 ratings)

For the final output, my program prints out the top rated movies but also includes functionality that returns the highest rated movies with the most number of user ratings in the case of a tie.

<img src="https://github.com/julianweisbord/AppSheetChallenge/blob/master/imgs/highest_rated.png" width="425" height="375"/>

2.) Write a program that prints out the 5 most similar movies to a given input movie, assuming that two movies are similar if people who like one movie tend to like the other movie. Write a couple of sentences justifying your choice of similarity.

Usage: python3 recommender.py <movie id>

I believe that the most important metrics of movie similarity is 1.) User's who liked movie A also rated movie B with around the same score, 2.) Movie A and Movie B contain the same genres and 3.) Popularity, around the same number of people watched and rated both Movie A and Movie B. For this problem, I created a python module (recommender.py) that takes movies with the same genre and outputs the top 5 movies that have the best normalized-weighted-euclidean similarity.

Input Movie (movieId: 1, Avg Rating: 3.87):


<img src="https://github.com/julianweisbord/AppSheetChallenge/blob/master/imgs/toy_story.jpg" width="125" height="150"/>


Similar Movies:

<p float="left">
	<img src="https://github.com/julianweisbord/AppSheetChallenge/blob/master/imgs/shrek.jpg" width="125" height="150"/>
	<img src="https://github.com/julianweisbord/AppSheetChallenge/blob/master/imgs/monsters_inc.jpg" width="125" height="150"/>
	<img src="https://github.com/julianweisbord/AppSheetChallenge/blob/master/imgs/toy_story2.jpg" width="125" height="150"/>
	<img src="https://github.com/julianweisbord/AppSheetChallenge/blob/master/imgs/Antz.jpeg" width="125" height="150"/>
	<img src="https://github.com/julianweisbord/AppSheetChallenge/blob/master/imgs/who_framed_roger_rabbit.jpg" width="125" height="150"/>
	
</p>


<img src="https://github.com/julianweisbord/AppSheetChallenge/blob/master/imgs/part2.png" width="700" height="65"/>


3.) Let's say you use your similarity function as a way to recommend movies. How would you evaluate the performance of your system? Write a paragraph or so explaining your performance metric and test methodology. 

For an app in production, I would have a feedback mechanism from the users. Once a user tells our app that they enjoyed a movie, the app will recommend other movies that they might like based on other users who enjoyed the movie they just watched. If the user then clicks on a recommended movie and rates it positively, that would be a positive evaluation. If they left a negative rating or maybe even didn't rate the recommend movie, that would be a negative evaluation of the app. For an advanced movie recommending agent, I could even implement a reinforcement learning model that rewarded our recommender system for positive evaluations and penalized the agent for negative evaluations.

## Install:
pip install -r ./dependencies.txt
