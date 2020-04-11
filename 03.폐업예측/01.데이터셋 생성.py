## 데이터 세트 만들기
import pandas as pd
import numpy as np

rootDir = 'e:/research/2020/data/'

## 일반음식점 데이터 읽기
pohang = pd.read_excel(rootDir + '01.Pohang_Restaurants_v5.xlsx')

## 인접한 식당정보
nearbyRest = pd.read_csv(rootDir + '99.NearbyRestaurants.csv')
nearbyRestSameMenu = pd.read_csv(rootDir + '99.NearbyRestaurantsSameMenu.csv')
nearbyOpen = pd.read_csv(rootDir + '99.NearbyNewRestaurants.csv')
nearbyOpenSameMenu = pd.read_csv(rootDir + '99.NearbyNewRestaurantsSameMenu.csv')
nearbyClosed = pd.read_csv(rootDir + '99.NearbyClosedRestaurants.csv')
nearbyClosedSameMenu = pd.read_csv(rootDir + '99.NearbyClosedRestaurantsSameMenu.csv')

## 인구데이터
pop = []
diff = []
pop.append(pd.read_excel(rootDir + '20.포항_주민등록인구(합계).xlsx'))
pop.append(pd.read_excel(rootDir + '20-1.포항_주민등록인구(10세이하).xlsx'))
pop.append(pd.read_excel(rootDir + '20-2.포항_주민등록인구(10대).xlsx'))
pop.append(pd.read_excel(rootDir + '20-3.포항_주민등록인구(20대).xlsx'))
pop.append(pd.read_excel(rootDir + '20-4.포항_주민등록인구(30대).xlsx'))
pop.append(pd.read_excel(rootDir + '20-5.포항_주민등록인구(40대).xlsx'))
pop.append(pd.read_excel(rootDir + '20-6.포항_주민등록인구(50대).xlsx'))
pop.append(pd.read_excel(rootDir + '20-7.포항_주민등록인구(60대).xlsx'))
pop.append(pd.read_excel(rootDir + '20-8.포항_주민등록인구(70대).xlsx'))
pop.append(pd.read_excel(rootDir + '20-9.포항_주민등록인구(80대).xlsx'))
pop.append(pd.read_excel(rootDir + '20-10.포항_주민등록인구(90대).xlsx'))

for p in pop:
    p.rename({'Unnamed: 0':'Year'}, axis=1, inplace=True)
    p.set_index(p.Year, inplace=True)
    p.drop('Year', axis=1, inplace=True)
    diff.append(p.diff(axis=0))

## 일반음식점 주위 아파트 수, 면적 데이터
apts = pd.read_excel(rootDir + '15.포항 일반음식점 주변 아파트 수, 면적.xlsx')

## 학교 위치(연도무시)
schools = pd.read_excel(rootDir + '11.포항 일반음식점 주변 학교 수.xlsx')

## 행정기관 위치(연도무시)
admins = pd.read_excel(rootDir + '13.포항 일반음식점 주변 일선행정기관 수.xlsx')

## 공시지가 연도별 데이터
landvalue = pd.read_csv(rootDir + '99.LandValue.csv')

## 지역실물경제데이터
region = pd.read_excel(rootDir + '14.실물경제통계.xlsx')
region.set_index(region.Year, inplace=True)
region.drop('Year', axis=1, inplace=True)

## 행정동 목록

