import csv
import nltk
from flask import Flask
from flask import request
from flask import json

DATABASE_PATH = 'imdb_top1000.csv'
MOVIES = []
TITLE_INDEX = {}
ACTORS_INDEX = {}
QUERY_TYPE = ['both', '']
app = Flask(__name__)


def load_database():
    file = open(DATABASE_PATH, 'r', encoding='utf-8')
    s = csv.reader(file)
    first_row = True
    keys = []
    for row in s:
        id = 0
        if first_row:
            for key in row:
                keys.append(key)
            first_row = False
        else:
            movie = {}
            length = len(row)
            for i in range(length):
                if keys[i] == 'Rank':
                    id = int(row[i]) - 1
                    movie['id'] = id
                    movie[keys[i]] = int(row[i])
                elif row[i] != '' and (keys[i] == 'Metascore' or keys[i] == 'Rating' or keys[i] == 'Revenue (Millions)'):
                    movie[keys[i]] = float(row[i])
                elif row[i] != '' and (keys[i] == 'Year' or keys[i] == 'Votes' or keys[i] == 'Runtime (Minutes)'):
                    movie[keys[i]] = int(row[i])
                elif keys[i] == 'Title':
                    title = row[i]
                    title_keywords = nltk.word_tokenize(title)
                    for keyword in title_keywords:
                        if keyword == ',' or keyword == '\'':
                            continue
                        if not keyword.lower() in TITLE_INDEX:
                            TITLE_INDEX[keyword.lower()] = []
                        TITLE_INDEX[keyword.lower()].append(id)
                elif keys[i] == 'Actors':
                    actors = row[i]
                    actors_keywords = nltk.word_tokenize(actors)
                    for keyword in actors_keywords:
                        if keyword == ',' or keyword == '\'':
                            continue
                        if not keyword.lower() in ACTORS_INDEX:
                            ACTORS_INDEX[keyword.lower()] = []
                        ACTORS_INDEX[keyword.lower()].append(id)
                else:
                    movie[keys[i]] = row[i]
            movie['comments'] = []
            MOVIES.append(movie)

@app.route('/search')
def search():
    if MOVIES == []:
        load_database()
    query = request.args.get('query', '')
    attribute = request.args.get('attribute', '')
    sortby = request.args.get('sortby', '')
    order = request.args.get('order', '')

    return json.dumps(ACTORS_INDEX)
    

@app.route('/movie/<int:id>')
def movie(id=0):
    if MOVIES == []:
        load_database()
    json_str = json.dumps(MOVIES[id])
    return json_str