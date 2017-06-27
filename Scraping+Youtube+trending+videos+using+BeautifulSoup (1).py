
# coding: utf-8

# In[1]:

import requests, re, json
from bs4 import BeautifulSoup
import json, csv
import pandas as pd
import numpy as np
from numpy import s_


# In[2]:

url='https://www.youtube.com/feed/trending'
content=requests.get(url)
page=content.text
soup=BeautifulSoup(page,'lxml')


# In[13]:

#Getting URLs
base_url='http://www.youtube.com'
a_tags_1=soup.findAll('a', attrs={'class':'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link '})
urls=[]
for i in a_tags_1:
    urls.append(i.get("href"))
urls = [base_url + i for i in urls]
a_tags_2=soup.findAll('a', attrs={'class':' yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link '})
a_tags_2
urls_6=[]
for i in a_tags_2:
    urls_6.append(i.get("href"))
urls_6=[base_url+i for i in urls_6]
urls_first_4=urls[:4]
urls_last_68=urls[-68:]
urls_all=urls_first_4+urls_6+urls_last_68
len(urls_all)


# In[5]:

# Getting titles
titles_1=[]
for i in a_tags_1:
     titles_1.append(i.text)
titles_2=[]
for i in a_tags_2:
    titles_2.append(i.text)
titles_first_4=titles_1[:4]
titles_last_68=titles_1[-68:]
titles=titles_first_4+titles_2+titles_last_68
len(titles)


# In[6]:

#Getting durations
span_tags=soup.findAll('span', attrs={'class':'video-time'})
durations=[]
for i in span_tags:
    durations.append(i.text)
len(durations)


# In[9]:

#Getting Usernames
a_tags_1=soup.findAll('a', attrs={'class':'g-hovercard yt-uix-sessionlink spf-link '})
usernames=[]
for i in a_tags_1:
    usernames.append(i.text)
len(usernames)


# In[7]:

#Getting views
views=[]
views_all=[]
ul_tags=soup.findAll('ul', attrs={'class':'yt-lockup-meta-info'})
for i in ul_tags:
    views.append(i)
views_6=views[4:10]
views_first_4=views[:4]
views_last=views[10:]
for i in views:
    del i
for i in views_first_4:
     views_all.append(i.findChildren()[1].text)
for i in views_6:
     views_all.append(i.findChildren()[0].text)
for i in views_last:
     views_all.append(i.findChildren()[1].text)
len(views_all)


# In[10]:

#Appending data into a list
data_list=[]
for i in range(0, len(views)):
    video={'1 Video Title': titles[i],
           '2 Duration': durations[i],
           '3 Views': views_all[i],
           '4 Username':usernames[i],
           '5 URL':urls_all[i]}
    data_list.append(video)


# In[11]:

#Creating a json file
with open('Trending.json', 'w') as file:
    json.dump(data_list, file, sort_keys=True, indent=4)


# In[12]:

#Creating a csv file
data_frame=pd.DataFrame(data_list)
data_frame.to_csv('Trending.csv', index= False)


# In[14]:

#Calculating average number of views
data_frame['3 Views'] = data_frame['3 Views'].str.split(' ', 1).str[0]
for i in range (0, len(data_frame['3 Views'])):
    data_frame['3 Views'][i]=re.sub(',',"", str(data_frame['3 Views'][i]))
data_frame['3 Views']=data_frame['3 Views'].astype(np.int64)
int(data_frame["3 Views"].mean())


# In[ ]:



