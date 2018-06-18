# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib3.request

urllib3.disable_warnings()
def crawl_data(crawl_url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 
    http = urllib3.PoolManager()
    response = http.request('GET', crawl_url, headers=headers)
    soup = BeautifulSoup(response.data)
    return soup

def get_fit_data(data, keyword, base_url, remove_keywords):
    return_data=[]
    if (len(remove_keywords)>0):
        for x in range(0, len(remove_keywords)):
            data = [single_data for single_data in data if remove_keywords[x] not in single_data.text.encode('utf-8')]

    for anchor in data:
        if (keyword in anchor.text.encode('utf-8')):
            return_data.append(anchor.text.encode('utf-8') + ':<a href="' + base_url.encode('utf-8') + anchor['href'].encode('utf-8')+'">'+ anchor['href'].encode('utf-8') +'</a>')
    return return_data

def crawl(keyword):
    results=[]
    for x in range(0, 5):
        soup = crawl_data('http://www.supervr.net/catbbs/forums/show/'+ str(x) +'/12.page')
        data = soup.findAll("a", {"class": "topictitle"})
        return_data = get_fit_data(data, keyword, 'http://www.supervr.net',['已尋獲','已找到'])
        results.extend(return_data)

    ppt_index = 3772
    fit_titles=['拾獲', '協尋', '走失']
    for x in range(ppt_index-21, 3773):
        print('https://www.ptt.cc/bbs/cat/index'+ str(x) +'.html')
        soup = crawl_data('https://www.ptt.cc/bbs/cat/index'+ str(x) +'.html')
        data = soup.findAll("a")
        return_data1 = get_fit_data(data, '拾獲', 'https://www.ptt.cc',['已尋獲','已找到'])
        return_data2 = get_fit_data(data, '協尋', 'https://www.ptt.cc',['已尋獲','已找到'])
        return_data3 = get_fit_data(data, '走失', 'https://www.ptt.cc',['已尋獲','已找到'])
        return_data1 = [data for data in return_data1 if keyword in data]
        return_data2 = [data for data in return_data2 if keyword in data]
        return_data3 = [data for data in return_data3 if keyword in data]
        results.extend(return_data1)
        results.extend(return_data2)
        results.extend(return_data3)
    return results


if __name__ == '__main__':
    crawl('板橋')
