#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import glob
from natsort import natsorted

# Custom_module
from custom_modules import (animal_centers as ac,
                            geocoder as g)


# In[2]:


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


# In[3]:


files = glob.glob('입양대상 동물_*.xls')
recent_file = natsorted(seq=files, reverse=True)[0]


# In[4]:


def get_adopt_animals():
    adopt_animals = pd.read_excel(recent_file)

    adopt_animals.drop(['공고번호', '동물등록번호', '색상', '구조시 특징', '특징(사회성)', '특징(건강)', '발생장소', '기타사항', '관할기관', '상태', '보호센터연락처'], axis=1, inplace=True)

    animal_details = adopt_animals['나이/체중'].str.split(' / ', expand=True)
    animal_details.columns = ['age', 'kg']
    animal_details['less_than_60_days'] = animal_details['age'].apply(lambda x: True if '60일미만' in x else False)

    animal_details['age'] = animal_details['age'].apply(lambda x: x[:4])
    animal_details['kg'] = animal_details['kg'].str.replace(' (Kg)', '')

    adopt_animals.drop(['나이/체중'], axis=1, inplace=True)
    adopt_animals = pd.concat([animal_details, adopt_animals], axis=1)

    # 중성화 결측치 
    adopt_animals['중성화'] = adopt_animals['중성화'].fillna('미상')

    # # 중성화 encoding (0~2)
    # adopt_animals['중성화'].replace({'아니오':0, '예':1, '미상':2}, inplace=True)

    # # 성별 encoding (0~2)
    # adopt_animals['성별'].replace({'수컷':0, '암컷':1, '미상':2}, inplace=True)

    animal_type = adopt_animals['품종'].str.split(' ', n=1, expand=True)
    animal_type.columns = ['type', 'detail_type']
    animal_type['type'] = animal_type['type'].str.replace('[', '').str.replace(']', '')

    adopt_animals.drop(['품종'], axis=1, inplace=True)
    adopt_animals = pd.concat([animal_type, adopt_animals], axis=1)

    animal_centers = ac.get_animal_centers()

    center_locs = pd.DataFrame(columns = ['보호센터 시도', '보호센터 시군구', '보호센터 위도', '보호센터 경도'])

    for index, row in adopt_animals.iterrows():
        try:
            target = animal_centers.loc[animal_centers['보호센터명'] == row['보호센터'], ['시도', '시군구', '위도', '경도']]
            center_locs.loc[index] = target.values[0]
        except Exception as e:
            lat, lon = g.get_geocode(row['보호장소'], row['보호센터'])
            center_locs.loc[index] = row['보호장소'].split()[:2] + [float(lat), float(lon)]
            continue
        except:
            print(f"index {index} error: {e}, {row['관할 보호센터명']}")
            continue

    adopt_animals = pd.concat([adopt_animals, center_locs], axis=1)
    return adopt_animals


# In[ ]:


def save_adopt_animals():
    get_adopt_animals().to_csv(recent_file[:-4] + '.csv', index_label=['index'], encoding="utf-8-sig")
    return


# In[5]:


if __name__ == "__main__":
    save_adopt_animals()

