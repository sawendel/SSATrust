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

def getTrainingQuestions(surveyVersion):
    if surveyVersion in ('1', '2', '3'):
        trainingQuestions = {'ProtectYourself': ('Real', 'Email', 'Govt', 'protectYourself.html'),
                             'AmazonHP': ('Real', 'Web', 'Biz', 'amazonHP.html'),
                             'email_IRS': ('Scam', 'Email', 'Govt', 'irs.html'),
                             'web_IRS': ('Real', 'Web', 'Govt', 'IRS_YourAccount.html'),
                             'apple': ('Real', 'Web', 'Biz', 'appleID.html'),
                             'amazon_Product': ('Scam', 'Web', 'Biz', 'amazonProductPage.html'),
                             'email_mcafee': ('Real','Email', 'Biz', 'mcafee.html'),
                             'GetProtected': ('Scam','Email', 'Govt', 'getProtected.html'),
                        }
    elif surveyVersion in ('4'):
        trainingQuestions = {'ProtectYourself': ('Real', 'Email', 'Govt', 'protectYourself.html'),
                             'WalmartProduct': ('Real', 'Web', 'Biz', 'walmart.html'),
                             'email_IRS': ('Scam', 'Email', 'Govt', 'irs.html'),
                             'web_IRS': ('Real', 'Web', 'Govt', 'IRS_YourAccount.html'),
                             'apple': ('Real', 'Web', 'Biz', 'appleID.html'),
                             'amazon_Product': ('Scam', 'Web', 'Biz', 'amazonProductPage.html'),
                             'email_mcafee': ('Real','Email', 'Biz', 'mcafee.html'),
                             'GetProtected': ('Scam','Email', 'Govt', 'getProtected.html'),
                        }
    elif surveyVersion in ('5', '6', '7', '8'):
        trainingQuestions = {'ProtectYourself': ('Real', 'Email', 'Govt', 'protectYourself.html'),
                             'AmazonHP': ('Real', 'Web', 'Biz', 'amazonHP.html'),
                             'email_IRS': ('Scam', 'Email', 'Govt', 'irs.html'),
                             'web_IRS': ('Real', 'Web', 'Govt', 'IRS_YourAccount.html'),
                             'apple': ('Real', 'Web', 'Biz', 'appleID.html'),
                             'amazon_Product': ('Scam', 'Web', 'Biz', 'amazonProductPage.html'),
                             'email_mcafee': ('Real','Email', 'Biz', 'mcafee.html'),
                             'GetProtected': ('Scam','Email', 'Govt', 'getProtected.html'),
                        }

    return trainingQuestions


