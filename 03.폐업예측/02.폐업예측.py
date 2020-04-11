'''
제목: 포항지역 일반음식점 폐업 예측
작성자: 한승욱
작성일: 2020.04.06(월)
코드내용 요약
 - 서브 샘플링 기법으로 클래스간 데이터양 조절 후 홀드아웃 검증
 - 무작위로 100번 돌려서 그 평균값을 최종 성능치로 사용
 - 정확도(accuracy), 정밀도(precision), 민감도(sensibility), 특이도(specificity) 측정
  1. 인공신경망
  2. 랜덤포레스트
  3. AdaBoost
  4. XGBoost
  5. 모형간 성능 비교 및 ROC 그래프 생성
'''

import pandas as pd
import numpy as np

rootDir = 'e:/research/2020/data/'
filename = '00.Pohang_Dataset.xlsx'

dataset = pd.read_excel(rootDir + filename)

## 필요없는 칼럼 삭제
dataset.drop('Restaurant No.', axis=1, inplace=True)
dataset.drop('OpenYear', axis=1, inplace=True)
dataset.drop('Year', axis=1, inplace=True)

## 정규화를 위해서 라벨(영업, 폐업 구분) 분리하기
dataset_label = dataset['IsClosed']
dataset_norm = dataset.drop('IsClosed', axis=1)

## 신경망에 들어가는 입력은 정규화 과정이 필요
for c in dataset_norm.columns:
    ## 더미변수인경우 (-1, 1)로 값을 조정
    if (min(dataset_norm[c]) == 0) and (max(dataset_norm[c]) == 1):
        dataset_norm[c] -= 0.5
        dataset_norm[c] *= 2
    ## 일반적인 수치형 변수는 정규화(normalize)
    else:
        dataset_norm[c] -= dataset_norm[c].mean(axis=0)
        dataset_norm[c] /= dataset_norm[c].std(axis=0)

## 앞서 분리해 놓았던 라벨(영업, 폐업 구분)을 다시 붙이기
dataset_norm = pd.concat([dataset_norm, dataset_label], axis=1)

## 앙상블용 데이터 셋
dataset_open = dataset[dataset.IsClosed == 0]
dataset_closed = dataset[dataset.IsClosed == 1]

## 신경망용 데이터 셋
dataset_open_norm = dataset_norm[dataset.IsClosed == 0]
dataset_closed_norm = dataset_norm[dataset.IsClosed == 1]

## 0. 업-샘플링, 다운-샘플링 후 데이터 셋 분할(학습용, 테스트용)

## 0-1. 업-샘플링(양이 적은 데이터 복제해서 양이 많은 쪽에 맞춤)
def upsampling(data1, data2):
    if len(data1) > len(data2):
        tmpSmall = data2
        tmpBig = data1
    elif len(data1) == len(data2):
        return data1, data2
    else:
        tmpSmall = data1
        tmpBig = data2
        
    ret1 = tmpBig
    ret2 = tmpSmall.take(np.random.choice(range(0, len(tmpSmall)), len(tmpBig), True))
    return ret1, ret2

## 0-2. 다운-샘플링(양이 많은 데이터를 임의 선택해서 양이 적은 쪽에 맞춤)
def downsampling(data1, data2):
    if len(data1) > len(data2):
        tmpSmall = data2
        tmpBig = data1
    elif len(data1) == len(data2):
        return data1, data2
    else:
        tmpSmall = data1
        tmpBig = data2

    ret1 = tmpBig.take(np.random.permutation(len(tmpBig))[0:len(tmpSmall)])
    ret2 = tmpSmall    
    return ret1, ret2

## 0-3. 데이터 셋을 학습용, 테스트용으로 분할 
from sklearn.model_selection import train_test_split
def splitDataset(class1, class2, ratio):
    data = pd.concat([class1, class2], axis=0)
    label = data['IsClosed']
    data.drop('IsClosed', axis=1, inplace=True)    
    data_train, data_test, label_train, label_test = train_test_split(data, label, train_size=ratio, stratify=label)
    
    return data_train, data_test, label_train, label_test
    
