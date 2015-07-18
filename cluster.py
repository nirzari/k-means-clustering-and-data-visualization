import csv
import pylab
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
import uuid
from matplotlib import *
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
from scipy.cluster.vq import *

# listing all column names of dataset
col_names = ["time","latitude","longitude","depth","mag","magType","nst","gap","dmin","rms","net","id","updated","place","type"]
# importing data set
myfile = open("earthquake.csv","r")
# reading csv file using Dictreader
csv_reader = csv.DictReader(myfile, fieldnames=col_names)
#skipping the header line
csv_reader.next()
# initializing empty list
mylist = []
# geting data file
def getdata(attr1,attr2):
    #Initializing counter
    c = 0
    #iterating through all rows
    for row in csv_reader:
        #import pdb
        #pdb.set_trace()
        #Incrementing counter
        c += 1
        # breaking loop if it exceeds 1000 records
        if c == 5000: 
            break
        # initializing an empty list for making pairs of x and y co-ordinates
        pair = []
        # replacing null values with zero
        if row[attr1] == "":
            row[attr1] = 0
        if row[attr2] == "":
            row[attr2] = 0
        x = float(row[attr1])
        y = float(row[attr2])
        # appending x co-ordinate       
        pair.append(x)
        # appending y co-ordinate
        pair.append(y)
        # apeending (x,y) to mainlist 'mylist'
        mylist.append(pair)
    return mylist

def main():
    try:
        # printing menu
        print "Choose Attribute from "
        print "1) latitude \n2) longitude \n3) depth \n4) mag \n5) nst \n6) gap \n7) dmin \n8) rms \n"
        # taking attribute 1 value from user
        attr1 = raw_input("Enter value of attribute 1: ")
        # taking attribute 2 value from user
        attr2 = raw_input("Enter value of attribute 2: ")
        # taking value for number of clusters from user
        no_cluster = raw_input("Enter number of clusters k: ")
        k = int(no_cluster)
        # getting data file
        mylist = getdata(attr1,attr2)
        # initializing array 'data'
        data = []
        data = array(mylist)
        # applying k means algorithm to get centroids as 'res' and co-ordinate pair values as 'idx'
        res, idx = kmeans2(data,k)
        for i in range(len(res)):
            x1 = res[i][0]
            y1 = res[i][1]
            # limiting decimal points up to 3
            x1 = float("{0:.3f}".format(x1))
            y1 = float("{0:.3f}".format(y1))
            #print x1
            #print y1
            for j in range(i+1,len(res)):
                x2 = res[j][0]
                y2 = res[j][1]
                # limiting decimal points up to 3
                x2 = float("{0:.3f}".format(x2))
                y2 = float("{0:.3f}".format(y2))
                #print x2
                #print y2
                dist = np.sqrt((x1-x2)**2 + (y1-y2)**2)
                print "Distance between cluster " + str(i) + " and cluster " + str(j) + " is: " + str(dist)
        # initializing set of colors
        clr = ([1, 1, 0.0],[0.2,1,0.2],[1,0.2,0.2],[0.3,0.3,1],[0.0,1.0,1.0],)
        colors = ([(clr)[i] for i in idx])
        # initializing dictionary having initial color counts
        clr_dict = {"yellow":0,"green":0,"red":0,"blue":0,"cyan":0}
        # incrementing color count
        for x in colors:
            if str(x) == "[1, 1, 0.0]":
                clr_dict["yellow"] += 1
            if str(x) == "[0.2, 1, 0.2]":
                clr_dict["green"] += 1
            if str(x) == "[1, 0.2, 0.2]":
                clr_dict["red"] += 1
            if str(x) == "[0.3, 0.3, 1]":
                clr_dict["blue"] += 1
            if str(x) == "[0, 1.0, 1.0]":
                clr_dict["cyan"] += 1         
        # printing number of points in each cluster
        for i in clr_dict:
            if clr_dict[i] == 0:
                continue
            print "No of points in cluster with " + str(i) + " is: " + str(clr_dict[i])   
        # ploting points
        pylab.scatter(data[:,0],data[:,1], c=colors)
        pylab.scatter(res[:,0],res[:,1], marker='o', s = 400, linewidths=3, c='none')
        pylab.scatter(res[:,0],res[:,1], marker='x', s = 400, linewidths=3)
        # generating unique file name
        fname = uuid.uuid4()
        filename = str(fname) +".png"
        # creating and saving output as a file
        pylab.savefig(filename)
        print "Cluster Created, Check folder for output file"

    except Exception as e:
	print str(e)
        print "*** Enter valid Input ***"

main()
# end_all
