import requests
from bs4 import BeautifulSoup
import re


def get_imdb_top(limit=250):
    url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
    source = requests.get(url=url).text

    movies = BeautifulSoup(source, 'html.parser').select('.titleColumn')
    movie_list = {}
    for movie in movies:
        movie = movie.select_one('a').text + ' ' + movie.select_one('span').text
        movie_list[movie] = ""
        limit -= 1

        if limit < 1:
            break

    return movie_list


def get_torrents(movie_list):
    url = 'https://thepiratebay.org/search/'
    counter = 0

    for key in movie_list:
        search_url = url + re.sub(r'[\':-]', '', key + " 1080p")
        print(search_url)
        source = requests.get(url=search_url).text
        first_torrent = BeautifulSoup(source, 'html.parser').select_one('.detName a')
        if first_torrent:
            movie_list[key] = get_magnet(first_torrent['href'])

        counter += 1
        print(f'{counter}. movie is completed')
        with open("movies.txt", "a") as movies.txt:
            print(f'{counter}. {key}\n{movie_list[key]}', file=movies.txt)


def get_magnet(href):
    url = 'https://thepiratebay.org/' + href
    source = requests.get(url=url).text
    magnet = BeautifulSoup(source, 'html.parser').select_one('.download a')

    if magnet:
        return magnet['href']
    else:
        return ''


with open("movies.txt", "w") as movies:
    print('IMDb Top 250 Movies\n', file=movies)

list_of_movies = get_imdb_top(250)
get_torrents(list_of_movies)
