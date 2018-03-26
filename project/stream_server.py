from flask import Response
from flask import Flask
import time
app = Flask(__name__)

@app.route('/test')
def generate_large_csv():
    def generate():
        count = 0
        while True:
            count += 1
            yield str(count) + '\n'
            time.sleep(1)
    return Response(generate())