
# coding: utf-8

# In[60]:

from urllib.request import urlopen
from lxml import html
import numpy as np
import json, csv
import pandas as pd
import re
from decimal import Decimal, ROUND_DOWN


# In[3]:

url='https://www.youtube.com/feed/trending'


# In[4]:

response=urlopen(url)
page=response.read()
tree=html.document_fromstring(page)


# In[5]:

#Getting URLs
base_url='http://www.youtube.com'
a_tags_1=tree.xpath('//a[@class="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link "]')
a_tags_2=tree.xpath('//a[@class=" yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link "]')
urls=[]
for i in a_tags_1:
    urls.append(i.get("href"))
urls = [base_url + i for i in urls]
urls_6=[]
for i in a_tags_2:
    urls_6.append(i.get("href"))
urls_6 = [base_url + i for i in urls_6]
urls_first_4=urls[:4]
urls_last_68=urls[-68:]
urls_last_68
urls_all=urls_first_4+urls_6+urls_last_68
len(urls_all)


# In[6]:

#Getting titles
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


# In[7]:

#Getting durations
span_tags=tree.xpath('//span[@class="video-time"]')
durations=[]
for i in span_tags:
    durations.append(i.text)
len(durations)


# In[8]:

#Getting usernames
a_tags_1=tree.xpath('//a[@class="g-hovercard yt-uix-sessionlink       spf-link "]')
usernames=[]
for i in a_tags_1:
    usernames.append(i.text)
len(usernames)


# In[10]:

#Getting views
views=[]
ul_tags=tree.xpath('//ul[@class="yt-lockup-meta-info"]//li')
for i in ul_tags:
    views.append(i.text)
views=[i for i in views if "views" in i]


# In[11]:

#Creating data list
data_list=[]
for i in range(0, len(views)):
    video={'1 Video Title':titles[i],
           '2 Duration': durations[i],
           '3 Views': views[i],
           '4 Username': usernames[i],
           '5 URL':urls_all[i]}
    data_list.append(video)


# In[12]:

with open('Trending(XML).json', 'w') as file:
    json.dump(data_list, file, sort_keys=True, indent=4)


# In[68]:

data_frame=pd.DataFrame(data_list)
data_frame.to_csv('Trending(XML).csv', index= False)


# In[69]:

#Calculating average number of views
data_frame['3 Views'] = data_frame['3 Views'].str.split(' ', 1).str[0]
for i in range (0, len(data_frame['3 Views'])):
    data_frame['3 Views'][i]=re.sub(',',"", str(data_frame['3 Views'][i]))
data_frame['3 Views']=data_frame['3 Views'].astype(np.int64)
int(data_frame["3 Views"].mean())


# In[ ]:



