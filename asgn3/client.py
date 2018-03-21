import json
import sys
import urllib
import urllib.request
import urllib.parse


if __name__ == '__main__':
    addr = sys.argv[1]
    port = int(sys.argv[2])
    function = sys.argv[3]

    if function == 'search':
        query = sys.argv[4]
        attribute = sys.argv[5]
        sortby = sys.argv[6]
        order = sys.argv[7]
        params = urllib.parse.urlencode({'query': query, 'attribute': attribute, 'sortby': sortby, 'order': order})
        url = 'http://' + addr + ':' + str(port) + '/search?%s' % params
        with urllib.request.urlopen(url) as f:
            json_str = f.read().decode('utf-8')
        fomatted_json = json.dumps(json_str, indent=4)
        print(fomatted_json)
    elif function == 'movie':
        movie_id = sys.argv[4]
        url = 'http://' + addr + ':' + str(port) + '/movie/' + movie_id
        with urllib.request.urlopen(url) as f:
            json_str = f.read().decode('utf-8')
        fomatted_json = json.dumps(json_str, indent=4)
        print(fomatted_json)
    elif cuntion == 'comment':
        user_name = sys.argv[4]
        movie_id = sys.argv[5]
        print('What is your comment? <User inputs his/her comment here and press enter>')
        comment = raw_input()
        params = urllib.parse.urlencode({'user_name': user_name, 'movie_id': movie_id, 'comment': comment})
        url = 'http://' + addr + ':' + str(port) + '/comment'
        with urllib.request.urlopen(url, params) as f:
            json_str = f.read().decode('utf-8')
        fomatted_json = json.dumps(json_str, indent=4)
        print(fomatted_json)