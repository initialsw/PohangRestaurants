## 일반음식점 인허가데이터에서 포항지역 식당데이터 추출 및 가공

## Step 1. 경상북도 데이터에서 포항지역 음식점만 추출
import pandas as pd
import numpy as np

rootDir = 'D:/Research/Data/'
filename = '01.경상북도_일반음식점_201912.xlsx'
df = pd.read_excel(rootDir + filename)

## select only necessary columns
df = df[['번호', '인허가일자', '폐업일자', '소재지전체주소', 
         '도로명전체주소', '사업장명', '업태구분명', 
         '좌표정보(X)', '좌표정보(Y)', '시설총규모']]

## select restaurants in Pohang
pohang = df[df.소재지전체주소.str.contains('포항시') | 
            df.도로명전체주소.str.contains('포항시')]

## reset index and drop index column
pohang.reset_index(inplace=True)
pohang.drop('index', axis=1, inplace=True)

## rename columns
pohang.columns = ['No', 'Open', 'Close', 'Address', 'Address2',
                  'Name', 'Menu', 'X', 'Y', 'Size']

## convert float to date
pohang['Open'] = np.array(pd.to_datetime(pohang['Open'], format='%Y%m%d'))
pohang['Close'] = np.array(pd.to_datetime(pohang['Close'], format='%Y%m%d'))

import datetime

## Set close date to '2020-01-01' if the restaurant is not closed yet
pohang.loc[np.isnat(pohang.Close), 'Close'] = datetime.date(2020, 1, 1)
pohang['Close'] = pd.to_datetime(pohang['Close'], format='%Y-%m-%d %H:%M:%S')

## Remove restaurants that are closed before 2000-01-01
pohang = pohang.loc[pohang.Close > '1999-12-31']

pohang.to_excel(rootDir + '01.Pohang_Restaurants_v1.xlsx')

## Step 2. Kakao API 사용해서 위경도 얻기
## Get correct coordinates(longitude, latitude) of restaurants using Kakao API
pohang = pd.read_excel(rootDir + '01.Pohang_Restaurants_v1.xlsx')
pohang.drop('Unnamed: 0', axis=1, inplace=True)

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
        print('Cannot find the location!')
        return 0, 0

## reset index and drop index column
pohang.reset_index(inplace=True)
pohang.drop('index', axis=1, inplace=True)

for i, r in pohang.iterrows():
    lon, lat = getLocFromAddr(r.Address)
    if lon != 0:
        pohang.at[i, 'X'] = lon
        pohang.at[i, 'Y'] = lat
    elif str(r.Address2) != 'nan':
        lon, lat = getLocFromAddr(str(r.Address2))
        pohang.at[i, 'X'] = lon
        pohang.at[i, 'Y'] = lat
    else:
        pohang.at[i, 'X'] = 0
        pohang.at[i, 'Y'] = 0

## Save pre-processed dataframe to excel
pohang.to_excel(rootDir + '01.Pohang_Restaurants_v2.xlsx', sheet_name='Pohang', index=False)

## 주소 잘못된 부분 일부 수정 (우현롯트.. -> 포항시 북구 우현동 롯트...)

## Step3. 행정구역명(구, 읍/면/동 ) 얻기
pohang = pd.read_excel(rootDir + '01.Pohang_Restaurants_v2.xlsx')

lstDist = []
lstTown = []

## Add Gu and Dong(Myeon, Eup) columns
for i, r in pohang.iterrows():
    lstDist.append(r.Address.split(' ')[2])
    lstTown.append(r.Address.split(' ')[3])

dist = np.array(lstDist)
town = np.array(lstTown)

pohang['Dist'] = dist
pohang['Town'] = town

pohang.Dist.unique()
pohang.Town.unique()

## 잘못된 데이터 수정
pohang.at[10459, 'Address'] = '경상북도 포항시 북구 우현동 우현1지구토지구획정리사업지구 12블럭 5롯트 110호'
pohang.at[10459, 'Dist'] = '북구'
pohang.at[10459, 'Town'] = '우현동'

## mapping custom town name to administrative name (법정동 -> 행정동)
townMapping = { '두호동':'두호동', '득량동':'양학동', '학잠동':'양학동', '용흥동':'용흥동',
                '우현동':'우창동', '창포동':'우창동', '죽도동':'죽도동', '중앙동':'중앙동',
                '동빈1가':'중앙동', '동빈2가':'중앙동', '덕산동':'중앙동', '덕수동':'중앙동',
                '여천동':'중앙동', '상원동':'중앙동', '남빈동':'중앙동', '신흥동':'중앙동',
                '대흥동':'중앙동', '항구동':'중앙동', '대신동':'중앙동', '학산동':'중앙동',
                '장성동':'장량동', '양덕동':'장량동', '환호동':'환여동', '여남동':'환여동',
                '흥해읍':'흥해읍', '기계면':'기계면', '기북면':'기북면', '신광면':'신광면',
                '송라면':'송라면', '죽장면':'죽장면', '청하면':'청하면', '송도동':'송도동',
                '대잠동':'대이동', '이동':'대이동', '상도동':'상대동', '대도동':'상대동',
                '송내동':'제철동', '송정동':'제철동', '괴동동':'제철동', '호동':'제철동',
                '동촌동':'제철동', '장흥동':'제철동', '인덕동':'제철동', '지곡동':'효곡동',
                '청림동':'청림동', '일월동':'청림동', '해도동':'해도동', '효자동':'효곡동',
                '구룡포읍':'구룡포읍', '연일읍':'연일읍', '오천읍':'오천읍', '대송면':'대송면',
                '동해면':'동해면', '장기면':'장기면', '호미곶면':'호미곶면'}

