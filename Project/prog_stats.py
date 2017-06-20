
# coding: utf-8

# In[1]:

import requests
import json
import re
from datetime import datetime, date
#import gensim, logging
from flask import Flask, render_template, request, redirect, url_for


# In[47]:

#get_ipython().magic('matplotlib inline')
app = Flask(__name__)
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# def model_params():
#     m = r'C:\Users\Masha\Documents\Programming\4 модуль\Project\web_0_300_20.bin.gz'
#     if m.endswith('.vec.gz'):
#         model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
#     elif m.endswith('.bin.gz'):
#         model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
#     else:
#         model = gensim.models.KeyedVectors.load(m)
#
#     model.init_sims(replace=True)
#
#     word_to_search = ["программирование", "код", "программист", "сервер", "веб"]
#     global words
#     words = {"программирование", "код", "программист", "сервер", "веб"}
#
#     stop = ['с++', 'captcha', 'инициализация', 'сервак']
#     for word in word_to_search:
#     # есть ли слово в модели? Может быть, и нет
#         word += '_NOUN'
#         if word in model:
#             print(word)
#         # смотрим на вектор слова (его размерность 300, смотрим на первые 10 чисел)
#             print(model[word][:5])
#         # выдаем 10 ближайших соседей слова:
#             for i in model.most_similar(positive=[word], topn=3):
#             # слово + коэффициент косинусной близости
#             #print(i[0])
#                 res = re.search('(.+?)(_|:)', i[0])
#                 w = res.group(1)
#                 if w not in stop:
#                     words.add(w)
#             print('\n')
#         else:
#         # Увы!
#             print(word + ' is not present in the model')

# In[48]:

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+ method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)


# In[49]:

def get_date(date):

    date = datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')

    year = date[:4]
    month = date[5:7]

    return int(month), int(year)


# In[50]:

def get_wall(group_id):
    posts = []

    result = vk_api('wall.get', owner_id=-group_id,
                    access_token = 'f835f6daf835f6daf835f6da09f86936dcff835f835f6daa170ead7b8d6fb013ea86f4d',
                    v='5.63', count=30)
    posts += result['response']['items']
    date = posts[-1]['date']

    while date > 1452564000:
        result = vk_api('wall.get', owner_id=-group_id,
                        access_token = 'f835f6daf835f6daf835f6da09f86936dcff835f835f6daa170ead7b8d6fb013ea86f4d',
                        v='5.63', count=10, offset=len(posts))
        posts += result['response']['items']

        date = posts[-1]['date']

    return posts


# In[51]:

def group_id(dom):
    group_info = vk_api('groups.getById', group_id=dom, v='5.63')
    group_id = group_info['response'][0]['id']
    return group_id


# In[52]:

def get_words(dom):
    freq = {}
    idx = group_id(dom)
    posts = get_wall(idx)

    for post in posts:
        #print(post)
        month, year = get_date(post['date'])

        for word in words:
            word = re.sub('\+', '\+', word)
            res = re.findall(word, post['text'])

            if word in freq:
                if month in freq[word]:
                    if year in freq[word][month]:
                        freq[word][month][year] += len(res)
                    else:
                        freq[word][month][year] = len(res)
                else:
                    freq[word][month] = {year: len(res)}
            else:
                freq[word] = {month: {year: len(res)}}

    return freq



# In[53]:


def for_js(totall):
    itog = {}
    for dom in totall:
        itog[dom] = []
        for word in totall[dom]:
            js = []
            for month in totall[dom][word]:
                if 2017 in totall[dom][word][month]:
                    js.append([month, totall[dom][word][month][2016], totall[dom][word][month][2017]])
                else:
                    js.append([month, totall[dom][word][month][2016], 0])
            js = sorted(js)
           #js.insert(0, ["Month", "2016", "2017"])
            itog[dom].append({word: js})
    return itog


# In[56]:

@app.route('/', methods=['GET', 'HEAD'])
def page():
    global words
    words = {'ассемблер', 'браузер', 'веб', 'код', 'кодировка',
             'программирование', 'программист', 'разработчик', 'сервер', 'тестировщик', 'файл',
             'хост'}
    domain = ['kaspercareer', 'pirsipy', 'tproger', 'habr']
    totall = {}
    for dom in domain:
        totall[dom] = get_words(dom)
    itog = for_js(totall)
    return render_template('test.html', itog = itog)


# In[ ]:




app.run(debug=True)


# In[ ]:


