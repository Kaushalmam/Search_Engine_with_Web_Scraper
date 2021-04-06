# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:57:39 2020

@author: kaush
"""
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import operator                    #Importing the required libraries
import glob
#import re
import math
import json
with open('link_info.txt') as f:
    jsondata=json.load(f)
f.close()
#print(data['4.txt'])
def preprocess(data):                    #This function performs the preprocessing and tokenize the data
    clean = re.compile('<.*?>')         # Remove the tags
    new= re.sub(clean, '', data)
    new = new.lower()                   # Convert the data to lower case
    new = re.sub(r'[^\w\s]','',new)     # Remove the punctuations
    new = re.sub(r'[0-9]','',new)       # Remove all Digits
    new = new.split()                   # Remove white spaces
    stopWords = set(stopwords.words('english')) # Remove stop words.
    filtered = []
    for w in new:
        if w not in stopWords:
            filtered.append(w)
    #print(filtered)
    tokens = []                         # Remove all the words of length less than 3.
    for w in filtered:
        if len(w)>2:
            tokens.append(w)   
    #print(tokens)
    
    ps = PorterStemmer()                # Stem the Data.
    ps_data=[ps.stem(x) for x in tokens]
    #print(ps_data)
    stopWords = set(stopwords.words('english')) #Again look for stop wordsand remove them.
    new_filtered = []
    for w in ps_data:
        if w not in stopWords:
            new_filtered.append(w)
    return(new_filtered)                #Return the preprocessed data.

 
    



address= 'D:\\UIC\\Information Retrieval by Cornelia Caragea Spring 2020\\final project\\data' #Change file location here
folder = glob.glob(address + "/*")
data=dict()
temp=dict()
counter=0
for file_list in folder:
    try:
        file_open=open(file_list,'r',encoding="utf8")
        file_read=file_open.read()
        #print(file_list)
        k=preprocess(file_read)
        #x=file_list[-13:]
        data.update({file_list.split('\\')[-1]: k})
        counter+=1
    except Exception:
        continue

index=dict()                        #Following is used to calculate TF value for rach word in each document.
for key,value in data.items():
    for each in value:
        if each not in index:
            index.update({each:{key : 1}})
        else:
            if key not in index[each]:
                index[each].update({key : 1})
            else:
                index[each][key]=index[each][key]+1


idf=dict()                          #Here we calculate the IDF for rach document.
for key,value in index.items():
    id=math.log(1400/(len(value)+1),10)
    idf.update({key: id})
    
tfidf=dict()                        #Here we calculate the TFIDF for each word in each document.
for key,value in index.items():
    for key1,value1 in value.items():
            if key1 not in tfidf:
                tfidf.update({key1:{key:idf[key]*value1}})
            else:
                tfidf[key1].update({key:idf[key]*value1})
                
doc_len=dict()                      #This will calculate the leach of each document that helps in finding the cosine similarity.
for key, value in tfidf.items():
    s=0
    for key1, value1 in value.items():
        s= s + pow(value1,2)
    doc_len.update({key: s})
f=open("data_use01.txt","w+")
json.dump(data,f)
f.close()
f=open("tfidf_use01.txt","w+")
json.dump(tfidf,f)
f.close()
f=open("doc_len_use01.txt","w+")
json.dump(doc_len,f)
f.close()
