'''
제목: 포항지역 일반음식점 현황 분석(사회적요소)
작성자: 한승욱
작성일: 2020.04.05(일)
코드내용 요약
  1. 행정동별 주민등록 인구와 음식점 수의 관계
  2. 행정동별 주민등록 인구 증감과 개업/폐업의 관계
  3. 행정동별 연령별 인구 수와 개업/폐업의 관계
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

## 1. 행정동별 주민등록인구와 음식점 수의 관계
bytown = pohang_city_open.groupby(pohang_city_open.AdminTownName).No.count()

filename = '20.포항_주민등록인구(합계).xlsx'
pop = pd.read_excel(rootDir + filename)
pop.rename({'Unnamed: 0':'Year'}, axis=1, inplace=True)
pop.set_index(pop.Year, inplace=True)
pop.drop('Year', axis=1, inplace=True)
diff = pop.diff(axis=0)   ## 전년대비 주민등록인구 변화

## 연도별로 영업중인 음식점 수 얻기
adminTowns = ['상대동', '해도동', '송도동', '청림동', '제철동', '효곡동',
              '대이동', '중앙동', '양학동', '죽도동', '용흥동', '우창동', 
              '두호동', '장량동', '환여동']

## 연도별로 해당연도에 영업중이었던 음식점 수를 카운트
BEGIN_YEAR = 2010
END_YEAR = 2019

Yearly = { }
for t in adminTowns:
    Yearly[t] = []
    for y in range(BEGIN_YEAR, END_YEAR + 1):
        Yearly[t].append(0)

for i, r in pohang_city.iterrows():
    begin = max(r.OpenYear, BEGIN_YEAR)
    end = min(r.CloseYear, END_YEAR)
    if ( end < BEGIN_YEAR ):
        continue
    for y in range(begin, end + 1):
        Yearly[r.AdminTownName][y - BEGIN_YEAR] += 1
       
Yearly = pd.DataFrame(Yearly).transpose()
tmp = []
for y in range(BEGIN_YEAR, END_YEAR + 1):
    tmp.append(y)
Yearly.columns = tmp

X = []  ## 동별 인구
Y = []  ## 영업중이 음식점 수

for y in range(BEGIN_YEAR, END_YEAR+1):
    for t in bytown.index:
        X.append(pop.loc[y][t])
        Y.append(Yearly.loc[t][y])

import statsmodels.api as sm

X0 = pd.DataFrame(X)
y = pd.DataFrame(Y)
X = sm.add_constant(X0)

result = sm.OLS(y, X).fit()
result.summary()

plt.rcParams["font.family"] = 'Malgun Gothic'
plt.rcParams['figure.figsize'] = (5, 5)
plt.rcParams['axes.unicode_minus'] = False

endpoints = [[1,0], [1,80000]]
fig, ax = plt.subplots()
plt.scatter(X0, Y, s=30, c='black', marker='+', linewidth=1)
plt.plot([1, 80000], result.predict(endpoints), color='red', linewidth=1)
labels = [x * 10000 for x in range(0, 9)]
vals = [x for x in range(0, 9)]
plt.xticks(labels, vals, fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel('주민등록인구(만명)', fontsize=15)
plt.ylabel('음식점 수(개)', fontsize=15)


## 2. 인구 증감과 개업 및 폐업간의 관계
BEGIN_YEAR = 2010
END_YEAR = 2019

numOpen = pohang_city.pivot_table('No', index='OpenYear', columns='AdminTownName', aggfunc='count')
numClose = pohang_city.pivot_table('No', index='CloseYear', columns='AdminTownName', aggfunc='count')
numOpen = numOpen.loc[BEGIN_YEAR:END_YEAR].astype(int)
numClose = numClose.loc[BEGIN_YEAR:END_YEAR].astype(int)

X = []    ## 동별 인구변화
Y = []    ## 동별 개업 음식점 수
Z = []    ## 동별 폐업 음식점 수

for y in range(BEGIN_YEAR, END_YEAR+1):
    for t in adminTowns:
        X.append(diff.loc[y][t])
        Y.append(numOpen.loc[y][t])
        Z.append(numClose.loc[y][t])


tmp1 = pd.concat([pd.DataFrame(X), pd.DataFrame(Y)], axis=1)
tmp2 = pd.concat([pd.DataFrame(X), pd.DataFrame(Z)], axis=1)
tmp1['GRP'] = ['개업'] * len(X)
tmp2['GRP'] = ['폐업'] * len(Y)

tmp = pd.concat([tmp1, tmp2], axis=0)
tmp.columns = ['주민등록인구 증감(명)', '음식점 수(개)', '상태']

rc={'axes.labelsize': 15, 'font.size': 15, 'legend.fontsize': 15.0, \
    'axes.titlesize': 15, 'figure.figsize':[6,4]}
plt.rcParams.update(**rc)
sns.scatterplot(x='주민등록인구 증감(명)', y='음식점 수(개)', hue='상태', style='상태', 
                s=70, data=tmp, linewidth=0.5, alpha=1)

X0 = pd.DataFrame(X)
y = pd.DataFrame(Y)
X = sm.add_constant(X0)

result = sm.OLS(y, X).fit()
result.summary()

SCALE = 2000

plt.rcParams["font.family"] = 'Malgun Gothic'


endpoints = [[1, -SCALE], [1, SCALE]]
plt.scatter(X0, Y, s=20, c='black', marker='o', linewidth=1)
plt.xlim([-SCALE, SCALE])
plt.plot([-SCALE, SCALE], result.predict(endpoints), c='red', linewidth=1)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

z = pd.DataFrame(Z)

result = sm.OLS(z, X).fit()
result.summary()

SCALE = 2000

endpoints = [[1, -SCALE], [1, SCALE]]
plt.scatter(X0, Z, s=20, c='black', marker='x', linewidth=1)
plt.xlim([-SCALE, SCALE])
plt.plot([-SCALE, SCALE], result.predict(endpoints), c='red', linewidth=1)


## 3. 연령대별 인구 증감과 개업 및 폐업간의 관계
pop0s = pd.read_excel(rootDir + '20-1.포항_주민등록인구(10세이하).xlsx')
pop10s = pd.read_excel(rootDir + '20-2.포항_주민등록인구(10대).xlsx')
pop20s = pd.read_excel(rootDir + '20-3.포항_주민등록인구(20대).xlsx')
pop30s = pd.read_excel(rootDir + '20-4.포항_주민등록인구(30대).xlsx')
pop40s = pd.read_excel(rootDir + '20-5.포항_주민등록인구(40대).xlsx')
pop50s = pd.read_excel(rootDir + '20-6.포항_주민등록인구(50대).xlsx')
pop60s = pd.read_excel(rootDir + '20-7.포항_주민등록인구(60대).xlsx')
pop70s = pd.read_excel(rootDir + '20-8.포항_주민등록인구(70대).xlsx')
pop80s = pd.read_excel(rootDir + '20-9.포항_주민등록인구(80대).xlsx')
pop90s = pd.read_excel(rootDir + '20-10.포항_주민등록인구(90대).xlsx')

########################
## 이 라인의 입력값을 바꾸면서 테스트 할 것!
pop = pop20s + pop30s
########################

pop.rename({'Unnamed: 0':'Year'}, axis=1, inplace=True)
pop.set_index(pop.Year, inplace=True)
pop.drop('Year', axis=1, inplace=True)
diff = pop.diff(axis=0)   ## 전년대비 주민등록인구 변화

## 연도별로 영업중인 음식점 수 얻기
adminTowns = ['상대동', '해도동', '송도동', '청림동', '제철동', '효곡동',
              '대이동', '중앙동', '양학동', '죽도동', '용흥동', '우창동', 
              '두호동', '장량동', '환여동']

BEGIN_YEAR = 2010
END_YEAR = 2019

numOpen = pohang_city.pivot_table('No', index='OpenYear', columns='AdminTownName', aggfunc='count')
numClose = pohang_city.pivot_table('No', index='CloseYear', columns='AdminTownName', aggfunc='count')
numOpen = numOpen.loc[BEGIN_YEAR:END_YEAR].astype(int)
numClose = numClose.loc[BEGIN_YEAR:END_YEAR].astype(int)


X = []    ## 동별 인구변화
Y = []    ## 동별 개업 음식점 수
Z = []    ## 동별 폐업 음식점 수

for y in range(BEGIN_YEAR, END_YEAR+1):
    for t in adminTowns:
        X.append(diff.loc[y][t])
        Y.append(numOpen.loc[y][t])
        Z.append(numClose.loc[y][t])

tmp1 = pd.concat([pd.DataFrame(X), pd.DataFrame(Y)], axis=1)
tmp2 = pd.concat([pd.DataFrame(X), pd.DataFrame(Z)], axis=1)
tmp1['GRP'] = ['개업'] * len(X)
tmp2['GRP'] = ['폐업'] * len(Y)

tmp = pd.concat([tmp1, tmp2], axis=0)
tmp.columns = ['주민등록인구 증감(명)', '음식점 수(개)', '상태']

rc={'axes.labelsize': 15, 'font.size': 15, 'legend.fontsize': 15.0, \
    'axes.titlesize': 15, 'figure.figsize':[6,4]}
plt.ylim([-10, 260])
plt.rcParams.update(**rc)
sns.scatterplot(x='주민등록인구 증감(명)', y='음식점 수(개)', hue='상태', style='상태', 
                s=70, data=tmp, linewidth=0.5, alpha=1)




X0 = pd.DataFrame(X)
X = sm.add_constant(X0)

## 인구변화와 개업음식점 수 변화 (연도별)
y = pd.DataFrame(Y)

result = sm.OLS(y, X).fit()
result.summary()

LOW = -100
HIGH = 1000
SCALE = 1000

endpoints = [[1, LOW], [1, HIGH]]
plt.scatter(X0, Y, s=20, c='black', marker='+', linewidth=1)
plt.xlim([LOW, HIGH])
plt.plot([LOW, HIGH], result.predict(endpoints), c='red', linewidth=1)


## 인구변화와 폐업음식점 수 변화 (연도별)

z = pd.DataFrame(Z)

result = sm.OLS(z, X).fit()
result.summary()

LOW = -100
HIGH = 1000
SCALE = 1000

endpoints = [[1, LOW], [1, HIGH]]
plt.scatter(X0, Z, s=20, c='black', marker='+', linewidth=1)
plt.xlim([LOW, HIGH])
plt.plot([LOW, HIGH], result.predict(endpoints), c='red', linewidth=1)


## 특정기간(누적) 동별 인구변화와 개/폐업 음식점 수 변화

BEGIN_YEAR = 2010
END_YEAR = 2019

numOpen = pohang_city.pivot_table('No', index='OpenYear', columns='AdminTownName', aggfunc='count')
numClose = pohang_city.pivot_table('No', index='CloseYear', columns='AdminTownName', aggfunc='count')
numOpen = numOpen.loc[BEGIN_YEAR:END_YEAR].astype(int)
numClose = numClose.loc[BEGIN_YEAR:END_YEAR].astype(int)

X = []   ## 인구변화
Y = []   ## 개업 음식점 수
Z = []   ## 폐업 음식점 수

for t in adminTowns:
    X.append(diff.loc[BEGIN_YEAR:END_YEAR][t].sum())
    Y.append(numOpen.loc[BEGIN_YEAR:END_YEAR][t].sum())
    Z.append(numClose.loc[BEGIN_YEAR:END_YEAR][t].sum())

X0 = pd.DataFrame(X)
X = sm.add_constant(X0)

## 인구변화와 개업음식점 수 변화 (누적)
y = pd.DataFrame(Y)

result = sm.OLS(y, X).fit()
result.summary()

SCALE = 3000

endpoints = [[1, -SCALE], [1, SCALE]]
plt.scatter(X0, Y, s=20, c='black', marker='+', linewidth=1)
#plt.xlim([-SCALE, SCALE])
plt.plot([-SCALE, SCALE], result.predict(endpoints), c='red', linewidth=1)


## 인구변화와 폐업음식점 수 변화 (누적)

z = pd.DataFrame(Z)

result = sm.OLS(z, X).fit()
result.summary()

SCALE = 3000

endpoints = [[1, -SCALE], [1, SCALE]]
plt.scatter(X0, Z, s=20, c='black', marker='+', linewidth=1)
plt.xlim([-SCALE, SCALE])
plt.plot([-SCALE, SCALE], result.predict(endpoints), c='red', linewidth=1)