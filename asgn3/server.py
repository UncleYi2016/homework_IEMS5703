import json
import csv
from flask import Flask
from flask import request

DATABASE_PATH = 'imdb_top1000.csv'
MOVIES = []
app = Flask(__name__)


def load_database():
    file = open(DATABASE_PATH, 'r', encoding='utf-8')
    s = csv.reader(file)
    first_row = True
    keys = []
    for row in s:
        if first_row:
            for key in row:
                keys.append(key)
            first_row = False
        else:
            movie = {}
            length = len(row)
            for i in range(length):
                if keys[i] == 'Rank':
                    movie['id'] = int(row[i]) - 1
                    movie[keys[i]] = int(row[i])
                elif row[i] != '' and (keys[i] == 'Metascore' or keys[i] == 'Rating' or keys[i] == 'Revenue (Millions)'):
                    movie[keys[i]] = float(row[i])
                elif row[i] != '' and (keys[i] == 'Year' or keys[i] == 'Votes' or keys[i] == 'Runtime (Minutes)'):
                    movie[keys[i]] = int(row[i])
                else:
                    movie[keys[i]] = row[i]
            movie['comments'] = []
            MOVIES.append(movie)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    attribute = request.args.get('attribute', '')
    sortby = request.args.get('sortby', '')
    order = request.args.get('order', '')
    return 'query: %s<br>attribute: %s<br>sortby: %s<br>order: %s' % (query, attribute, sortby, order)

@app.route('/movie/<int:id>')
def movie(id=0):
    json_str = json.dumps(MOVIES[id])
    return json_str
if __name__ == '__main__':
    load_database()
    json_str = json.dumps(MOVIES[7])
    print(json_str)