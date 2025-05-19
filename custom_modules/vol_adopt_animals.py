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


files = glob.glob('국가봉사동물 입양정보_*.xls')
recent_file = natsorted(seq=files, reverse=True)[0]


# In[4]:


def get_vol_adopt_animals():
    vol_adopt_animals = pd.read_excel(recent_file)

    # 공고날짜 정리 - 공고 시작일, 공고 종료일 분할
    periods = vol_adopt_animals['공고날짜'].str.split(' ~ ', expand=True)
    periods.columns = ['공고 시작일', '공고 종료일']
    vol_adopt_animals = pd.concat([periods, vol_adopt_animals], axis=1)

    vol_adopt_animals.drop(['공고날짜', '공고번호', '품종(기타)', '털색(기타)', '특징', '전화번호', '동영상링크', '스토리', '주소', '선정방법', '인수자 주의사항', '기관 방문 및 인수 절차', '기타사항'], axis=1, inplace=True)
    return vol_adopt_animals


# In[ ]:


def save_vol_adopt_animals():
    get_vol_adopt_animals().to_csv(recent_file[:-4] + '.csv', index_label=['index'], encoding="utf-8-sig")
    return


# In[5]:


if __name__ == "__main__":
    save_vol_adopt_animals()

