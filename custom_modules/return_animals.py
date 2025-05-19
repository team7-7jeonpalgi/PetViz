#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import glob
from natsort import natsorted

# Custom_module
from custom_modules import (new_addr_list,
                            animal_centers as ac,
                            geocoder as g)


# In[2]:


files = glob.glob('반환대상 동물공고_*.xls')
recent_file = natsorted(seq=files, reverse=True)[0]


# In[7]:


def get_return_animals():
    return_animals = pd.read_excel(recent_file)

    # 주소 정리
    return_animals['주소'] = [re.sub('\s\s0', '', i) for i in return_animals['주소']]

    # 공고기간 정리 - 공고 시작일, 공고 종료일 분할
    periods = return_animals['공고기간'].str.split(' ~ ', expand=True)
    periods.columns = ['공고 시작일', '공고 종료일']
    return_animals = pd.concat([return_animals, periods], axis=1)

    return_animals.drop(['공고번호', '동물등록번호', '털색', '특징', '구조사유', '대표자', '전화번호', '공고기간'], axis=1, inplace=True)
    return_animals.rename(columns={'주소':'관할 보호센터 주소'}, inplace=True)

    animal_centers = ac.get_animal_centers()
    center_locs = pd.DataFrame(columns = ['관할 보호센터 시도', '관할 보호센터 시군구', '관할 보호센터 위도', '관할 보호센터 경도'])

    for index, row in return_animals.iterrows():
        try:
            target_city = row['관할 보호센터 주소'].split()[:2]
            target_list = animal_centers[(animal_centers['보호센터명'] == row['관할 보호센터명']) & (target_city[0] == animal_centers['시도']) & (target_city[1] == animal_centers['시군구'])]
            target = target_list.iloc[0]
            if row['관할 보호센터 주소'] != target['주소']:
                return_animals.loc[index, '관할 보호센터 주소'] = target['주소']
            center_locs.loc[index] = target[['시도', '시군구', '위도', '경도']].values
        except Exception as e:
            try:
                lat, lon = g.get_geocode(row['관할 보호센터 주소'], row['관할 보호센터명'])
            except:
                addr = new_addr_list.new_addrs[row['관할 보호센터명']]
                lat, lon = g.get_geocode(addr, row['관할 보호센터명'])
            center_locs.loc[index] = target_city + [float(lat), float(lon)]
            continue

    return_animals = pd.concat([return_animals, center_locs], axis=1)

    rescue_loc = return_animals['구조장소'].str.split(expand=True)
    rescue_loc[0] = rescue_loc[0].replace('경기', '경기도')\
                                    .replace('서울', '서울특별시')\
                                    .replace('세종시', '세종특별자치시')\
                                    .replace('강원도', '강원특별자치도')\
                                    .replace('강원', '강원특별자치도')\
                                    .replace('전라북도', '전북특별자치도')\
                                    .replace('전북', '전북특별자치도')\
                                    .replace('경남', '경상남도')\
                                    .replace('경북', '경상북도')\
                                    .replace('전남', '전라남도')\
                                    .replace('충남', '충청남도')\
                                    .replace('충북', '충청북도')\
                                    .replace('부산', '부산광역시')\
                                    .replace('울산', '울산광역시')\
                                    .replace('광주', '광주광역시')\
                                    .replace('대구', '대구광역시')\
                                    .replace('대전', '대전광역시')\
                                    .replace('인천', '인천광역시')

    regions = pd.read_excel('전국행정동리스트.xlsx')
    reg_unique = regions.대분류.unique()

    tmp = pd.DataFrame(columns=['구조장소 시도', '구조장소 시군구'])
    for i, row in rescue_loc.iterrows():
        if row[0] in reg_unique:
            tmp.loc[i] = row[:2].values
            return_animals.loc[i, '구조장소'] = ' '.join(row.dropna())
        else:
            cities = regions.loc[regions['대분류'] == return_animals['관할 보호센터 시도'][i]]
            if (row[0] in cities['시/군']) or ((row[0] in cities['구']) & (cities.loc[(cities['구'] == row[0]) & cities['시/군'].isna()].empty is False)):
                tmp.loc[i] = [return_animals['관할 보호센터 시도'][i], row[0]]
                return_animals.loc[i, '구조장소'] = return_animals['관할 보호센터 시도'][i] + ' ' + ' '.join(row.dropna())
            else:
                tmp.loc[i] = return_animals.loc[i, ['관할 보호센터 시도', '관할 보호센터 시군구']].values.tolist()
                return_animals.loc[i, '구조장소'] = return_animals['관할 보호센터 시도'][i] + ' ' + ('' if return_animals['관할 보호센터 시군구'][i] is None else return_animals['관할 보호센터 시군구'][i] + ' ') + ' '.join(row.dropna())

    return_animals = pd.concat([return_animals, tmp], axis=1)

    return return_animals


# In[4]:


# # 구조장소 정리
# def loc_change(row):
#     addr = row['구조장소']
#     addr = addr.replace(' : ', ' ').replace('@', '아파트')
#     if '보호' in addr:
#         return row['관할 보호센터 주소']
#     if re.search(r'\w+[시군구]', addr) is None:
#         addr = f"{row['시군구']} {addr}"
#     if row['시도'] not in addr:
#         addr = f"{row['시도']} {addr}"
#     p = re.compile("[ 가-힣]+\d*[ 가-힣]*\d*[-]?\d*")

#     result = re.search(p, addr)
#     if result is not None:
#         result = result.group()
#     return result

# tmp = pd.DataFrame(columns = ['new_addr', '구조장소 위도', '구조장소 경도'])

# for index, row in return_animals.iterrows():
#     tmp.loc[index, 'new_addr'] = loc_change(row)
#     lat, lon = getGeoCode(tmp.loc[index, 'new_addr'])
#     tmp.loc[index, '구조장소 위도'] = float(lat)
#     tmp.loc[index, '구조장소 경도'] = float(lon)
#     # if [lat, lon] == [0, 0]:
#     #     tmp.loc[i, '구조장소 위도'] = return_animals.loc[i, '보호센터 주소 위도'].copy()
#     #     tmp.loc[i, '구조장소 경도'] = return_animals.loc[i, '보호센터 주소 경도'].copy()
#     # else:
#     #     tmp.loc[i, '구조장소 위도'] = float(lat)
#     #     tmp.loc[i, '구조장소 경도'] = float(lon)

# # 근처, 부근, 인근, 주변, 일대, 내, 에서, 입구, 
# tmp.sort_values(['구조장소 위도', 'new_addr'])

# return_animals.head()

# animal_rescue_locs = pd.DataFrame(columns = ['구조장소 위도', '구조장소 경도'])

# for i, addr in enumerate(return_animals['구조장소']):
#     lat, lon = getGeoCode(addr)
#     animal_rescue_locs.loc[i, '구조장소 위도'] = float(lat)
#     animal_rescue_locs.loc[i, '구조장소 경도'] = float(lon)

# animal_rescue_locs[:100]

# tmps = pd.DataFrame(columns = ['구조장소 위도', '구조장소 경도'])

# for i, addr in enumerate(tmp):
#     lat, lon = getGeoCode(addr)
#     tmps.loc[i, '구조장소 위도'] = float(lat)
#     tmps.loc[i, '구조장소 경도'] = float(lon)


# In[ ]:


def save_return_animals():
    get_return_animals().to_csv(recent_file[:-4] + '.csv', index_label=['index'], encoding="utf-8-sig")
    return


# In[ ]:


if __name__ == "__main__":
    save_return_animals()

