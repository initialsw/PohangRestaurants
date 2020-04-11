'''
제목: 포항지역 일반음식점 현황 분석(지역경제상황)
작성자: 한승욱
작성일: 2020.04.06(월)
코드내용 요약
  1. POSCO 조강생산량과 개업/폐업 음식점 수
  2. 철강산단 생산량과 개업/폐업 음식점 수
  3. 수출액/수입앱과 개업/폐업 음식점 수
  4. 유통업체 판매액과 개업/폐업 음식점 수
  5. BSI(제조업/비제조업)와 개업/폐업 음식점 수
  6. 아파트 매매 건수와 개업/폐업 음식점 수
  7. 아파트 매매가 지수와 개업/폐업 음식점 수
'''

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt 
import seaborn as sns

rootDir = 'd:/research/data/'
filename = '01.Pohang_Restaurants_v5.xlsx'

pohang = pd.read_excel(rootDir + filename)
pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
pohang_city['OpenYears'] = pohang_city.OpenMonths / 12
pohang_city_open = pohang_city[pohang_city.IsClosed == 0]

region = pd.read_excel(rootDir + '14.실물경제통계.xlsx')
region.set_index(region.Year, inplace=True)
region.drop('Year', axis=1, inplace=True)

## 연도별 영업한 음식점 수
nRest = []
for y in range(2010, 2020):
    nRest.append(0)

for i, r in pohang_city.iterrows():
    if r.CloseYear < 2010:
        continue
    yOpen = max(2010, r.OpenYear)
    yClose = min(r.CloseYear, 2019)
    for y in range(yOpen, yClose+1):
        nRest[y-2010] += 1

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'

#region_monthly = pd.read_excel(rootDir + '14-1.실물경제데이터(월별).xlsx')
#region_monthly.set_index([region_monthly.Year, region_monthly.Month], inplace=True)
#region_monthly.drop('Year', axis=1, inplace=True)
#region_monthly.drop('Month', axis=1, inplace=True)

## 1. POSCO 조강생산량(백만톤)
tmp = { }
tmp['POSCO'] = region.POSCO / 1000
tmp['영업중'] = np.array(nRest) / 1000
#tmp['POSCO'] = region.POSCO.diff().loc[2011:2019]
tmp['개업'] = pohang_city.groupby(pohang_city.OpenYear).No.count().loc[2010:2019]
tmp['폐업'] = pohang_city.groupby(pohang_city.CloseYear).No.count().loc[2010:2019]
tmpdf = pd.DataFrame(tmp)

plt.scatter('POSCO', '영업중', s=30, c='blue', marker='s', linewidth=1, data=tmpdf)
#plt.scatter('POSCO', '개업', s=30, c='blue', marker='o', linewidth=1, data=tmpdf)
#plt.scatter('POSCO', '폐업', s=30, c='red', marker='x', linewidth=1, data=tmpdf)
#plt.legend(loc='upper left', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('음식점 수(천개)',fontsize=15)
plt.xlabel('POSCO 연간 조강생산량(백만톤)',fontsize=15)

## 2. 철강산단 생산액(억원)
tmp = {}
tmp['Steel'] = region.SteelProd/1000
tmp['영업중'] = np.array(nRest)/1000
tmpdf = pd.DataFrame(tmp)

plt.scatter('Steel', '영업중', s=30, c='black', marker='s', linewidth=1, data=tmpdf)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('음식점 수(천개)',fontsize=15)
plt.xlabel('철강산단 생산액(천억원)',fontsize=15)


## 3. 수출액/수입액
## 3-1. 수출액(백만불)
tmp = {}
tmp['Export'] = region.Export/100000
tmp['영업중'] = np.array(nRest)/1000
tmpdf = pd.DataFrame(tmp)

plt.scatter('Export', '영업중', s=30, c='black', marker='s', linewidth=1, data=tmpdf)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('음식점 수(천개)',fontsize=15)
plt.xlabel('포항지역 수출액(억불)',fontsize=15)


## 3-2. 수입액
tmp = {}
tmp['Import'] = region.Import/100000
tmp['영업중'] = np.array(nRest)/1000
tmpdf = pd.DataFrame(tmp)

plt.scatter('Import', '영업중', s=30, c='black', marker='s', linewidth=1, data=tmpdf)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('음식점 수(천개)',fontsize=15)
plt.xlabel('포항지역 수입액(억불)',fontsize=15)


## 3-3. 수출-수입액과 영업중인 음식점 수
tmp = {}
tmp['수입'] = region.Import/100000
tmp['수출'] = region.Export/100000
tmp['수출액'] = np.array(nRest)/1000
tmp['수입액'] = np.array(nRest)/1000
tmpdf = pd.DataFrame(tmp)

