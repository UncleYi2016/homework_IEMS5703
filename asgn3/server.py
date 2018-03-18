import json
import csv
DATABASE_PATH = 'imdb_top1000.csv'
MOVIES = []

def load_database():
    file = open(DATABASE_PATH, 'r', encoding='utf-8')
    s = csv.reader(file)
    print(s)
    for row in s:
        print(row)
        break
    # dic_key = file.readline()
    # dic_key = dic_key.strip().split(',')  # The dictionary keys
    # keys = []                           # Store key list into array
    # for key in dic_key:
    #     keys.append(key)
    # print(len(keys))
    # for line in file:
    #     movie_element = line.split(',')
    #     for element in movie_element:
    #         if element.
    #     movie = {}
    #     length = len(movie_element)
    #     print(length)
    #     print(json.dumps(movie_element))
    #     for i in range(length):
    #         print(i)
    #         movie[keys[i]] = movie_element[i]
    # movie['comment'] = []

if __name__ == '__main__':
    load_database()
    json_str = json.dumps(MOVIES[0])
    print(json_str)