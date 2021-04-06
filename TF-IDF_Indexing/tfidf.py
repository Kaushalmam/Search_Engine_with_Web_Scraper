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
    tokens = []                         # Remove all the words of length less than 3.
    for w in filtered:
        if len(w)>2:
            tokens.append(w)   
    
    ps = PorterStemmer()                # Stem the Data.
    ps_data=[ps.stem(x) for x in tokens]
    stopWords = set(stopwords.words('english')) #Again look for stop wordsand remove them.
    new_filtered = []
    for w in ps_data:
        if w not in stopWords:
            new_filtered.append(w)
    return(new_filtered)                #Return the preprocessed data.

 
f=open("tfidf_use.txt","r")
tfidf=json.load(f)
f.close()
f=open("data_use.txt","r")
data=json.load(f)
f.close()
f=open("doc_len_use.txt","r")
doc_len=json.load(f)
f.close()



    
def get_search_result(query, TOP =10):
    count=1
    query_data = dict()
    temp = preprocess(query)
    query_data.update({count:temp})
    
    qindex=dict()                       # This is used to calculate tf for each word in a document
    for key,value in query_data.items():
        for each in value:
            if each not in qindex:
                qindex.update({each:{key : 1}})
            else:
                if key not in qindex[each]:
                    qindex[each].update({key : 1})
                else:
                    qindex[each][key]=qindex[each][key]+1
                    
    qidf=dict()                         # This is used to calculate the IDF for each word in queries w.r.t. documents.
    for key,value in qindex.items():
        id=math.log(10/(len(value)+1),10)
        qidf.update({key: id})
        
    q_tfidf=dict()                      #Following is used to calculate the TFIDF value for rach word in each document(TF*IDF).
    for key,value in qindex.items():
        for key1,value1 in value.items():
                if key1 not in q_tfidf:
                    q_tfidf.update({key1:{key:qidf[key]*value1}})
                else:
                    q_tfidf[key1].update({key:qidf[key]*value1})
    qdoc_len=dict()                     #Following is used to calculate the document length for each query.
    for key, value in q_tfidf.items():
        s=0
        for key1, value1 in value.items():
            s= s + pow(value1,2)
        qdoc_len.update({key: s})
    
    relevant = dict()                   #Here we find out all the relevant documents to the specified queries.
    for key1,value1 in query_data.items():
        inter=dict()
        for key,value in data.items():
            common=[]
            for each in value1:
                if each in value:
                    common.append(each)
            inter.update({key:common})
        relevant.update({key1 : inter})
                             #Cosine similarity is calculated for each query w.r.t. each document.
    num=dict()
    for key, value in relevant.items():
        for key1, value1 in value.items():
            if key1!="233.txt":
                xf=0.0
                den=0.0
                for each in value1:
                    a=q_tfidf[key][each]
                    b=tfidf[key1][each]
                    xf=xf+(a*b)
                den=math.sqrt(doc_len[key1]*qdoc_len[key])
                final_cosine=xf/den
                if key not in num:
                    num.update({key : {key1 : final_cosine}})
                else:
                    num[key].update({key1: final_cosine})
            else:
                continue
    
    sorted_val=dict()                   #Used to sort the documents in the descending order of their cosine similarity.
    for key, value in num.items():
        sorted_x = sorted(value.items(), key=operator.itemgetter(1), reverse=True)
        sorted_val.update({key: sorted_x})
    
    output_list=[]
    for key, value in sorted_val.items():
        for i in range(0,len(value)):
            output_list.append(value[i][0])
    output_list
    
    inter=[]
    for each in output_list:
        inter.append(jsondata[each])
    return inter
