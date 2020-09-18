from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from matplotlib import colors
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import GridSearchCV
import pickle
import time


import numpy as np
import matplotlib.pyplot as plt
from numpy import float as floaty
import csv
import pandas as pd


if __name__ == "__main__":

    #read data
    data = pd.read_csv("/Users/ryangould/Desktop/hammerTradeTrainData.csv", header = 0)
    #create models
    logisticRegr = LogisticRegression()
    knnModel = KNeighborsClassifier(n_neighbors=3)
    dTC = DecisionTreeClassifier()

    #normalize tail lengths
    maxTail = data['tailLength'].max()
    minTail = data['tailLength'].min()
    data['tailLength'] = data['tailLength'].apply(lambda x: (x - minTail)/(maxTail- minTail))

    #normalizing volumes
    maxVol = data['volume'].max()
    minVol = data['volume'].min()
    data['volume'] = data['volume'].apply(lambda x: (x - minVol)/(maxVol- minVol))

    #separating data from classifications
    x = data.drop('profitable', axis=1)
    print(x.iloc[0])
    y = data.profitable

    #split into training and test sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=4)

    #fit and predict models
    logisticRegr.fit(x_train, y_train)
    knnModel.fit(x_train, y_train)
    dTC.fit(x_train, y_train)

    knnYPred = knnModel.predict(x_test)
    y_pred = logisticRegr.predict(x_test)
    dTC_pred = dTC.predict(x_test)

    #print(y_pred)
    #print(knnYPred)

    #calculate model accuracies
    accuracy = metrics.accuracy_score(y_test, y_pred)
    accuracy_percentage = 100 * accuracy

    knnAccuracy = metrics.accuracy_score(y_test, knnYPred)
    knnAccuracy_percentage = 100 * knnAccuracy

    dtCAccuracy = metrics.accuracy_score(y_test, dTC_pred)
    dTCAccuracy_percentage = 100 * dtCAccuracy

    #confusion matricies
    logConfusionMatrix = confusion_matrix(y_test, y_pred)
    knnConfusionMatrix = confusion_matrix(y_test, knnYPred)
    dTCConfusionMatrix = confusion_matrix(y_test, dTC_pred)

    #find the importance of each feature in set
    importanceLR = logisticRegr.coef_[0]

    #subSet data to only include important features
    bestFit = data.filter(['SMA','tailLength','volume'], axis=1)
    bFx_train, bFx_test, bFy_train, bFy_test = train_test_split(bestFit, y, random_state=4)

    #create separate models to train with best fit data
    bFlogisticRegr = LogisticRegression()
    bFknnModel = KNeighborsClassifier(n_neighbors=2)
    bFdTC = DecisionTreeClassifier()

    #fit and predict best fit models
    bFlogisticRegr.fit(bFx_train, bFy_train)
    bFknnModel.fit(bFx_train, bFy_train)
    bFdTC.fit(bFx_train, bFy_train)

    neighbors = {'n_neighbors': np.arange(1, 10)}

    #use gridsearch to test all values for n_neighbors and find best n
    knnGS = GridSearchCV(bFknnModel, neighbors, cv=5)

    #using knn_best allows voting classifier to iterate over knn model
    knnGS.fit(bFx_train, y_train)
    knnBestFit = knnGS.best_estimator_
    print("neighbors:",knnBestFit)
    bFknnYPred = bFknnModel.predict(bFx_test)
    bFy_pred = bFlogisticRegr.predict(bFx_test)
    bFdTC_pred = bFdTC.predict(bFx_test)

    #calculate model accuracies
    bFaccuracy = metrics.accuracy_score(bFy_test, bFy_pred)
    bFaccuracy_percentage = 100 * bFaccuracy

    bFknnAccuracy = metrics.accuracy_score(bFy_test, bFknnYPred)
    bFknnAccuracy_percentage = 100 * bFknnAccuracy

    bFdtCAccuracy = metrics.accuracy_score(bFy_test, bFdTC_pred)
    bFdTCAccuracy_percentage = 100 * bFdtCAccuracy

    #confusion matricies
    bFlogConfusionMatrix = confusion_matrix(bFy_test, bFy_pred)
    bFknnConfusionMatrix = confusion_matrix(bFy_test, bFknnYPred)
    bFdTCConfusionMatrix = confusion_matrix(bFy_test, bFdTC_pred)

    #plots important features
    plt.title('Importance of Features')
    plt.xlabel('Feature')
    plt.ylabel('Importance')
    plt.bar([x for x in range(len(importanceLR))], importanceLR)

    estimators=[('knn', knnBestFit), ('log_reg', bFlogisticRegr), ('dtc', bFdTC)]

    #weighting LR as 2 yeilds overall highest accuracy for democracy
    democracy = VotingClassifier(estimators, voting='soft', weights=[1, 2, 1])
    democracy.fit(bFx_train, bFy_train)
    votes = democracy.predict(bFx_test)
    filename = '/Users/ryangould/Desktop/vc_model.sav'
    pickle.dump(democracy, open(filename, 'wb'))

    start = time.time()
    loaded_model = pickle.load(open(filename, 'rb'))
    end = time.time()
    print("time ", end - start)

    dAccuracy = metrics.accuracy_score(bFy_test, votes)
    dAccuracy_percentage = 100 * dAccuracy
    dConfusionMatrix = confusion_matrix(bFy_test, votes)


    #test voting classifier
    print(democracy.score(bFx_test, bFy_test))
    print("democracy:", dAccuracy)
    print("democracy:\n", dConfusionMatrix)

    probas = [c.fit(bFx_train, bFy_train).predict_proba(bFx_train) for c in (knnBestFit, bFlogisticRegr, bFdTC, democracy)]
    print("knn:", knnAccuracy_percentage)
    print("logR:", accuracy_percentage)
    print("dTC:", accuracy_percentage)

    print("knn matrix:\n", knnConfusionMatrix)
    print("logR matrix:\n", logConfusionMatrix)
    print("dTC\n:", dTCConfusionMatrix)

    print("bFknn:", bFknnAccuracy_percentage)
    print("bFlogR:", bFaccuracy_percentage)
    print("bFdTC:", bFaccuracy_percentage)

    print("bFknn matrix:\n", bFknnConfusionMatrix)
    print("bFlogR matrix:\n", bFlogConfusionMatrix)
    print("bFdTC\n:", bFdTCConfusionMatrix)
    print("data:\n",data['profitable'].value_counts())
    print("y_test value counts \n",y_test.value_counts())
    print("hourOfBuy value counts\n", data['hourOfBuy'].value_counts())
    #print(data.groupby('takeProfit').mean())
    #print(data.groupby('takeLoss').mean())
    #print(data.groupby('profitable').mean())
    print("hourOfBuy mean\n", data.groupby('hourOfBuy').mean())

    pd.crosstab(data.hourOfBuy,data.profitable).plot(kind='bar')
    plt.title('Profitable vs hourOfBuy')
    plt.xlabel('hourOfBuy')
    plt.ylabel('Profitable')
    #plt.show()

    pd.crosstab(data.takeProfit,data.profitable).plot(kind='bar')
    plt.title('Profitable vs takeProfit%')
    plt.xlabel('takeProfit%')
    plt.ylabel('Profitable')
    #plt.show()

    fig, axs = plt.subplots(1, 1, sharex=True, sharey=True,
                            tight_layout=True)
    axs.hist2d(data.SMA, data.profitable, bins=40, norm=colors.LogNorm())
    plt.title('Profitable vs SMA%')
    plt.xlabel('SMA%')
    plt.ylabel('Profitable')

    fig, ax1 = plt.subplots(tight_layout=True)
    hist1 = ax1.hist2d(data.tailLength,data.profitable, bins = 40, norm = colors.LogNorm())
    plt.title('Profitable vs tailLength')
    plt.xlabel('tailLength')
    plt.ylabel('Profitable')
    plt.show()