## 0-4. 성능측정을 위한 수치(P, N, TP, TN 등등)
## Numpy Array로 입력할 것!!! 결과는 0(Negative) or 1(Positive)
def getStats(label_test, label_pred):
    P = N = TP = TN = FP = FN = 0
    
    ## 길이가 같은 경우에만 점검
    if (len(label_test) == len(label_pred)):
        for i in range(0, len(label_test)):
            if (label_test[i] == 0):
                N += 1
                if (label_pred[i] == 0):
                    TN += 1
                else:
                    FP += 1
            else:
                P += 1
                if (label_pred[i] == 0):
                    FN += 1
                else:
                    TP += 1
    else:
        print("ERROR!!!")
        print(label_test)
        print(label_pred)
        
    return ( P, N, TP, TN, FP, FN )

## 0-5. 성능측정함수(정확도, 정밀도, 민감도, 특이도 등)
def getPerformance(predResult):
    predResult['FP_Rate'] = predResult['FP'] / predResult['N']
    predResult['TP_Rate'] = predResult['TP'] / predResult['P']
    predResult['Precision'] = predResult['TP'] / (predResult['TP'] + predResult['FP'])
    predResult['Sensitivity'] = predResult['TP'] / predResult['P']
    predResult['Accuracy'] = (predResult['TP'] + predResult['TN']) / (predResult['P'] + predResult['N'])
    predResult['Specificity'] = predResult['TN'] / ( predResult['FP'] + predResult['TN'] )
    predResult['F_Measure'] = 2 / (1 / predResult['Precision'] + 1 / predResult['Sensitivity'])
        
    return predResult


## 1. 인공신경망(tensorflow + keras), 정규화된 데이터를 입력해야 함!!!
def trainAndTestNeuralNetworks(dataset_open, dataset_closed, nTest=100, train_ratio=0.8, 
                               nNodesInLayer=20, nHiddenLayers=5, nEpoch = 50, Threshold=0.5,
                               batchSize=128, drop_out=0.3, doUpSampling=False):
    from keras import models
    from keras import layers
    from keras.utils import to_categorical    
    from keras import optimizers
    from sklearn import metrics
    
    ret = { 'P':[], 'N':[], 'TP':[], 'TN':[], 'FP':[], 'FN':[] }    
    
    ## up-sampling, down-sampling 해서 두 클래스간 데이터 비율 맞추기
    if ( doUpSampling == True ):
        data1, data2 = upsampling(dataset_open, dataset_closed)
    else:
        data1, data2 = downsampling(dataset_open, dataset_closed)        
    
    ret_roc_auc = []
    ret_fprs = []
    ret_tprs = []
    
    ## 학습 데이터(ratio)와 테스트 데이터(1-ratio)로 나누고 학습 및 예측 성능 측정
    for i in range(0, nTest):
        print('Test No.' + str(i+1))
        trainData, testData, trainLabel, testLabel = splitDataset(data1, data2, train_ratio)
        
        ## Make neural networks here!!!
        network = models.Sequential()
        ## Input layer
        network.add(layers.Dense(nNodesInLayer, activation='relu', input_shape=(len(trainData.columns),)))
        ## Add hidden layers
        for i in range(0, nHiddenLayers):
            network.add(layers.Dense(nNodesInLayer, activation='relu'))
            network.add(layers.Dropout(drop_out))
        network.add(layers.Dense(1, activation='sigmoid'))
        
        network.compile(optimizer='rmsprop',
                        loss='binary_crossentropy', metrics=['accuracy'])
        history = network.fit(trainData.to_numpy(), 
                              trainLabel,
                              batch_size=batchSize,
                              epochs=nEpoch)
        ## 예측 테스트
        pred_NN_orig = network.predict(testData)
        ## 예측결과 조정(0 또는 1로 조정)
        pred_NN = []
        pred_prob = []
        for j in range(0, len(pred_NN_orig)):
            pred_prob.append(pred_NN_orig[j][0])
            if ( pred_NN_orig[j][0] >= Threshold ):
                pred_NN.append(1)
            else:
                pred_NN.append(0)        
        
        ## 기초 성능통계자료 계산
        ( P, N, TP, TN, FP, FN ) = getStats(np.array(testLabel), np.array(pred_NN))
        
        ret['P'].append(P)
        ret['N'].append(N)
        ret['TP'].append(TP)
        ret['TN'].append(TN)
        ret['FP'].append(FP)
        ret['FN'].append(FN)

        ## AUC Curve 생성
        fpr, tpr, threshold = metrics.roc_curve(testLabel, np.array(pred_prob))
        
        ## AUC 값 계산
        roc_auc = metrics.auc(fpr, tpr)
        
        ret_roc_auc.append(roc_auc)
        ret_fprs.append(np.array(fpr))
        ret_tprs.append(np.array(tpr))
        
    ret = pd.DataFrame(ret)
    return (ret, ret_roc_auc, ret_fprs, ret_tprs)

