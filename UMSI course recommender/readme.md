1) **UMSI course recommender.ipynb** reads courseenrollment.txt and coursetitles.txt, and recommends 5 courses to take for each SI course based on the cosine score similarity. The recommendations exclude the foundation courses and those that were taken by no more than a single student. It also generates the top 2 matches for each SI course to coursepairs.txt.

**Course pairs network**
![course network.png](https://github.com/shngli/Data-Mining-Python/blob/master/UMSI%20course%20recommender/course%20network.png)

2) **Course database.ipynb** outputsevery pair of courses (Source Course and Target Course) and their Cosine Similarity scores to allpairs.txt. **createDB.py** then creates a database classSimilarity.db and create tables for allpairs.txt, and uses SQL queries to insert the data (the source class, the target class, and the cosine similarity value) into the database. **Course database.ipynb** then queries the database for courses with cosine similarity value in distinct ranges of 0 <= x <= 0.25, 0.25 < x <= 0.5, 0.5 < x <= 0.75, 0.75 < x <= 1. **Output**: cosine0.25.txt, cosine0.25-0.5.txt, cosine0.5-0.75.txt, cosine0.75-1.txt. 