dataset = {'Restaurant No.': [],  ## 제외 필요
           'Year':[],             ## 제외 필요
           'OpenYear':[],         
           'OpenYears':[],
           'Size':[],
           'Korean':[],
           'KoreanNoodle':[],
           'KoreanMeat':[],
           'KoreanSeafood':[],
           'Chinese':[],
           'Japanese':[],
           'Western':[],
           'Foreign':[],
           'Fastfood':[],
           'Chicken':[],
           'Snack':[],
           'Pub':[],
           'Cafe':[],
           'ETC':[],
           'IsFranchise':[],
           'Latitude':[],
           'Longitude':[],
           'NearbyRest':[],
           'NearbyRestSameMenu':[],
           'NearbyOpen':[],
           'NearbyOpenSameMenu':[],
           'NearbyClosed':[],
           'NearbyClosedSameMenu':[],           
           'TownPop':[],
           'TownPopInc':[],
           'TownPop0s':[],
           'TownPopInc0s':[],
           'TownPop10s':[],
           'TownPopInc10s':[],
           'TownPop20s':[],
           'TownPopInc20s':[],
           'TownPop30s':[],
           'TownPopInc30s':[],
           'TownPop40s':[],
           'TownPopInc40s':[],
           'TownPop50s':[],
           'TownPopInc50s':[],
           'TownPop60s':[],
           'TownPopInc60s':[],
           'TownPop70s':[],
           'TownPopInc70s':[],
           'TownPop80s':[],
           'TownPopInc80s':[],
           'TownPop90s':[],
           'TownPopInc90s':[],
           ## 행정동
           'Jookdodong':[],
           'Yongheungdong':[],
           'Sangdaedong':[],
           'Haedodong':[],
           'Cheonglimdong':[],
           'Doohodong':[],
           'Woochangdong':[],
           'Joongangdong':[],
           'Songdodong':[],
           'Daeyidong':[],
           'Jangryangdong':[],
           'Hyogokdong':[],
           'Yanghakdong':[],
           'Jecheoldong':[],
           'Hwanyeodong':[],
           ## 토지유형
           'Residential':[],
           'Commercial':[],
           'Industrial':[],
           'LandValue':[],
           'NumApts':[],
           'AptTotalSize':[],
           'NumSchools':[],
           'NumAdmins':[],                      
           'Export':[],
           'Import':[],
           'SteelProd':[],
           'POSCOProd':[],
           'Sales':[],
           'BSIManufacture':[],
           'BSIService':[],
           'AptSalesCnt':[],
           'AptPriceIndex':[],
           'IsClosed':[]
           }

## 2010년부터 2019년까지의 데이터만 생성
## 2010년 이전에 개업했으면 2010년 부터의 폐업할 때까지의 데이터를 생성
## 2010년 이전에 폐업했으면 데이터 입력하지 않음
## 개업연도와 폐업연도가 같은 경우 그 해 데이터를 입력

