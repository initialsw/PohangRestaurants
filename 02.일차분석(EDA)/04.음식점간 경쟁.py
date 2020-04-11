'''
제목: 포항지역 일반음식점 현황 분석(음식점간 경쟁요소)
작성자: 한승욱
작성일: 2020.04.04(토)
코드내용 요약
  1. 주위 음식점 수에 따른 영업기간의 변화
  2. 주위 개업 음식점 수에 따른 영업기간의 변화
  3. 주위 폐업 음식점 수에 따른 영업기간의 변화
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import statsmodels.api as sm


## 작업 경로(rootDir)와 파일이름은 상황에 따라 변경할 것
rootDir = 'e:/research/2020/data/'
outDir = 'e:/research/2020/'

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'


## 1. 주위 음식점 수 (폐업한 연도 기준)
filename = '01.Pohang_Restaurants_v5.xlsx'
pohang = pd.read_excel(rootDir + filename)

filename = '99.NearbyRestaurants.csv'
nearby = pd.read_csv(rootDir + filename)
nearby.drop(['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Menu','Latitude','Longitude'],axis=1, inplace=True)
pohang = pd.concat([pohang, nearby], axis=1)

pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
pohang_city['OpenYears'] = pohang_city.OpenMonths / 12
recent = pohang_city[pohang_city.OpenYear >= 2010]
recent = recent[recent.IsClosed == 1]
## 위치정보 없는 음식점 제외
recent = recent[recent.X != 0]

X = []  ## 폐업한 연도 주위 음식점 수
Y = []  ## 영업기간

for i, r in recent.iterrows():   
    if (r.OpenYear <= 2000) or (r.CloseYear <= 2000):
        continue
    t = r[str(r.CloseYear-1)]
    if t > 0:
        X.append(t)
        Y.append(r.OpenYears)
        
X = pd.DataFrame(X)
X.rename({0:'음식점 수(개)'}, axis=1, inplace=True)
Y = pd.DataFrame(Y)
Y.rename({0:'영업기간(년)'}, axis=1, inplace=True)
tmp = pd.concat([X, Y], axis=1)

rc={'axes.labelsize': 15, 'font.size': 15, 'legend.fontsize': 15.0, \
    'axes.titlesize': 15, 'figure.figsize':[7,5]}
plt.rcParams.update(**rc)
plt.xlim([-50, 650])
plt.ylim([-1,11])
sns.kdeplot(tmp['음식점 수(개)'], tmp['영업기간(년)'], cmap="Blues", shade=True)

## 1-1. 주위 음식점 수, 같은 메뉴
filename = '99.NearbyRestaurantsSameMenu.csv'
nearbySameMenu = pd.read_csv(rootDir + filename)

filename = '01.Pohang_Restaurants_v5.xlsx'
pohang = pd.read_excel(rootDir + filename)

nearbySameMenu.drop(['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Menu','Latitude','Longitude'],axis=1, inplace=True)
pohang = pd.concat([pohang, nearbySameMenu], axis=1)

pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
pohang_city['OpenYears'] = pohang_city.OpenMonths / 12
recent = pohang_city[pohang_city.OpenYear >= 2010]
recent = recent[recent.IsClosed == 1]
## 위치정보 없는 음식점 제외
recent = recent[recent.X != 0]

#plt.scatter(x=X, y=Y, s=3, color='black', marker='o', alpha=0.1)

X = []  ## 폐업한 연도 주위 음식점 수
Y = []  ## 영업기간

for i, r in recent.iterrows():   
    if (r.OpenYear <= 2000) or (r.CloseYear <= 2000):
        continue
    t = r[str(r.CloseYear-1)]
    if t > 0:
        X.append(t)
        Y.append(r.OpenYears)
        
X = pd.DataFrame(X)
X.rename({0:'음식점 수(개)'}, axis=1, inplace=True)
Y = pd.DataFrame(Y)
Y.rename({0:'영업기간(년)'}, axis=1, inplace=True)
tmp = pd.concat([X, Y], axis=1)

rc={'axes.labelsize': 15, 'font.size': 15, 'legend.fontsize': 15.0, \
    'axes.titlesize': 15, 'figure.figsize':[7,5]}
plt.rcParams.update(**rc)
plt.xlim([-50, 650])
plt.ylim([-1,11])
sns.kdeplot(tmp['음식점 수(개)'], tmp['영업기간(년)'], cmap="Blues", shade=True)




## 2. 주위 개업 음식점 수
filename = '99.NearbyNewRestaurants.csv'
nearbyOpen = pd.read_csv(rootDir + filename)

filename = '01.Pohang_Restaurants_v5.xlsx'
pohang = pd.read_excel(rootDir + filename)

nearbyOpen.drop(['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Menu','Latitude','Longitude'],axis=1, inplace=True)
pohang = pd.concat([pohang, nearbyOpen], axis=1)

pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
pohang_city['OpenYears'] = pohang_city.OpenMonths / 12
recent = pohang_city[pohang_city.OpenYear >= 2010]
recent = recent[recent.IsClosed == 1]
## 위치정보 없는 음식점 제외
recent = recent[recent.X != 0]

X = []  ## 폐업한 연도 주위 개업한 음식점 수
Y = []  ## 영업기간

for i, r in recent.iterrows():   
    if (r.OpenYear <= 2000) or (r.CloseYear <= 2000):
        continue
    t = r[str(r.CloseYear-1)]
    if t > 0:
        X.append(t)
        Y.append(r.OpenYears)
        
X = pd.DataFrame(X)
X.rename({0:'음식점 수(개)'}, axis=1, inplace=True)
Y = pd.DataFrame(Y)
Y.rename({0:'영업기간(년)'}, axis=1, inplace=True)
tmp = pd.concat([X, Y], axis=1)

rc={'axes.labelsize': 15, 'font.size': 15, 'legend.fontsize': 15.0, \
    'axes.titlesize': 15, 'figure.figsize':[7,5]}
plt.rcParams.update(**rc)
sns.kdeplot(tmp['음식점 수(개)'], tmp['영업기간(년)'], cmap="Blues", shade=True)



## 2-1. 주위 동일메뉴 개업 음식점 수
filename = '99.NearbyNewRestaurantsSameMenu.csv'
nearbyOpenSameMenu = pd.read_csv(rootDir + filename)

filename = '01.Pohang_Restaurants_v5.xlsx'
pohang = pd.read_excel(rootDir + filename)

nearbyOpenSameMenu.drop(['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Menu','Latitude','Longitude'],axis=1, inplace=True)
pohang = pd.concat([pohang, nearbyOpenSameMenu], axis=1)

pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
pohang_city['OpenYears'] = pohang_city.OpenMonths / 12
recent = pohang_city[pohang_city.OpenYear >= 2010]
recent = recent[recent.IsClosed == 1]
## 위치정보 없는 음식점 제외
recent = recent[recent.X != 0]

X = []  ## 폐업한 연도 주위 동일메뉴이면서 개업한 음식점 수
Y = []  ## 영업기간

for i, r in recent.iterrows():   
    if (r.OpenYear <= 2000) or (r.CloseYear <= 2000):
        continue
    t = r[str(r.CloseYear-1)]
    if t > 0:
        X.append(t)
        Y.append(r.OpenYears)
        
X = pd.DataFrame(X)
X.rename({0:'음식점 수(개)'}, axis=1, inplace=True)
Y = pd.DataFrame(Y)
Y.rename({0:'영업기간(년)'}, axis=1, inplace=True)
tmp = pd.concat([X, Y], axis=1)

rc={'axes.labelsize': 15, 'font.size': 15, 'legend.fontsize': 15.0, \
    'axes.titlesize': 15, 'figure.figsize':[7,5]}
plt.rcParams.update(**rc)
sns.kdeplot(tmp['음식점 수(개)'], tmp['영업기간(년)'], cmap="Blues", shade=True)


## 3. 주위 폐업 음식점 수
filename = '99.NearbyClosedRestaurants.csv'
nearbyClosed = pd.read_csv(rootDir + filename)

filename = '01.Pohang_Restaurants_v5.xlsx'
pohang = pd.read_excel(rootDir + filename)

nearbyClosed.drop(['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Menu','Latitude','Longitude'],axis=1, inplace=True)
pohang = pd.concat([pohang, nearbyClosed], axis=1)

pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
pohang_city['OpenYears'] = pohang_city.OpenMonths / 12
recent = pohang_city[pohang_city.OpenYear >= 2010]
recent = recent[recent.IsClosed == 1]
## 위치정보 없는 음식점 제외
recent = recent[recent.X != 0]

X = []  ## 폐업한 연도 주위 동일메뉴이면서 개업한 음식점 수
Y = []  ## 영업기간

for i, r in recent.iterrows():   
    if (r.OpenYear <= 2000) or (r.CloseYear <= 2000):
        continue
    t = r[str(r.CloseYear-1)]
    if t > 0:
        X.append(t)
        Y.append(r.OpenYears)
        
X = pd.DataFrame(X)
X.rename({0:'음식점 수(개)'}, axis=1, inplace=True)
Y = pd.DataFrame(Y)
Y.rename({0:'영업기간(년)'}, axis=1, inplace=True)
tmp = pd.concat([X, Y], axis=1)

rc={'axes.labelsize': 15, 'font.size': 15, 'legend.fontsize': 15.0, \
    'axes.titlesize': 15, 'figure.figsize':[7,5]}
plt.rcParams.update(**rc)
sns.kdeplot(tmp['음식점 수(개)'], tmp['영업기간(년)'], cmap="Blues", shade=True)



## 3-1. 주위 폐업 동일메뉴 음식점 수
filename = '99.NearbyClosedRestaurantsSameMenu.csv'
nearbyClosedSameMenu = pd.read_csv(rootDir + filename)

filename = '01.Pohang_Restaurants_v5.xlsx'
pohang = pd.read_excel(rootDir + filename)

nearbyClosedSameMenu.drop(['No','OpenYear','OpenMonth','CloseYear','CloseMonth','Menu','Latitude','Longitude'],axis=1, inplace=True)
pohang = pd.concat([pohang, nearbyClosedSameMenu], axis=1)

pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
pohang_city['OpenYears'] = pohang_city.OpenMonths / 12
recent = pohang_city[pohang_city.OpenYear >= 2010]
recent = recent[recent.IsClosed == 1]
## 위치정보 없는 음식점 제외
recent = recent[recent.X != 0]

X = []  ## 폐업한 연도 주위 동일메뉴이면서 개업한 음식점 수
Y = []  ## 영업기간

for i, r in recent.iterrows():   
    if (r.OpenYear <= 2000) or (r.CloseYear <= 2000):
        continue
    t = r[str(r.CloseYear-1)]
    if t > 0:
        X.append(t)
        Y.append(r.OpenYears)
        
X = pd.DataFrame(X)
X.rename({0:'음식점 수(개)'}, axis=1, inplace=True)
Y = pd.DataFrame(Y)
Y.rename({0:'영업기간(년)'}, axis=1, inplace=True)
tmp = pd.concat([X, Y], axis=1)

rc={'axes.labelsize': 15, 'font.size': 15, 'legend.fontsize': 15.0, \
    'axes.titlesize': 15, 'figure.figsize':[7,5]}
plt.rcParams.update(**rc)
sns.kdeplot(tmp['음식점 수(개)'], tmp['영업기간(년)'], cmap="Blues", shade=True)
