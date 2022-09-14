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

    dta = processFraud(dta)

    dta = processTrust(dta)

    dta = markCorrectAnswers(dta, surveyVersion)
    dta.to_csv(dataDir + "SSA_v" + str(surveyVersion) +"_Processed.csv")

    scoringVars = ['numCorrect', 'numCorrect_Govt', 'numCorrect_Biz',
                   'numEmailsCorrect', 'numWebsitesCorrect',
                   # 'numLettersCorrect', 'numSMSesCorrect',
                   'numFakeLabeledReal', 'numRealLabeledFake',
                    'numRealLabeledReal', 'numFakeLabeledFake', 'numLabeledReal', 'numLabeledFake', 'numNoAnswer']

    if (surveyVersion in ['8','9', '10', '11', '14', '15']):
        scoringVars = scoringVars + ['numLettersCorrect']

    if (surveyVersion in ['2', '3', '4', '5', '6', '7', '8','9', '10', '11', '14', '15']):
        scoringVars = scoringVars + ['NumWithHeadersOpened','NumWithLinksClicked']

    analyzeResults(dta, outputFileName = surveyVersion, scoringVars = scoringVars, surveyVersion = surveyVersion, dataDir = dataDir,
                   primaryOnly= True)



# Default "Main"
if __name__ == '__main__':
    # 3: First Nat Rep, Prolific, No Delay
    # 10: Final Nat Rep, Prolific, No Delay
    # 14: Final BBB, No Delay
    # 15: Final Nat Rep, Prolific, With Delay

    if True:
        doIt("3")
        print("Done with 3: First Nat Rep, Prolific, No Delay")
        doIt("10")
        print("Done with 10: Final Nat Rep, Prolific, No Delay")
        doIt("14")
        print("Done with 14: Final BBB, No Delay")
        doIt("15")
        print("Done with 15: Final Nat Rep, Prolific, With Delay")