for i, r in pohang.iterrows():    
    
    if ( r.CloseYear >= 2010 ):
        beginYear = max(r.OpenYear, 2010)
        endYear = min(r.CloseYear, 2019)
        #print(str(beginYear) + '-' + str(endYear))
        if ((beginYear == endYear) and (endYear > 2010)):
            beginYear = endYear - 1
        for y in range(beginYear, endYear):
            #print('\tMake a record of a year ' + str(y))
            dataset['Restaurant No.'].append(int(r.No))
            dataset['Year'].append(y)
            dataset['OpenYear'].append(r.OpenYear)
            dataset['OpenYears'].append(y - r.OpenYear)
            dataset['Size'].append(r.Size)
            ## 메뉴별 더미변수 입력
            menuKor = menuKorNoodle = menuKorMeat = menuKorSeafood \
            = menuChn = menuJap = menuWest = menuFor = menuFastfood \
            = menuChicken = menuSnack = menuPub = menuCafe = menuEtc = 0
            if r.Category == '한식일반':
                menuKor = 1
            elif r.Category == '한식면류':
                menuKorNoodle = 1
            elif r.Category == '한식육류':
                menuKorMeat = 1
            elif r.Category == '한식해산물':
                menuKorSeafood = 1
            elif r.Category == '중식':
                menuChn = 1
            elif r.Category == '일식':
                menuJap = 1
            elif r.Category == '서양식':
                menuWest = 1
            elif r.Category == '기타외국식':
                menuFor = 1
            elif r.Category == '패스트푸드':
                menuFastfood = 1
            elif r.Category == '치킨':
                menuChicken = 1
            elif r.Category == '분식':
                menuSnack = 1
            elif r.Category == '주점':
                menuPub = 1
            elif r.Category == '카페':
                menuCafe = 1
            else:
                menuEtc = 1
            dataset['Korean'].append(menuKor)
            dataset['KoreanNoodle'].append(menuKorNoodle)
            dataset['KoreanMeat'].append(menuKorMeat)
            dataset['KoreanSeafood'].append(menuKorSeafood)
            dataset['Chinese'].append(menuChn)
            dataset['Japanese'].append(menuJap)
            dataset['Western'].append(menuWest)
            dataset['Foreign'].append(menuFor)
            dataset['Fastfood'].append(menuFastfood)
            dataset['Chicken'].append(menuChicken)
            dataset['Snack'].append(menuSnack)
            dataset['Pub'].append(menuPub)
            dataset['Cafe'].append(menuCafe)
            dataset['ETC'].append(menuEtc)
            dataset['IsFranchise'].append(r.isFranchise)
            dataset['Latitude'].append(r.Y)
            dataset['Longitude'].append(r.X)
            dataset['NearbyRest'].append(int(nearbyRest.iloc[i][str(y)]))
            dataset['NearbyRestSameMenu'].append(int(nearbyRestSameMenu.iloc[i][str(y)]))
            dataset['NearbyOpen'].append(int(nearbyOpen.iloc[i][str(y)]))
            dataset['NearbyOpenSameMenu'].append(int(nearbyOpenSameMenu.iloc[i][str(y)]))
            dataset['NearbyClosed'].append(int(nearbyClosed.iloc[i][str(y)]))
            dataset['NearbyClosedSameMenu'].append(int(nearbyClosedSameMenu.iloc[i][str(y)]))
            dataset['TownPop'].append(pop[0][r.AdminTownName].loc[y])
            dataset['TownPopInc'].append(diff[0][r.AdminTownName].loc[y])
            dataset['TownPop0s'].append(pop[1][r.AdminTownName].loc[y])
            dataset['TownPopInc0s'].append(diff[1][r.AdminTownName].loc[y])
            dataset['TownPop10s'].append(pop[2][r.AdminTownName].loc[y])
            dataset['TownPopInc10s'].append(diff[2][r.AdminTownName].loc[y])
            dataset['TownPop20s'].append(pop[3][r.AdminTownName].loc[y])
            dataset['TownPopInc20s'].append(diff[3][r.AdminTownName].loc[y])
            dataset['TownPop30s'].append(pop[4][r.AdminTownName].loc[y])
            dataset['TownPopInc30s'].append(diff[4][r.AdminTownName].loc[y])
            dataset['TownPop40s'].append(pop[5][r.AdminTownName].loc[y])
            dataset['TownPopInc40s'].append(diff[5][r.AdminTownName].loc[y])
            dataset['TownPop50s'].append(pop[6][r.AdminTownName].loc[y])
            dataset['TownPopInc50s'].append(diff[6][r.AdminTownName].loc[y])
            dataset['TownPop60s'].append(pop[7][r.AdminTownName].loc[y])
            dataset['TownPopInc60s'].append(diff[7][r.AdminTownName].loc[y])
            dataset['TownPop70s'].append(pop[8][r.AdminTownName].loc[y])
            dataset['TownPopInc70s'].append(diff[8][r.AdminTownName].loc[y])
            dataset['TownPop80s'].append(pop[9][r.AdminTownName].loc[y])
            dataset['TownPopInc80s'].append(diff[9][r.AdminTownName].loc[y])
            dataset['TownPop90s'].append(pop[10][r.AdminTownName].loc[y])
            dataset['TownPopInc90s'].append(diff[10][r.AdminTownName].loc[y])
            ## 행정동구분
            Jookdo = Yongheung = Sangdae = Haedo = Cheonglim = Dooho \
                = Woochang = Joongang = Songdo = Daeyi = Jangryang \
                = Hyogok = Yanghak = Jecheol = Hwanyeo = 0
                    
            if r.AdminTownName == '죽도동':
                Jookdo = 1
            elif r.AdminTownName == '용흥동':
                Yongheung = 1
            elif r.AdminTownName == '상대동':
                Sangdae = 1
            elif r.AdminTownName == '해도동':
                Haedo = 1
            elif r.AdminTownName == '청림동':
                Cheonglim = 1
            elif r.AdminTownName == '두호동':
                Dooho = 1
            elif r.AdminTownName == '우창동':
                Woochang = 1
            elif r.AdminTownName == '중앙동':
                Joongang = 1
            elif r.AdminTownName == '송도동':
                Songdo = 1
            elif r.AdminTownName == '대이동':
                Daeyi = 1
            elif r.AdminTownName == '장량동':
                Jangryang = 1
            elif r.AdminTownName == '효곡동':
                Hyogok = 1
            elif r.AdminTownName == '양학동':
                Yanghak = 1
            elif r.AdminTownName == '제철동':
                Jecheol = 1
            elif r.AdminTownName == '환여동':
                Hwanyeo = 1
            
            dataset['Jookdodong'].append(Jookdo)
            dataset['Yongheungdong'].append(Yongheung)
            dataset['Sangdaedong'].append(Sangdae)
            dataset['Haedodong'].append(Haedo)
            dataset['Cheonglimdong'].append(Cheonglim)
            dataset['Doohodong'].append(Dooho)
            dataset['Woochangdong'].append(Woochang)
            dataset['Joongangdong'].append(Joongang)
            dataset['Songdodong'].append(Songdo)
            dataset['Daeyidong'].append(Daeyi)
            dataset['Jangryangdong'].append(Jangryang)
            dataset['Hyogokdong'].append(Hyogok)
            dataset['Yanghakdong'].append(Yanghak)
            dataset['Jecheoldong'].append(Jecheol)
            dataset['Hwanyeodong'].append(Hwanyeo)
            
            landtype = landvalue.iloc[i][str(y) + ' LandType']
            tResidential = tCommercial = tIndustrial = 0
            if landtype == 1:
                tResidential = 1
            elif landtype == 2:
                tCommercial = 1
            elif landtype == 3:
                tIndustrial = 1
            dataset['Residential'].append(tResidential)
            dataset['Commercial'].append(tCommercial)
            dataset['Industrial'].append(tIndustrial)
            dataset['LandValue'].append(landvalue.iloc[i][str(y) + ' AvgLandValue'])
            dataset['NumApts'].append(apts.iloc[i][str(y) + ' NumApts'])
            dataset['AptTotalSize'].append(apts.iloc[i][str(y) + ' TotalAptArea'])
            dataset['NumSchools'].append(schools.iloc[i].NumSchools)
            dataset['NumAdmins'].append(admins.iloc[i].NumAdmins)
            dataset['Export'].append(region.loc[y].Export)
            dataset['Import'].append(region.loc[y].Import)
            dataset['SteelProd'].append(region.loc[y].SteelProd)
            dataset['POSCOProd'].append(region.loc[y].POSCO)
            dataset['Sales'].append(region.loc[y].Sales)
            dataset['BSIManufacture'].append(region.loc[y].BSI_Manufacture)
            dataset['BSIService'].append(region.loc[y].BSI_Service)
            dataset['AptSalesCnt'].append(region.loc[y].AptSalesCnt)
            dataset['AptPriceIndex'].append(region.loc[y].AptPriceIndex)
            isClosed = 0
            if r.CloseYear == 2020: ## 2019년 말까지 영업을 계속함
                isClosed = 0                
            elif r.CloseYear == y + 1: ## 내년에 폐업
                isClosed = 1
            dataset['IsClosed'].append(isClosed)
    else:    
        ## 2010년 이전에 폐업했으므로 모두 0으로 처리(나중에 제외)
        dataset['Restaurant No.'].append(int(r.No))
        for k in dataset.keys():l
            if k != 'Restaurant No.':
                dataset[k].append(0)
    bOk = True
    tmpLen = len(dataset['Restaurant No.'])
    for k in dataset.keys():
        if len(dataset[k]) != tmpLen:
            bOk = False
            break    
    print(str(i) + '/' + str(len(pohang)) + ' => Is OK? ' + str(bOk))
    if not bOk:
        break

df_dataset = pd.DataFrame(dataset)
#df_dataset.to_excel(rootDir + '00.Pohang_Dataset_all.xlsx', index=False)
df_dataset = df_dataset[df_dataset.Year != 0]
df_dataset.to_excel(rootDir + '00.Pohang_Dataset.xlsx', index=False)

