import urllib2
import csv
import bottle
from bottle import route, request, response, template, get, run, HTTPResponse
import json
from bottle import static_file
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
#bottle = Bottle()

filename = open('data.csv','r')
myfile = open('./static/data.tsv','w')
c = 0
csv_reader = csv.reader(filename)
writer = csv.writer(myfile,delimiter = '\t')
for row in csv_reader:       
    c += 1
    if c == 50:
        break 
    row[6] = row[6].replace("+/-","")
    if row[0] == "" or row[1] == "" or row[2] == "" or row[3] == "" or row[4] == "" or row[5] == "" or row[6] == "":
        continue
    writer.writerow(row)
myfile.close()

@route('/static/<myfile>')
def server_static(myfile):
    return static_file(myfile, root="static")

@route('/bar1')
def bar1():   
    return template('index1.html')

@route('/bar2')
def bar2():   
    return template('index2.html')
    
@route('/scatter')
def scatter():
    fname = open('data.csv','r')
    reader = csv.reader(fname)
    c = 0
    myfile2 = open('./static/data2.tsv','w')
    wr = csv.writer(myfile2,delimiter = '\t')
    for row in reader:       
        c += 1
        if c == 800:
            break 
        row[6] = row[6].replace("+/-","")
        if row[0] == "" or row[1] == "" or row[2] == "" or row[3] == "" or row[4] == "" or row[5] == "" or row[6] == "":
            continue
        wr.writerow(row)
    myfile2.close()
    filename.close()   
    return template('index3.html')    

# geting data file
def getdata(attr1,attr2):
    #iterating through all rows
    for row in csv_reader:
        #import pdb
        #pdb.set_trace()
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

def kmeans_cluster():
    try:
        # listing all column names of dataset
        col_names = ["LINE_NUMBER","ESTIMATE"]
        # importing data set
        myfile3 = open("data.csv","r")
        # reading csv file using Dictreader
        csv_reader = csv.DictReader(myfile, fieldnames=col_names)
        #skipping the header line
        csv_reader.next()
        # initializing empty list
        mylist = []
        no_cluster = raw_input("Enter number of clusters k: ")
        k = int(no_cluster)
        # getting data file
        attr1 = 'LINE_NUMBER'
        attr2 = 'ESTIMATE'
        mylist = getdata(attr1,attr2)
        # initializing array 'data'
        data = []
        data = array(mylist)
        # applying k means algorithm to get centroids as 'res' and co-ordinate pair values as 'idx'
        res, idx = kmeans2(data,k)
        # initializing set of colors
        colors = ([([0.2,1,0.2],[1,0.2,0.2],[0.3,0.3,1])[i] for i in idx])
        # ploting points
        pylab.scatter(data[:,0],data[:,1], c=colors)
        pylab.scatter(res[:,0],res[:,1], marker='o', s = 400, linewidths=3, c='none')
        pylab.scatter(res[:,0],res[:,1], marker='x', s = 400, linewidths=3)
        fname = "koutput.png"
        # creating and saving output as a file
        pylab.savefig(fname)
        #print "Cluster Created, Check folder for output file"
        #return filename

    except Exception as e:
	      print str(e)

kmeans_cluster()
@route('/koutput.png')
def server_static():
    return static_file('koutput.png', root=".")

@route('/kmeans')
def ans_kmeans():
    return template(cluster.tpl)
    
if __name__ == '__main__':
    run(host='ec2-52-26-244-170.us-west-2.compute.amazonaws.com', port=8089, debug=True)

#end_all