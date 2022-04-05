import pandas as pd
import numpy as np
from statsmodels.formula.api import ols

debugging = False

dataDir = "C:/Users/steve/Google Drive/Dev/sensitive_data/CFS/Y4/"
# dataFile = "Vetting Trust Measures_10March_2022_Clean.csv"
dataFile = "Vetting Trust Measures_22March_2022_Clean.csv"

dta = pd.read_csv(dataDir + dataFile, dtype={'pid': str})

############
# Filter Out Bad Data
############

# There was a problem with the display of the matrix questions on large screens.
# This showed up expecially with the Trust questions
dta = dta[~dta.TrustInInternet_1.isna()]

# dta.HonestyCheck.value_counts()
dta = dta[dta.HonestyCheck.eq("Yes, use the responses.")]

############
# Process Combined Scores
############

# SuscPersuasion_1	SuscPersuasion_2	SuscPersuasion_3	SuscPersuasion_4	SuscPersuasion_5	SuscPersuasion_6	SuscPersuasion_7	SuscPersuasion_8	SuscPersuasion_9	SuscPersuasion_10	SuscPersuasion_11	SuscPersuasion_12
likert7WeakToStrong = {"Strongly Disagree": 1, "Disagree": 2, "Slightly Disagree":3, "Neither Agree nor Disagree": 4, "Slightly Agree": 5, "Agree": 6, "Strongly Agree": 7}
dta['SuscPersuasionScore'] = (dta['SuscPersuasion_1'].replace(likert7WeakToStrong) + \
                    (8 - dta['SuscPersuasion_2'].replace(likert7WeakToStrong)) + \
                    dta['SuscPersuasion_3'].replace(likert7WeakToStrong) + \
                    dta['SuscPersuasion_4'].replace(likert7WeakToStrong) + \
                    (8 - dta['SuscPersuasion_5'].replace(likert7WeakToStrong)) + \
                    dta['SuscPersuasion_6'].replace(likert7WeakToStrong) + \
                    dta['SuscPersuasion_7'].replace(likert7WeakToStrong) + \
                    dta['SuscPersuasion_8'].replace(likert7WeakToStrong) + \
                    dta['SuscPersuasion_9'].replace(likert7WeakToStrong) + \
                    dta['SuscPersuasion_10'].replace(likert7WeakToStrong) + \
                    (8 - dta['SuscPersuasion_11'].replace(likert7WeakToStrong)) + \
                    dta['SuscPersuasion_12'].replace(likert7WeakToStrong) )/12

dta['SelfControlScore'] = (dta['SuscPersuasion_1'].replace(likert7WeakToStrong) + \
                    (8 - dta['SuscPersuasion_2'].replace(likert7WeakToStrong)) + \
                    dta['SuscPersuasion_3'].replace(likert7WeakToStrong))/3

dta['SuscPersuasionScore_NoSelfControl'] = ((dta['SuscPersuasionScore'] * 12) - (dta['SelfControlScore'] * 3))/8


# GenTrust_1	GenTrust_2	GenTrust_3	GenTrust_4	GenTrust_5	GenTrust_6

likert5WeakToStrong = {"Strongly disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly agree": 5}
dta['GenTrustScore'] = (dta['GenTrust_1'].replace(likert5WeakToStrong) + \
                    dta['GenTrust_2'].replace(likert5WeakToStrong) + \
                    dta['GenTrust_3'].replace(likert5WeakToStrong) + \
                    dta['GenTrust_4'].replace(likert5WeakToStrong) + \
                    dta['GenTrust_5'].replace(likert5WeakToStrong))/5

# GovtConf1_Future	GovtConf2_Feel	GovtConf3_Trust	GovtConf4_Views

dta['GovtConfScore'] = (dta['GovtConf1_Future'].replace({"None at all": 1, "Very little": 2, "Some":3, "Quite a lot":4}) + \
                        (4-dta['GovtConf2_Feel'].replace({"Basically content":1,  "Frustrated":2, "Angry":3})) + \
                        dta['GovtConf3_Trust'].replace({"Never":1,  "Only some of the time":2, "Most of the time":3, "Just about always":4}) + \
                        (3-dta['GovtConf4_Views'].replace({"Government should do more to solve problems.":1,  "Government is doing too many things better left to businesses and individuals.":2})) )

