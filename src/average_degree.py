"""
Python script for calculating average degree in Twiiter hashtags graph for the last 60 seconds
It reads each input twitter and outputs the average degree simulaneously
Add --print argument to print out the vaules on the screen
It also prints out the total tweets and running time at the end
"""

import numpy as np
import pandas as pd
import os
import sys
import json
from dateutil import parser
from itertools import combinations, permutations
import time


# Check the input argument

if len(sys.argv) == 3:
    fileinput = sys.argv[1]
    fileoutput = sys.argv[2]
    printornot = "noprint"
if len(sys.argv) == 4:
    fileinput = sys.argv[1]
    fileoutput = sys.argv[2]
    printornot = sys.argv[3]

#Function 1
def timewindow(df):
    """
    Function to decide input tweets are within 60 seconds time window or not

    Parameters
    -----------
    df : pandas dataframe
         A pandas dataframe with the contents of the file,
         The first row index should starts with 0


    Returns
    --------
    Pandas dataframe that evict the tweets outside the 60 seconds time window

    """

    if len(df) <= 1:
        pass

    if len(df) > 1:

        s = 61
        while s > 60:

            maximum = max(df['created_at'])
            minimum = min(df['created_at'])

            c = parser.parse(maximum) - parser.parse(minimum)

            s = c.seconds

            if s > 60:
                df = df[df.created_at != minimum]  # drop minimum

            if s < 60:
                continue

        df.reset_index(drop=True)

    return df

#Function 2
def count(df, ref, prvd):
    """
    Function that return the average degree from a "60 seconds time window" pandas dataframe

    Note: gy is the function that actually do the math

    Parameters
    -----------
    df : pandas dataframe
    ref : list of tuples that contains hashtags within previous time window
    prvd : int, the average degree of previous time window

    Returns
    -------
    average degree: int
    list of tuples: that contains updated hashtags within current time window

    """
    gw = []
    for i in range(0, len(df)):
        lst = df['hashtags'][i]
        if len(lst) != 0:
            gw.append(lst)
    gwt = [tuple(x) for x in gw]
    
    if set(gwt) == set(ref):
        
        return prvd, gwt
        
    avedegree = gy(gw)
        
    return avedegree, gwt

#Function 3
def gy(lst):
    """
    The algorithm that calculate the average degree of tweets hashtags graph
    

    Parameters
    -----------
    lst : list contains exist hashtags within time window 

    Returns
    -------
    average degree: int

    """
    att = [item for sublist in lst for item in sublist]  # Flatten the list

    index = set(att)

    dictt = {s:nx for nx, s in enumerate(index)}

    gyma = np.zeros([len(index), len(index)])  # Empty Matrix


    pointer = []
    for i in lst:
        for item in combinations(i, 2):
            pointer.append([dictt[item[0]], dictt[item[1]]])
    if len(pointer) == 0:
        return 0
    
    
    if len(pointer) != 0:
        
        for i in pointer:

            gyma[i[0]][i[1]] = 1
            gyma[i[1]][i[0]] = 1

    nodelst = [x for x in lst if len(x) > 1]

    node_flat = [item for sublist in nodelst for item in sublist]

    node = len(set(node_flat))
    

    return gyma.sum()/float(node)



# Start recording the time
start_time = time.time()


# Start reading the file
with open(fileinput, 'r') as f:
    
    dataf = []              # data list [(hashtag and created_at)]  
    avad = []               # All output data
    G = 0                   # Initial value of average of degree
    ref = []                # Initial list of tweet hashtags
    
    for line in f:          # Read line
        
        if line.startswith('{"created_at":'):    #Skip limited data
            data = json.loads(line)
            created_at = [data['created_at']]
            hashtag = [data['entities']["hashtags"]]
            
            

            # Convert hashtags into list
            for nx, n in enumerate(hashtag):
                hashword = []
                for y in n:
                    hashword.append(y['text'])
                dataf.append((hashword, created_at[nx]))

            
            # Make pandas dataframe    
            df = pd.DataFrame(dataf, columns=['hashtags', 'created_at'])

            
            within_sixty = timewindow(df)   #Evict the tweet outside the 60 seconds time window
            

            dataf = within_sixty.values.tolist()  # Update dataf
            
            dataf = [tuple(x) for x in dataf]
            
            
            newf = pd.DataFrame(dataf, columns=['hashtags', 'created_at'])   # Updated pandas dataframe
            
 
            
            # count function

            G, ref = count(newf, ref, G)
            
 
            avad.append(G)
            
            if printornot == "--print":
                print "%.2f" % (G)
            
            # Avoid overfloating 
            if G > 100:
                print "Opps, there must be something wrong"
                break
    
    with open(fileoutput, 'w') as f:
        for s in avad:
            f.write("%.2f" % (s) + '\n')

    
print ("%s Tweets     " % (len(avad)) + "--- %s seconds ---" % (time.time() - start_time))
