# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re

BASE_URL = 'https://www.skisport.ru/'
FORUM = 'forum/22/'

def get_list_of_posts(url):
    text = requests.get(BASE_URL + FORUM).text
    soup = BeautifulSoup(text, features='html.parser')
    posts_tr = [tr for tr in soup.findChildren('tr') if len(tr) == 11]
    posts = [{'post_text': tr.find('td').find('a').string, 'local_url': tr.find('td').find('a').get('href'), 'date': tr.find('td', {'class': 'tc', 'width': "100px"}).string}  for tr in posts_tr[1:]]
    return posts

def filter_out(posts, template):
    filtered_posts = [p for p in posts if re.findall(template, p['post_text']) != []]
    return filtered_posts

def main():
    posts = get_list_of_posts(BASE_URL + FORUM)
    posts = filter_out(posts, 'палки')
    for p in posts:
        print(p)

if __name__ == '__main__':
    main()
