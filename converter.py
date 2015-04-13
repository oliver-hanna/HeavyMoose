import urllib2
import json
from random import randint

locu_thes_api='7da0dc34a9953de034e1828c6215cc09'
locu_dic_api='a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'

fwordlist = []
f = open('flaggedwords.txt','r')
for line in f:
    fwordlist.append(line[:-1])
f.close()

#gets definition of word and returns 2d array with key words in definition
def get_def(query):
    word=query
        #type=pos
    url1='http://api.wordnik.com:80/v4/word.json/'
    url2='/definitions?limit=200&partOfSpeech=adjective'
    url3='&inludeRelated=true&useCanonical=false&includeTags=false&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'
    definition=[]
    item_split=[]
    final_list=[]
    final_url= url1 + word + url2 + url3
    try:
        json_obj=urllib2.urlopen(final_url)
    except urllib2.HTTPError:
        definition.append(query)
        return definition

    data= json.load(json_obj)

    for item in data:
        item_split=item['text'].split()
        for wordz in item_split:
            definition.append(wordz)

    ##definition is now 2d array [definiton #][word in definition]
    final_list=clean_str(definition)

    #print final_list
    #for item in final_list:
    #	print item
    return final_list


def clean_str(strlist):
    clean_list=[]
    word_list=fwordlist
    flaglist = [',',':',';','.']
    for defi in strlist:
        for flag in flaglist:
            if defi[len(defi)-1] == flag:
                defi = defi[:-1]
            if(word_list.count(defi) != 1):
                clean_list.append(defi)

    return clean_list

#Compares the definitions of two words and returns an int based on how many times their definitions shared words
def compare_def(word1,word2):
    like=0
    list1=get_def(word1)
    list2=get_def(word2)

    list1 = list(set(list1))
    list2 = list(set(list2))

    for items in list1:
        for element in list2:
            if items==element:
                like+=1
            if word1 == element:
                like+=2
            if word2 == items:
                like+=2
    return like




def thes_search(query):
    original = query
    punct = False
    if(query[len(query)-1] == '!' or query[len(query)-1] == '.' or
       query[len(query)-1] == '?'):
        query=query[:-1]
        punct = True
    capBool = query[0].isupper()
    query = query.lower()

    if fwordlist.count(query) == 1:
        return original

    api_key=locu_thes_api
    url='http://words.bighugelabs.com/api/2/7da0dc34a9953de034e1828c6215cc09/'
    word=query

    syn_list=[]
    final_url= url+ query + '/json'
    try:
        json_obj=urllib2.urlopen(final_url)
    except urllib2.HTTPError:
        return original+'%'
    data= json.load(json_obj)

    ##ADDS ALL SYNONYMS IN REL, SIM, AND SYN TO SYN_LIST LIST
    if data.get('noun') or data.get('verb'):
        return original
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
    else:
        return original
    #PASSES SYN_LIST INTO IN_QUERY WHICH CHOOSES SYNONYM			
    final_word=in_query(word, syn_list)
    syn_list=[]
    ##PRINTS FINAL WORD RETURNED FROM IN_QUERY
    if(punct == True):
        final_word+=original[len(original)-1]
    if(capBool == True):
        final_word = final_word.title()
    return final_word

def in_query(query, syn_list):
    ##CHOOSES RANDOM WORD AND RETURNS
    syns=[]
    word=query
    word_count=0
    val_dic= {}
    length=len(syn_list)
    max_key=' **unchanged** '
    max_val=0

#makes a random list of appropraite size based on amount of synonyms returned by thesaurus API
    if length>=40:
        while word_count<11:
            rand=randint(0,length-1)
            if (syns.count(syn_list[rand]) == 1)==False:
                syns.append(syn_list[rand])
                word_count+=1
    elif length>=30:
        while word_count<6:
            rand=randint(0,length-1)
            if (syns.count(syn_list[rand]) == 1)==False:
                syns.append(syn_list[rand])
                word_count+=1
    elif length>=20:
        while word_count<5:
            rand=randint(0,length-1)
            if (syns.count(syn_list[rand]) == 1)==False:
                syns.append(syn_list[rand])
                word_count+=1
    elif length>=10:
        while word_count<4:
            rand=randint(0,length-1)
            if (syns.count(syn_list[rand]) == 1)==False:
                syns.append(syn_list[rand])
                word_count+=1
    elif length>=5:
        while word_count<2:
            rand=randint(0,length-1)
            if (syns.count(syn_list[rand]) == 1)==False:
                syns.append(syn_list[rand])
                word_count+=1
    else:
        while word_count<length:
            rand=randint(0,length-1)
            if (syns.count(syn_list[rand]) == 1)==False:
                syns.append(syn_list[rand])
                word_count+=1

    for item in syns:
        val_dic[item]=compare_def(word,item)

    for key in val_dic:
        if val_dic[key]>=max_val:
            max_val=val_dic[key]
            max_key=key


    return max_key
