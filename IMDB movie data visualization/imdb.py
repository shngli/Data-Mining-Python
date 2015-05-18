# Author: Sheng Li

from bs4 import BeautifulSoup
import json, time, itertools, urllib2, re, unicodecsv
import pydot

# Step 1:
# Open the imdb link with urllib, read the html codes, and output the top 100 movies to step 1's html file
response = urllib2.urlopen("http://www.imdb.com/search/title?at=0&sort=num_votes&count=100")
IMDB = response.read()

step1 = open("IMDBtop100.html", "w")
step1.write(IMDB)

# Step 2:
# Output the top 100 movies' codes (eg. tt0068646), ranks and titles
soup = BeautifulSoup(IMDB)
#print soup prints out the entire html file
movieRanks = soup.td
#print movies prints <td class="number">1.</td>
movieOutput = list()
 
for i in range(100):
	# Typical rank tag in the html code <td class="number">2.</td>
	# Extract every movie rank by removing "." from the html code
	movieRank = movieRanks.string.replace(".", "")
	#print movieRank
	# Typical movie title tag in the html code: <a href="/title/tt0468569/" title="The Dark Knight (2008)">
	# Extract every movie code from the a href title tags
	movieCode = re.match(r'\/title\/([0-9A-Za-z]+)\/',str(movieRanks.find_next("a")['href'])).group(1)
	#print movieCode
	# Extract every movie title from the title tag
	movieTitle = movieRanks.find_next("a")['title']
	#print movieTitle
	movieOutput.append([movieCode, movieRank, movieTitle])
	# Move on to find the next movie rank
	movieRanks = movieRanks.find_next("a").find_next("td").find_next("td").find_next("td")
	'''1
	tt0111161
	The Shawshank Redemption (1994)
	2
	tt0468569
	The Dark Knight (2008)
	3
	tt1375666
	Inception (2010)
	'''
	
with open("TitlesRanks.txt", "w") as f:
	f.write("Movie Code\tMovie Rank\tMovie Title (Year)\n")
	f.write("-------------------------------------------------------\n")
	step2 = unicodecsv.writer(f, lineterminator="\n", delimiter="\t")
	step2.writerows(movieOutput)

# Step 3:
# Print out into a text file the information of all top 100 movies in JSON structure using OMDb API service
# checkout http://www.omdbapi.com/
jsonOutput = open("MoviesJSON.txt", "w")
for i in range(100):
	# Access each movie using its movie code
	# eg. The Shawshank Redemption at http://www.omdbapi.com/?i=tt0111161
	movieLink = "http://www.omdbapi.com/?i=" + movieOutput[i][0]
	# Open the OMDB link with urllib 
	JSONinfo = urllib2.urlopen(movieLink)
	OMDb = JSONinfo.read()
	jsonOutput.write(OMDb)
	jsonOutput.write("\n")
	
jsonOutput.close()

# Step 4:
# Print out to a text file a list of actors for all top 100 movies from MoviesJSON.txt
movieActors = open("MoviesJSON.txt", "rU")
actors = []

for i in range(100):
	actorsJSON = movieActors.readline()
	actorsDict = json.loads(actorsJSON)
	#Append movie titles and actors information to actors []
	actors.append([actorsDict['Title'], json.dumps(actorsDict['Actors'].split(", "))])
	# eg. [[u'The Shawshank Redemption', '["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"]']
movieActors.close()

actorsOutput = open("MoviesActors.txt", "w")
for i in range(100):
	# Extract movie titles and actors from actors []
	titleActors = actors[i][0] + u'\t' + actors[i][1] + u'\n'
	actorsOutput.write(titleActors.encode('UTF-8'))
	#Eg. The Shawshank Redemption	["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"]
actorsOutput.close()

# Step 5:
# Output a .dot file and add edges to create networks of actors from the top 100 movies
# Note: Use Graphviz to open .dot file and export to png or jpeg
graph = open("MoviesActors.txt", "rU")
with graph as f:
	textfile = unicodecsv.reader(f, delimiter = "\t")
	actorsList = list(textfile)

actorsNet = []
for i in range(100):
	# Extract list of actors
	actorsNet.append(actorsList[i][1].replace("[", "").replace("]", "").replace("\"", "").split(", "))
	# eg. [u'Daniel Craig', u'Judi Dench', u'Javier Bardem', u'Ralph Fiennes']

networkEdges = []
for i in range(100):
	# Create a list containing actors in pairs for network edges
    networkEdges.append(list(itertools.combinations(actorsNet[i], 2)))
    # eg. [(u'Daniel Craig', u'Judi Dench'), (u'Daniel Craig', u'Javier Bardem'), (u'Daniel Craig', u'Ralph Fiennes'), (u'Judi Dench', u'Javier Bardem'), (u'Judi Dench', u'Ralph Fiennes'), (u'Javier Bardem', u'Ralph Fiennes')]

# Plot a network of actors from networkEdges using pydot
network = pydot.Dot(graph_type='graph', charset="utf-8")

for i in range(100):
	for j in range(6):
		network.add_edge(pydot.Edge(networkEdges[i][j][0].encode("UTF-8"), networkEdges[i][j][1].encode("UTF-8")))

network.write_raw("ActorsNetwork.dot")