def getTestQuestions(surveyVersion):
    if surveyVersion in ('1', '2', '3'):
        testQuestions = {
                            'RedCross': ('Scam', 'Email', 'Biz', 'redcross_covidRelief.html'),
                            'SSA_HP': ('Real', 'Web', 'Govt', 'ssa.html'),
                            'mySSA': ('Scam', 'Web', 'Govt', 'mySocialSecurity.html'),
                            'AmazonDeliveryDelay': ('Real', 'Email', 'Biz', 'amazon_maskDelivery.html'),
                            'FB_SSA': ('Scam', 'Web', 'Biz', 'ssaFb.html'),
                            'ssa_optout': ('Scam', 'Email', 'Govt', 'ssa_optOut.html'),
                            'replacementCard': ('Real', 'Email', 'Govt', 'ssa_replacementCard.html'),
                            'WalmartProduct': ('Real', 'Web', 'Biz', 'walmart.html')
        }
    elif surveyVersion in ('4'):
        testQuestions = {
            'RedCross': ('Scam', 'Email', 'Biz', 'redcross_covidRelief.html'),
            'SSA_HP': ('Real', 'Web', 'Govt', 'ssa.html'),
            'mySSA': ('Scam', 'Web', 'Govt', 'mySocialSecurity.html'),
            'AmazonDeliveryDelay': ('Real', 'Email', 'Biz', 'amazon_maskDelivery.html'),
            'FB_SSA': ('Scam', 'Web', 'Biz', 'ssaFb.html'),
            'ssa_optout': ('Scam', 'Email', 'Govt', 'ssa_optOut.html'),
            'replacementCard': ('Real', 'Email', 'Govt', 'ssa_replacementCard.html'),
            'AmazonHP': ('Real', 'Web', 'Biz', 'amazonHP.html')
        }
    elif surveyVersion in ('5', '6'):
        testQuestions = {
                            'WalmartProduct': ('Real', 'Web', 'Biz', 'walmart.html'),
                            'RedCross': ('Scam', 'Email', 'Biz', 'redcross_covidRelief.html'),
                            'SSA_HP': ('Real', 'Web', 'Govt', 'ssa.html'),
                            'mySSA': ('Scam', 'Web', 'Govt', 'mySocialSecurity.html'),
                            'AmazonDeliveryDelay': ('Real', 'Email', 'Biz', 'amazon_maskDelivery.html'),
                            'FB_SSA': ('Scam', 'Web', 'Biz', 'ssaFb.html'),
                            'ssa_optout': ('Scam', 'Email', 'Govt', 'ssa_optOut.html'),
                            'replacementCard': ('Real', 'Email', 'Govt', 'ssa_replacementCard.html'),
                            'benefitsSuspension': ('Scam', 'Letter', 'Govt', 'benefitsSuspension.html'),
                            'medicareReview': ('Real', 'Letter', 'Govt', 'medicareReview.html'),
        }
    elif surveyVersion in ('7'):
        testQuestions = {
            'RedCross': ('Scam', 'Email', 'Biz', 'redcross_covidRelief.html'),
            'SSA_HP': ('Real', 'Web', 'Govt', 'ssa.html'),
            'mySSA': ('Scam', 'Web', 'Govt', 'mySocialSecurity.html'),
            'AmazonDeliveryDelay': ('Real', 'Email', 'Biz', 'amazon_maskDelivery.html'),
            'FB_SSA': ('Scam', 'Web', 'Biz', 'ssaFbClear.html'),
            'ssa_optout': ('Scam', 'Email', 'Govt', 'ssa_optOut.html'),
            'WalmartProduct': ('Real', 'Web', 'Biz', 'walmart.html'),
            'medicareReview': ('Real', 'Letter', 'Govt', 'medicareReview.html'),
            'replacementCard': ('Real', 'Email', 'Govt', 'ssa_replacementCardClean.html'),
            'benefitsSuspension': ('Scam', 'Letter', 'Govt', 'benefitsSuspension.html')
        }
    elif surveyVersion in ('8'): # TestWERLast
        testQuestions = {
            'WalmartProduct': ('Real', 'Web', 'Biz', 'walmart.html'),
            'RedCross': ('Scam', 'Email', 'Biz', 'redcross_covidRelief.html'),
            'SSA_HP': ('Real', 'Web', 'Govt', 'ssa.html'),
            'mySSA': ('Scam', 'Web', 'Govt', 'mySocialSecurity.html'),
            'AmazonDeliveryDelay': ('Real', 'Email', 'Biz', 'amazon_maskDelivery.html'),
            'FB_SSA': ('Scam', 'Web', 'Biz', 'ssaFbClear.html'),
            'ssa_optout': ('Scam', 'Email', 'Govt', 'ssa_optOut.html'),
            'medicareReview': ('Real', 'Letter', 'Govt', 'medicareReview.html'),
            'benefitsSuspension': ('Scam', 'Letter', 'Govt', 'benefitsSuspension.html'),
            'replacementCard': ('Real', 'Email', 'Govt', 'ssa_replacementCardClean.html'),
        }
    return testQuestions


