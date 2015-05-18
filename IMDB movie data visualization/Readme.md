The updated IMDB datasets are accessible at ftp://ftp.fu-berlin.de/pub/misc/movies/database/.

1) Create a world map to display the average movie rating by country. **countRatings.py** reads countries.list and ratings.list, and compiles the countries and each rating score into countryRating.txt. **avgCountRats.py** then calculates the average ratings score for each country and outputs avgRating.txt. See the world map visualization **[here](http://www-969.ibm.com/software/analytics/manyeyes/#/visualizations?view=200523)**.
![IMDB world map.png](https://github.com/shngli/Python-data-manipulation/blob/master/IMDB%20movie%20data%20visualization/IMDB%20world%20map.png)

2) Create a wordle from the titles of all movies in a genre. **genreWordle.py** reads genres.list and compiles all comedy movie titles into comedyNames.txt. **filterNames.py** then filter some common stopwords from the list and outputs the new list into filterNames.txt. See the visualized wordle **[here](http://www-958.ibm.com/software/data/cognos/manyeyes/visualizations/imdb-comedy-titles)**. ![Comedy title wordle.png](https://github.com/shngli/Python-data-manipulation/blob/master/IMDB%20movie%20data%20visualization/Comedy%20title%20wordle.png)

3) Create a line chart (the new IBM Many Eyes does not offer stackgraph visualization) of the number of movies made in each genre over time. **genreStack.py** reads genres.list and compiles the genres and their years into genreYear.txt. **sortGreYr.py** then sorts the list and outputs them into a table in sortGreYr.txt. See the visualized line chart **[here](http://www-969.ibm.com/software/analytics/manyeyes/#/visualizations?view=200532)**.
![IMDB genre year.png](https://github.com/shngli/Python-data-manipulation/blob/master/IMDB%20movie%20data%20visualization/IMDB%20genre%20year.png)

4) **imdb.py** extracts the top 100 movies from the IMDB website with Beautifulsoup and plots a network of actors using pydot. **Output**: IMDBtop100.html, TitlesRanks.txt, MoviesJSON.txt, MoviesActors.txt. The actors network (see raw file to enlarge):
![ActorsNetwork.png](https://github.com/shngli/Python-data-manipulation/blob/master/IMDB%20movie%20data%20visualization/ActorsNetwork.png)
