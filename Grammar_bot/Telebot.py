import telebot  
import flask
from pymorphy2 import MorphAnalyzer
import random
import re
import json
import urllib.request
import html

morph = MorphAnalyzer()

def open_json():
    req = urllib.request.Request(r'https://raw.githubusercontent.com/Maria192/myslina-hw/master/grammar.txt')
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')

    global gr   
    gr = json.loads(html)

open_json()
          
def make_form(word, left, right):
    ps = morph.parse(word)[0].tag.POS
    gram = str(morph.parse(word)[0].tag).split()
    
    try:    
        rand = random.choice(gr[gram[0]])
    except:
        return left + word + right

    if len(gram) != 1:
        infl = set(gram[1].split(','))
        rand = morph.parse(rand)[0]
        
        try:
            rand = rand.inflect(infl)
            new = rand.word
        except:
            new = word        
        
    else:
        new = rand
        
    itog = left + new + right
    
    return itog

def create_sent(mes):
    
        punct = '.+?-^;:\'\,"!@#%&*№()+=~'
        back = ''
        
        for word in mes.split():
                left = ''
                right = ''

                if word[0] in punct:
                        left = word[0]
                if word[-1] in punct:
                        right = word[-1]
                        
                word = word.strip(punct)
                
                if word != '':
                    itog = make_form(word, left, right)
                        
                else:
                    itog = left  
            
                
                back += itog + ' '
                
        return back[:-1]                                

def main():
        while True:
                print(create_sent(input('Введите сообщение: ')))
if __name__ == '__main__':
        main()
