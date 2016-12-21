import os
import re
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def open_file(name):
    f = open(name, "r", encoding = "utf-8")
    s = f.read()
    f.close()
    return s


def open_lines(name):
    f = open(name, "r", encoding = "utf-8")
    arr = f.readlines()
    f.close()
    return arr
            
def do_mystem():
    os.system("C:\\Users\\Masha\\Documents\\Programming\\Data_Base\\mystem.exe " + "-ni " + \
              "C:\\Users\\Masha\\Documents\\Programming\\Data_Base\\text.txt " +\
              "C:\\Users\\Masha\\Documents\\Programming\\Data_Base\\data.txt")
    

def writting(s, name):
    f = open(name, 'a', encoding = 'utf-8')
    f.write(s)
    f.close()

def do_dict(itog, name):
    i = 1
    d = {}
    for el in itog:
        d[i] = el
        i += 1
        writting('Insert into rawwords (form, lemma) values ("' + el[0] + '", ' + '"' + el[1] +'");\n', name)
    return d
        
    
    
def lemma(arr, name):
    itog = set()
    pattern = '.+?{(.+?)(\?)?='
    pat = '(.+?){'
    for word in arr:
        res = re.search(pattern, word)
        res1 = re.search(pat, word)
        if res != None:
            form = res1.group(1).lower()
            lemma = res.group(1)

        itog.add((form, lemma))
    d = do_dict(itog, name)
    return d
          


def do_table(d, name):
    clean = set()
    s = open_file('text.txt')
    raw = s.split()
    i = 1
    for word in raw:          
        for key in d:
            
            if raw[i - 1] != None and raw[i - 1] == '—' or raw[i - 1] == '-':
                dash = raw[i - 1]
            else:
                dash = ''

            t = word.strip(',.-«:*;–!?"»')
            if d[key][0] == t.lower():
                res = re.search('^(.*?)'+d[key][0]+'(.*)', word.lower())
                bef = res.group(1)
                aft = res.group(2)
                #clean.add((key, t, bef, aft))
                writting('Insert into Analyses (analyse_id, word, punct_before, punct_after, in_text) values ("' \
                 + str(key) + '", "' + t + '", "' + dash + bef +'", "' + aft +'", "'+ str(i)+'");\n', name)
                i += 1

def main(file_name):
    do_mystem()
    d = lemma(open_lines('data.txt'), file_name)
    do_table(d, file_name)
    

@app.route('/main')
def form():
    if request.args:
        text = request.args['txt']
        file_name = request.args['name']
        writting(text, 'text.txt')
        main(file_name)       
        return 'Done'
    else:
        return render_template('form.html')
       
    
if  __name__ == '__main__':
    app.run(debug = True)
