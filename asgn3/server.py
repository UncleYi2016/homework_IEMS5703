import csv
import nltk
import copy
import time
import sys
from flask import Flask
from flask import request
from flask import json

DATABASE_PATH = 'imdb_top1000.csv'
NO_RESULT_STR = 'There is no result'
MOVIES = []
TITLE_INDEX = {}
ACTORS_INDEX = {}
ATTRIBUTE_TYPE = ['both', 'title', 'actor']
SORT_TYPE = ['year', 'revenue', 'rating']
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
                elif row[i] == '':
                    movie[keys[i]] = 0
                elif keys[i] == 'Metascore' or keys[i] == 'Rating' or keys[i] == 'Revenue (Millions)':
                        movie[keys[i]] = float(row[i])
                elif keys[i] == 'Year' or keys[i] == 'Votes' or keys[i] == 'Runtime (Minutes)':
                    movie[keys[i]] = int(row[i])
                elif keys[i] == 'Title':
                    title = row[i]
                    movie[keys[i]] = row[i]
                    title_keywords = nltk.word_tokenize(title)
                    for keyword in title_keywords:
                        if keyword == ',' or keyword == '\'':
                            continue
                        if not keyword.lower() in TITLE_INDEX:
                            TITLE_INDEX[keyword.lower()] = []
                        TITLE_INDEX[keyword.lower()].append(id)
                elif keys[i] == 'Actors':
                    actors = row[i]
                    movie[keys[i]] = row[i]
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
    search_actor = False
    search_title = False
    sortby = 'Year'
    sort_reversed = False
    movie_query = []
    id_query = []

    query = request.args.get('query', '')
    attribute = request.args.get('attribute', '')
    sortby = request.args.get('sortby', '')
    order = request.args.get('order', '')

    query = query.lower()
    attribute = attribute.lower()
    sortby = sortby.lower()
    order = order.lower()

    if attribute == ATTRIBUTE_TYPE[0]:      # type: both
        search_actor = True
        search_title = True
    elif attribute == ATTRIBUTE_TYPE[1]:    # type: title
        search_title = True
    elif attribute == ATTRIBUTE_TYPE[2]:    # type: actor
        search_actor = True
    
    if sortby == SORT_TYPE[0]:
        sortby = 'Year'
    elif sortby == SORT_TYPE[1]:
        sortby = 'Revenue (Millions)'
    elif sortby == SORT_TYPE[2]:
        sortby = 'Rating'
    else:
        sortby = 'Year'

    if order == 'descending':
        sort_reversed = True
    
    if search_actor:
        if query in ACTORS_INDEX:
            for id in ACTORS_INDEX[query]:
                if id not in id_query:
                    id_query.append(id)
    if search_title:
        if query in TITLE_INDEX:
            for id in TITLE_INDEX[query]:
                if id not in id_query:
                    id_query.append(id)
    if len(id_query) == 0:
        return NO_RESULT_STR
    for id in id_query:
        movie_element = copy.copy(MOVIES[id])
        movie_element.pop('Description')
        movie_element.pop('Metascore')
        movie_element.pop('Rank')
        movie_element.pop('Runtime (Minutes)')
        movie_element.pop('Votes')
        movie_element.pop('comments')
        movie_query.append(movie_element)
    movie_query.sort(key=lambda a:a[sortby], reverse = sort_reversed)
    movie_query_result = movie_query[0:10]
    return json.dumps(movie_query_result)

@app.route('/movie/<int:id>')
def movie(id=0):
    if MOVIES == []:
        load_database()
    if id >= len(MOVIES):
        return NO_RESULT_STR
    json_str = json.dumps(MOVIES[id])
    return json_str

@app.route('/comment', methods=['POST'])
def comment():
    if MOVIES == []:
        load_database()
 
    
    movie_id = int(request.form['movie_id'])
    user_name = request.form['user_name']
    comment = request.form['comment']
    timestamp = time.strftime('%Y-%M-%d %H:%M:%S')

    if movie_id >= len(MOVIES):
        return NO_RESULT_STR
    
    comment_dict = {}
    comment_dict['comment'] = comment
    comment_dict['timestamp'] = timestamp
    comment_dict['user_name'] = user_name

    MOVIES[movie_id]['comments'].append(comment_dict)

    return movie(movie_id)

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port, debug=True)
