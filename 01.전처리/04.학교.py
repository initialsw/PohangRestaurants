## 전국 학교 데이터에서 포항시에 위치한 학교의 좌표값만 추출
import pandas as pd
import numpy as np

rootDir = rootFolder = 'd:/research/data/'
filename = '11.전국_학교.csv'

school = pd.read_csv(rootFolder + filename, encoding='euc-kr')
filtered = school[['학교명','학교급구분','소재지지번주소','소재지도로명주소',
                   '위도','경도']]
filtered.columns = ['School','Type','Address','Address2','Latitude','Longitude']

pohang = filtered[filtered.Address.str.find('포항') != -1]
pohang.reset_index(inplace=True)
pohang.drop('index', axis=1, inplace=True)

pohang.to_excel(rootFolder + '11.Pohang_School_v1.xlsx', sheet_name='Pohang', index=False)

## 대학교 5개(포항공대, 한동대, 포항대, 선린대, 폴리텍) 수작업으로 추가

## 일반음식점 주위 반경 500m내 학교 수를 카운트
pohang = pd.read_excel(rootDir + '01.Pohang_Restaurants_v5.xlsx')
schools = pd.read_csv(rootDir + '99.Location_Schools.csv')

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

numSchools = []
for i, r in pohang.iterrows():
    print(str(i) + '/' + str(len(pohang)))
    if r.X == 0.0:
        numSchools.append(0)
        continue
    cntSchools = 0
    for j, s in schools.iterrows():        
        dist = getDistance(r.Y, r.X, s.Latitude, s.Longitude)
        if dist <= RADIUS:
            cntSchools = cntSchools + 1
    numSchools.append(cntSchools)

pohang = pohang[['No']]
pohang['NumSchools'] = np.array(numSchools)

pohang.to_excel(rootDir + '11.포항 일반음식점 주변 학교 수.xlsx', index=False)