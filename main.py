# -*- coding: utf-8 -*-
from flask import Flask,request, render_template
from ptt_crawler import crawl
import json
from pyClass import SearchInfo
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():    
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():    
    return render_template('about.html')

@app.route('/find_by_keyword', methods=['POST'])
def find_by_keyword():    
    return_data=[]
    try:
        from_pageno=0
        keyword = request.args.get('keyword')
        findCategory = request.args.get('findCategory')
        pageno = request.args.get('pageno')
        from_pageno, data = crawl(keyword.encode('utf-8'), findCategory, int(pageno.encode('utf-8')))
        data.sort(key=lambda x: x.post_date, reverse=True)
        print('finished.')
        
        for i in range(0, len(data)):
            return_data.append({'from_pageno':from_pageno, 'photo_desc': data[i].photo_desc, 'from_web': data[i].from_web, 'article_content': data[i].article_content ,'title':data[i].title, 'url':data[i].url, 'photo_url':data[i].photo_url, 'post_date': str(data[i].post_date)})
    except Exception as ee:
        print(str(ee))
    return json.dumps(return_data, ensure_ascii=False)


if __name__ ==  '__main__':
        #app.run(debug=True, port=5000)
        app.run(debug=True)  # Heroku