(result_NNd, roc_auc_NNd, fprs_NNd, tprs_NNd) = \
    trainAndTestNeuralNetworks(dataset_open_norm, dataset_closed_norm,
                               nTest=100, train_ratio=0.8, nNodesInLayer=30, 
                               nHiddenLayers=5, nEpoch = 50, Threshold=0.5,
                               batchSize=128, drop_out=0.3, doUpSampling=False)

## 성능지표 계산
perf_NNd = getPerformance(result_NNd)
print(perf_NNd)

## 성능지표 평균 구하기
perf_NNd.mean(axis=0)

## AUC값 평균 구하기
np.mean(roc_auc_NNd)

## 2. 랜덤포레스트(Random Forest) nTest번 돌리고 결과를 DataFrame으로 리턴
def trainAndTestRandomForest(datasetOpen, datasetClosed, nTest = 100, nEstimators = 10, train_ratio = 0.8, doUpSampling = False):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import metrics
    
    ret = { 'P':[], 'N':[], 'TP':[], 'TN':[], 'FP':[], 'FN':[] }    
    
    ## up-sampling, down-sampling 해서 두 클래스간 데이터 비율 맞추기
    if ( doUpSampling == True ):
        data1, data2 = upsampling(datasetOpen, datasetClosed)
    else:
        data1, data2 = downsampling(datasetOpen, datasetClosed)
    
    ret_roc_auc = []
    ret_fprs = []
    ret_tprs = []           
    
    ## 학습 데이터(ratio)와 테스트 데이터(1-ratio)로 나누고 학습 및 예측 성능 측정
    for i in range(0, nTest):
        print('Test No.' + str(i+1))
        trainData, testData, trainLabel, testLabel = splitDataset(data1, data2, train_ratio)
        
        rf = RandomForestClassifier(n_estimators=nEstimators)
        model_rf = rf.fit(trainData, trainLabel)
        pred_rf = model_rf.predict(testData)
        pred_prob = model_rf.predict_proba(testData)
        pred_prob = pred_prob[:,1]

        ## 기본적인 통계자료 계산        
        ( P, N, TP, TN, FP, FN ) = getStats(np.array(testLabel), np.array(pred_rf))        
        
        ret['P'].append(P)
        ret['N'].append(N)
        ret['TP'].append(TP)
        ret['TN'].append(TN)
        ret['FP'].append(FP)
        ret['FN'].append(FN)

        ## AUC Curve 생성
        fpr, tpr, threshold = metrics.roc_curve(testLabel, pred_prob)
        
        ## AUC값 계산
        roc_auc = metrics.auc(fpr, tpr)
        
        ret_roc_auc.append(roc_auc)
        ret_fprs.append(np.array(fpr))
        ret_tprs.append(np.array(tpr))
        
    ret = pd.DataFrame(ret)
    return (ret, ret_roc_auc, ret_fprs, ret_tprs)

## 실행하기
(result_RFd, roc_auc_RFd, fprs_RFd, tprs_RFd) \
    = trainAndTestRandomForest(dataset_open, dataset_closed, 
                               nTest=100, nEstimators=50, train_ratio=0.8, 
                               doUpSampling = False)

## 성능지표 구하기
perf_RFd = getPerformance(result_RFd)
print(perf_RFd)

## 성능지표의 평균값 구하기
perf_RFd.mean(axis=0)

## AUC값의 평균 구하기
np.mean(roc_auc_RFd)

