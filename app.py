from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def convert():
    if request.method == 'POST':
        origin = request.form['origin']
        return render_template('index.html', origin=origin, result=origin)
    else:
        return render_template('index.html')
