### InsightDataScience Coding Challenge Final
***Hsin-Ju (Michael), Tung - ChemE Grad at University of Washingotn***

### Description

This is insight data science coding challenge. In this challenge, it requires you to:

"Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.  You will thus be calculating the average degree over a 60-second sliding window."

The detail challenge instruction can see [here][1]

I wrote it in Python language to slove this challenge. The following will show the workflow and methods I used to slove this problem. To execute it, you can simply run `./run.sh` from the command line.


### Software dependencies

**All the required software is open source.**  The implementation was done using the following language and packages.

**Programming language:**   
Python version 2.7  ([https://www.python.org/](https://www.python.org/))

**Python packages needed:**
- NumPy 1.10.4
- pandas 0.18.0

### Workflow and Methods

The data showing here are just example to illustrate my algorithm


**Step 1** 

Read one tweet from the input file each time, convert the data form to the data structure that only contains the hashtags and created time information, shown as in the diagram, and store it. 

**Function 1** 

Find the maximum and the minimum time from that data sets, remove the minimum time data if `max_time - min_time` > 60 seconds, until `max_time - min_time` <= 60 seconds. 

 **Step 2** 

Now we have data sets that are within 60 seconds time window. Extract the hashtags from there and do the average degree calculation.


**Function 2** 

To make the program more efficient, if the new hashtags are same as previous hashtags then return the same average degree value.Note: the hashtags mentioned here are the stored hashtags that within 60 seconds timewindow. If they are not, then do the average degree calculation (Function 3)

**Function 3** 





[1]: https://github.com/hsintmike/InsightDataScience/blob/master/instruction.md "here"




