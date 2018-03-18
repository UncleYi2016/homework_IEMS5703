import json

DATABASE_PATH = 'imdb_top1000.csv'
MOVIES = []

def load_database():
    file = open(DATABASE_PATH, 'r', encoding='utf-8')
    dic_key = file.readline()
    dic_key = dic_key.strip().split(',')  # The dictionary keys
    keys = []                           # Store key list into array
    for key in dic_key:
        keys.append(key)
    for line in file:
        line = line.strip()
        movie_element = line.split(',')
        movie = {}
        length = len(movie_element)
        for i in length:
            movie[keys[i]] = movie_element[i]
    movie['comment'] = []

if __name__ == '__main__':
    load_database()
    json_str = json.dumps(MOVIES[0])
    print(json_str)