def readData(surveyVersion, dataDir):

    surveyOutputFilesByVersion = {
        '1': ("V1/SSA_Y4_v1_SinglePart_April 20, 2022_09.26_clean.csv"),
        '2': ("V2/SSA_Y4_v2_FullApp_EntryPart_July 9, 2022_13.39_Clean.csv",
              "V2/SSA_Y4_v2_FullApp_AfterTraining_July 10, 2022_13.58_Clean.csv",
              "V2/SSA_Y4_v2_FullApp_FinalSection_July 10, 2022_13.57_Clean.csv",
              "V2/Mongo_logs_1657482882955.csv"),
        '3': ("V3/SSA_Y4_v2_FullApp_Entry_BBBOrProlific_July 13, 2022_18.48_Clean.csv",
              "V3/SSA_Y4_v2_FullApp_AfterTraining_July 13, 2022_18.48_Clean.csv",
              "V3/SSA_Y4_v2_FullApp_FinalSection_July 13, 2022_18.47_Clean.csv",
              "V3/Mongo_logs_1657759477983_13July.csv",
              "V3/SSA Lists_First20_NoPII.csv"),
        '4': ("V4_Walmart/SSA_Y4_v2_FullApp_Entry_BorP_TrainingOnly_July 19, 2022_22.18.csv",
              "V4_Walmart/SSA_Y4_v2_FullApp_AfterTraining_July 19, 2022_22.20.csv",
              "V4_Walmart/SSA_Y4_v2_FullApp_FinalSection_July 19, 2022_22.20.csv",
              "V4_Walmart/logs_1658290748789.csv",
              "V3/SSA Lists_First20_NoPII.csv"),
        '5': ("V5_WalmartEarlyInTest/SSA_Y4_v2_FullApp_Entry_BorP_TrainingOnly_July 24, 2022_21.04.csv",
              "V5_WalmartEarlyInTest/SSA_Y4_v2_FullApp_AfterTraining_July 24, 2022_21.03.csv",
              "V5_WalmartEarlyInTest/SSA_Y4_v2_FullApp_FinalSection_July 24, 2022_21.04.csv",
              "V5_WalmartEarlyInTest/logs_1658718293889.csv",
              "V3/SSA Lists_First20_NoPII.csv"),
        '6': ("V6_WalmartSimplified/SSA_Y4_v2_FullApp_Entry_BorP_TrainingOnly_July 26, 2022_06.50.csv",
              "V6_WalmartSimplified/SSA_Y4_v2_FullApp_AfterTraining_July 26, 2022_06.51.csv",
              "V6_WalmartSimplified/SSA_Y4_v2_FullApp_FinalSection_July 26, 2022_06.51.csv",
              "V6_WalmartSimplified/logs_1658839991300.csv",
              "V3/SSA Lists_First20_NoPII.csv"),
        '7': ("V7_FacebookAndReplacementCard/SSA_Y4_v2_FullApp_Entry_BorP_TrainingOnly_July 26, 2022_12.10.csv",
              "V7_FacebookAndReplacementCard/SSA_Y4_v2_FullApp_AfterTraining_July 26, 2022_12.10.csv",
              "V7_FacebookAndReplacementCard/SSA_Y4_v2_FullApp_FinalSection_July 26, 2022_12.11.csv",
              "V7_FacebookAndReplacementCard/logs_1658859121371.csv",
              "V3/SSA Lists_First20_NoPII.csv"),
        '8': ("v8_WalmartEarly_ReplacementEnd/SSA_Y4_v2_FullApp_Entry_BorP_TrainingOnly_July 27, 2022_09.07.csv",
              "v8_WalmartEarly_ReplacementEnd/SSA_Y4_v2_FullApp_AfterTraining_July 27, 2022_09.05.csv",
              "v8_WalmartEarly_ReplacementEnd/SSA_Y4_v2_FullApp_FinalSection_July 27, 2022_09.06.csv",
              "v8_WalmartEarly_ReplacementEnd/logs_1658934472618.csv",
              "V3/SSA Lists_First20_NoPII.csv")

    }

    # ###############
    # Get the data
    # ###############

    priorPids = None

    if surveyVersion == '1':
        dataFileName = surveyOutputFilesByVersion[surveyVersion][1]
        dta = pd.read_csv(dataDir + dataFileName)
    if surveyVersion in ('2', '3', '4', '5', '6', '7', '8'):
        p1File = surveyOutputFilesByVersion[surveyVersion][0]
        dta_p1_BeforeTraining = pd.read_csv(dataDir + p1File)

        p2File = surveyOutputFilesByVersion[surveyVersion][1]
        dta_p2_AfterTraining = pd.read_csv(dataDir + p2File)

        p3File = surveyOutputFilesByVersion[surveyVersion][2]
        dta_p3_Closing = pd.read_csv(dataDir + p3File)

        mongoFile = surveyOutputFilesByVersion[surveyVersion][3]
        mongoDta = pd.read_csv(dataDir + mongoFile)

        # Process the Training Responses directly after the opening demographics
        trainingQuestions = getTrainingQuestions(surveyVersion)
        dta = convertMongoToResponseHistory(dta_p1_BeforeTraining, mongoDta, trainingQuestions)
        dta['ExistInMongo_Training'] = dta[trainingQuestions.keys()].isin(["Scam", "Real","Both"]).any(axis=1)
        dta['MongoTraining_Complete'] = dta[trainingQuestions.keys()].isin(["Scam", "Real","Both"]).all(axis=1)
        # Pull in the survey questions in the middle - betweeen training and test
        dta = dta.merge(dta_p2_AfterTraining, left_on="PID", right_on="PID", how="left", suffixes=["", "_p2"])
        dta['ExistInPart2'] = ~dta['ResponseId_p2'].isna()
        # Process the Test Responses directly after the opening demographics
        testQuestions = getTestQuestions(surveyVersion)
        dta = convertMongoToResponseHistory(dta, mongoDta, testQuestions)
        dta['ExistInMongo_Test'] = dta[testQuestions.keys()].isin(["Scam", "Real","Both"]).any(axis=1)
        dta['MongoTest_Complete'] = dta[testQuestions.keys()].isin(["Scam", "Real","Both"]).all(axis=1)
        # Pull in the survey questions at the end
        dta = dta.merge(dta_p3_Closing, right_on="PID", left_on="PID", how="left", suffixes=["", "_p3"])
        dta['ExistInPart3'] = ~dta['ResponseId_p3'].isna()

    # remove empty columns
    # dta = dta.dropna(axis=1, how='all')
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

    return (dta, priorPids)


