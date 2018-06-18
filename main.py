# -*- coding: utf-8 -*-
from flask import Flask,request
from ptt_crawler import crawl
import json
app = Flask(__name__)

@app.route('/find_by_keyword', methods=['GET'])
def find_by_keyword():    
    keyword = request.args.get('keyword')
    data = crawl(keyword.encode('utf-8'))
    return_data='Keyword=' + keyword.encode('utf-8') + '\n\n'
    for i in range(0, len(data)):
        return_data += data[i] + '\n\n'

    return return_data

if __name__ ==  '__main__':
        app.run(debug=True)


