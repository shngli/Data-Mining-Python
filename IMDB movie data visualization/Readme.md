IMDB movie data visualization
----------------------------

Retrieve the updated IMDB datasets countries.list.gz, genres.list.gz and ratings.list.gz at ftp://ftp.fu-berlin.de/pub/misc/movies/database/.

**IMDB visualization.ipynb:**

1) Create a world map to display the average movie rating by country. 

![world map.png](https://github.com/shngli/Data-Mining-Python/blob/master/IMDB%20movie%20data%20visualization/world%20map.png)

2) Create a wordle from the titles of all movies in the comedy genre. 

![Comedy title wordle.png](https://github.com/shngli/Data-Mining-Python/blob/master/IMDB%20movie%20data%20visualization/Comedy%20title%20wordle.png)

3) Create a line plot (the new IBM Many Eyes doesn't have stackgrpah visualization anymore) of the number of movies made in each genre (for an individual country or all countries combined) over time.

![Movie Genre lineplot.png](https://github.com/shngli/Data-Mining-Python/blob/master/IMDB%20movie%20data%20visualization/Movie%20Genre%20lineplot.png)

4) **imdb.py** extracts the top 100 movies from the IMDB website with Beautifulsoup and plots a network of actors using pydot. **Output**: IMDBtop100.html, TitlesRanks.txt, MoviesJSON.txt, MoviesActors.txt. The actors network (see raw file to enlarge):
![ActorsNetwork.png](https://github.com/shngli/Data-Mining-Python/blob/master/IMDB%20movie%20data%20visualization/ActorsNetwork.png)
