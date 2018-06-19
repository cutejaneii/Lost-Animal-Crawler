# -*- coding: utf-8 -*-
import os
from flask import Flask,request
from ptt_crawler import crawl
import json
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():    
    return 'Hello, World! This is Lost-Animal-Crawler app.'

@app.route('/find_by_keyword', methods=['GET'])
def find_by_keyword():    
    keyword = request.args.get('keyword')
    data = crawl(keyword.encode('utf-8'))
    return_data='Keyword=' + keyword.encode('utf-8') + '\n\n'
    for i in range(0, len(data)):
        return_data += data[i] + '\n\n'

    return return_data

if __name__ ==  '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(debug=True, host='0.0.0.0', port=port)
        #app.run(debug=True)


