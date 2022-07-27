import pandas as pd
import numpy as np
from InputProcessor import *
from ResultsAnalyzer import *
import random

debugging = False

dataDir = "C:/Users/steve/Google Drive/Dev/src/SSATrust/SSATrust/data/"

def doIt(surveyVersion):

    (dta,priorPids) = readData(surveyVersion, dataDir)
    dta.to_csv(dataDir + "SSA_v" + str(surveyVersion) +"_Combined.csv")

    dta = cleanData(dta, priorPids, surveyVersion, dataDir)
    dta.to_csv(dataDir + "SSA_v" + str(surveyVersion) +"_WithCleanFlag.csv")
    dta = dta[dta.cleanStatus == "Keep"].copy()

    dta = processDemographics(dta)

    dta = processTrust(dta)

    dta = markCorrectAnswers(dta, surveyVersion)
    dta.to_csv(dataDir + "SSA_v" + str(surveyVersion) +"_Processed.csv")

    scoringVars = ['numCorrect', 'numCorrect_Govt', 'numCorrect_Biz',
                   'numEmailsCorrect', 'numWebsitesCorrect',
                   # 'numLettersCorrect', 'numSMSesCorrect',
                   'numFakeLabeledReal', 'numRealLabeledFake',
                    'numRealLabeledReal', 'numFakeLabeledFake', 'numLabeledReal', 'numLabeledFake', 'numNoAnswer']

    if (surveyVersion in ['2', '3', '4', '5', '6', '7']):
        scoringVars = scoringVars + ['NumWithHeadersOpened','NumWithLinksClicked']

    analyzeResults(dta, outputFileName = surveyVersion, scoringVars = scoringVars, surveyVersion = surveyVersion, dataDir = dataDir,
                   primaryOnly= True)



# Default "Main"
if __name__ == '__main__':
    doIt("7")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
