from flask import Flask, render_template, request
app = Flask(__name__)

import urllib2
import json
from random import randint
import time

locu_thes_api='7da0dc34a9953de034e1828c6215cc09'


def thes_search(query):
	api_key=locu_thes_api
	url='http://words.bighugelabs.com/api/2/7da0dc34a9953de034e1828c6215cc09/'
	word=query
	syn_list=[]
	final_url= url+ query + '/json'
        try:
	    json_obj=urllib2.urlopen(final_url)
        except:
            return query
	data= json.load(json_obj)
	##ADDS ALL SYNONYMS IN REL, SIM, AND SYN TO SYN_LIST LIST
	if data.get('adjective'):
	    for type in data['adjective']:
	        if type=='syn':
		    for item in data['adjective']['syn']:
			syn_list.append(item)
		if type=='rel':
		    for item in data['adjective']['rel']:
			syn_list.append(item)
		if type=='sim':
		    for item in data['adjective']['sim']:
			syn_list.append(item)
        #PASSES SYN_LIST INTO IN_QUERY WHICH CHOOSES SYNONYM
        else:
            return query
	final_word=in_query(syn_list)
	syn_list=[]
	##PRINTS FINAL WORD RETURNED FROM IN_QUERY
	return final_word
	
def in_query(syn_list):
	##CHOOSES RANDOM WORD AND RETURNS
        if syn_list:
            length=len(syn_list)
            rand=randint(0,length-1)
            return syn_list[rand]
        else:
            return ''

@app.route('/', methods=['POST', 'GET'])
def convert():
    if request.method == 'POST':
        origin = request.form['origin']
        finalString = ""
        L = origin.split() 
        for word in L:
            finalString += thes_search(word) + " "
            time.sleep(1)

        return render_template('index.html', origin=origin, result=finalString)
    else:
        return render_template('index.html')
