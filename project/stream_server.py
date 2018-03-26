from flask import Response
from flask import Flask
app = Flask(__name__)

@app.route('/large.csv')
def generate_large_csv():
    def generate():
        count = 0
        while True:
            count += 1
            yield str(count) + '\n'
    return Response(generate(), mimetype='text/csv')