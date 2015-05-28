# Sheng Li
# Task: Read sentences.txt and output the total number of pairs of sentences which are edit distance <= 1.
# Result: 429493953 total matching pairs (at edit distance <= 1) from the list of 9397023 sentences. 
# 426873920 matches are because of duplicate lines.

import string
import time
import random
from math import floor
from collections import defaultdict

def edit1(s1,s2):
    # Take two lists and return true if they differ in one element by one of:
    # deletion, insertion, mutation   
    l1 = len(s1)
    l2 = len(s2)
    if l1 == l2:
        n = 0
        for i in xrange(l1):
            if s1[i] != s2[i]:
                n += 1
                if n == 2:
                    return False
        return True
    elif l1 == l2 - 1:
        i = 0
        j = 0
        while i < l1:
            if s1[i] != s2[j]:
                j += 1
                if j-i == 2:
                    return False
            else:
                i += 1
                j += 1
        return True
    elif l1 == l2 + 1:
        i = 0
        j = 0
        while j < l2:          
            if s1[i] != s2[j]:
                i += 1
                if i-j == 2:
                    return False
            else:
                i += 1
                j += 1
        return True
    else:
        return False

def main():
    start_time = time.time()
    
    sent_file = open("sentences.txt", "r")
    
    # Compute word list and store sentence words
    s_list = []
    s = sent_file.readline()

    while not (s == ""):
        s_words = (s[:-1]).split()
        if len(s_words) >= 10:
            s_list.append(s_words)
        s = sent_file.readline()

    n_sent = len(s_list)
    
    sent_file.close()   

    
    run_time = time.time() - start_time
    run_min = floor(run_time/60)
    run_sec = round(run_time - 60 * run_min,2)
    print "Done constructing word list"
    print "Running time: " + str(run_min) + " minutes, " + str(run_sec) + " seconds"
    start_time = time.time()
    
    # Remove duplicates and write output files
    # Sort by the sentence and ignore the line number
    s_list.sort(key=lambda s: s[1:])
    
    nodupes = open("sentnodupes.txt", "w")
    dupelist = open("sentdupelist.txt", "w")
    
    k = 0
    dup_matches = 0
    dup_count = 1
    tmp_list = []
    for k in xrange(n_sent):
        if k == n_sent - 1 or s_list[k][1:] != s_list[k+1][1:]:
            # Output the unique sentences, append the number of sentence duplicates to the end
            nodupes.write(" ".join(s_list[k]) + " " + str(dup_count) + "\n")
            if dup_count > 1:
                # Count number of duplicates
                dup_matches += (dup_count * (dup_count - 1))/2
                # Write duplicates to file
                dupelist.write(s_list[k][0] + " " + " ".join(tmp_list) + "\n")
                dup_count = 1
                tmp_list = []
        else:
            dup_count += 1
            tmp_list.append(s_list[k][0])
    
    nodupes.close()
    dupelist.close()
    
    del s_list
    
    print "Total matches due to duplicates: " + str(dup_matches)
    
    run_time = time.time() - start_time
    run_min = floor(run_time/60)
    run_sec = round(run_time - 60 * run_min,2)
    print "Done printing duplicate free file and duplicate list"
    print "Running time: " + str(run_min) + " minutes, " + str(run_sec) + " seconds"
    start_time = time.time()


    # Count the total matches from the duplicated lines
    tot = dup_matches
        
    nodupes_read = open("sentnodupes.txt", "r")
    
    # Compute the word list that is duplicate-free and store the words    
    s_list = []
    s = nodupes_read.readline()

    while not (s == ""):
        s_words = (s[:-1]).split()
        if len(s_words) >= 10:
            s_list.append(s_words)
        s = nodupes_read.readline()

    n_sent = len(s_list)
    
    sent_file.close()    
    
    s_list.sort(key=len)
    
    run_time = time.time() - start_time
    run_min = floor(run_time/60)
    run_sec = round(run_time - 60 * run_min,2)
    print "Done reading duplicate free list and sorting by number of words"
    print "Running time: " + str(run_min) + " minutes, " + str(run_sec) + " seconds"
    start_time = time.time()
    
    # For odd number sentence length
    h1o = defaultdict(list)
    h2o = defaultdict(list)
    
    # For even number sentence length
    h1e = defaultdict(list)
    h2e = defaultdict(list)
    
    # 2 dictionaries to store the first 5 words and last 5 words as keys
    # And list the sentence number as values
    h1 = [h1e,h1o]
    h2 = [h2e,h2o]
                   
    # Store the list of values as tuples (index 1, index 2, weight)
    # Weight is the product of the number of duplicates between 2 sentences
    match1 = set()
    
    p = 12
    i = 0
    while(True):
        if (i == n_sent or len(s_list[i]) > p):
            # Get all the pairs of length p
            for k in h1[p%2].keys():
                for m in xrange(len(h1[p%2][k])):
                    ind1 = h1[p%2][k][m]
                    for n in xrange(m+1,len(h1[p%2][k])):
                        ind2 = h1[p%2][k][n]
                        if edit1(s_list[ind1][1:-1],s_list[ind2][1:-1]):
                            mult = int(s_list[ind1][-1]) * int(s_list[ind2][-1])
                            if ind1 < ind2:
                                match1.add((ind2,ind1, mult))
                            else:
                                match1.add((ind2,ind1, mult))
            for k in h2[p%2].keys():
                for m in xrange(len(h2[p%2][k])):
                    ind1 = h2[p%2][k][m]
                    for n in xrange(m+1,len(h2[p%2][k])):
                        ind2 = h2[p%2][k][n]
                        if edit1(s_list[ind1][1:-1],s_list[ind2][1:-1]):
                            mult = int(s_list[ind1][-1]) * int(s_list[ind2][-1])
                            if ind1 < ind2:
                                match1.add((ind2,ind1, mult))
                            else:
                                match1.add((ind2,ind1, mult))
            tmp = 0
            for m in match1:
                tmp += m[2]
            tot += tmp
            del match1
            match1 = set()
            
            # Get all the pairs of length p & p-1
            for k in h1[p%2].keys():
                if h1[(p+1)%2].get(k,-1) != -1:
                    for m in xrange(len(h1[p%2][k])):
                        ind1 = h1[p%2][k][m]
                        for n in xrange(len(h1[(p+1)%2][k])):
                            ind2 = h1[(p+1)%2][k][n]
                            if edit1(s_list[ind1][1:-1],s_list[ind2][1:-1]):
                                mult = int(s_list[ind1][-1]) * int(s_list[ind2][-1])
                                if ind1 < ind2:
                                    match1.add((ind2,ind1,mult))
                                else:
                                    match1.add((ind2,ind1,mult))
            for k in h2[p%2].keys():
                if h2[(p+1)%2].get(k,-1) != -1:
                    for m in xrange(len(h2[p%2][k])):
                        ind1 = h2[p%2][k][m]
                        for n in xrange(len(h2[(p+1)%2][k])):
                            ind2 = h2[(p+1)%2][k][n]
                            if edit1(s_list[ind1][1:-1],s_list[ind2][1:-1]):
                                mult = int(s_list[ind1][-1]) * int(s_list[ind2][-1])
                                if ind1 < ind2:
                                    match1.add((ind2,ind1,mult))
                                else:
                                    match1.add((ind2,ind1,mult))
            tmp = 0
            for m in match1:
                tmp += m[2]
            tot += tmp
            del match1
            match1 = set()
            
            h1[(p+1)%2] = defaultdict(list)
            h2[(p+1)%2] = defaultdict(list)
            p += 1
            if i == n_sent:
                break      
        else:
            # Add the sentence to the dictionaries
            cur_list = s_list[i]
            cur_str = ' '.join(cur_list[1:6])
            h1[p%2][cur_str].append(i)
            cur_str = ' '.join(cur_list[-6:-1])
            h2[p%2][cur_str].append(i)
            i += 1            
        
    run_time = time.time() - start_time
    run_min = floor(run_time/60)
    run_sec = round(run_time - 60 * run_min,2)
    print "Done counting: " + str(tot) + " matches!"
    print "Running time: " + str(run_min) + " minutes, " + str(run_sec) + " seconds"
    start_time = time.time()
    
if __name__ == "__main__":
    main()