def convertMongoToResponseHistory(dta, mongoDta, questions):
    dta['NumWithHeadersOpened']=0
    dta['NumWithLinksClicked']=0

    for question in questions.keys():
        correctAnswer = questions[question][0]
        messageType = questions[question][1]
        messageSender = questions[question][2]
        mongoTemplateName = questions[question][3]

        dtaField_Answer = question
        dtaField_Clicked = question + "_Clicked"
        dtaField_Details = question + "_Details"

        mongoDtaForQuestion = mongoDta.loc[mongoDta.templateName == mongoTemplateName]
        mongoIds_MarkedReal = mongoDtaForQuestion.loc[mongoDta.eventType == 'marked_real']['userId'].unique()
        mongoIds_MarkedScam = mongoDtaForQuestion.loc[mongoDta.eventType == 'marked_scam']['userId'].unique()
        mongoIds_MarkedBoth = set(mongoIds_MarkedReal).intersection(set(mongoIds_MarkedScam))

        dta[dtaField_Answer] = None
        dta.loc[dta.PID.isin(mongoIds_MarkedReal), dtaField_Answer] = "Real"
        dta.loc[dta.PID.isin(mongoIds_MarkedScam), dtaField_Answer] = "Scam"
        dta.loc[dta.PID.isin(mongoIds_MarkedBoth), dtaField_Answer] = "Both"

        mongoIds_Clicked = mongoDtaForQuestion.loc[mongoDta.eventType == "link_clicked"]['userId'].unique()
        mongoIds_Details = mongoDtaForQuestion.loc[mongoDta.eventType.isin({'email_details_expanded', 'email_details_collapsed'})]['userId'].unique()

        dta[dtaField_Clicked] = None
        dta.loc[dta.PID.isin(mongoIds_Clicked), dtaField_Clicked] = "Click"
        dta['NumWithLinksClicked'] = dta['NumWithLinksClicked'] + (dta[dtaField_Clicked]=="Click")

        dta[dtaField_Details] = None
        dta.loc[dta.PID.isin(mongoIds_Details), dtaField_Details] = "Details"
        dta['NumWithHeadersOpened'] = dta['NumWithHeadersOpened'] + (dta[dtaField_Details]=="Details")


    return dta

