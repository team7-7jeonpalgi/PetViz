#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
from natsort import natsorted


# In[2]:


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


# In[3]:


files = glob.glob('동물병원 목록_*.xls')
recent_file = natsorted(seq=files, reverse=True)[0]


# In[ ]:


def get_animal_hospitals():
    animal_hospitals = pd.read_excel(recent_file)
    animal_hospitals.drop(['번호', '전화번호', '인허가번호'], axis=1, inplace=True)

    locs = animal_hospitals['소재지'].str.split(expand=True)

    animal_hospitals['시도'] = locs[0].copy()
    animal_hospitals['시군구'] = locs[1].copy()

    return animal_hospitals


# In[ ]:


def save_animal_hospitals():
    get_animal_hospitals().to_csv(recent_file[:-4] + '.csv', index_label=['index'], encoding="utf-8-sig")
    return


# In[ ]:


if __name__ == "__main__":
    save_animal_hospitals()

