## 공시지가 데이터

import pandas as pd
import numpy as np

rootDir = 'd:/research/data/공시지가/'
filename = ' LandValue.csv'

##year = ['2014','2015','2017','2018','2019']
##enc = ['cp949','cp949','cp949','cp949','cp949']

year = ['2009','2010']
enc = ['utf-8','utf-8']

for i in range(0, len(year)):
    landvalue = pd.read_csv(rootDir + year[i] + filename, encoding=enc[i], error_bad_lines=False)    
    landvalue = landvalue[['일련번호','시도명','시군구명','소재지','면적','용도지역1','이용상황','주위환경','공시지가']]
    landvalue.columns = ['No','Province','City','Town','Area','Usage','Status','Surroundings','LandValue']
    
    pohang = landvalue[landvalue.City.str.contains('포항', na=False)]
    pohang.reset_index(inplace=True)
    pohang.drop('index', axis=1, inplace=True)
    
    pohang.to_excel(rootDir + '40.' + year[i] + '_LandValue_Prep.xlsx', sheet_name='Pohang', index=False)
    

## 연도별로 작업 (연도마다 칼럼이 조금씩 다름)
    
## 2011년 일부 데이터 칼럼이 18개고 칼럼이름이 다름(시도명->시도, 시군구명->시군구)
landvalue = pd.read_csv(rootDir + '2011' + filename, encoding='cp949', error_bad_lines=False)
landvalue = landvalue[['일련번호','시도','시군구','소재지','면적','용도지역1','이용상황','주위환경','공시지가(단위:원)']]
landvalue.columns = ['No','Province','City','Town','Area','Usage','Status','Surroundings','LandValue']

pohang = landvalue[landvalue.City.str.contains('포항', na=False)]
pohang.reset_index(inplace=True)
pohang.drop('index', axis=1, inplace=True)

pohang.to_excel(rootDir + '40.2011' + '_LandValue_Prep.xlsx', sheet_name='Pohang', index=False)

## 2012년 구분자가 탭(\t)임
landvalue = pd.read_csv(rootDir + '2012' + filename, encoding='cp949', error_bad_lines=False, sep='\t')
landvalue = landvalue[['일련번호','시도명','시군구명','소재지','면적','용도지역1','이용상황','주위환경','공시지가']]
landvalue.columns = ['No','Province','City','Town','Area','Usage','Status','Surroundings','LandValue']

pohang = landvalue[landvalue.City.str.contains('포항', na=False)]
pohang.reset_index(inplace=True)
pohang.drop('index', axis=1, inplace=True)

pohang.to_excel(rootDir + '40.2012' + '_LandValue_Prep.xlsx', sheet_name='Pohang', index=False)


## 2013년 
landvalue = pd.read_csv(rootDir + '2013' + filename, encoding='utf-8', error_bad_lines=False)
landvalue = landvalue[['일련번호','시도명','시군구명','소재지','면적','용도지역1','이용상황','주위환경','공시지가']]
landvalue.columns = ['No','Province','City','Town','Area','Usage','Status','Surroundings','LandValue']

pohang = landvalue[landvalue.City.str.contains('포항', na=False)]
pohang.reset_index(inplace=True)
pohang.drop('index', axis=1, inplace=True)

pohang.to_excel(rootDir + '40.2013' + '_LandValue_Prep.xlsx', sheet_name='Pohang', index=False)


## 2016년도 데이터는 다르게 처리해야함...
import pandas as pd
import numpy as np

rootDir = 'd:/research/data/공시지가/'
filename = ' LandValue.csv'

year = '2016'
enc = 'cp949'

landvalue = pd.read_csv(rootDir + year + filename, encoding=enc)
landvalue = landvalue[['일련번호','시도','시군구.1','읍면','동리','본번지','부번지','면적','용도지역','이용상황','주위환경','공시지가']]
landvalue.columns = ['No','Province','City','Town1','Town2','Addr1','Addr2','Area','Usage','Status','Surroundings','LandValue']

