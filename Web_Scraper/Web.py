import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import scrapy
from queue import Queue 
import os
import json

q=Queue()
q.put('https://www.cs.uic.edu/')
os.mkdir(r'D:\UIC\Information Retrieval by Cornelia Caragea Spring 2020\final project\Scraped_data_corpus') #Change file location here
count = 1
flag=0
visited=[]
linkdic=dict()
invalid_extensions = ["pdf", "jpg", "jpeg", "doc", "docx", "ppt", "pptx", "png", "txt", "exe", "ps", "psb",'aspx']
def is_valid_extension(url):
    if True in [ext in url for ext in invalid_extensions]:
        return False
    return True


name_count=1
while (q.empty()==False and flag==0):
    url = q.get()
    if(url not in visited):
        print(url)
    
        headers = {'user-agent': 'Chrome/55.0.2883.87'}
        try:
            response = requests.get(url,headers, verify=False,timeout=(3, 60))
        except requests.RequestException:
            continue
        if(response.status_code!=200):
            continue
        if(response.status_code==200):
            soup = BeautifulSoup(response.text, "html.parser")
            visited.append(url)
            linkdic.update({str(name_count)+'.txt':url})
            try:
                urllib.request.urlretrieve(url, "data\\"+str(name_count)+".txt",None,None)
            except Exception as e:
                continue
            name_count+=1
            for each in soup.findAll('a'):  #'a' tags are for links
                link=each.get('href')
                if(link!=None):
                    if('http'not in link):
                        link='https://www.uic.edu/'+link
                    if(link not in visited):
                        if (is_valid_extension(link)):
                            q.put(link)
        print(len(visited))
        if(len(visited)==4000):
            break
    else:
        continue

with open("link_info01.txt",'w+') as f:
    json.dump(linkdic,f)
f.close()
