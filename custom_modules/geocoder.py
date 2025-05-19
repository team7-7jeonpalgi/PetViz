#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import requests


# In[ ]:


def get_geocode(addr, name):
    try:
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
        headers = {"Authorization": "KakaoAK ec0a67c13e12426033eb825ba4fbfd95"}
        api_json = json.loads(str(requests.get(url, headers=headers).text))
        geo_info = api_json['documents'][0]['address']
        loc = [str(geo_info['y']), str(geo_info['x'])]
        return loc
    except:
        # 위경도 직접 수정 목록
        new_locs = {
            '대구시수의사회(삼성)': [35.860186857, 128.557148742], 
            '창녕 유기동물보호소': [35.574085, 128.50745], 
            '(사)영일동물플러스': [36.145683, 129.33263], 
            '유기동물임시보호센터': [34.331898, 126.781204],
            '검단종합동물병원': [37.6055206, 126.6670439],

        }
        return new_locs[name]

