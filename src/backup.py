import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import json
from dateutil import parser
from itertools import combinations, permutations
import time
import os, sys

fileinput = sys.argv[1]
fileoutput = sys.argv[2]


def timewindow(df):
    if len(df) <=1:
        pass
   
    if len(df) > 1:
        Fl = len(df)  #Frame length

        for i in range(Fl-1,0,-1):
            x = parser.parse(df['created_at'][0])
            z = parser.parse(df['created_at'][i-1])
            y = parser.parse(df['created_at'][i])
            
            if y >= x:
                c = y - x
            if y < z:
                c = z - y
            
            s = c.seconds
            
            if s > 60:
                df = df.ix[1:]
                df =  df.reset_index(drop=True)
            
            if s < 60:
                break
                
                
                
    return df



def new_window(df):
    if len(df) <=1:
        pass
    
    if len(df) > 1:
        
        s = 61
        while s > 60:
        
            maximum = max(df['created_at'])
            minimum = min(df['created_at'])


            c =  parser.parse(maximum) - parser.parse(minimum) 

            s = c.seconds

            if s > 60:
                df = df[df.created_at != minimum]  #drop minimum

            if s < 60:
                continue

        
        
        df.reset_index(drop=True)
        
    return df


def speedup_count(df, ref, prvd):
    
    gw = []
    for i in range(0,len(df)):
        lst = df['hashtags'][i]
        if len(lst) != 0:
            gw.append(lst)
    gwt = [tuple(x) for x in gw]
    

    
    if set(gwt) == set(ref):
        
        return prvd, gwt
        
    avedegree = gy(gw)
        
    return avedegree, gwt

def gy(lst):
    att = [item for sublist in lst for item in sublist]


    index = set(att)

    dictt = {s:nx for nx, s in enumerate(index)}


    gyma = np.zeros([len(index),len(index)]) #Empty Matrix


    pointer = []
    for i in lst:
        for item in combinations(i,2):
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
    
    #print node
    #print gyma.sum()
    return gyma.sum()/float(node)



start_time = time.time()


with open(fileinput,'r') as f:
    
    alldf = pd.DataFrame()  # Empty dataframe
    dataf = []              # Empty data[hashtag and created_at]
    
    avad = []
    
    G = 0
    ref = []
    
    for line in f:          # Read line
        
        if line.startswith('{"created_at":'):
            data = json.loads(line)
            created_at = [data['created_at']]
            hashtag = [data['entities']["hashtags"]]
            
            

            # convert data
            for nx, n in enumerate(hashtag):
                hashword = []
                for y in n:
                    hashword.append(y['text'])
                dataf.append((hashword, created_at[nx]))

            
            # Make pandas dataframe    "
            df = pd.DataFrame(dataf,columns=['hashtags','created_at'])

            
            
            
            within_sixty = new_window(df)
            
            dataf = within_sixty.values.tolist()  #Update dataf
            
            
            dataf = [tuple(x) for x in dataf]
            
            
            newf = pd.DataFrame(dataf,columns=['hashtags','created_at'])
            
            
            
            
            #count function
           
            
            G, ref = speedup_count(newf, ref, G)
            
           
        
        
            #print newf['hashtags']
            avad.append(G)
            
            #print "%.2f" % (G)
            
            if G > 10:
                print newf
                break
    with open(fileoutput, 'w') as f:
        for s in avad:
            f.write("%.2f" % (s) + '\n')


#cProfile.run('new_window(df)')
#cProfile.run('speedup_count(newf, ref, G)')
    
print("--- %s seconds ---" % (time.time() - start_time))