# TrustInSSA_3	TrustInSSA_4	TrustInSSA_5	TrustInSSA_6	TrustInSSA_7	TrustInSSA_8	TrustInSSA_9	TrustInSSA_10
dta['TrustInSSAScore'] = (dta['TrustInSSA_1'].replace(likert7WeakToStrong) + \
                    dta['TrustInSSA_2'].replace(likert7WeakToStrong) + \
                    dta['TrustInSSA_3'].replace(likert7WeakToStrong) + \
                    dta['TrustInSSA_4'].replace(likert7WeakToStrong) + \
                    dta['TrustInSSA_5'].replace(likert7WeakToStrong) + \
                    dta['TrustInSSA_6'].replace(likert7WeakToStrong) + \
                    dta['TrustInSSA_7'].replace(likert7WeakToStrong) + \
                    dta['TrustInSSA_8'].replace(likert7WeakToStrong) + \
                    dta['TrustInSSA_9'].replace(likert7WeakToStrong) + \
                    dta['TrustInSSA_10'].replace(likert7WeakToStrong) )/10

# TrustInInternet_1	TrustInInternet_2	TrustInInternet_3	TrustInInternet_4	TrustInInternet_5	TrustInInternet_6	TrustInInternet_7	TrustInInternet_8
dta['TrustInInternetScore'] = (dta['TrustInInternet_1'].replace(likert7WeakToStrong) + \
                    dta['TrustInInternet_2'].replace(likert7WeakToStrong) + \
                    dta['TrustInInternet_3'].replace(likert7WeakToStrong) + \
                    dta['TrustInInternet_4'].replace(likert7WeakToStrong) + \
                    (8-dta['TrustInInternet_5'].replace(likert7WeakToStrong)) + \
                    (8-dta['TrustInInternet_6'].replace(likert7WeakToStrong)) + \
                    (8-dta['TrustInInternet_7'].replace(likert7WeakToStrong)) + \
                    (8-dta['TrustInInternet_8'].replace(likert7WeakToStrong)) )/8

# OnlineShopping
dta['OnlineShoppingScore'] = (dta['OnlineShopping'].replace({"Never": 1, "Once a year": 2,
                    "Few times a year":3, "Once a month":4,"Once a week":5, "Few times a week/Daily":6}))

# Get the data we want to keep
toExtract = dta[['PID', 'GovtConfScore', 'SuscPersuasionScore', 'SelfControlScore', 'SuscPersuasionScore_NoSelfControl', 'GenTrustScore',
                 'TrustInSSAScore', 'TrustInInternetScore','OnlineShoppingScore',
                 'GovtConf1_Future', 'GovtConf2_Feel', 'GovtConf3_Trust', 'GovtConf4_Views']]

##########
# Get the Prior data we have on these people
##########

y3DataDir = "C:/Users/steve/Google Drive/Dev/src/SSAScams/data/"
fieldsToKeep = ['PID','surveyArm','trustScore','incomeAmount','race5','employment3','educYears','marriedI','ageYears','genderI','ageYearsSq',\
'lIncomeAmount','numCorrect','numFakeLabeledReal','numRealLabeledFake','numRealLabeledReal','numFakeLabeledFake',\
'numEmailsCorrect','numLettersCorrect','numSMSesCorrect','numCorrect_SSA','numCorrect_Other','numEmailsCorrect_SSA',\
'numEmailsCorrect_Other','numLabeledReal','numLabeledFake','numNoAnswer','percentCorrect']

r4 = pd.read_excel(y3DataDir + 'Results/RESULTS_4.xlsx', sheet_name='theData')
r4 = r4[fieldsToKeep]
r4['TestRound'] = 4

r6 = pd.read_excel (y3DataDir + 'Results/RESULTS_6_BothWaves.xlsx', sheet_name='theData')
r6 = r6[fieldsToKeep]
r6['TestRound'] = 6

r46 = pd.concat([r4, r6])


cDta = pd.merge(r46, toExtract, on='PID', how='right')

cDta = cDta[~cDta.TestRound.isna()]

cDta.to_csv(dataDir + "CombinedData_VettingTrustMeasures.csv")


##########
# Run some simple analyses
##########

''' Analyze the answers'''
writer = pd.ExcelWriter(dataDir + 'RESULTS_VettingTrustMeasures.xlsx', engine='xlsxwriter')

# Basic Summary Stats
summaryStats = cDta.describe()
summaryStats.to_excel(writer, sheet_name="summary", startrow=0, header=True, index=True)

