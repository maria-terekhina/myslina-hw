import re
import urllib.request
import os
import html

#июль 2015 года
#/obschestvo/palomniki-iz-zelenchukskogo-rajona-pobyvali-v-krymu.html

def writing(f, fl):
    if not os.path.exists('text-for-mystem'):
        os.makedirs('text-for-mystem')
    fw = open('.\\text-for-mystem' + os.sep + fl,'w', encoding = 'UTF-8')
    fw.write(f)
    fw.close()
    #exit(0)

def file_for_mystem():
    inp = ".\\plain"
    lst = os.listdir(inp)
    for fl in lst:
        f = open(inp+os.sep+fl,'r', encoding = 'UTF-8')
        fread = f.readlines()
        f.close()
        fread = fread[5:]
        fread = ''.join(fread)
        writing(fread, fl)




def do_mystem():
    inp = ".\\text-for-mystem"
    lst = os.listdir(inp)
    for fl in lst:
        os.system("C:\\Users\\Masha\\Documents\\Programming\\mystem.exe " + "-ndi " + inp \
+ os.sep + fl + " C:\\Users\\Masha\\Documents\\Programming\\mystem-plain" + os.sep + fl)
        fl_xml = fl.replace('.txt', '.xml')
        os.system(".\\mystem.exe " + "-ndi --format xml " + inp + os.sep + fl + " .\\\
mystem-xml" + os.sep + fl_xml)
    exit(0)
        
def write_articles(text, name, refer_full, topic, autor_name, file_name): #make documents with articles
    #print (refer, topic, name)
    if not os.path.exists('plain'):
        os.makedirs('plain')
    file_name = os.getcwd() + '\\' + 'plain\\' + file_name + '.txt'
    fw = open(file_name,'w', encoding = 'UTF-8')
    fw.write('@au '+ autor_name +'\n@ti ' + name + '\n@da Nodata\n@topic ' + topic + '\n@url ' + refer_full + '\n' + text)
    fw.close()


def write_metadata(name, autor_name, url, topic):
    local_address = os.getcwd()+ '\\plain' + '\\' + name + '.txt'
    #print(local_address)
    fw = open('metadata.csv','a', encoding = 'UTF-8')
    row = '%s\t%s\t\t\t%s\t\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\
\t%s\tЗеленчукская правда\t\t2015-2016\tгазета\tРоссия\tЗеленчукский район\tru\n'
    fw.write(row % (local_address, autor_name, name, topic, url))
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
        refer = refer.replace('/obrazovanie/', '')
    elif '/kultura' in refer:
        topic = 'Культура'
        refer = refer.replace('/kultura/', '')
    elif '/proisshestvija' in refer:
        topic = 'Происшествия'
        refer = refer.replace('/proisshestvija/', '')
    elif '/obschestvo' in refer:
        topic = 'Общество'
        refer = refer.replace('/obschestvo/', '')
    elif '/sport' in refer:
        topic = 'Спорт'
        refer = refer.replace('/sport/', '')
    elif '/vlast' in refer:
        topic = 'Власть'
        refer = refer.replace('/vlast/', '')
    elif '/religija' in refer:
        topic = 'Религия'
        refer = refer.replace('/religija/', '')
    elif '/kriminal' in refer:
        topic = 'Криминал'
        refer = refer.replace('/kriminal/', '')
    elif '/turizm' in refer:
        topic = 'Туризм'
        refer = refer.replace('/turizm/', '')
    else: print('ALARM!')

    refer = refer.replace('.html', '')
    return topic, refer
    



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
        #print(refer)
        topic, file_name = get_topic(refer)
        refer = 'http://www.zelpravda.ru' + refer
        article = load_page(refer)
        name = name_of_article(article)
        
        regTag = re.compile('<td valign="top">(.+?)<script>', flags=re.U | re.DOTALL)
        res = re.search(regTag, article)
        rawText = res.group(1)
        clean_text = clean(rawText)
        autor_name = get_autor(rawText)
        write_articles(clean_text, name, refer, topic, autor_name, file_name)
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
    do_mystem()
    file_for_mystem()
    url = 'http://www.zelpravda.ru/sitemap.html'
    html = load_page(url)
    refers = get_types(html)    
    load_themes(refers)
    do_mystem()
    


    
if  __name__ == '__main__':
    main()