## 3. AdaBoost
def trainAndTestAdaBoost(datasetOpen, datasetClosed, nTest = 100, nEstimators = 10, learn_rate=0.1, train_ratio = 0.8, doUpSampling = False):
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn import metrics
    
    ret = { 'P':[], 'N':[], 'TP':[], 'TN':[], 'FP':[], 'FN':[] }    
    
    ## up-sampling, down-sampling 해서 두 클래스간 데이터 비율 맞추기
    if ( doUpSampling == True ):
        data1, data2 = upsampling(datasetOpen, datasetClosed)
    else:
        data1, data2 = downsampling(datasetOpen, datasetClosed)
    
    ret_roc_auc = []
    ret_fprs = []
    ret_tprs = []  
    
    ## 학습 데이터(ratio)와 테스트 데이터(1-ratio)로 나누고 학습 및 예측 성능 측정
    for i in range(0, nTest):
        print('Test No.' + str(i+1))
        trainData, testData, trainLabel, testLabel = splitDataset(data1, data2, train_ratio)
        
        abc = AdaBoostClassifier(n_estimators=nEstimators, learning_rate=learn_rate)
        model_abc = abc.fit(trainData, trainLabel)
        pred_abc = abc.predict(testData)
        pred_prob = model_abc.predict_proba(testData)
        pred_prob = pred_prob[:,1]
        
        ( P, N, TP, TN, FP, FN ) = getStats(np.array(testLabel), np.array(pred_abc))
        
        ret['P'].append(P)
        ret['N'].append(N)
        ret['TP'].append(TP)
        ret['TN'].append(TN)
        ret['FP'].append(FP)
        ret['FN'].append(FN)        

        ## AUC Curve 생성
        fpr, tpr, threshold = metrics.roc_curve(testLabel, pred_prob)
        
        ## AUC값 계산
        roc_auc = metrics.auc(fpr, tpr)
        
        ret_roc_auc.append(roc_auc)
        ret_fprs.append(np.array(fpr))
        ret_tprs.append(np.array(tpr))
        
    ret = pd.DataFrame(ret)
    return (ret, ret_roc_auc, ret_fprs, ret_tprs)

## AdaBoost with downsampling
(result_ADAd, roc_auc_ADAd, fprs_ADAd, tprs_ADAd) \
    = trainAndTestAdaBoost(dataset_open, dataset_closed, 
                           nTest=100, nEstimators=50, learn_rate=0.1, 
                           train_ratio=0.8, doUpSampling=False)

## 성능지표 구하기
perf_ADAd = getPerformance(result_ADAd)
print(perf_ADAd)

## 성능지표의 평균값 구하기
perf_ADAd.mean(axis=0)

## AUC값 평균 구하기
np.mean(roc_auc_ADAd)

## 4. XGBoost
def trainAndTestXGBoost(datasetOpen, datasetClosed, nTest = 100, nEstimators = 10, learning_rate=0.1, train_ratio = 0.8, doUpSampling = False):
    from xgboost import plot_importance
    from xgboost import XGBClassifier    
    from sklearn import metrics
    
    ret = { 'P':[], 'N':[], 'TP':[], 'TN':[], 'FP':[], 'FN':[] }    
    
    ## up-sampling, down-sampling 해서 두 클래스간 데이터 비율 맞추기
    if ( doUpSampling == True ):
        data1, data2 = upsampling(datasetOpen, datasetClosed)
    else:
        data1, data2 = downsampling(datasetOpen, datasetClosed)
    
    ret_roc_auc = []
    ret_fprs = []
    ret_tprs = []  
    
    ## 학습 데이터(ratio)와 테스트 데이터(1-ratio)로 나누고 학습 및 예측 성능 측정
    for i in range(0, nTest):
        print('Test No.' + str(i+1))
        trainData, testData, trainLabel, testLabel = splitDataset(data1, data2, train_ratio)
        
        xg = XGBClassifier(n_estimators=nEstimators, learning_rate=learning_rate)
        model_xg = xg.fit(trainData, trainLabel)
        pred_xg = xg.predict(testData)
        pred_prob = model_xg.predict_proba(testData)
        pred_prob = pred_prob[:,1]
        
        ( P, N, TP, TN, FP, FN ) = getStats(np.array(testLabel), np.array(pred_xg))
        
        ret['P'].append(P)
        ret['N'].append(N)
        ret['TP'].append(TP)
        ret['TN'].append(TN)
        ret['FP'].append(FP)
        ret['FN'].append(FN)
        
        ## AUC Curve 생성
        fpr, tpr, threshold = metrics.roc_curve(testLabel, pred_prob)
        
        ## AUC값 계산
        roc_auc = metrics.auc(fpr, tpr)
        
        ret_roc_auc.append(roc_auc)
        ret_fprs.append(np.array(fpr))
        ret_tprs.append(np.array(tpr))
    
    ret = pd.DataFrame(ret)
    return (ret, ret_roc_auc, ret_fprs, ret_tprs)

