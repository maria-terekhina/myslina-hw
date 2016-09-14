import re
import urllib.request  # импортируем модуль

def clean(titles):
    new_titles = []
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
    
    for t in titles:
        clean_t = regTag.sub("", t)
        clean_t = clean_t.replace('&hellip;', '...')
        new_titles.append(clean_t)
        
    for t in new_titles:
        print(t)  


def load():
    
    url = 'http://www.zelpravda.ru/'  # адрес страницы, которую мы хотим скачать
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'  # хотим притворяться браузером

    req = urllib.request.Request(url, headers={'User-Agent':user_agent})  
    # добавили в запрос информацию о том, что мы браузер Мозилла

    with urllib.request.urlopen(req) as response:
       html = response.read().decode('utf-8')

    res = '<h2 class="nsp_header.+?</h2>'
    titles = re.findall(res, html)

    clean(titles)

    #print(len(titles))
    #print(titles[:3])

def main():
    load()

    
if  __name__ == '__main__':
    main()
