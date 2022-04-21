import pandas as pd
import numpy as np
from DataProcessor import *
from ResultsAnalyzer import *
import random

debugging = False
trainingQuestions = {'ProtectYourself':'Real',
                    'AmazonHP':'Real',
                    'email_IRS': 'Scam',
                    'web_IRS': 'Real',
                    'apple':'Real',
                     'amazon_Product':'Scam',
                     'email_mcafee':'Real',
                     'GetProtected':'Scam',
                     }

def doIt(surveyVersion):

    testQuestions = getTestQuestions(surveyVersion)

    (dta,priorPids) = readData(surveyVersion)

    dta = cleanData(dta, priorPids, surveyVersion, testQuestions)

    dta = processDemographics(dta)

    dta = markCorrectAnswers(dta, testQuestions)

    scoringVars = ['numCorrect', 'numEmailsCorrect', 'numLettersCorrect', 'numSMSesCorrect', 'numFakeLabeledReal', 'numRealLabeledFake',
                           'numRealLabeledReal', 'numFakeLabeledFake', 'numLabeledReal', 'numLabeledFake', 'numNoAnswer']

    if (surveyVersion in ['5D', '5P']):
        scoringVars = scoringVars + ['NumHeadersOpened']

    analyzeResults(dta, outputFileName = surveyVersion, scoringVars = scoringVars, surveyVersion = surveyVersion,
                   primaryOnly= True)



# Default "Main"
if __name__ == '__main__':
    doIt("1")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
