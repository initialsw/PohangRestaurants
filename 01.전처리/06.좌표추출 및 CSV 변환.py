## 위치 좌표만 뽑아내기
import pandas as pd
import numpy as np

rootDir = 'd:/research/data/'

## 일반음식점
filename = '01.Pohang_Restaurants_v5.xlsx'
outFilename = '99.Location_Restaurants.csv'

pohang = pd.read_excel(rootDir + filename)
location = pohang[['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Category','Y','X']]

category_map = {'한식일반':1,'한식면류':2,'한식육류':3,'한식해산물':4,
               '중식':5,'일식':6,'서양식':7,'기타외국식':8,'패스트푸드':9,
               '치킨':10,'분식':11,'주점':12,'카페':13,'기타':14}
menu = []
for i, r in location.iterrows():
    menu.append(category_map[r.Category])
location['Menu'] = menu
location = location[['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Menu','Y','X']]
location.columns = ['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Menu','Latitude','Longitude']
location.reset_index(inplace=True)
location.drop('index',axis=1,inplace=True)

location.to_csv(rootDir + outFilename, encoding='euc-kr', index=False)

## 편의점
filename = '02.Pohang_ConvenientStores_v1.xlsx'
outFilename = '99.Location_ConvenientStores.csv'

pohang = pd.read_excel(rootDir + filename)
openMonth = []
closeMonth = []
openYear = []
closeYear = []

for i, r in pohang.iterrows():
    openMonth.append(r.Open.month)
    closeMonth.append(r.Close.month)
    openYear.append(r.Open.year)
    closeYear.append(r.Close.year)

pohang['OpenYear'] = np.array(openYear)
pohang['OpenMonth'] = np.array(openMonth)
pohang['CloseYear'] = np.array(closeYear)
pohang['CloseMonth'] = np.array(closeMonth)

location = pohang[['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Y','X']]
location.columns = ['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Latitude','Longitude']
location.to_csv(rootDir + outFilename, encoding='euc-kr', index=False)

## 학교
filename = '11.Pohang_School_v1.xlsx'
outFilename = '99.Location_Schools.csv'

pohang = pd.read_excel(rootDir + filename)
school_type = []
map_type = { '초등학교':1, '중학교':2, '고등학교':3, '대학교':4 }
for i, r in pohang.iterrows():
    school_type.append(map_type[r.Type])
pohang['Type1'] = school_type
location = pohang[['Type1','Latitude','Longitude']]
location.columns = ['Type', 'Latitude', 'Longitude']
location.to_csv(rootDir + outFilename, encoding='euc-kr',index=False)

## 행정기관
filename = '13.Pohang_Admin_v1.xlsx'
outFilename = '99.Location_Admin.csv'

pohang = pd.read_excel(rootDir + filename)
location = pohang[['Latitude','Longitude']]
location.to_csv(rootDir + outFilename, encoding='euc-kr',index=False)

## 공시지가 좌표 추출
rootDir = 'd:/research/data/'

## 토지용도
## 주거지역(1): 제1종일반주거지역, 제2종일반주거지역, 제3종일반주거지역, 준주거지역
## 상업지역(2): 일반상업지역
## 공업지역(3): 일반공업지역, 준공업지역, 전용공업지역
## 녹지(4): 자연녹지지역, 보전녹지지역, 생산녹지지역, 자연환경보전지역
## 관리지역(5): 계획관리지역, 생산관리지역, 보전관리지역, 관리지역
## 농림지역(6): 농림지역
usageMap = {'제1종일반주거지역':1, '제2종일반주거지역':1, '제3종일반주거지역':1, '준주거지역':1,
            '1종일주':1, '2종일주':1, '3종일주':1, '준주거':1, 
            '일반상업지역':2, 
            '일반상업':2, 
            '일반공업지역':3,'준공업지역':3, '전용공업지역':3, 
            '일반공업':3, '준공업':3, '전용공업':3,
            '자연녹지지역':4, '보전녹지지역':4, '생산녹지지역':4, '자연환경보전지역':4,
            '자연녹지':4, '보전녹지':4, '생산녹지':4, '자연환경':4, 
            '계획관리지역':5, '생산관리지역':5, '보전관리지역':5,
            '계획관리':5, '생산관리':5, '보전관리':5, '관리지역':5, '농림지역':6 }

for y in range(2010,2020):
    filename = '41.' + str(y) + '_LandValue_v1.xlsx'
    outFilename = '42.' + str(y) + '_LandValue.csv'
    landvalue = pd.read_excel(rootDir + filename)
    
    landvalue['LandType'] = landvalue['Usage'].map(lambda x: usageMap[x])
    landvalue = landvalue[['Latitude','Longitude','LandType','Area','LandValue']]
    landvalue.to_csv(rootDir + outFilename, index=False)

