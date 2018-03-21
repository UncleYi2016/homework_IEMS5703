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