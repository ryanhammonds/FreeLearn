#!/usr/bin/env python

import numpy as np
import csv
from math import sqrt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import GridSearchCV

data = np.genfromtxt('data.csv', delimiter=',')
target = np.genfromtxt('labels.txt')

X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.5, random_state=0)


n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt', 30, 60, 80]
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
min_samples_split = [2, 5, 10, 20]
min_samples_leaf = [1, 2, 4, 50, 80]
bootstrap = [True, False]
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")

clf = RandomForestClassifier()
#random_search = RandomizedSearchCV(estimator = clf, param_distributions = random_grid, n_iter = 100, cv = 5, verbose=2, random_state=2, n_jobs = 30)
#random_search.fit(X_train, y_train)
#report(random_search.cv_results_)

grid_search = GridSearchCV(clf, param_grid=random_grid, cv=5, n_jobs=30)
grid_search.fit(X_train, y_train)
report(grid_search.cv_results_)


#clf = RandomForestClassifier(n_estimators=50, max_features=round(sqrt(len(data[0]))), oob_score=True, n_jobs=30)
#scores = cross_val_score(clf, X_train, y_train, cv=5, n_jobs=30)
#print(scores)
