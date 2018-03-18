import json
import csv
DATABASE_PATH = 'imdb_top1000.csv'
MOVIES = []

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
                elif keys[i] == 'Metascore' or keys[i] == 'Rating'
                     or keys[i] == 'Revenue (Millions)':
                    movie[keys[i]] = float(row[i])
                elif keys[i] == 'Year' or keys[i] == 'Votes' or
                     keys[i] == 'Runtime (Minutes)':
                     movie[keys[i]] = int(row[i])
            movie['comments'] = []
            MOVIES.append(movie)

if __name__ == '__main__':
    load_database()
    json_str = json.dumps(MOVIES[2])
    print(json_str)