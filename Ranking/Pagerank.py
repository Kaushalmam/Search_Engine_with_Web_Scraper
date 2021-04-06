# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:22:47 2020

@author: kaush
"""
import numpy as np         #including all the desired libraries
import nltk
import re
from nltk.stem.porter import PorterStemmer
import glob
from nltk.corpus import stopwords
import operator
#nltk.download('averaged_perceptron_tagger')
#Un-comment the line above if averaged_perceptron_tagger not installed

path=input("Please enter the path to www folder on your computer. This path should have two slashes for it to work. See example in code reference")
path="D:\\UIC\\Information Retrieval by Cornelia Caragea Spring 2020\\final project\\data"  #This stores the path for the data
folder = glob.glob(path+ "/*")           #opened folder with data

listdata = []                   #Declared the required variables
glistdata = []
global_mrr=[0 for i in range(10)] #this stores the global mrr score
c=0
ps= PorterStemmer()     #This will be used to stem the data
l=[]
for file in folder:             #this loop reads all the files and forms two text corpus(abstract and gold)
    x = file.split('\\')
    xg = gold_file.split('\\')
    if x[-1] == xg[-1]:             #we include only those files that have a gold standard file for it.
        l.append(x[-1])
        file_open=open(file,'r')    #Preprocessing is done
        file_read=file_open.read()
        clean = re.compile('<.*?>')
        word = re.sub(clean, '', file_read)
        word = word.lower()
        word = re.sub(r'[^\w\s]','',word)
        word = re.sub(r'[0-9]','',word)
        t=word.split()
        #print(t)
        stopWords = set(stopwords.words('english'))
        filtered = []
        for w in t:
            if w not in stopWords:
                filtered.append(w)   
        ps_data=[ps.stem(x) for x in filtered]
        listdata.append(ps_data)
        c+=1
        g=[]
        gfile_open=open(gold_file,'r')
        gfile_read=gfile_open.readlines()
        for each in gfile_read:             #similar process is done for each file in Gold folder
            delta=each[:-1]
            dclean = re.compile('<.*?>')
            delta=re.sub(dclean, '', delta)
            delta = delta.lower()
            delta = re.sub(r'[^\w\s]','',delta)
            ps_delta = ps.stem(delta)
            g.append(ps_delta)
        glistdata.append(g)
docs_no=len(listdata)
w=int(input("What should be the window size?"))             # This takes the desired inputs for further processing
iteration=int(input("How many number of Iterations do you want to execute?"))
inter=dict()
word_graph= dict()
k=1
m=0

for each in listdata:       #This is an outer look that takes each document into account one by one
    t=[]
    un_stem=[]
    for every in each:
        if(every!="_"):         #forms a list of tuples
            temp=every.split('_')
            un_stem.append(temp[0])
            temp[0] = ps.stem(temp[0])
            t.append(temp)

    vocab=[]
    c=0
    for k in t:
        if(k[1]== "nn" or k[1]== "nns" or k[1] == "nnp" or k[1] == "nnps" or k[1] =="jj"):  #This helps in considering only the desired POS tags
            if k[0] not in vocab:
                c+=1
                vocab.append(k[0])

    graph=np.zeros((c,c))   # this will store the graph
      
    i=0
    for i in range(0,len(t)-w+1):   #this forms an adjacency matrix
        if(t[i][1]== "nn" or t[i][1]== "nns" or t[i][1] == "nnp" or t[i][1] == "nnps" or t[i][1] =="jj"):
            for j in range(1,w):
                if(t[i+j][1]== "nn" or t[i+j][1]== "nns" or t[i+j][1] == "nnp" or t[i+j][1] == "nnps" or t[i+j][1] =="jj"):
                    graph[vocab.index(t[i][0])][vocab.index(t[i+j][0])]+=1
                    graph[vocab.index(t[i+j][0])][vocab.index(t[i][0])]+=1

    graph1=np.zeros((c,c)) #This will be the normalized graph
    
    for i in range(c):
        s=0
        for j in range(c):
            s+=graph[i][j]
        for j in range(c):
            if(s!=0):
                graph1[i][j]=graph[i][j]/s
            else:
                graph1[i][j]=0
    
    s0=np.zeros(c)      #this will be used for calculating the page rank scores
    for i in range(c):
        s0[i]=(1/c)

    for i in range(iteration):  #This runs the Page rank Algorithm
        st=0.85*(np.dot(s0,graph1)) + (0.15)*1/c
        s0=st


