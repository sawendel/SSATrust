import pandas as pd
import numpy as np
import random


debugging = False


def getPIDs(dataDir, fileNames):
    pids = set()
    for theFileName in fileNames:
        dta = pd.read_csv(dataDir + theFileName)
        pids.update(dta.PID)
    return pids


def processTwoPartQualtricsTestResults(dataDir, dataFileName_p1, dataFileName_p2, dataFileName_prolific, surveyOutputFilesByVersion):
    dta_p1 = pd.read_csv(dataDir + dataFileName_p1)
    dta_profilic = pd.read_csv(dataDir + dataFileName_prolific)
    dta_p2 = pd.read_csv(dataDir + dataFileName_p2)
    dta_p2.drop(columns={'surveyArm'})

    dta = dta_p1.merge(dta_profilic, right_on="participant_id", left_on="PID", how="left")
    dta = dta.merge(dta_p2, right_on="PID", left_on="PID", how="left", suffixes=["", "_p2"])

    priorPids = getPIDs(dataDir, [surveyOutputFilesByVersion['1'], surveyOutputFilesByVersion['3']])

    return (dta, priorPids)


def getTestQuestions(surveyVersion):
    if surveyVersion == '1':  # There was an unintentional mistake in the SSA_Optout and Replacement Card in v3
        testQuestions = {'ImportantInformation': ('Real', 'Email', 'Amazon'),
                         'AmazonPayment': ('Fake', 'Email', 'Amazon'),
                         'AmazonDelay': ('Real', 'Email', 'Amazon'),
                         'RedCross': ('Fake', 'Email', 'RedCross'),
                         'Disability': ('Fake', 'Email', 'Lawyer'),
                         'ssa_optout': ('Fake', 'Email', 'SSA'),
                         'replacementCard': ('Real', 'Email', 'SSA'),
                         'annualReminderKLEW': ('Fake', 'Email', 'SSA'),
                         'lt_medicare': ('Real', 'Letter', 'SSA'),
                         'sms_disability': ('Fake', 'SMS', 'SSA'),
                         'lt_suspension': ('Fake', 'Letter', 'SSA'),
                         'sms_redcross': ('Real', 'SMS', 'RedCross')
                         }
    return testQuestions


def readData(surveyVersion):

    dataDir = "C:/Users/steve/Google Drive/Dev/src/SSATrust/SSATrust/data/"

    surveyOutputFilesByVersion = {'1': "V1/SSA_Y4_v1_SinglePart_April 19, 2022_16.25_clean.csv",
                    }

    # ###############
    # Get the data
    # ###############

    priorPids = None
    if surveyVersion == '1':
        dataFileName = surveyOutputFilesByVersion['1']
        dta = pd.read_csv(dataDir + dataFileName)

    outputFileName = "SSA_v" + str(surveyVersion)

    # remove empty columns
    dta = dta.dropna(axis=1, how='all')
    dta.surveyArm.fillna(value="Unknown", inplace=True)

    # Mark the Various Waves of the Study
    dta['StartDate'] = pd.to_datetime(dta.StartDate)

    # ###############
    # Tag Waves of Study over time
    # ###############

    dta['Wave'] = None
    dta['IsPrimaryWave'] = False


    if surveyVersion == 'LALA':  # Final Prolific
        dta['Wave'] = 1
        dta.loc[(dta.StartDate < '8/1/2021 23:59'), 'Wave'] = 1
        dta.loc[dta.Wave.isin([3]), "IsPrimaryWave"] = True
    else:
        dta.Wave = 1
        dta['IsPrimaryWave'] = True

    dta.rename(columns={'Previous Fraud':'previousFraud',    # From V5
                        'Previously_Targeted':'previousFraud', 'Lost_Money':'lose_money', # From v4
                        'Duration (in seconds)':'duration_p1',
                        'Duration (in seconds)_p2':'duration_p2'}, inplace=True)

    dta['previousFraudYN'] = ~dta.previousFraud.isna()
    dta['lose_moneyYN'] = dta.lose_money == "Yes"
    dta['duration_p1_Quantile'] = pd.qcut(dta.duration_p1, q=5, labels=False)
    dta['duration_p2_Quantile'] = pd.qcut(dta.duration_p2, q=5, labels=False)

    dta['daysFromTrainingToTest'] = (dta['StartDate_p2'].astype('datetime64') - dta['StartDate'].astype('datetime64')).dt.days

    return (dta, priorPids)



