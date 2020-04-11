## 전국 일선행정기관 목록에서 포항시에 위치한 항목만 추출하고 주소로 위도,경도 얻기
## 일선행정기관: 동사무소, 경찰서, 소방서, 보건소 등
import pandas as pd
import numpy as np

rootDir = 'd:/research/data/'
## 동해면사무소, 보건지소 주소 수정 (일원로 -> 일월로)
filename = '13.일선행정기관 주소와 전화번호_20191130_수정.xlsx'

ad = pd.read_excel(rootDir + filename)
ad.columns = ['Name', 'Address']

pohang = ad[ad.Address.str.contains('포항시')]
pohang.reset_index(inplace=True)
pohang.drop('index', axis=1, inplace=True)

REST_KEY = '6bd6718879c207eda2ad2a53484e5c9f'

import requests
import json

def getLocFromAddr(address):
    url="https://dapi.kakao.com/v2/local/search/address.json" 
    queryString={"query":address}
    header={"authorization": "KakaoAK " + REST_KEY}
    print(address)
    r = requests.get(url, headers=header, params=queryString)
    t = json.loads(r.text)
    
    try:
        longitude = t['documents'][0]['address']['x']
        latitude = t['documents'][0]['address']['y']
        print(str(longitude) + 'E', str(latitude) + 'N')
        return longitude, latitude
    except:
        return 0, 0
    
    
Longitude = []
Latitude = []

for i, r in pohang.iterrows():
    lon, lat = getLocFromAddr(r.Address)    
    Longitude.append(lon)
    Latitude.append(lat)
    
pohang['Latitude'] = Latitude
pohang['Longitude'] = Longitude

pohang.to_excel(rootDir + '13.Pohang_Admin_v1.xlsx', sheet_name='Pohang', index=False)

admin_location = pohang[['Latitude','Longitude']]
admin_location.to_csv(rootDir + '90.Location_Admin.csv', index=False)


## 일반음식점 주위 행정기관 수 카운
pohang = pd.read_excel(rootDir + '01.Pohang_Restaurants_v5.xlsx')
admins = pd.read_csv(rootDir + '99.Location_Admin.csv')

## 위경도 사용 거리측정
from math import sin, cos, sqrt, atan2, radians

def getDistance(lat1, lon1, lat2, lon2):    
    # approximate radius of earth in km
    R = 6373.0
    
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance

RADIUS = 0.5

numAdmins = []
for i, r in pohang.iterrows():
    print(str(i) + '/' + str(len(pohang)))
    if r.X == 0.0:
        numAdmins.append(0)
        continue
    cntAdmins = 0
    for j, a in admins.iterrows():        
        dist = getDistance(r.Y, r.X, a.Latitude, a.Longitude)
        if dist <= RADIUS:
            cntAdmins = cntAdmins + 1
    numAdmins.append(cntAdmins)

pohang = pohang[['No']]
pohang['NumAdmins'] = np.array(numAdmins)

pohang.to_excel(rootDir + '13.포항 일반음식점 주변 일선행정기관 수.xlsx', index=False)