pohang['AdminTownName'] = pohang['Town'].map(lambda x: townMapping[x])

pohang.to_excel(rootDir + '01.Pohang_Restaurants_v3.xlsx', sheet_name='Pohang', index=False)

## Step 4: 영업기간(개월), 현재 영업여부, 개업연월, 폐업연월 얻기
pohang = pd.read_excel(rootDir + '01.Pohang_Restaurants_v3.xlsx')

openMonths = []
isClosed = []

oYear = []
oMonth = []
cYear = []
cMonth = []

thisYear = datetime.datetime(2020,1,1)
lastDate = thisYear
for i, r in pohang.iterrows():        
    oYear.append(r.Open.year)
    oMonth.append(r.Open.month)
    if r.Close.year == 2020: ## not closed yet    
        lastDate = thisYear
        cYear.append(2020)
        cMonth.append(1)
    else:   ## closed...
        lastDate = r.Close        
        cYear.append(r.Close.year)
        cMonth.append(r.Close.month)
    isClosed.append(int(r.Close.year != 2020))    
    nMonths = (lastDate.year - r.Open.year) * 12 + (lastDate.month - r.Open.month)
    openMonths.append(nMonths)

pohang['OpenYear'] = np.array(oYear)
pohang['OpenMonth'] = np.array(oMonth)
pohang['CloseYear'] = np.array(cYear)
pohang['CloseMonth'] = np.array(cMonth)

pohang['OpenMonths'] = np.array(openMonths)
pohang['IsClosed'] = np.array(isClosed)

pohang.to_excel(rootDir + '01.Pohang_Restaurants_v4.xlsx',sheet_name='Pohang', index=False)

## Step 5: 메뉴와 프랜차이즈 여부 확인

franchise = pd.read_excel(rootDir + '00.프랜차이즈 목록.xlsx', converters={'영업표지':str})
franchise.columns = ['No', 'Company', 'ResName', 'Rep', 'RegCode', 'Type']
franchise.ResName = franchise.ResName.str.strip()

## Separate secondary names in parenthesis
lstFranchise = []

## Case 1: (ABC)DEF -> ABC, DEF
## Case 2: A(BC)DEF -> ADEF, DB
## Case 3: ABC(DEF) -> ABC, DEF
for i, r in franchise.iterrows():        
    t = r.ResName.split(')')
    if len(t) > 1:
        y = t[0].split('(')
        lstFranchise.append((y[0] + t[1]).lower().strip())
        #print(y[0]+t[1])
        if len(y[1]) > 1:
            lstFranchise.append(y[1].lower())
            #print(y[1])
    else:
        if len(r.ResName) > 1:
            lstFranchise.append(r.ResName.lower())
           
pohang = pd.read_excel(rootDir + '01.Pohang_Restaurants_v4.xlsx')
nTotal = len(pohang)

## '포항점', '장량점' => OK
## 예외: 전문점, 음식점, 편의점, 주점, 반점
lstException = ['전문점', '음식점', '편의점', '주점', '반점']

isFranchise = []
for i, r in pohang.iterrows():
    bFranchise = False
    tmp = tmpName = r.Name.lower()
    ## 예외 키워드를 제거 (전문점, 반점, 편의점 등)
    for e in lstException:
        tmp = tmp.replace(e, '')
    if tmp.strip()[-1] == '점':   ## check if the restaurant is a branch e.g. 포항점
        bFranchise = True
        #print(tmpName, str(bFranchise), str(i), '/', str(nTotal-1))
    else:
        for f in lstFranchise:
            if f.strip() == tmp.strip():
                #print(tmp + ' -> ' + f)
                bFranchise = True
                break
    isFranchise.append(int(bFranchise))

pohang['isFranchise'] = np.array(isFranchise)

## 메뉴 입력 (Category 칼럼으로 추가)
# 통계청 한국표준산업분류(KSIC)의 숙박 및 음식점업(56) 메뉴별 분류
## Source : http://kssc.kostat.go.kr/ksscNew_web/mobile/treeList.html

listMenu = ['한식일반','한식면류','한식육류','한식해산물',
            '중식','일식','서양식','기타외국식','패스트푸드',
            '치킨','분식','주점','카페','기타']

