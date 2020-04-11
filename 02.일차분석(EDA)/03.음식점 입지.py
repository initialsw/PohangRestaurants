'''
제목: 포항지역 일반음식점 현황 분석(음식점 입지)
작성자: 한승욱
작성일: 2020.04.04(토)
코드내용 요약
  1. 행정동별 
  2. 토지용도별 
  3. 학교, 아파트, 일선행정기관 유무
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

## 작업 경로(rootDir)와 파일이름은 상황에 따라 변경할 것
rootDir = 'e:/research/2020/data/'
outDir = 'e:/research/2020/'
filename = '01.Pohang_Restaurants_v5.xlsx'

pohang = pd.read_excel(rootDir + filename)
pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
pohang_city['OpenYears'] = pohang_city.OpenMonths / 12

recent_close = pohang_city[pohang_city.CloseYear >= 2010]
recent_close = recent_close[recent_close.IsClosed == 1]

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'


## 1. 행정동별 최근 10년간 개업-폐업한 음식점의 영업기간 분포 
recent_close.groupby(recent_close.AdminTownName).No.count()
north = recent_close[recent_close.Dist == '북구']
north_recent = north[north.OpenYear >= 2010]
south = recent_close[recent_close.Dist == '남구']
south_recent = south[south.OpenYear >= 2010]

## 북구 음식점 
plt.rcParams['figure.figsize'] = [8, 6]
ax1 = sns.boxplot(y='AdminTownName', x='OpenYears', data=north_recent, orient='h')
plt.xlabel('영업기간(년)', fontsize=15)
plt.ylabel('음식점 메뉴', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.setp(ax1.artists, edgecolor='k', facecolor='w')
plt.setp(ax1.lines, color='k')

## 남구 음식점 
plt.rcParams['figure.figsize'] = [8, 6]
ax1 = sns.boxplot(y='AdminTownName', x='OpenYears', data=south_recent, orient='h')
plt.xlabel('영업기간(년)', fontsize=15)
plt.ylabel('음식점 메뉴', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.setp(ax1.artists, edgecolor='k', facecolor='w')
plt.setp(ax1.lines, color='k')


## 2. 토지용도에 따른 영업기간의 변화(최근 10년간 개업 후 폐업한 음식점)
filename = '16.포항 일반음식점 주변 토지용도.csv'
landvalue = pd.read_csv(rootDir + filename)
landvalue.drop('No', axis=1, inplace=True)
landvalue = pd.concat([pohang, landvalue], axis=1)
landvalue = landvalue[landvalue.AdminTownName.str[-1] == '동']
landvalue = landvalue[landvalue['2019 LandType'] != -1]
landvalue['OpenYears'] = landvalue['OpenMonths'] / 12
## 2010년 이후에 개업하고 폐업한 음식점들
recent_close = landvalue[landvalue.OpenYear >= 2010]
recent_close = recent_close[recent_close.IsClosed == 1]

ax2 = sns.boxplot(x='2019 LandType', y='OpenYears', data=recent_close,
                  order=[1,2,3,4])
plt.xlabel('토지용도', fontsize=15)
plt.ylabel('영업기간(년)', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks([0,1,2,3],['주거','상업','공업','녹지'],fontsize=15)
plt.setp(ax2.artists, edgecolor='k', facecolor='w')
plt.setp(ax2.lines, color='k')

## 3. 학교의 유무
filename = '11.포항 일반음식점 주변 학교 수.xlsx'
schools = pd.read_excel(rootDir + filename)
schools.drop('No',axis=1,inplace=True)
pohang = pd.concat([pohang, schools], axis=1)
pohang['OpenYears'] = pohang['OpenMonths']/12
pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
recent = pohang_city[pohang_city.OpenYear >= 2010]
recent_close = recent[recent.IsClosed == 1]
recent_close = recent_close[recent_close.X != 0]

ax3 = sns.boxplot(x='NumSchools', y='OpenYears', data=recent_close)
plt.xlabel('학교 수(개)', fontsize=15)
plt.ylabel('영업기간(년)', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.setp(ax3.artists, edgecolor='k', facecolor='w')
plt.setp(ax3.lines, color='k')

## 4. 일선행정기관 유무
filename = '13.포항 일반음식점 주변 일선행정기관 수.xlsx'
admins = pd.read_excel(rootDir + filename)
admins.drop('No', axis=1, inplace=True)
pohang = pd.concat([pohang, admins], axis=1)
pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
recent = pohang_city[pohang_city.OpenYear >= 2010]
recent_closed = recent[recent.IsClosed == 1]
recent_closed = recent_closed[recent_closed.X != 0]
recent_closed['hasAdmin'] = recent_closed.NumAdmins > 0

ax4 = sns.boxplot(x='NumAdmins', y='OpenYears', data=recent_closed)
ax4 = sns.boxplot(x='hasAdmin', y='OpenYears', data=recent_closed)
plt.xlabel('일선행정기관 수(개)', fontsize=15)
plt.ylabel('영업기간(년)', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.setp(ax4.artists, edgecolor='k', facecolor='w')
plt.setp(ax4.lines, color='k')

## 5. 아파트 유무
filename = '15.포항 일반음식점 주변 아파트 수, 면적.xlsx'
apts = pd.read_excel(rootDir + filename)
apts['OpenYears'] = apts['OpenMonths'] / 12

## 2010년 이후 개업한 후 폐업한 음식점이 폐업할 당시에 아파트 수를 사용
X = []   ## 아파트 수
Y = []   ## 영업기간(년)
Z = []   ## 아파트 면적

for i, r in apts.iterrows():
    if (r.OpenYear >= 2010) and (r.IsClosed == 1):
        if (r.X != 0):
            X.append(r[str(r.CloseYear) + ' NumApts'])
            Y.append(r.OpenYears)
            Z.append(r[str(r.CloseYear) + ' TotalAptArea'])

ax5 = sns.boxplot(x=X, y=Y)
plt.xlabel('아파트 단지 수(개)', fontsize=15)
plt.ylabel('영업기간(년)', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.setp(ax5.artists, edgecolor='k', facecolor='w')
plt.setp(ax5.lines, color='k')

ax6 = plt.scatter(Z, Y, s=1, color='black', marker='+')