pohang = landvalue[landvalue.City.str.contains('포항', na=False)]
pohang.reset_index(inplace=True)
pohang.drop('index', axis=1, inplace=True)

town = []

for i, r in pohang.iterrows():
    if str(r.Town1).lower() == 'nan':
        tmpTown = str(r.Town2)
    else:
        tmpTown = str(r.Town1) + ' ' + str(r.Town2)
    tmpTown = tmpTown + ' ' + str(r.Addr1)
    if str(r.Addr2) != '0':
        tmpTown = tmpTown + '-' + str(r.Addr2)
    print(tmpTown)
    town.append(tmpTown)

pohang['Town'] = np.array(town)
pohang = pohang[['No','Province','City','Town','Area','Usage','Status','Surroundings','LandValue']]

pohang.to_excel(rootDir + '40.' + year + '_LandValue_Prep.xlsx', sheet_name='Pohang', index=False)


## 나머지 연도 (2014, 2015, 2017, 2018, 2019)

year = ['2014','2015','2017','2018','2019']
enc = ['utf-8','utf-8','cp949','cp949','cp949']

for i in range(0, len(year)):
    landvalue = pd.read_csv(rootDir + year[i] + filename, encoding=enc[i], error_bad_lines=False)    
    landvalue = landvalue[['일련번호','시도명','시군구명','소재지','면적','용도지역1','이용상황','주위환경','공시지가']]
    landvalue.columns = ['No','Province','City','Town','Area','Usage','Status','Surroundings','LandValue']
    
    pohang = landvalue[landvalue.City.str.contains('포항', na=False)]
    pohang.reset_index(inplace=True)
    pohang.drop('index', axis=1, inplace=True)
    
    pohang.to_excel(rootDir + '40.' + year[i] + '_LandValue_Prep.xlsx', sheet_name='Pohang', index=False)



## 포항만 추출한 공시지가 데이터 읽어서 좌표입력
import pandas as pd
import numpy as np
    
rootDir = 'd:/research/data/공시지가/'
filename = '_Landvalue_Prep.xlsx'
year = ['2009', '2010', '2011', '2012', '2013', 
        '2014', '2015', '2016', '2017', '2018',
        '2019']

REST_KEY = '6bd6718879c207eda2ad2a53484e5c9f'

import requests
import json

def getLocFromAddr(address):
    url="https://dapi.kakao.com/v2/local/search/address.json" 
    queryString={"query":address}
    header={"authorization": "KakaoAK " + REST_KEY}
    #print(address)
    r = requests.get(url, headers=header, params=queryString)
    t = json.loads(r.text)
    
    try:
        longitude = t['documents'][0]['address']['x']
        latitude = t['documents'][0]['address']['y']
        #print(str(longitude) + 'E', str(latitude) + 'N')
        return longitude, latitude
    except:
        return 0, 0

## 위도, 경도를 추가해서 다시 저장
for y in year:
    pohang = pd.read_excel(rootDir + '40.' + y + filename)
    ##pohang.drop('Unnamed: 0', axis=1, inplace=True)
    
    address = []
    latitude = []
    longitude = []    
    for i, r in pohang.iterrows():
        tmpAddr = '경상북도 포항시 '
        if r.City.strip() == '포항남구':
            tmpAddr = tmpAddr + '남구 '
        else:
            tmpAddr = tmpAddr + '북구 '        
        tmpAddr = tmpAddr + r.Town.strip()
        address.append(tmpAddr)
        lon, lat = getLocFromAddr(tmpAddr)        
        longitude.append(lon)
        latitude.append(lat)
    pohang['Address'] = np.array(address)
    pohang['Latitude'] = np.array(latitude)
    pohang['Longitude'] = np.array(longitude)
    
    pohang.to_excel(rootDir.replace('공시지가/','') + '41.' + y + '_LandValue_v1.xlsx', sheet_name='Pohang',index=False)