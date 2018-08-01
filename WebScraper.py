# -*- coding: utf-8 -*-
"""
@author: Abhishek Chattopadhyay
"""

import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup

pages=int(sys.argv[1])
print('You have chosen to scrape {} pages\n'.format(pages))

url='https://www.imdb.com/search/title?sort=num_votes,desc&start=1&title_type=feature&year=1950,2012&page={}&ref_=adv_nxt'
movielist=[]
for curr_page in range(1,pages+1):
    response = requests.get(url.format(curr_page))
    print("Scraping Page {}".format(curr_page))
    bs = BeautifulSoup(response.text,'html.parser')
    for movie in bs.findAll('div','lister-item-content'):
        movie_det={}
        movie_det['rank']=movie.find('span','lister-item-index unbold text-primary').text.strip()
        movie_det['name']=movie.find('a',href=True).text.strip()
        movie_det['year']=movie.find('span','lister-item-year text-muted unbold').text.strip().strip('()')
        movie_det['runtime']=movie.find('span','runtime').text.strip()
        movie_det['genre']=movie.find('span','genre').text.strip()
        movie_det['imdb_rating']=movie.find('div','inline-block ratings-imdb-rating')['data-value']
        movie_det['description']=movie.find_all('p','text-muted')[1].text.strip()
        movie_det['total_votes']=movie.find_all('span',{'name':'nv'})[0]['data-value']
        movie_cast=movie.find_all('p','')[2].text.strip('\n')
        director_list=movie_cast.split('|')[0].split(':')[1:]
        actor_list=movie_cast.split('|')[1].split(':')[1:]
        movie_det['director']=''.join(director_list).replace('\n','')
        movie_det['actor']=''.join(actor_list).replace('\n','')
        movielist.append(movie_det)

df = pd.DataFrame(movielist) 
file_name='IMDB Top Rated Movies.csv'
df.to_csv(file_name,index=False) 
print("Finished processing. Please check for {} in present working directory".format(file_name))