def cleanData(dta, priorPids, surveyVersion, testQuestions):
    # ###############
    # Do core data cleaning / filtering
    # ###############

    dta['cleanStatus'] = "Keep"
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta.PID.isin(priorPids)), 'cleanStatus'] = 'PID from prior version'

    if surveyVersion == '3':
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Duration (in seconds)'] < 60*3), 'cleanStatus'] = 'Too Fast'
    elif surveyVersion == '4':
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['status'] == 'RETURNED'), 'cleanStatus'] = 'Task Returned'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress_p2'].isna()), 'cleanStatus'] = 'No Second Round'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress_p2'] <= 95), 'cleanStatus'] = 'Incomplete Round 2'
    elif surveyVersion == '5P' or surveyVersion == '5D':
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['duration_p1'] < 60*2), 'cleanStatus'] = 'Too Fast'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress_p2'].isna()), 'cleanStatus'] = 'No Second Round'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress_p2'] <= 95), 'cleanStatus'] = 'Incomplete Round 2'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Consent_p2'] == 'No'), 'cleanStatus'] = 'No Consent Round 2'


    # dta.loc[(dta['cleanStatus'] == "Keep") & (dta['statusCode'] != 200), 'cleanStatus'] = 'Email Error'
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Consent'] == 'No'), 'cleanStatus'] = 'No Consent'
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress'] <= 95), 'cleanStatus'] = 'Incomplete'


    if (debugging):
        # dta.cleanStatus.value_counts(dropna=False)
        # Check for repeat Prolific users
        len(dta.PID.unique())/len(dta.PID)

    dta.sort_values('StartDate', inplace=True)  # This now sorts in date order
    dta['DuplicatedPID'] = False
    dta.loc[(dta['cleanStatus'] == "Keep"), 'DuplicatedCleanPID'] = dta.loc[(dta['cleanStatus'] == "Keep"), 'PID'].duplicated(keep='first')
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['DuplicatedCleanPID']), 'cleanStatus'] = 'Dup PID within current Version'

    # dta['DuplicatedIP'] = dta.IPAddress.duplicated(keep='first')
    # dta.loc[(dta['cleanStatus'] == "Keep") & (dta['DuplicatedIP']), 'cleanStatus'] = 'Dup IPAddress'

    dta['PID_Length'] = dta.PID.map(str).apply(len)
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta.PID_Length < 10), 'cleanStatus'] = 'Invalid PID'

    if (debugging):
        dta.cleanStatus.value_counts(dropna=False)

        dta['duration_p1'].describe()
        dta.loc[dta.surveyArm == "arm1_control", 'duration_p1'].describe()
        dta.loc[dta.surveyArm == "arm2_written_techniques", 'duration_p1'].describe()
        dta.loc[dta.surveyArm == "arm3_existingssa", 'duration_p1'].describe()
        dta.loc[dta.surveyArm == "arm4_interactive_training", 'duration_p1'].describe()

        dta.numReal.value_counts(dropna=False)
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.numReal == len(testQuestions.keys())), 'cleanStatus'] = 'Straightline_Real'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.numReal == 0), 'cleanStatus'] = 'Straightline_Fake'
        grouped = dta.groupby("surveyArm")
        grouped.agg(["count"])
        grouped.cleanStatus.value_counts(dropna=False, normalize=True)
        # Interesting -- this is STRONGLY by arm. The training arm isn't straightining, the others are.
        # So, not something we can clean on.


    # dta.cleanStatus.value_counts(dropna=False)
    dta = dta[dta.cleanStatus == "Keep"].copy()
    # dta = dta[dta.Wave==5].copy()

    return dta


