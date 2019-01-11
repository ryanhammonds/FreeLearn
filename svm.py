#!/usr/bin/env python

import numpy as np
import csv
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
from sklearn import svm
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

# load data
data = np.genfromtxt('volsTrans.csv', delimiter=',')
target = np.genfromtxt('labels.txt')

# randomly split data into test and training arrays
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.5)

# apply mean and variance center
scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train) 
X_test = scaler.transform(X_test)

'''
clf = svm.SVC(kernel='rbf', C=20, gamma = 0.00017)
clf.fit(X_train, y_train)
clf.predict(X_test)
print(clf.score(X_test, y_test))
'''

cost = np.arange(0, 1010, 10)
cost = [int(i) for i in cost]
cost[0] = 1

gamma = np.arange(0.0000, 0.001, 0.00001)
gamma = [float(i) for i in gamma]

tuned_parameters = [{'kernel': ['rbf'], 'gamma': gamma, 'C': cost}, {'kernel': ['linear'], 'C': cost}, {'kernel': ['poly'], 'gamma': gamma, 'C': cost}, {'kernel': ['sigmoid'], 'gamma': gamma, 'C': cost}]
scores = ['precision', 'recall']

for score in scores:
	clf = GridSearchCV(SVC(class_weight='balanced'), tuned_parameters, cv=5, n_jobs=20, scoring='%s_macro' % score)
	clf.fit(X_train, y_train)
	means = clf.cv_results_['mean_test_score']
	stds = clf.cv_results_['std_test_score']
	y_true, y_pred = y_test, clf.predict(X_test)
	

	print("# Tuning hyper-parameters for %s" % score)
	print()
	print("Best parameters set found on development set:")
	print()
	print(clf.best_params_)
	print()
	print("Grid scores on development set:")
	print()
	for mean, std, params in zip(means, stds, clf.cv_results_['params']):
			if mean > 0.6:
				print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
	print()
	print("Detailed classification report:")
	print()
	print("The model is trained on the full development set.")
	print("The scores are computed on the full evaluation set.")
	print()
	print(classification_report(y_true, y_pred))
	print()