cDta[['GenTrustScore','educYears','marriedI','ageYears','genderI','lIncomeAmount']].corr()
result = ols('numCorrect ~ C(surveyArm) + GenTrustScore + educYears + marriedI + ageYears + genderI + lIncomeAmount', data=cDta).fit().summary()
resultTables = result.tables

ols('numCorrect ~ C(surveyArm) + GenTrustScore', data=cDta).fit().summary() # Nothing
ols('numCorrect ~ C(surveyArm) + SuscPersuasionScore', data=cDta).fit().summary() # Nothing
ols('numCorrect ~ C(surveyArm) + TrustInSSAScore', data=cDta).fit().summary()  # Bingo, but small effect
ols('numCorrect ~ C(surveyArm) + TrustInInternetScore', data=cDta).fit().summary()  # Bingo, larger effect
ols('numCorrect ~ C(surveyArm) + OnlineShoppingScore', data=cDta).fit().summary()  # Bingo, largest effect

ols('numFakeLabeledReal ~ C(surveyArm) + GenTrustScore', data=cDta).fit().summary() # Nothing
ols('numFakeLabeledReal ~ C(surveyArm) + SuscPersuasionScore', data=cDta).fit().summary() # Yes, strong
ols('numFakeLabeledReal ~ C(surveyArm) + TrustInSSAScore', data=cDta).fit().summary()  # Bingo, Moderate effect
ols('numFakeLabeledReal ~ C(surveyArm) + TrustInInternetScore', data=cDta).fit().summary()  # Nothing
ols('numFakeLabeledReal ~ C(surveyArm) + OnlineShoppingScore', data=cDta).fit().summary()  # Bingo, Moderate effect

ols('numRealLabeledFake ~ C(surveyArm) + GenTrustScore', data=cDta).fit().summary() # Nothing
ols('numRealLabeledFake ~ C(surveyArm) + SuscPersuasionScore', data=cDta).fit().summary() # BINGO
ols('numRealLabeledFake ~ C(surveyArm) + TrustInSSAScore', data=cDta).fit().summary()  # Nothing
ols('numRealLabeledFake ~ C(surveyArm) + TrustInInternetScore', data=cDta).fit().summary()  # BINGO
ols('numRealLabeledFake ~ C(surveyArm) + OnlineShoppingScore', data=cDta).fit().summary()  # Bingo

ols('numCorrect ~ C(surveyArm) + GovtConfScore', data=cDta).fit().summary()  # Nothing
ols('numRealLabeledFake ~ C(surveyArm) + GovtConfScore', data=cDta).fit().summary() # Nothing
ols('numFakeLabeledReal ~ C(surveyArm) + GovtConfScore', data=cDta).fit().summary()  # Nothing

ols('numCorrect ~ C(surveyArm) + GovtConf1_Future', data=cDta).fit().summary()  # Bingo, largest effect
ols('numRealLabeledFake ~ C(surveyArm) + GovtConf1_Future', data=cDta).fit().summary() # Strong
ols('numFakeLabeledReal ~ C(surveyArm) + GovtConf1_Future', data=cDta).fit().summary()  # Bingo, Moderate effect

ols('numCorrect ~ C(surveyArm) + GovtConf2_Feel', data=cDta).fit().summary()  # Bingo, largest effect
ols('numRealLabeledFake ~ C(surveyArm) + GovtConf2_Feel', data=cDta).fit().summary() # Nothing
ols('numFakeLabeledReal ~ C(surveyArm) + GovtConf2_Feel', data=cDta).fit().summary()  # Bingo, Moderate effect

ols('numCorrect ~ C(surveyArm) + SelfControlScore', data=cDta).fit().summary()  # Nothing
ols('numRealLabeledFake ~ C(surveyArm) + SelfControlScore', data=cDta).fit().summary() # Bingo
ols('numFakeLabeledReal ~ C(surveyArm) + SelfControlScore', data=cDta).fit().summary()  # Nothing

ols('numRealLabeledFake ~ C(surveyArm) + SelfControlScore + SuscPersuasionScore_NoSelfControl', data=cDta).fit().summary() # All power comes from the Self Control Measure
ols('numFakeLabeledReal ~ C(surveyArm) + SelfControlScore + SuscPersuasionScore_NoSelfControl', data=cDta).fit().summary()  # Only OTHER parts of the persuasion score. Not the self-control
