from flask import Flask, render_template, request
from converter import thes_search, in_query

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def convert():
    if request.method == 'POST':
        origin = request.form['origin']
        final_string = ""
        capnext = false
        words_list = origin.split()
        for word in words_list:
            thesWord = thes_search(word)
            if capnext == true:
                finalstring += thesWord.title() + " "
                capnext = false
            else:
                final_string += thesWord + " "
            cl = len(thesWord)-1
            if
            (
                    thesWord[cl] == '!' or thesWord[cl] == '.' or
                    thesWord[cl] == '?'
            ):
                capnext = true
        return render_template('index.html', origin=origin, result=final_string)
    else:
        return render_template('index.html')
