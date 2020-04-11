'''
제목: 포항지역 일반음식점 현황 분석(음식점 자체의 속성)
작성자: 한승욱
작성일: 2020.04.04(토)
코드내용 요약
  1. 메뉴에 따른 음식점의 영업기간 분포(2010년 이후)
  2. 음식점 규모에 따른 영업기간 변화
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

## 작업 경로(rootDir)와 파일이름은 상황에 따라 변경할 것
rootDir = 'd:/research/data/'
outDir = 'd:/research/'
filename = '01.Pohang_Restaurants_v5.xlsx'

pohang = pd.read_excel(rootDir + filename)
pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
pohang_city['OpenYears'] = pohang_city.OpenMonths / 12

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'


## 1.메뉴에 따른 음식점의 영업기간 분포
## 2010년 이후 폐업한 음식점
recent_closed = pohang_city[pohang_city.CloseYear >= 2010]
recent_closed = recent_closed[recent_closed.IsClosed == 1]
## 2010년 이후 개업한 후 폐업한 음식점 목록
recent_open_closed = recent_closed[recent_closed.OpenYear >= 2010]

## 2010년 이후 개업해서 현재까지 영업중인 음식점 목록
recent_open = pohang_city[pohang_city.OpenYear >= 2010]
recent_open = recent_open[recent_open.IsClosed == 0]

## 최근 10년간 폐업한 모든 음식점을 메뉴별로 영업기간 boxplot
fig1 = plt.figure(figsize=(6,5))
ax1 = sns.boxplot(x='OpenYears', y='Category', orient='h', \
                  data=recent_closed, linewidth=1, \
                  order=np.sort(recent_open_closed.Category.unique())[::-1])

plt.xlabel('영업기간(년)', fontsize=15)
plt.ylabel('음식점 메뉴', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.setp(ax1.artists, edgecolor='k', facecolor='w')
plt.setp(ax1.lines, color='k')
fig1.savefig(outDir + '2010년 이후 폐업한 음식점 메뉴별 영업기간.png', dpi=240)

## 최근 10년간 개업과 폐업을 모두 경험한 음식점 메뉴별로 영업기간 boxplot
fig2 = plt.figure(figsize=(6,5))
ax2 = sns.boxplot(x='OpenYears', y='Category', orient='h', \
                 data=recent_open_closed, linewidth=1, \
                 order=np.sort(recent_open_closed.Category.unique())[::-1])
plt.xlabel('영업기간(년)', fontsize=15)
plt.ylabel('음식점 메뉴', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.xlim([-0.3, 10.3])
plt.setp(ax2.artists, edgecolor='k', facecolor='w')
plt.setp(ax2.lines, color='k')
fig2.savefig(rootDir + '2010년 이후 개업 후 폐업한 음식점 메뉴별 영업기간.png', dpi=240)

## 최근 10년간 개업한 음식점의 메뉴별 영업기간 boxplot
fig3 = plt.figure(figsize=(6,5))
ax3 = sns.boxplot(x='OpenYears', y='Category', orient='h', \
                  data=recent_open, linewidth=1, \
                  order=np.sort(recent_open.Category.unique())[::-1])
plt.xlabel('영업기간(년)', fontsize=15)
plt.ylabel('음식점 메뉴', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.setp(ax3.artists, edgecolor='k', facecolor='w')
plt.setp(ax3.lines, color='k')
fig3.savefig(outDir + '2010년 이후 개업 후 현재까지 영업중인 음식점 메뉴별 영업기간.png', dpi=240)



## 2. 음식점 규모에 따른 영업기간 변화

## 규모에 따라 그룹을 나누어 표현
UNIT_SIZE = 50.0   ## 50 제곱미터 단위
pohang_city['SizeGrp'] = pohang_city.Size // UNIT_SIZE
pohang_city['SizeGrp'] = pohang_city['SizeGrp'].astype(int)
recent_open = pohang_city[pohang_city.OpenYear >= 2010]
recent_open_closed = recent_open[recent_open.IsClosed == 1]
recent_open = recent_open[recent_open.IsClosed == 0]

## 2010년 이후 개업한 음식점 
fig4 = plt.figure()
ax4 = sns.boxplot(x='SizeGrp', y='OpenYears', data=recent_open, linewidth=1)
plt.xlabel('음식점면적(50㎡단위)', fontsize=15)
plt.ylabel('영업기간(년)', fontsize=15)
plt.xlim([-0.5, 10.5])
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.setp(ax4.artists, edgecolor='k', facecolor='w')
plt.setp(ax4.lines, color='k')

## 2010년 이후 폐업한 음식점 
fig5 = plt.figure()
ax5 = sns.boxplot(x='SizeGrp', y='OpenYears', data=recent_open_closed, linewidth=1)
plt.xlabel('음식점면적(50㎡단위)',fontsize=15)
plt.ylabel('영업기간(년)', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim([-0.5, 10.5])
plt.setp(ax5.artists, edgecolor='k', facecolor='w')
plt.setp(ax5.lines, color='k')