def processDemographics(dta):

    # ################
    # Randomization
    # ################

    createRandomization = False
    if (createRandomization):
        dta['RAND'] = [random.randint(1, 2) for k in dta.index]
        dta.groupby(["RAND", "Wave", 'Ethnicity (Simplified)']).count()
        dta.groupby(["RAND", "Wave", 'Sex']).count()
        grouped = dta.groupby(["RAND", "Wave"])
        grouped.agg(["count"])
        grouped['Ethnicity (Simplified)'].count()
        grouped['Sex'].mean()


    # ##############
    # Demographic processing, etc
    # ##############
    dta['trustScore'] = dta['GeneralTrust'].replace({"Most people can't be trusted":0, "Most people can be trusted":1}) + \
                        dta['TakeAdvantage'].replace({"Would try to take advantage of you if they got a chance": 0, "Would try to be fair no matter what": 1}) + \
                        dta['TryToHelp'].replace({"Just look out for themselves": 0, "Try to help others": 1})

    dta['incomeAmount'] = dta['TotalIncome'].replace({"$0 - $19,999":10, "$20,000 - $39,999":30,
                        "$40,000 - $59,999":60, "$60,000 - $79,999":70, "$80,000 - $99,999":90,
                        "$100,000 - $149,999":125, "$150,000 or more":175})

    dta['race5'] = dta['Race'].replace({"White or Caucasian (Non-Hispanic)":'W',
                                               "Hispanic":'H',
                        "African American or African (Non-Hispanic)":'B',
                                               "Asian American or Asian":'A',
                                               "Native American, Native Hawaiian or Pacific Islander":'O',
                                        "White or Caucasian (Non-Hispanic),Hispanic": 'H',
                                        "White or Caucasian (Non-Hispanic),Native American, Native Hawaiian or Pacific Islander": 'O',
                                        'White or Caucasian (Non-Hispanic),African American or African (Non-Hispanic)':'B',
                                        'White or Caucasian (Non-Hispanic),African American or African (Non-Hispanic),Native American, Native Hawaiian or Pacific Islander':'O',
                                        'Asian American or Asian,Hispanic':'O',
                                        'Asian American or Asian,African American or African (Non-Hispanic)':'O',
                                        "White or Caucasian (Non-Hispanic),Asian American or Asian":'A',
                        "I prefer not to say":'O'})
    dta['employment3'] = dta['Employment'].replace({"Employed, working 1-29 hours per week": 'U',
                                           "Employed, working 30 or more hours per week": 'E',
                                           "Retired": 'R',
                                           "Not employed, looking for work": 'U',
                                           "Not employed, NOT looking for work": 'U',
                                           "Disabled, not able to work": 'R'})

    dta['educYears'] = dta['Education'].replace({"Some high school": 8,
                "High school degree or equivalent (e.g., GED)": 12,
                "Some college but no degree": 13, "Associate degree": 14,
                "Bachelor degree": 16,
                "Graduate or professional degree": 18})

    dta['marriedI'] = dta['Married'].replace({"Married": 1,
                                             "Divorced or Separated": 0,
                                             "Widowed": 0, "Single": 0,
                                             "I prefer not to say": None})

    dta['ageYears'] = dta['Age'].replace({"Under 18": 16,
                                             "18-24": 21.5,
                                             "25-34": 29.5, "35-44": 39.5,
                                             "45-54": 49.5,
                                             "55-64": 59.5,
                                             "65 or older": 69.5,
                                             "Prefer not to say": None})

    dta['genderI'] = dta['Gender'].replace({"Male": 0,
                                             "Female": 1,
                                             "Other": None})
    dta['ageYearsSq'] = dta.ageYears * dta.ageYears
    dta['lIncomeAmount'] = np.log(dta.incomeAmount)

    return dta