## Run XGBoost with downsampling
(result_XGd, roc_auc_XGd, fprs_XGd, tprs_XGd) = \
    trainAndTestXGBoost(dataset_open, dataset_closed, 
    nTest=100, nEstimators=50, learning_rate=0.1, train_ratio=0.8, doUpSampling=False)

## 성능지표 계산
perf_XGd = getPerformance(result_XGd)
print(perf_XGd)

## 성능지표의 평균 구하기
perf_XGd.mean(axis=1)

## AUC값 평균 구하기
np.mean(roc_auc_XGd)


## 5. 예측모형간 성능 비교(ROC 그래프 생성)

## 데이터 프레임 생성
roc = { 'NN':[], 'RF':[], 'ADA':[], 'XG':[] }

roc['NN'].append(perf_NNd.FP_Rate.mean())
roc['NN'].append(perf_NNd.TP_Rate.mean())
roc['RF'].append(perf_RFd.FP_Rate.mean())
roc['RF'].append(perf_RFd.TP_Rate.mean())
roc['ADA'].append(perf_ADAd.FP_Rate.mean())
roc['ADA'].append(perf_ADAd.TP_Rate.mean())
roc['XG'].append(perf_XGd.FP_Rate.mean())
roc['XG'].append(perf_XGd.TP_Rate.mean())

roc = pd.DataFrame(roc)
roc.rename({0:'FP_Rate',1:'TP_Rate'}, axis=0, inplace=True)
roc = roc.transpose()

## ROC 그래프 생성
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.scatter(roc.loc['NN'].FP_Rate, roc.loc['NN'].TP_Rate, 
           s=50, marker='+', c='green', label='NN')
ax.scatter(roc.loc['RF'].FP_Rate, roc.loc['RF'].TP_Rate, 
           s=50, marker='s', c='blue', label='RF')
ax.scatter(roc.loc['ADA'].FP_Rate, roc.loc['ADA'].TP_Rate, 
           s=50, marker='o', c='red', label='ADA')
ax.scatter(roc.loc['XG'].FP_Rate, roc.loc['XG'].TP_Rate, 
           s=50, marker='x', c='black', label='XG')
plt.legend(loc='upper left', fontsize=15)
plt.xlim([0.25,0.4])
plt.ylim([0.55,0.7])
plt.xlabel('FP Rate', fontsize=15)
plt.ylabel('TP Rate', fontsize=15)
plt.grid(color='k', linestyle='-', linewidth=0.5, alpha=0.2)
plt.xticks([0.25, 0.3, 0.35, 0.4], fontsize=15)
plt.yticks([0.55, 0.6, 0.65, 0.7],fontsize=15)


## AUC 그래프 생성

## AUC가 최대인 인덱스 구하기
auc_NNd_max = roc_auc_NNd.index(np.max(roc_auc_NNd))
auc_RFd_max = roc_auc_RFd.index(np.max(roc_auc_RFd))
auc_ADAd_max = roc_auc_ADAd.index(np.max(roc_auc_ADAd))
auc_XGd_max = roc_auc_XGd.index(np.max(roc_auc_XGd))

## AUC가 최대인 경우의 tprs, fprs 구하기
tprs_NNd_max = tprs_NNd[auc_NNd_max]
fprs_NNd_max = fprs_NNd[auc_NNd_max]
tprs_RFd_max = tprs_RFd[auc_RFd_max]
fprs_RFd_max = fprs_RFd[auc_RFd_max]
tprs_ADAd_max = tprs_ADAd[auc_ADAd_max]
fprs_ADAd_max = fprs_ADAd[auc_ADAd_max]
tprs_XGd_max = tprs_XGd[auc_XGd_max]
fprs_XGd_max = fprs_XGd[auc_XGd_max]

## AUC 그래프 그리기
import matplotlib.pyplot as plt

plt.plot(fprs_NNd_max, tprs_NNd_max, color='y', linewidth=2, label='NN')
plt.plot(fprs_RFd_max, tprs_RFd_max, color='r', linewidth=2, label='RF')
plt.plot(fprs_ADAd_max, tprs_ADAd_max, color='g', linewidth=2, label='ADA')    
plt.plot(fprs_XGd_max, tprs_XGd_max, color='b', linewidth=2, label='XG')       

plt.legend(loc='lower right', fontsize=15)
plt.plot([0, 1], [0, 1],'k--', linewidth=1)
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate',fontsize=15)
plt.xlabel('False Positive Rate', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show() 
