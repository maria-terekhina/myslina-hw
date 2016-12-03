import re
import urllib.request
import os
import html

def writting(sets):
    f = open('allwords.txt', 'w', encoding = 'UTF-8')
    f.write('Пересечение')
    for s in sorted(list(sets)):
        f.write(s + '\n')
    f.write('\n')
    f.write('Разность\n')
    f.close()    


def writting1(arr, i):
    f = open('allwords.txt', 'a', encoding = 'UTF-8')
    f.write('Заметка ' + str(i) + '\n')
    for s in sorted(arr):
        f.write(s + '\n')
    f.write('\n')
    f.close()

    
def clean(t): #clean text
    
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL) #all tags
    regScript = re.compile('<(script|em)>.*?</(script|em)>', flags=re.U | re.DOTALL) #all scripts
    regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL) #all comments
    regReg = re.compile('  |\t|\n(\r)?', flags=re.U | re.DOTALL)
    regStaff = re.compile('<b>.+?</a>.', flags=re.U | re.DOTALL)
    regName = re.compile('(Фото|Источник) (Дела|ДЕЛА).ru', flags=re.U | re.DOTALL)
    
    clean_t = regScript.sub("", t)
    clean_t = regStaff.sub("", clean_t)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = html.unescape(clean_t)
    clean_t = regName.sub("", clean_t)
    clean_t = clean_t.replace('© ТВК, 1994—2016', '')
    clean_t = regReg.sub("", clean_t)
    return clean_t


def clean_split (s):
    s = s.replace('\n', ' ')
    s = s.replace('.', ' ')
    s = s.lower()
    txt = s.split()
    clean = []
    for word in txt:
        word = word.strip('.,?!/;:"()[]{}-«»—–')
        if word != ('' or '\u200bв'):
            clean.append(word)
    return clean
        

def load_page(arr): #download the site-map page    
    
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    
    for url in arr:
        req = urllib.request.Request(url, headers={'User-Agent':user_agent})# trying to look like Mozilla
        try:
            with urllib.request.urlopen(req) as response:
               html = response.read().decode('utf-8')
        except:
            print('Error at', url)
        
        yield html


def differ(arr):
    d = {}
    for el in arr:
        for word in el:
            if not word in d:
                d[word] = 1
            else:
                d[word] += 1
        
    dif = [(((set(arr[0])-set(arr[1]))-set(arr[2]))-set(arr[3]))-set(arr[4]),\
    (((set(arr[1])-set(arr[0]))-set(arr[2]))-set(arr[3]))-set(arr[4]),\
    (((set(arr[2])-set(arr[1]))-set(arr[0]))-set(arr[3]))-set(arr[4]),\
    (((set(arr[3])-set(arr[1]))-set(arr[2]))-set(arr[0]))-set(arr[4]),\
    (((set(arr[4])-set(arr[1]))-set(arr[2]))-set(arr[3]))-set(arr[0])]
    
    i = 1
    
    for el in dif:        
        itog = []
        for word in el:
            if d[word] > 1:
                itog.append(word)
        writting1(itog, i)
        i +=1    
    
    
def intersect(arr):
    writting(set(arr[0])&set(arr[1])&set(arr[2])&set(arr[3])&set(arr[4]))
    

def find_text(page):
    pattern = '<h1.*?>(.+?)</h1>'
    res = re.search(pattern, page, flags=re.DOTALL)
    title = clean(res.group(1))
    
    pattern = '<h1.*?<p.*?>(.+?)</?div'
    res = re.search(pattern, page, flags=re.DOTALL)
    text = clean(res.group(1))
    return clean_split (title + ' ' +text)


def main():
    all_words = []
    refers = ['http://ngs24.ru/news/more/50180071/', 'http://vg-news.ru/n/125277', \
              'http://krsk.sibnovosti.ru/society/342092-roev-ruchey-predlozhil-krasnoyartsam-dat-imya-novorozhdennoy-zebre',\
              'http://www.dela.ru/lenta/204737/', 'http://tvk6.ru/publications/news/22836/']
    for page in load_page(refers):
        all_words.append(find_text(page))
    intersect(all_words)
    differ(all_words)

    
if  __name__ == '__main__':
    main()