def markCorrectAnswers(dta, testQuestions):
    # ##############
    # Count Correct Answers
    # ##############

    # Setup Vars for tracking data on the # correct, etc.
    dta['numCorrect'] = 0
    dta['numFakeLabeledReal'] = 0 # It is FAKE, and the person thought it was a REAL
    dta['numRealLabeledFake'] = 0 # It is REAL, and the person thought it was a FAKE
    dta['numRealLabeledReal'] = 0 # It is REAL, and the person recognized it
    dta['numFakeLabeledFake'] = 0  # It is a FAKE, and the person recognized it

    dta['numEmailsCorrect'] = 0
    dta['numLettersCorrect'] = 0
    dta['numSMSesCorrect'] = 0

    dta['numCorrect_SSA'] = 0
    dta['numCorrect_Other'] = 0
    dta['numEmailsCorrect_SSA'] = 0
    dta['numEmailsCorrect_Other'] = 0

    dta['numLabeledReal'] = 0
    dta['numLabeledFake'] = 0
    dta['numNoAnswer'] = 0

    scoringVars = ['numCorrect', 'numEmailsCorrect', 'numLettersCorrect', 'numSMSesCorrect', 'numFakeLabeledReal', 'numRealLabeledFake',
                       'numRealLabeledReal', 'numFakeLabeledFake',  'numLabeledReal', 'numLabeledFake', 'numNoAnswer']

    for testQuestion in testQuestions.keys():
        # Get the correct answer
        correctAnswer = testQuestions[testQuestion][0]
        messageType = testQuestions[testQuestion][1]
        messageSender = testQuestions[testQuestion][2]

        # Increment each peron's correct count if they go it
        correctMask = dta[testQuestion] == correctAnswer
        dta.loc[correctMask, 'numCorrect'] = 1 + dta.loc[correctMask, 'numCorrect']

        if messageType == "Email":
            dta.loc[correctMask, 'numEmailsCorrect'] = 1 + dta.loc[correctMask, 'numEmailsCorrect']
        elif messageType == "Letter":
            dta.loc[correctMask, 'numLettersCorrect'] = 1 + dta.loc[correctMask, 'numLettersCorrect']
        elif messageType == "SMS":
            dta.loc[correctMask, 'numSMSesCorrect'] = 1 + dta.loc[correctMask, 'numSMSesCorrect']

        if messageSender == "SSA":
            dta.loc[correctMask, 'numCorrect_SSA'] = 1 + dta.loc[correctMask, 'numCorrect_SSA']
            if messageType == "Email":
                dta.loc[correctMask, 'numEmailsCorrect_SSA'] = 1 + dta.loc[correctMask, 'numEmailsCorrect_SSA']
        else:
            dta.loc[correctMask, 'numCorrect_Other'] = 1 + dta.loc[correctMask, 'numCorrect_Other']
            if messageType == "Email":
                dta.loc[correctMask, 'numEmailsCorrect_Other'] = 1 + dta.loc[correctMask, 'numEmailsCorrect_Other']


        # Create a new boolean var indicating, for each question, if they got it right
        dta['Correct_' + testQuestion] = (dta[testQuestion] == correctAnswer)
        scoringVars = scoringVars + ['Correct_' + testQuestion]

        # Dig into the response correct/incorrect to label as true positive / false positive , etc.
        if (correctAnswer == "Fake"):
            dta.loc[(dta[testQuestion] == "Real"), 'numFakeLabeledReal'] = 1 + dta.loc[(dta[testQuestion] == "Real"), 'numFakeLabeledReal']
            dta.loc[(dta[testQuestion] == "Fake"), 'numFakeLabeledFake'] = 1 + dta.loc[(dta[testQuestion] == "Fake"), 'numFakeLabeledFake']
        elif (correctAnswer == "Real"):
            dta.loc[(dta[testQuestion] == "Real"), 'numRealLabeledReal'] = 1 + dta.loc[(dta[testQuestion] == "Real"), 'numRealLabeledReal']
            dta.loc[(dta[testQuestion] == "Fake"), 'numRealLabeledFake'] = 1 + dta.loc[(dta[testQuestion] == "Fake"), 'numRealLabeledFake']
        else:
            raise Exception("Invalid Question Data")

        # Count how many total they marked as 'real' or 'fake'
        dta.loc[dta[testQuestion] == 'Real', 'numLabeledReal'] = 1 + dta.loc[dta[testQuestion] == 'Real', 'numLabeledReal']
        dta.loc[dta[testQuestion] == 'Fake', 'numLabeledFake'] = 1 + dta.loc[dta[testQuestion] == 'Fake', 'numLabeledFake']
        dta.loc[~(dta[testQuestion].isin(['Fake','Real'])), 'numNoAnswer'] = 1 + dta.loc[~(dta[testQuestion].isin(['Fake','Real'])), 'numNoAnswer']

    dta['percentCorrect'] = dta.numCorrect/len(testQuestions) * 100

    return dta