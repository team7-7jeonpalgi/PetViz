#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import natsort
from geopy.geocoders import Nominatim

# Custom module
from custom_modules import new_addr_list, geocoder as g


# In[2]:


files = glob.glob('동물보호센터 목록_*.xls')
recent_file = natsort.natsorted(seq=files, reverse=True)[0]


# In[5]:


def get_animal_centers():
    animal_centers = pd.read_excel(recent_file)

    animal_centers.drop(['번호', '전화번호'], axis=1, inplace=True)

    # 명칭변경 및 시/도, 시/군/구 추가
    locs = animal_centers['관할구역'].str.split(expand=True)
    animal_centers['시도'] = locs[0].copy()
    animal_centers['시군구'] = locs[1].copy()

    # 관할 보호센터 주소 기반 좌표 탐색
    geo_local = Nominatim(user_agent='South Korea')

    center_locs = pd.DataFrame(columns = ['위도', '경도'])

    for i, row in animal_centers.iterrows():
        name = row['보호센터명']
        if (name in new_addr_list.new_addrs.keys()) and (new_addr_list.new_addrs[name].split()[:2] == row[['시도', '시군구']].values.tolist()):
            animal_centers.loc[i, '주소'] = new_addr_list.new_addrs[name]
        animal_centers.loc[i, '주소'] = animal_centers.loc[i, '주소'].replace(' null', '')
        addr = animal_centers.loc[i, '주소']
        try:
            lat, lon = g.get_geocode(addr, name)
        except:
            lat, lon = g.get_geocode(new_addr_list.new_addrs[name], name)
        finally:
            center_locs.loc[i, '위도'] = float(lat)
            center_locs.loc[i, '경도'] = float(lon)

    animal_centers = pd.concat([animal_centers, center_locs], axis=1)

    return animal_centers


# In[ ]:


def save_animal_centers():
    get_animal_centers().to_csv(recent_file[:-4] + '.csv', index_label=['index'], encoding="utf-8-sig")
    return


# In[4]:


if __name__ == "__main__":
    save_animal_centers()