def cleanData(dta, priorPids, surveyVersion, dataDir):
    testQuestions = getTestQuestions(surveyVersion)
    # ###############
    # Do core data cleaning / filtering
    # ###############

    dta.rename(columns={'Previous Fraud':'previousFraud',
                        'Duration (in seconds)':'duration_p1',
                        'Duration (in seconds)_p2':'duration_p2',
                        'Duration (in seconds)_p3':'duration_p3'}, inplace=True)

    dta['previousFraudYN'] = ~dta.previousFraud.isna()
    dta['lose_moneyYN'] = dta.lose_money == "Yes"
    dta['duration_p1_Quantile'] = pd.qcut(dta.duration_p1, q=5, labels=False)
    dta['duration_p2_Quantile'] = pd.qcut(dta.duration_p2, q=5, labels=False)
    dta['duration_p3_Quantile'] = pd.qcut(dta.duration_p3, q=5, labels=False)

    if surveyVersion in ('2', '3', '4', '5', '6', '7', '8'):
        dta['daysFromTrainingToTest'] = (dta['StartDate_p3'].astype('datetime64') - dta['StartDate'].astype('datetime64')).dt.days

    # dta['duration_p2_Quantile'] = pd.qcut(dta.duration_p2, q=5, labels=False)
    # dta['daysFromTrainingToTest'] = (dta['StartDate_p2'].astype('datetime64') - dta['StartDate'].astype('datetime64')).dt.days

    dta['cleanStatus'] = "Keep"
    if priorPids is not None:
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.PID.isin(priorPids)), 'cleanStatus'] = 'PID from prior version'

    if surveyVersion == '2':
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.Consent == 'No'), 'cleanStatus'] = 'No to Consent: First Survey'
    elif surveyVersion in ('3', '4', '5', '6', '7', '8'):
        dta.loc[(dta['cleanStatus'] == "Keep") & ((dta.Consent_Prolific == 'No') | (dta.Consent_BBB == 'No')), 'cleanStatus'] = 'No to Consent: First Survey'

    if surveyVersion in ('2', '3', '4', '5', '6', '7', '8'):
        # No such - only with time delay. dta.loc[(dta['cleanStatus'] == "Keep") & (dta.Consent_p2=='No'), 'cleanStatus'] = 'No to Consent: Second Survey'
        # No such - only with time delay.  dta.loc[(dta['cleanStatus'] == "Keep") & (dta.Consent_p3=='No'), 'cleanStatus'] = 'No to Consent: Third Survey'

        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.Progress <= 90), 'cleanStatus'] = 'Incomplete: First Survey'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.Progress_p2 <= 90), 'cleanStatus'] = 'Incomplete: Second Survey'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.Progress_p3 <= 90), 'cleanStatus'] = 'Incomplete: Third Survey'

        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['duration_p1'] < 60*2), 'cleanStatus'] = 'Too Fast'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.ExistInPart2 == False), 'cleanStatus'] = 'No Second Survey'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.ExistInMongo_Test == False), 'cleanStatus'] = 'No Test Results'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.MongoTest_Complete == False), 'cleanStatus'] = 'Test Results are Incomplete'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.ExistInPart3 == False), 'cleanStatus'] = 'No Third Survey'

    if (debugging):
        # dta.cleanStatus.value_counts(dropna=False)
        # Check for repeat Prolific users
        len(dta.PID.unique())/len(dta.PID)

    dta.sort_values('StartDate', inplace=True)  # This now sorts in date order
    dta['DuplicatedPID'] = False
    dta.loc[(dta['cleanStatus'] == "Keep"), 'DuplicatedCleanPID'] = dta.loc[(dta['cleanStatus'] == "Keep"), 'PID'].duplicated(keep='first')
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['DuplicatedCleanPID']), 'cleanStatus'] = 'Dup PID within current Version'

    dta.loc[(dta['cleanStatus'] == "Keep") & (~dta.KeepResponse.eq("Yes, use the responses.")), 'cleanStatus'] = 'Honesty Check Failed'


    # dta['DuplicatedIP'] = dta.IPAddress.duplicated(keep='first')
    # dta.loc[(dta['cleanStatus'] == "Keep") & (dta['DuplicatedIP']), 'cleanStatus'] = 'Dup IPAddress'

    dta['PID_Length'] = dta.PID.map(str).apply(len)
    if set(dta.columns).isdisjoint({"BID"}):
        dta['IsBBB'] = False
    else:
        dta['IsBBB'] = (~dta['BID'].isna())
    dta.loc[(dta['cleanStatus'] == "Keep") & (~dta.IsBBB) & (dta.PID_Length < 10), 'cleanStatus'] = 'Invalid PID'

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

    dta['ageYears'] = dta['Age_1']


    dta['genderI'] = dta['Gender'].replace({"Male": 0,
                                             "Female": 1,
                                             "Other": None})
    dta['ageYearsSq'] = dta.ageYears * dta.ageYears
    dta['lIncomeAmount'] = np.log(dta.incomeAmount)

    return dta


