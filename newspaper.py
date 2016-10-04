import re
import urllib.request
import os
import html

#июль 2015 года
#/obschestvo/palomniki-iz-zelenchukskogo-rajona-pobyvali-v-krymu.html

def write_articles(text, name, refer, topic, autor_name): #make documents with articles
    #print (refer, topic, name)
    if not os.path.exists('plain'):
        os.makedirs('plain')
    file_name = os.getcwd() + '\\' + 'plain\\' + name + '.txt'
    fw = open(file_name,'w', encoding = 'UTF-8')
    fw.write('@au '+ autor_name +'\n@ti ' + name + '\n@da Nodata\n@topic ' + topic + '\n@url ' + refer + '\n' + text)
    fw.close()

def write_metadata(name, autor_name, url, topic):
    fw = open('metadata.xml','a', encoding = 'UTF-8')
    row = '%s\t%s\t\t\t%s\t2015-2016\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\
    \t%s\tЗеленчукская правда\t\t%s\tгазета\tРоссия\tЗеленчукский район\tru'
    fw.write(row % ('тут ссылка', autor_name, name, topic, url, '2016'))
    #print(row)
    fw.close()
    
    
def clean(t): #clean text
    
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL) #all tags
    regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL) #all scripts
    regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL) #all comments
    regReg = re.compile('\t|\n(\r)?', flags=re.U | re.DOTALL)
    

    clean_t = regScript.sub("", t)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = html.unescape(clean_t)
    clean_t = regReg.sub("", clean_t)
    return clean_t
 


def get_types(html): #get themes of articles

    pattern = '<ul class="tMenu2">(.+?)</li></ul></ul></div>'
    res = re.search(pattern, html)
    titles = res.group(1)
    pattern = '<a href="(.+?)"><span>'
    refers = re.findall(pattern, titles)
    return refers

    

def load_page(url): #download the site-map page    
    
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

    req = urllib.request.Request(url, headers={'User-Agent':user_agent})# trying to look like Mozilla

    try:
        with urllib.request.urlopen(req) as response:
           html = response.read().decode('utf-8')
    except:
        print('Error at', url)
        
    return html

def amount_of_pages(page): #search amount of pages in themes
    
    pattern = 'Страница 1 из (.+?)	</td>'
    res = re.search(pattern, page)
    pages = res.group(1)
    return pages

def name_of_article(rawText): # search for author name

    regTag = re.compile('contentpagetitle">(.+?)</a>', flags=re.U | re.DOTALL)
    res = re.search(regTag, rawText)
    name = res.group(1)
    name = clean(name)
    name = name.replace('?', '')
    name = name.replace('!', '')

    return name

def get_topic(refer): #name of the topic by fererenсe
    #print (refer)
    if '/obrazovanie' in refer:
        topic = 'Образование'
    elif '/kultura' in refer:
        topic = 'Культура'
    elif '/proisshestvija' in refer:
        topic = 'Происшествия'
    elif '/obschestvo' in refer:
        topic = 'Общество'
    elif '/sport' in refer:
        topic = 'Спорт'
    elif '/vlast' in refer:
        topic = 'Власть'
    elif '/religija' in refer:
        topic = 'Религия'
    elif '/kriminal' in refer:
        topic = 'Криминал'
    elif '/turizm' in refer:
        topic = 'Туризм'
    else: print('ALARM!')

    return topic



def get_autor(text): #get author name, if given
    
    regTag = re.compile('<p>.+?\t([А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+)</p>', flags=re.U | re.DOTALL)
    res = re.search(regTag, text)
    if res != None:
        name = res.group(1)
        print(name)
    else:
        name = 'Noname'

    
    return name
    
def articles_info(refers): #get information about article
    
    for refer in refers:
        topic = get_topic(refer)
        refer = 'http://www.zelpravda.ru' + refer
        article = load_page(refer)
        name = name_of_article(article)
        
        regTag = re.compile('<td valign="top">(.+?)<script>', flags=re.U | re.DOTALL)
        res = re.search(regTag, article)
        rawText = res.group(1)
        clean_text = clean(rawText)
        autor_name = get_autor(rawText)
        write_articles(clean_text, name, refer, topic, autor_name)
        write_metadata(name, autor_name, refer, topic)
    

def article_refer(PageWithArticle): #get referenсes
    pattern = '<h1><a href="(.+?)" class="contentpagetitle">'
    refers = re.findall(pattern, PageWithArticle)
    articles_info(refers)


def articles_in_themes(pagesTheme): #download themes' pages
    i = 0
    j = 0
    for refer in pagesTheme:
        while j < int(pagesTheme[refer]):
            PageWithArticle = load_page('http://www.zelpravda.ru' + refer + '?start=' + str(i))
            #print ('http://www.zelpravda.ru' + refer + '?start=' + str(i))
            article_refer(PageWithArticle)
            if '/obrazovanie.html' == refer or '/kultura.html' == refer or '/proisshestvija.html' == refer or '/obschestvo.html' == refer or '/sport.html' == refer or '/turizm.html' == refer:
                i += 4
            else:
                i += 8
            j += 1
        i = 0
        j = 0


def load_themes(refers): #get names of themes

    pagesTheme = {}
    
    for theme in refers:
        page = load_page('http://www.zelpravda.ru' + theme) 
        pages = amount_of_pages(page)
        pagesTheme[theme] = pages
        
    articles_in_themes(pagesTheme) 


def main():
    url = 'http://www.zelpravda.ru/sitemap.html'
    html = load_page(url)
    refers = get_types(html)    
    load_themes(refers)
    


    
if  __name__ == '__main__':
    main()
