#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import glob
from natsort import natsorted
from geopy.geocoders import Nominatim

# Custom_module
from custom_modules import geocoder as g


# In[2]:


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


# In[4]:


files = glob.glob('동물등록 대행기관 목록_*.xls')
recent_file = natsorted(seq=files, reverse=True)[0]


# In[3]:


def get_animal_agency():
    animal_agency = pd.read_excel(recent_file)

    # 명칭변경 및 시/도, 시/군/구 추가
    locs = animal_agency['주소'].str.split(expand=True)
    locs[0] = locs[0].replace({'경기':'경기도', '강원도':'강원특별자치도', '전라북도':'전북특별자치도'})
    animal_agency['시도'] = locs[0].copy()
    animal_agency['시군구'] = locs[1].copy()
    # animal_agency['주소'] = locs.apply(lambda row: ' '.join(row.values.astype(str)).replace(' None', ''), axis=1)

    animal_agency.drop(['번호', '대표자명', '업체전화번호', '주소'], axis=1, inplace=True)
    return animal_agency


# In[ ]:


def save_animal_agency():
    get_animal_agency().to_csv(recent_file[:-4] + '.csv', index_label=['index'], encoding="utf-8-sig")
    return


# In[5]:


# def loc_change(addr):
#     addr = addr.replace(' null', '').replace('  ', ' ')
#     addr = re.sub(r'\s\w*\d*층', r'', addr)
#     addr = re.sub(r'(?<=\d)(번지\s\D*)(?=\d+호)', r'-', addr)
#     addr = re.sub(r'(?<=\d)\s.*$', r'', addr)
#     addr = re.sub(r'(번지|호\s.*|호[^가-힣]+.*|호|\s\(.+\).*)$', r'', addr)
#     addr = re.sub(r'번지.+$', r'', addr)
#     addr = re.sub(r'(?<=\d)[가-힣]+\d*$', r'', addr)
#     return addr

# animal_agency['주소'] = animal_agency['주소'].apply(loc_change)


# In[6]:


# # # 주소 오타 직접 수정 목록
# new_addrs = {
#     "경희궁바른동물병원": "서울특별시 종로구 홍파동 199",
#     "강북동물병원": "경상북도 경산시 하양읍 동서리 592-1",
#     "강아지나라 동물병원": "경기도 남양주시 진접읍 장현리 351-18",
#     "강아지와 고양이": "강원특별자치도 태백시 황지로 130",
#     "거제동물병원": "부산광역시 연제구 거제동 608-17",
#     "경동동물병원": "인천광역시 중구 개항로 68",
#     "고려동물병원"
# }

# # 좌표 탐색
# geo_local = Nominatim(user_agent='South Korea')

# agency_locs = pd.DataFrame(columns = ['위도', '경도'])

# for i, row in animal_agency.iterrows():
#     name = row['업체명']
#     if name in new_addrs.keys():
#         if row[['시도', '시군구']].values.tolist() == new_addrs[name].split()[:2]:
#             animal_agency.loc[i, '주소'] = new_addrs[name]
#     addr = animal_agency.loc[i, '주소']
#     print(i, name, addr)
#     lat, lon = g.get_geocode(addr, name)
#     agency_locs.loc[i, '위도'] = float(lat)
#     agency_locs.loc[i, '경도'] = float(lon)


# In[7]:


if __name__ == "__main__":
    save_animal_agency()