def markCorrectAnswers(dta, surveyVersion):
    testQuestions = getTestQuestions(surveyVersion)
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
    dta['numWebsitesCorrect'] = 0
    dta['numLettersCorrect'] = 0
    dta['numSMSesCorrect'] = 0

    dta['numCorrect_Govt'] = 0
    dta['numCorrect_Biz'] = 0
    dta['numEmailsCorrect_Govt'] = 0
    dta['numEmailsCorrect_Biz'] = 0
    dta['numWebsitesCorrect_Govt'] = 0
    dta['numWebsitesCorrect_Biz'] = 0

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
        elif messageType == "Web":
            dta.loc[correctMask, 'numWebsitesCorrect'] = 1 + dta.loc[correctMask, 'numWebsitesCorrect']
        elif messageType == "Letter":
            dta.loc[correctMask, 'numLettersCorrect'] = 1 + dta.loc[correctMask, 'numLettersCorrect']
        elif messageType == "SMS":
            dta.loc[correctMask, 'numSMSesCorrect'] = 1 + dta.loc[correctMask, 'numSMSesCorrect']

        if messageSender == "Govt":
            dta.loc[correctMask, 'numCorrect_Govt'] = 1 + dta.loc[correctMask, 'numCorrect_Govt']
            if messageType == "Email":
                dta.loc[correctMask, 'numEmailsCorrect_Govt'] = 1 + dta.loc[correctMask, 'numEmailsCorrect_Govt']
            elif messageType == "Web":
                dta.loc[correctMask, 'numWebsitesCorrect_Govt'] = 1 + dta.loc[correctMask, 'numWebsitesCorrect_Govt']
        elif messageSender == "Biz":
            dta.loc[correctMask, 'numCorrect_Biz'] = 1 + dta.loc[correctMask, 'numCorrect_Biz']
            if messageType == "Email":
                dta.loc[correctMask, 'numEmailsCorrect_Biz'] = 1 + dta.loc[correctMask, 'numEmailsCorrect_Biz']
            elif messageType == "Web":
                dta.loc[correctMask, 'numWebsitesCorrect_Biz'] = 1 + dta.loc[correctMask, 'numWebsitesCorrect_Biz']


        # Create a new boolean var indicating, for each question, if they got it right
        dta['Correct_' + testQuestion] = (dta[testQuestion] == correctAnswer)
        scoringVars = scoringVars + ['Correct_' + testQuestion]

        # Dig into the response correct/incorrect to label as true positive / false positive , etc.
        if (correctAnswer == "Scam"):
            dta.loc[(dta[testQuestion] == "Real"), 'numFakeLabeledReal'] = 1 + dta.loc[(dta[testQuestion] == "Real"), 'numFakeLabeledReal']
            dta.loc[(dta[testQuestion] == "Scam"), 'numFakeLabeledFake'] = 1 + dta.loc[(dta[testQuestion] == "Scam"), 'numFakeLabeledFake']
        elif (correctAnswer == "Real"):
            dta.loc[(dta[testQuestion] == "Real"), 'numRealLabeledReal'] = 1 + dta.loc[(dta[testQuestion] == "Real"), 'numRealLabeledReal']
            dta.loc[(dta[testQuestion] == "Scam"), 'numRealLabeledFake'] = 1 + dta.loc[(dta[testQuestion] == "Scam"), 'numRealLabeledFake']
        else:
            raise Exception("Invalid Question Data")

        # Count how many total they marked as 'real' or 'fake'
        dta.loc[dta[testQuestion] == 'Real', 'numLabeledReal'] = 1 + dta.loc[dta[testQuestion] == 'Real', 'numLabeledReal']
        dta.loc[dta[testQuestion] == 'Scam', 'numLabeledFake'] = 1 + dta.loc[dta[testQuestion] == 'Scam', 'numLabeledFake']
        dta.loc[~(dta[testQuestion].isin(['Scam','Real'])), 'numNoAnswer'] = 1 + dta.loc[~(dta[testQuestion].isin(['Scam','Real'])), 'numNoAnswer']

    dta['percentCorrect'] = dta.numCorrect/len(testQuestions) * 100

    return dta