plt.scatter('수출','수출액', s=50, c='blue', marker='o', linewidth=1, data=tmpdf)
plt.scatter('수입','수입액', s=50, c='red', marker='x', linewidth=1, data=tmpdf)
plt.legend(loc='upper right', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim([50,150])
plt.xlabel('포항지역 수출입액(억불)',fontsize=15)
plt.ylabel('음식점 수(천개)',fontsize=15)


## 4. 유통판매액(십억원)
tmp = {}
tmp['판매'] = region.Sales.diff()/1000
tmp['영업'] = np.array(nRest)/1000
tmp['개업'] = pohang_city.groupby(pohang_city.OpenYear).No.count().loc[2010:2019]
tmp['폐업'] = pohang_city.groupby(pohang_city.CloseYear).No.count().loc[2010:2019]
tmpdf = pd.DataFrame(tmp)

plt.scatter('판매', '영업', s=50, c='black', marker='s', linewidth=1, data=tmpdf)
plt.scatter('판매', '개업', s=50, c='blue', marker='o', linewidth=1, data=tmpdf)
plt.scatter('판매', '폐업', s=50, c='red', marker='x', linewidth=1, data=tmpdf)
plt.legend(loc='upper right', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel('포항지역 유통업체 판매액 변화(십억원)',fontsize=15)
plt.ylabel('음식점 수(개)',fontsize=15)



## 5. BSI(제조업/비제조업)
## 5-1. BSI 제조업
tmp = {}
tmp['BSI'] = region.BSI_Manufacture
tmp['영업'] = np.array(nRest)/1000
tmp['개업'] = pohang_city.groupby(pohang_city.OpenYear).No.count().loc[2010:2019]
tmp['폐업'] = pohang_city.groupby(pohang_city.CloseYear).No.count().loc[2010:2019]
tmpdf = pd.DataFrame(tmp)

plt.scatter('BSI', '영업', s=50, c='black', marker='s', linewidth=1, data=tmpdf)
plt.scatter('BSI', '개업', s=50, c='blue', marker='o', linewidth=1, data=tmpdf)
plt.scatter('BSI', '폐업', s=50, c='red', marker='x', linewidth=1, data=tmpdf)
plt.legend(loc='upper right', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylim([100,600])
plt.xlabel('제조업BSI',fontsize=15)
plt.ylabel('음식점 수(개)',fontsize=15)


## 5-2. BSI 비제조업
tmp = {}
tmp['BSI'] = region.BSI_Service
tmp['영업'] = np.array(nRest)/1000
tmp['개업'] = pohang_city.groupby(pohang_city.OpenYear).No.count().loc[2010:2019]
tmp['폐업'] = pohang_city.groupby(pohang_city.CloseYear).No.count().loc[2010:2019]
tmpdf = pd.DataFrame(tmp)

#plt.scatter('BSI', '영업', s=50, c='black', marker='s', linewidth=1, data=tmpdf)
plt.scatter('BSI', '개업', s=50, c='blue', marker='o', linewidth=1, data=tmpdf)
plt.scatter('BSI', '폐업', s=50, c='red', marker='x', linewidth=1, data=tmpdf)
plt.legend(loc='upper right', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylim([100,600])
plt.xlabel('비제조업BSI',fontsize=15)
plt.ylabel('음식점 수(개)',fontsize=15)


## 6. 아파트 매매 건수
X = region.AptSalesCnt
Y = pohang_city.groupby(pohang_city.OpenYear).No.count().loc[2010:2019]
Z = pohang_city.groupby(pohang_city.CloseYear).No.count().loc[2010:2019]

plt.scatter(X, Y, s=20, c='red', marker='x', linewidth=0.5)
plt.scatter(X, Z, s=20, c='blue', marker='o', linewidth=0.5)
plt.ylim([0, 600])


## 7. 아파트 매매가 지수
tmp = {}
tmp['매매가'] = region.AptPriceIndex
tmp['영업'] = np.array(nRest)/1000
tmp['개업'] = pohang_city.groupby(pohang_city.OpenYear).No.count().loc[2010:2019]
tmp['폐업'] = pohang_city.groupby(pohang_city.CloseYear).No.count().loc[2010:2019]
tmpdf = pd.DataFrame(tmp)

plt.scatter('매매가', '영업', s=50, c='black', marker='s', linewidth=1, data=tmpdf)
plt.scatter('매매가', '개업', s=50, c='blue', marker='o', linewidth=1, data=tmpdf)
plt.scatter('매매가', '폐업', s=50, c='red', marker='x', linewidth=1, data=tmpdf)
plt.legend(loc='upper right', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylim([100,600])
plt.xlabel('아파트 매매가 지수',fontsize=15)
plt.ylabel('음식점 수(개)',fontsize=15)