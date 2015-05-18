# Author: Chisheng Li
# Create courseSmilarity.db and insert values from allpairs.txt
# scourse: source course; tcourse: target course; score: cosine similarity

import sqlite3 as lite
import sys

con = None
try:
    con = lite.connect('courseSmilarity.db')
    cur = con.cursor()  
    cur.execute("CREATE TABLE courses(scourse varchar(50), tcourse varchar(50), score float)")
    courses=open('allpairs.txt').readlines()
    for line in courses:
        line1=line.strip()
        (course1,course2,score)=line1.split('\t')
        cur.execute("insert into courses(scourse, tcourse, score) values(?,?,?)",(course1,course2,score))
    con.commit()
        
except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:
    if con:
        con.close()