menu_map = { '불고기':'한식육류', '갈비':'한식육류', '식육':'한식육류', 
             '숯불':'한식육류', '삼겹':'한식육류', '한우':'한식육류', 
             '껍데기':'한식육류','고기':'한식육류', '오리':'한식육류',
             '곱창':'한식육류', '막창':'한식육류', '주물럭':'한식육류',
             '샤브':'한식육류', '보쌈':'한식육류', '족발':'한식육류',
             '고깃집':'한식육류', '축산':'한식육류', '찜닭':'한식육류',
             '닭발':'한식육류', '돼지':'한식육류',
             '복어':'한식해산물', '수산':'한식해산물', '횟집':'한식해산물',
             '가자미':'한식해산물', '회식당':'한식해산물', '대게':'한식해산물',
             '전복':'한식해산물', '조개':'한식해산물', '쭈꾸':'한식해산물', 
             '아구':'한식해산물', '복집':'한식해산물', '낙지':'한식해산물',
             '해물':'한식해산물', '생선':'한식해산물', '코다리':'한식해산물',
             '과메기':'한식해산물', '모리':'한식해산물',
             '국수':'한식면류', '밀면':'한식면류', '면옥':'한식면류',
             '냉면':'한식면류', '쫄면':'한식면류',
             '푸드':'기타', '도시락':'기타', '구내식당':'기타',
             '분식':'분식', '김밥':'분식', '떡볶이':'분식', 
             '우동':'분식', '만두':'분식',
             '반점':'중식', '짬뽕':'중식', '짜장':'중식', '탕수':'중식',
             '마라':'중식', '중국':'중식', '중식':'중식', '훠궈':'중식',         
             '일식':'일식', '초밥':'일식', '수사':'일식', 
             '참치':'일식', '스시':'일식', '라멘':'일식',         
             '치킨':'치킨', '통닭':'치킨', '닭강정':'치킨',
             '비에치씨':'치킨', 'BHC':'치킨', '또래오래':'치킨',
             '푸라닭':'치킨', '멕시카':'치킨', '페리카':'치킨', 
             '처갓집':'치킨',         
             '피자':'패스트푸드', '버거':'패스트푸드', '롯데리아':'패스트푸드',
             'KFC':'패스트푸드', '맘스터치':'패스트푸드', '맥도날드':'패스트푸드',         
             '레스토랑':'서양식', '돈까스':'서양식', '아웃백':'서양식',
             '카페':'카페', '주점':'주점', '커피':'카페', '다방':'카페',
             '비어':'주점', '호프':'주점', '소주':'주점', '간이역':'주점',
             '주막':'주점', '투다리':'주점', '포차':'주점', '막걸리':'주점',         
             '구내식당':'기타', '기사식당':'기타', '부페':'기타', '뷔페':'기타',                  
             '쌀국수':'기타외국식', '타이':'기타외국식', '아시아':'기타외국식',
             '추어':'한식일반', '매운탕':'한식일반', '찌게':'한식일반', 
             '찌개':'한식일반', '순대':'한식일반', '백반':'한식일반', '해장':'한식일반',       
             '고디':'한식일반', '장어':'한식일반', '국밥':'한식일반', 
             '곰탕':'한식일반', '감자':'한식일반', '빈대떡':'한식일반',
             '두부':'한식일반', '정식':'한식일반', '육개장':'한식일반',
             '식당':'한식일반', '밥':'한식일반', '탕':'한식일반', 
             '탕':'한식일반', '회':'한식해산물', '빵':'기타',
             '한식':'한식일반', '까페':'카페', '호프/통닭':'주점',
             '식육(숯불구이)':'한식육류', '경양식':'서양식', '통닭(치킨)':'치킨',
             '정종/대포집/소주방':'주점', '전통찻집':'카페', '회집':'한식해산물',
             '뷔페식':'기타', '감성주점':'주점', '탕류(보신용)':'한식일반',
             '출장조리':'기타', '패밀리레스토랑':'서양식', '복어취급':'한식해산물',
             '패밀리레스트랑':'서양식', '파스타':'서양식', 
             '김밥(도시락)':'기타', '외국음식전문점(인도,태국등)':'기타외국식',
             '냉면집':'한식면류', '키즈카페':'카페', '라이브카페':'카페', 
             '중국식':'중식' }

category = []
for i, r in pohang.iterrows():
    bFound = False
    for t in menu_map.keys():
        if t in r.Name:
            category.append(menu_map[t])
            #print(r.Name + ' ' + menu_map[t])
            bFound = True
            break
    if not bFound:      
        if r.Menu.strip() in menu_map.keys():
            category.append(menu_map[r.Menu.strip()])
            #print(r.Name + ' ' + menu_map[r.Menu])
        else:            
            category.append(r.Menu)
            #print(r.Name + ' ' + r.Menu)
        
pohang['Category'] = np.array(category)

pohang.to_excel(rootDir + '01.Pohang_Restaurants_v5.xlsx', sheet_name='Pohang', index=False)