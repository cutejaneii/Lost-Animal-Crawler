# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib3.request
from pyClass import SearchInfo

urllib3.disable_warnings()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 

def crawl_data(crawl_url):
    http = urllib3.PoolManager()
    response = http.request('GET', crawl_url, headers=headers)
    soup = BeautifulSoup(response.data)
    return soup

def get_ptt_page_no():
    page_no=''
    soup = crawl_data('https://www.ptt.cc/bbs/cat/index.html')
    data = soup.findAll("a", {"class": "btn wide"})
    remove_href=['/bbs/cat/index1.html', '/bbs/cat/index.html']
    for anchor in data:
        if (anchor['href'] !=''):
            if (anchor['href'] not in remove_href):
                page_no = anchor['href'].encode('utf-8').replace('/bbs/cat/index','').replace('.html','')  
    return page_no

def get_fit_data(data, keyword, base_url, remove_keywords):
    return_data=[]
    if (len(remove_keywords)>0):
        for x in range(0, len(remove_keywords)):
            data = [single_data for single_data in data if remove_keywords[x] not in single_data.text.encode('utf-8')]

    for anchor in data:
        if (keyword in anchor.text.encode('utf-8')):
            catInfo = SearchInfo()
            catInfo.title=anchor.text.encode('utf-8')
            catInfo.url=base_url.encode('utf-8') + anchor['href'].encode('utf-8')
            return_data.append(catInfo)
    return return_data

def get_imgur_img(imgur_url):
    photo_url=''
    print('===========================================')
    print(imgur_url)
    try:
        imgur_soup = crawl_data(imgur_url)
        imgs = imgur_soup.findAll('img')

        for img in imgs:
            if ('.jpg' in img['src']):
                photo_url=img['src'].encode('utf-8')

    except Exception as e1:
        print(str(e1))
    return photo_url

def get_ptt_content(ptt_article_url):
    photo_count=0
    photo_url='../static/img/cutekitty.jpeg'
    article_content=''
    post_date='post date'
    try:
        ptt_article_soup = crawl_data(ptt_article_url)

        imgs = ptt_article_soup.findAll('a', {"rel":"nofollow"})

        for img in imgs:
            if ('.jpg' in img['href']):
                photo_url=img['href'].encode('utf-8')
                photo_count+=1
            elif ('imgur.com' in img['href']):
                photo_url = get_imgur_img(img['href'].encode('utf-8')).encode('utf-8')
                photo_count+=1
            else:
                pass
    except Exception as e2:
        print(str(e2))

    return post_date, photo_count, photo_url, article_content

def get_ptt_fit_data(ptt_soup, keywords, base_url, remove_keywords):

    data = ptt_soup.findAll("a")
    return_data=[]

    if (len(remove_keywords)>0):
        for x in range(0, len(remove_keywords)):
            data = [single_data for single_data in data if remove_keywords[x] not in single_data.text.encode('utf-8')]

    for anchor in data:
        if (anchor['href'] is not None and '/bbs/cat/M.' in anchor['href']):
            check_keyword=False
        
            for i in range(0, len(keywords)):
                if (keywords[i] in anchor.text.encode('utf-8')):
                    check_keyword=True
            
            if (check_keyword):
                print(anchor.text.encode('utf-8'))
                catInfo = SearchInfo()
                catInfo.title=anchor.text.encode('utf-8')
                catInfo.url=base_url.encode('utf-8') + anchor['href'].encode('utf-8')
                catInfo.from_web='PTT'
                catInfo.article_content='this is content......'
                catInfo.post_date, catInfo.photo_count, catInfo.photo_url, catInfo.article_content = get_ptt_content(catInfo.url)
                if (catInfo.photo_count > 1):
                    catInfo.photo_desc='還有'+ str(catInfo.photo_count-1) + '張'
                
                return_data.append(catInfo)

    return return_data

def crawl(keyword, findCategory):
    results=[]
    #for x in range(0, 5):
    #    soup = crawl_data('http://www.supervr.net/catbbs/forums/show/'+ str(x) +'/12.page')
    #    data = soup.findAll("a", {"class": "topictitle"})
    #    return_data = get_fit_data(data, keyword, 'http://www.supervr.net',['已尋獲','已找到'])
        #results.extend(return_data)

    ppt_index = int(get_ptt_page_no())+1
    fit_titles=[]
    remove_titles=[]

    if (findCategory=="s01"):
        fit_titles.append('走失')
        fit_titles.append('協尋')
        remove_titles.append('已回家')
        remove_titles.append('找到了')
        remove_titles.append('回家了')
        remove_titles.append('已尋獲')
        remove_titles.append('已找到')
        remove_titles.append('已尋回')
    else:
        fit_titles.append('拾獲')
        remove_titles.append('已找到主人')

    for x in range(ppt_index-32, ppt_index):
        print('https://www.ptt.cc/bbs/cat/index'+ str(x) +'.html')
        ptt_soup = crawl_data('https://www.ptt.cc/bbs/cat/index'+ str(x) +'.html')
        
        return_data = get_ptt_fit_data(ptt_soup, fit_titles, 'https://www.ptt.cc',remove_titles)
        return_data = [data for data in return_data if keyword in data.title]
        results.extend(return_data)

    return results


if __name__ == '__main__':
    crawl('板橋')
