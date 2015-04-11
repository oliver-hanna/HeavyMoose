import urllib2
import json
import config
from random import randint

def thes_search(query):
    api_key = config.locu_thes_api
    url = 'http://words.bighugelabs.com/api/2/' + api_key +'/'
    syn_list = []
    final_url = url+ query + '/json'
    try:
        json_obj = urllib2.urlopen(final_url)
    except urllib2.HTTPError:
        return query
    data = json.load(json_obj)
    ##ADDS ALL SYNONYMS IN REL, SIM, AND SYN TO SYN_LIST LIST
    if data.get('adjective'):
        for word_type in data['adjective']:
            if word_type == 'syn':
                for item in data['adjective']['syn']:
                    syn_list.append(item)
            if word_type == 'rel':
                for item in data['adjective']['rel']:
                    syn_list.append(item)
            if word_type == 'sim':
                for item in data['adjective']['sim']:
                    syn_list.append(item)
    #PASSES SYN_LIST INTO IN_QUERY WHICH CHOOSES SYNONYM
    else:
        return query
    final_word = in_query(syn_list)
    syn_list = []
    ##PRINTS FINAL WORD RETURNED FROM IN_QUERY
    return final_word

def in_query(syn_list):
    """
    Chooses random word and returns
    """
    length = len(syn_list)
    rand = randint(0, length-1)
    return syn_list[rand]
