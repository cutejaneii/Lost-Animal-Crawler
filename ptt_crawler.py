# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib3.request
from pyClass import SearchInfo
import threading
import Queue
#from queuelib import queue

urllib3.disable_warnings()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 

def crawl_data(crawl_url):
    http = urllib3.PoolManager()
    response = http.request('GET', crawl_url, headers=headers)
    soup = BeautifulSoup(response.data, "html.parser")
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
    try:
        imgur_soup = crawl_data(imgur_url)
        imgs = imgur_soup.findAll("link", {"rel":"image_src"})
        for img in imgs:
            if ('.jpg' in img['href']):
                photo_url=img['href'].encode('utf-8')
                break
            elif ('.png' in img['href']):
                photo_url=img['href'].encode('utf-8')
                break
            else:
                pass

    except Exception as e1:
        print(str(e1))
    return photo_url

def get_ptt_content(ptt_article_url):
    photo_count=0
    photo_url='../static/img/cutekitty.jpeg'
    article_content=''
    post_date=''
    try:
        ptt_article_soup = crawl_data(ptt_article_url)

        imgs = ptt_article_soup.findAll('a', {"rel":"nofollow"})

        for img in imgs:
            if ('.jpg' in img['href']):
                photo_url=img['href'].encode('utf-8')
                photo_count+=1
            elif ('.png' in img['href']):
                photo_url = img['href'].encode('utf-8')
                photo_count+=1
            elif ('i.imgur.com' in img['href']):
                photo_url = img['href'].encode('utf-8')
                photo_count+=1
            elif ('imgur.com' in img['href']):
                photo_url = get_imgur_img(img['href'].encode('utf-8')).encode('utf-8')
                photo_count+=1
            else:
                pass
        
        dates = ptt_article_soup.findAll('span', {"class":"push-ipdatetime"})
        for d in dates:
            if (post_date==''):
                post_date=d.text
                break

    except Exception as e2:
        print(str(e2))

    return post_date, photo_count, photo_url, article_content

def get_ptt_fit_data(ptt_soup, keywords, base_url, remove_keywords, user_keyword):

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
                if (user_keyword in anchor.text.encode('utf-8')):
                    catInfo = SearchInfo()
                    catInfo.title=anchor.text.encode('utf-8')
                    catInfo.url=base_url.encode('utf-8') + anchor['href'].encode('utf-8')
                    catInfo.from_web='PTT'
                    catInfo.article_content='this is content......'
                    catInfo.photo_desc=''
                    catInfo.post_date, catInfo.photo_count, catInfo.photo_url, catInfo.article_content = get_ptt_content(catInfo.url)
                    if (catInfo.photo_count > 1):
                        catInfo.photo_desc='1/'+ str(catInfo.photo_count)
                    
                    return_data.append(catInfo)

    return return_data

def thread_job(from_pageno, to_pageno, q, fit_titles, remove_titles, keyword):
    my_result=[]
    try:
        for x in range(from_pageno, to_pageno+1):
            print('https://www.ptt.cc/bbs/cat/index'+ str(x) +'.html')
            ptt_soup = crawl_data('https://www.ptt.cc/bbs/cat/index'+ str(x) +'.html')
            
            return_data = get_ptt_fit_data(ptt_soup, fit_titles, 'https://www.ptt.cc',remove_titles, keyword)
            my_result.extend(return_data)
    except Exception as ee:
        print(str(ee))
    print('yes...we finished....'+str(from_pageno))
    q.put(my_result) #return results
    q.task_done()
    

def ptt_crawl(keyword, findCategory, pageno):
    results=[]
    threads=[]
    q = Queue.Queue(15)
    from_pageno=0

    ppt_index = pageno
    if (pageno==0):
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
        remove_titles.append('已找回')
        remove_titles.append('已尋回')
    else:
        fit_titles.append('拾獲')
        remove_titles.append('已找到主人')
    
    page_size = 1

    for x in range(0, 15):
        to_pageno = ppt_index - (page_size*x) 
        from_pageno = ppt_index - (page_size*(x+1))+1 

        thread = threading.Thread(target=thread_job, args=(from_pageno, to_pageno, q, fit_titles, remove_titles, keyword),)         
        thread.setDaemon(True)
        thread.start()  
        threads.append(thread)
    
    for _ in range(len(threads)):
        q.join()

    for _ in range(len(threads)):
        results.extend(q.get()) # 取出 queue 裡面的資料
    return from_pageno, results


if __name__ == '__main__':
    crawl('板橋')