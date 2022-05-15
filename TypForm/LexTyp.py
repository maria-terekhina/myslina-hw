from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

lang = []
new = []
answ = {}
res = []

def open_file():
    f = open('Answers.txt','r', encoding = 'UTF-8')
    s = f.read()
    f.close()
    return s
   
def open_lines():
    f = open('Search.txt','r', encoding = 'UTF-8')
    global new
    for line in f:
        if not 'Язык' in line and not 'end' in line:
            line = line.split(',')
        new.append(line)
    arr = f.readlines()
    f.close()


def write_answers(s):
    f = open('Answers.txt','a', encoding = 'UTF-8')
    f.write(s)
    f.close()
    
def write_for_search(d):
    f = open('Search.txt','a', encoding = 'UTF-8')
    f.write('Язык: ' + d['Язык'] + '\n')
    for key in d:
        if key != 'Язык':
            f.write(key + ':, ' + d[key][0] + ', ' + d[key][1] + ', '+ \
                    d[key][2] + ', ' + d[key][3] + '\n')
    f.write('end\n')
    f.close()
    
def langs(la):
    global lang
    lang.append(la)

def answers(d):
    global answ
    for key in d:
        if '1' in key:
            answ[key.replace('1', '')] = [d[key]]
    for key in d:
        if '2' in key:
            answ[key.replace('2', '')].append(d[key])
    for key in d:
        if '3' in key:
            answ[key.replace('3', '')].append(d[key])
    for key in d:
        if '4' in key:
            answ[key.replace('4', '')].append(d[key])
            
    answ['Язык'] = d['Язык']
    langs(d['Язык'])
    s = json.dumps(answ, ensure_ascii = False)
    write_answers(s)
    write_for_search(answ)
    open_lines()
    
def search_answ(q):
    global new
    i = 0
    res = {}
    for line in new:
        if q['language'] in line:
            i = 1
        if 'end' in line:
            i = 0
        if i == 1 and q['word'] in line[0]:
            res[line[0]] = line[1].strip()
    return res
              
@app.route('/done')
def done():
     return render_template('done_form.html')
    
@app.route('/')
def form():
    if request.args:
        answers(request.args)
        return redirect(url_for('done'))
    else:
        return render_template('main_form.html')
    
@app.route('/not_found')
def not_found():
    return render_template('non_search.html')    

@app.route('/results')
def results():    
    return render_template('results_form.html', res = res)


@app.route('/search')
def search():
    if request.args:
        global res
        res =  search_answ(request.args)
        
        if len(res) != 0:
            return redirect(url_for('results'))
        else: 
            return redirect(url_for('not_found'))
    else:
        return render_template('search_form.html', Lang = lang)
    
    
@app.route('/stats')
def stats():
    return render_template('stats_form.html', d = new)
    
    
@app.route('/json')
def return_json():
    s = open_file()
    return render_template('json_form.html', j = s)


if __name__ == '__main__':
    app.run(debug = True)
