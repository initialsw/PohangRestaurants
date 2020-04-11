'''
제목: 포항지역 일반음식점 현황 분석(일반음식점 현황)
작성자: 한승욱
작성일: 2020.04.04(토)
코드내용 요약
  1. 연도에 따른 영업중인 일반음식점 수 변화
  2. 연도에 따른 일반음식점 폐업 변화  
  3. 동별 음식점 분포 
  4. 음식점 분포 (히트맵)
  5. 법정동별 음식점 폐업 수 대비 개업  
'''
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt 
import seaborn as sns

rootDir = 'e:/research/2020/data/'
filename = '01.Pohang_Restaurants_v5.xlsx'
outDir = 'e:/research/2020/'

pohang = pd.read_excel(rootDir + filename)
pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']
pohang_city['OpenYears'] = pohang_city.OpenMonths / 12
pohang_city_open = pohang_city[pohang_city.IsClosed == 0]

## 1. 연도에 따른 영업중인 일반음식점 수 변화, 연도에 따른 폐업 변화 
nRest = { }
for y in range(2010, 2020):
    nRest[y] = [0]

for i, r in pohang_city.iterrows():
    ## 연도별로 음식점이 영업중이었는지 확인
    for y in range(2010, 2020):
        if (y >= r.OpenYear) and (y <= r.CloseYear):
            nRest[y][0] += 1
nRest = pd.DataFrame(nRest).transpose()
nRest.rename({0:'numRest'}, axis=1, inplace=True)

nOpen = pohang_city.groupby(pohang_city.OpenYear).No.count().loc[2010:2019]
nClose = pohang_city.groupby(pohang_city.CloseYear).No.count().loc[2010:2019]

nRest['numOpen'] = np.array(nOpen)
nRest['numClose'] = np.array(nClose)

plt.rcParams["font.family"] = 'Malgun Gothic'

fig, ax1 = plt.subplots(figsize=(5, 5))
ax1.set_xlabel('연도')
ax1.set_ylabel('음식점 수(개)')
ax1.set_ylim([4000, 6500])
plt.xticks(nRest.index, nRest.index, fontsize=10)
ax1.plot(nRest.index, nRest.numRest, color='red', marker='o', linewidth=2)

ax2 = ax1.twinx()
ax2.set_ylabel('폐업 음식점 수(개)')
ax2.set_ylim([0, 1500])
ax2.bar(nRest.index, nRest.numClose, color='blue', edgecolor='black')

## 3. 동별 음식점 분포 
pohang_open = pohang_city[pohang_city.IsClosed == 0]
total_rest = len(pohang_open)

ratio = pohang_open.groupby(pohang_open.AdminTownName).No.count().sort_values(ascending=False)
top10 = ratio.iloc[0:10].sort_values(ascending=True)
top10 / total_rest

ax = plt.barh(top10.index, top10.values, color='blue', edgecolor='black')
plt.yticks(top10.index, top10.index, fontsize=20)
plt.xticks([0,100,200,300,400,500,600,700,800,900,1000],[0,100,200,300,400,500,600,700,800,900,1000],fontsize=20)
plt.ylabel('행정동', fontsize=20)
plt.xlabel('음식점 수(개)', fontsize=20)

## 4. 음식점 분포(히트맵)
import folium
from folium import plugins
from folium.plugins import HeatMap
pohang_city_open.rename({'X':'Longitude', 'Y':'Latitude'}, axis=1, inplace=True)
location = pohang_city_open[['Longitude', 'Latitude']]
location.reset_index(inplace=True)
location.drop('index', axis=1, inplace=True)

location['Longitude'] = location['Longitude'].astype(float)
location['Latitude'] = location['Latitude'].astype(float)

heat_data = [[row['Latitude'], row['Longitude']] for index, row in location.iterrows()]

center_latitude = 36.032387
center_longitude = 129.371501

pohang_map = folium.Map(location=[center_latitude, center_longitude], zoom_start=12)
HeatMap(heat_data, max_opacity=0.5, radius=10).add_to(pohang_map)
pohang_map.save(outDir + 'heatmap.html')


## 5. 법정동별 폐업 대비 개업한 음식점 수 
import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify

pohang_city = pohang[pohang.AdminTownName.str[-1] == '동']

recent_open = pohang_city[pohang_city.OpenYear >= 2010]
recent_close = pohang_city[pohang_city.CloseYear >= 2010]

recent_close = recent_close[recent_close.CloseYear != 2020]

recent_open_by_town = recent_open.groupby(recent_open.Town).No.count()
recent_close_by_town = recent_close.groupby(recent_close.Town).No.count()

ratio = recent_open_by_town / recent_close_by_town
ratio.fillna(0, inplace=True)

plt.rcParams["font.family"] = 'Malgun Gothic'
plt.rcParams['figure.figsize'] = (10, 10)

shape_file = 'e:/research/2020/data/shape/TL_SCCO_EMD.shp'
korea = gpd.read_file(shape_file, encoding='cp949')
pohang_shp = korea[korea.EMD_CD.str[0:4] == '4711']
pohang_city_shp = pohang_shp[pohang_shp.EMD_KOR_NM.str[-1] == '동']
pohang_city_shp.reset_index(inplace=True)
pohang_city_shp.drop('index', axis=1, inplace=True)

lstRatio = []
for i, r in pohang_city_shp.iterrows():
    if r.EMD_KOR_NM not in ratio.index:
        lstRatio.append(0.0)
    else:
        lstRatio.append(ratio[r.EMD_KOR_NM])

pohang_city_shp['Ratio'] = lstRatio    

ax = pohang_city_shp.plot(column='Ratio', legend=True, scheme='quantiles', 
                          cmap='Blues', k=5, edgecolor='k')

import mapclassify
import geoplot

scheme = mapclassify.Quantiles(ratio, k=10)

geoplot.choropleth(pohang_city_shp, hue=list(ratio), scheme='quantiles', 
               cmap='Blues', figsize=(8,4))
ax.set_axis_off()
plt.show()
plt.savefig('e:/research/2020/pohang_open-close-ratio.jpg', dpi=300)