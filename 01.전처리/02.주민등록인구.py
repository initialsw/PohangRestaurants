## 읍/면/동별 인구 변화

import pandas as pd
import numpy as np

rootDir = 'D:/Research/Dataset/02.주민등록인구/'
filename = '포항_주민등록인구(합계).xlsx'

pop = pd.read_excel(rootDir + filename)

pop.drop('항목', axis=1, inplace=True)
pop.drop(index=0, axis=0, inplace=True)
pop.columns = ['연도', '2011', '2012', '2013', '2014', 
               '2015', '2016', '2017', '2018', '2019']
pop = pop.transpose()
pop.columns = pop.iloc[0]
pop.drop('연도', axis=0, inplace=True)
pop.index = pop.index.astype(int)
pop.columns = pop.columns.str.strip()
pop.replace('-', 0, inplace=True)

outRootDir = 'D:/Research/Data/'
outFilename = '포항_주민등록인구(합계).xlsx'

pop.to_excel(outRootDir + outFilename, sheet_name='Population', index=True)

pop = pop.loc[2011:2019].astype(int)
diff = pop.loc[2019] - pop.loc[2011]

## Get population of generations    
def cleansePopulationData(path):
    pop = pd.read_excel(path)
    
    pop.drop('항목', axis=1, inplace=True)
    pop.drop(index=0, axis=0, inplace=True)
    pop.columns = ['연도', '2011', '2012', '2013', '2014', 
                   '2015', '2016', '2017', '2018', '2019']
    pop = pop.transpose()
    pop.columns = pop.iloc[0]
    pop.drop('연도', axis=0, inplace=True)
    pop.index = pop.index.astype(int)
    ## Remove blanks
    pop.columns = pop.columns.str.strip()
    ## Change '-' to 0
    pop.replace('-', 0, inplace=True)
    
    return pop

rootDir = 'D:/Research/Dataset/02.주민등록인구/'

inputList = ['포항_주민등록인구(0-4세).xlsx', '포항_주민등록인구(5-9세).xlsx',
             '포항_주민등록인구(10-14세).xlsx', '포항_주민등록인구(15-19세).xlsx',
             '포항_주민등록인구(20-24세).xlsx', '포항_주민등록인구(25-29세).xlsx',
             '포항_주민등록인구(30-34세).xlsx', '포항_주민등록인구(35-39세).xlsx',
             '포항_주민등록인구(40-44세).xlsx', '포항_주민등록인구(45-49세).xlsx',
             '포항_주민등록인구(50-54세).xlsx', '포항_주민등록인구(55-59세).xlsx',
             '포항_주민등록인구(60-64세).xlsx', '포항_주민등록인구(65-69세).xlsx',
             '포항_주민등록인구(70-74세).xlsx', '포항_주민등록인구(75-79세).xlsx',
             '포항_주민등록인구(80-84세).xlsx', '포항_주민등록인구(85-89세).xlsx',
             '포항_주민등록인구(90-94세).xlsx', '포항_주민등록인구(95-99세).xlsx' ]

outputList = ['포항_주민등록인구(10세이하).xlsx', '포항_주민등록인구(10대).xlsx',
              '포항_주민등록인구(20대).xlsx', '포항_주민등록인구(30대).xlsx', 
              '포항_주민등록인구(40대).xlsx', '포항_주민등록인구(50대).xlsx',
              '포항_주민등록인구(60대).xlsx', '포항_주민등록인구(70대).xlsx', 
              '포항_주민등록인구(80대).xlsx', '포항_주민등록인구(90대).xlsx']

for i in range(0, len(inputList), 2):
    fileLower = rootDir + inputList[i]
    fileUpper = rootDir + inputList[i+1]
    outPath = rootDir + outputList[int(i/2)]
    lower = cleansePopulationData(fileLower)
    upper = cleansePopulationData(fileUpper)
    gen = lower + upper
    gen.to_excel(outPath, sheet_name='Population', index=True)
