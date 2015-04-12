from flask import Flask, render_template, request
from converter import thes_search, in_query

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def convert():
    if request.method == 'POST':
        origin = request.form['origin']
        final_string = ""
        words_list = origin.split()
        for word in words_list:
            final_string += thes_search(word) + " "
        return render_template('index.html', origin=origin, result=final_string)
    else:
        return render_template('index.html')