def processTrust(dta):
    #dta['trustScore'] = dta['GeneralTrust'].replace({"Most people can't be trusted":0, "Most people can be trusted":1}) + \
    #                    dta['TakeAdvantage'].replace({"Would try to take advantage of you if they got a chance": 0, "Would try to be fair no matter what": 1}) + \
    #                    dta['TryToHelp'].replace({"Just look out for themselves": 0, "Try to help others": 1})

    dta.rename(columns={'govt_trust_1':'GovtConf1_Future',
                        'govt_trust_2':'GovtConf2_Feel',
                        'govt_trust_3':'GovtConf3_Trust',
                        'govt_trust_4': 'GovtConf4_Views'}, inplace=True)

    dta['GovtConfScore'] = (
                dta['GovtConf1_Future'].replace({"None at all": 1, "Very little": 2, "Some": 3, "Quite a lot": 4}) + \
                (4 - dta['GovtConf2_Feel'].replace({"Basically content": 1, "Frustrated": 2, "Angry": 3})) + \
                dta['GovtConf3_Trust'].replace(
                    {"Never": 1, "Only some of the time": 2, "Most of the time": 3, "Just about always": 4}) + \
                (3 - dta['GovtConf4_Views'].replace({"Government should do more to solve problems.": 1,
                                                     "Government is doing too many things better left to businesses and individuals.": 2})))

    # TrustInSSA_3	TrustInSSA_4	TrustInSSA_5	TrustInSSA_6	TrustInSSA_7	TrustInSSA_8	TrustInSSA_9	TrustInSSA_10
    likert7WeakToStrong = {"Strongly Disagree": 1, "Disagree": 2, "Slightly Disagree": 3,
                           "Neither Agree nor Disagree": 4, "Slightly Agree": 5, "Agree": 6, "Strongly Agree": 7}
    dta['TrustInSSAScore'] = (dta['ssa_trust_1'].replace(likert7WeakToStrong) + \
                              dta['ssa_trust_2'].replace(likert7WeakToStrong) + \
                              dta['ssa_trust_3'].replace(likert7WeakToStrong) + \
                              dta['ssa_trust_4'].replace(likert7WeakToStrong) + \
                              dta['ssa_trust_5'].replace(likert7WeakToStrong) + \
                              dta['ssa_trust_6'].replace(likert7WeakToStrong) + \
                              dta['ssa_trust_7'].replace(likert7WeakToStrong) + \
                              dta['ssa_trust_8'].replace(likert7WeakToStrong) + \
                              dta['ssa_trust_9'].replace(likert7WeakToStrong) + \
                              dta['ssa_trust_10'].replace(likert7WeakToStrong)) / 10

    # TrustInInternet_1	TrustInInternet_2	TrustInInternet_3	TrustInInternet_4	TrustInInternet_5	TrustInInternet_6	TrustInInternet_7	TrustInInternet_8
    dta['TrustInInternetScore'] = (dta['internet_trust_1'].replace(likert7WeakToStrong) + \
                                   dta['internet_trust_2'].replace(likert7WeakToStrong) + \
                                   dta['internet_trust_3'].replace(likert7WeakToStrong) + \
                                   dta['internet_trust_4'].replace(likert7WeakToStrong) + \
                                   (8 - dta['internet_trust_5'].replace(likert7WeakToStrong)) + \
                                   (8 - dta['internet_trust_6'].replace(likert7WeakToStrong)) + \
                                   (8 - dta['internet_trust_7'].replace(likert7WeakToStrong)) + \
                                   (8 - dta['internet_trust_8'].replace(likert7WeakToStrong))) / 8

    # OnlineShopping
    dta['OnlineShoppingScore'] = (dta['OnlineShopping'].replace({"Never": 1, "Once a year": 2,
                                                                 "Few times a year": 3, "Once a month": 4,
                                                                 "Once a week": 5, "Few times a week/Daily": 6}))

    dta['LonelyScore'] = (
                dta['Lonely1'].replace({"Hardly ever": 1, "Some of the time": 2, "Often": 3}) + \
                dta['Lonely2'].replace({"Hardly ever": 1, "Some of the time": 2, "Often": 3}) + \
                dta['Lonely3'].replace({"Hardly ever": 1, "Some of the time": 2, "Often": 3})
        )/3


    return dta
