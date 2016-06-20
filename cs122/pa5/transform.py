# CS 122 W'16: Clean Pima Indians Diabetes Data
#
# Joseph Day

import pandas as pd
import csv
import random
import sys
import numpy as np


def go(raw_filename, training_filename, testing_filename):
    '''Given a raw_filename, training_filename, and testing_filename,
    cleans and transforms data in raw according to specifications of
    PA and then randomly splits into two groups, training and testing,
    which are then read into training and testing csv.
    '''
    pima = pd.read_csv(raw_filename)
    pima.drop(pima.columns[[3,4]], axis = 1, inplace = True)
    pima = pima[pima[" Diastolic Blood Pressure"] != 0]
    pima = pima[pima[" Plasma glucose level"] != 0]
    pima = pima[pima[" Body Mass Index"] != 0]
    pima = pima.dropna()

    pregnant = ["low", "medium", "high"]
    pima['Number of pregnancies'] = pd.cut(pima['Number of pregnancies'],
    bins = (0,2,6,float('inf')), right = False, labels = pregnant)

    plasma = pregnant
    pima[' Plasma glucose level'] = pd.cut(pima[' Plasma glucose level'],
    bins = (0.1,95,141,float('inf')), right = False, labels = plasma)

    diastolic_bp = ["normal", "pre-hypertension", "high"]
    pima[' Diastolic Blood Pressure'] = pd.cut(pima[' Diastolic Blood Pressure'],
    bins = (0.1, 80, 90, float('inf')), right = False, labels = diastolic_bp)

    bmi = ['low', 'healthy', 'overweight', 'obese', 'severely-obese']
    pima[' Body Mass Index'] = pd.cut(pima[' Body Mass Index'],
    bins = (0.1,18.5,25.1,30.1, 35.1, float('inf')), right = False, labels = bmi)

    diabetes_func = pregnant
    pima[' Diabetes Pedigree Function']  = pd.cut(pima[' Diabetes Pedigree Function'],
    bins = (0.1,0.42,0.82,float('inf')), right = False, labels = diabetes_func)

    age = ['r1', 'r2', 'r3']
    pima[' Age (in years)'] = pd.cut(pima[' Age (in years)'],
    bins = (0.1,41,60, float('inf')), right = False, labels = age)

    has_diabetes = ['no', 'yes']
    pima[' Has Diabetes (1 is yes and 0 is no)'] = pd.cut(pima[' Has Diabetes (1 is yes and 0 is no)'],
    bins = (0,0.1,1.1), right = False, labels = has_diabetes)

    sorter = np.random.rand(len(pima)) < 0.9
    train = pima[sorter]
    test = pima[~sorter]

    train.to_csv(training_filename, sep=',', index=False)
    test.to_csv(testing_filename, sep=',', index=False)

if __name__=="__main__":
    if len(sys.argv) != 4:
        print("usage: python3 {} <raw data filename> <training filename> <testing filename>".format(sys.argv[0]))
        sys.exit(1)

    go(sys.argv[1], sys.argv[2], sys.argv[3])

    
