import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from swstats import *
from scipy.stats import ttest_ind
import xlsxwriter
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportions_ztest

debugging = False

def pToSign(pval):
    if pval < .001:
        return "***"
    elif pval < .01:
        return "**"
    elif pval < .05:
        return "*"
    elif pval < .1:
        return "+"
    else:
        return ""

def analyzeExperiment_ContinuousVar(dta, varName):

    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", varName]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_generalinfo", varName]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_tips", varName]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_interactive", varName]


    # Arm 1
    arm1mean = np.mean(order_value_control_group)
    arm1sd = np.std(order_value_control_group)
    arm1text = "" + "{:.2f}".format(arm1mean) + " (" + "{:.2f}".format(arm1sd) + ")"

    # Effect of Arm 2
    arm2mean = np.mean(order_value_arm2_group)
    arm2sd = np.std(order_value_arm2_group)
    tscore, pval2 = ttest_ind(order_value_control_group, order_value_arm2_group)
    arm2sign = pToSign(pval2)
    arm2text = "" + "{:.2f}".format(arm2mean) + " (" + "{:.2f}".format(arm2sd) + ")" + arm2sign + " p:"  + "{:.3f}".format(pval2)

    # Effect of Arm 3
    arm3mean = np.mean(order_value_arm3_group)
    arm3sd = np.std(order_value_arm3_group)
    tscore, pval3 = ttest_ind(order_value_control_group, order_value_arm3_group)
    arm3sign = pToSign(pval3)
    arm3text = "" + "{:.2f}".format(arm3mean) + " (" + "{:.2f}".format(arm3sd) + ")" + arm3sign + " p:"  + "{:.3f}".format(pval3)

    # Effect of Arm 4
    arm4mean = np.mean(order_value_arm4_group)
    arm4sd = np.std(order_value_arm4_group)
    tscore, pval4 = ttest_ind(order_value_control_group, order_value_arm4_group)
    arm4sign = pToSign(pval4)
    arm4text = "" + "{:.2f}".format(arm4mean) + " (" + "{:.2f}".format(arm4sd) + ")" + arm4sign + " p:"  + "{:.3f}".format(pval4)

    # Correct P-values
    y = multipletests(pvals=[pval2, pval3, pval4], alpha=0.05, method="holm")
    # print(len(y[1][np.where(y[1] < 0.05)]))  # y[1] returns corrected P-vals (array)
    sigWithCorrection = y[1] < 0.05
    if sigWithCorrection[0]:
        arm2text = arm2text + ",#"
    if sigWithCorrection[1]:
        arm3text = arm3text + ",#"
    if sigWithCorrection[2]:
        arm4text = arm4text + ",#"

    # Additional checks
    tscore, pval2to4 = ttest_ind(order_value_arm2_group, order_value_arm4_group)
    arm2to4sign = pToSign(pval2to4)
    arm2to4text = "" + "{:.2f}".format(arm4mean - arm2mean) + " " + arm2to4sign + " p:" + "{:.3f}".format(pval2to4)

    tscore, pval3to4 = ttest_ind(order_value_arm3_group, order_value_arm4_group)
    arm3to4sign = pToSign(pval3to4)
    arm3to4text = "" + "{:.2f}".format(arm4mean - arm3mean) + " " + arm3to4sign + " p:" + "{:.3f}".format(pval3to4)


    results = {"Outcome": varName,
         "Arm1": arm1text,
         "Arm2": arm2text,
         "Arm3": arm3text,
         "Arm4": arm4text,
         "Arm2To4": arm2to4text,
         "Arm3To4": arm3to4text,
        }

    return results

def analyzeExperiment_BinaryVar(dta, varName):

    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", varName]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_generalinfo", varName]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_tips", varName]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_interactive", varName]

    # Arm 1
    arm1Successes = sum(order_value_control_group.isin([True, 1]))
    arm1Count = sum(order_value_control_group.isin([True, False, 1, 0]))
    arm1PercentSuccess = arm1Successes/arm1Count
    arm1text = "" + "{:.2f}".format(arm1PercentSuccess) + " (" + "{:.0f}".format(arm1Successes) + ")"

    # Effect of Arm 2
    arm2Successes = sum(order_value_arm2_group.isin([True, 1]))
    arm2Count = sum(order_value_arm2_group.isin([True, False, 1, 0]))
    if arm2Count == 0:
        arm2Count = 1
    arm2PercentSuccess = arm2Successes/arm2Count
    zstat, pval2 = proportions_ztest(count=[arm1Successes,arm2Successes], nobs=[arm1Count,arm2Count], alternative='two-sided')
    arm2sign = pToSign(pval2)
    arm2text = "" + "{:.2f}".format(arm2PercentSuccess) + " (" + "{:.0f}".format(arm2Successes) + ")" + arm2sign + " p:"  + "{:.3f}".format(pval2)

    # Effect of Arm 3
    arm3Successes = sum(order_value_arm3_group.isin([True, 1]))
    arm3Count = sum(order_value_arm3_group.isin([True, False, 1, 0]))
    if arm3Count == 0:
        arm3Count = 1
    arm3PercentSuccess = arm3Successes/arm3Count
    zstat, pval3 = proportions_ztest(count=[arm1Successes,arm3Successes], nobs=[arm1Count,arm3Count], alternative='two-sided')
    arm3sign = pToSign(pval3)
    arm3text = "" + "{:.2f}".format(arm3PercentSuccess) + " (" + "{:.0f}".format(arm3Successes) + ")" + arm3sign + " p:"  + "{:.3f}".format(pval3)

    # Effect of Arm 4
    arm4Successes = sum(order_value_arm4_group.isin([True, 1]))
    arm4Count = sum(order_value_arm4_group.isin([True, False, 1, 0]))
    arm4PercentSuccess = arm4Successes/arm4Count
    zstat, pval4 = proportions_ztest(count=[arm1Successes,arm4Successes], nobs=[arm1Count,arm4Count], alternative='two-sided')
    arm4sign = pToSign(pval4)
    arm4text = "" + "{:.2f}".format(arm4PercentSuccess) + " (" + "{:.0f}".format(arm4Successes) + ")" + arm4sign + " p:"  + "{:.3f}".format(pval4)

    # Correct P-values
    y = multipletests(pvals=[pval2, pval3, pval4], alpha=0.05, method="holm")
    # print(len(y[1][np.where(y[1] < 0.05)]))  # y[1] returns corrected P-vals (array)
    sigWithCorrection = y[1] < 0.05
    if sigWithCorrection[0]:
        arm2text = arm2text + ",#"
    if sigWithCorrection[1]:
        arm3text = arm3text + ",#"
    if sigWithCorrection[2]:
        arm4text = arm4text + ",#"

    # Additional checks
    zstat, pval2to4 = proportions_ztest(count=[arm2Successes,arm4Successes], nobs=[arm2Count,arm4Count], alternative='two-sided')
    arm2to4sign = pToSign(pval2to4)
    arm2to4text = "" + "{:.2f}".format(arm4PercentSuccess - arm2PercentSuccess) + " " + arm2to4sign + " p:" + "{:.3f}".format(pval2to4)

    zstat, pval3to4 = proportions_ztest(count=[arm3Successes,arm4Successes], nobs=[arm3Count,arm4Count], alternative='two-sided')
    arm3to4sign = pToSign(pval3to4)
    arm3to4text = "" + "{:.2f}".format(arm4PercentSuccess - arm3PercentSuccess) + " " + arm3to4sign + " p:" + "{:.3f}".format(pval3to4)

    results = {"Outcome": varName,
         "Arm1": arm1text,
         "Arm2": arm2text,
         "Arm3": arm3text,
         "Arm4": arm4text,
         "Arm2To4": arm2to4text,
         "Arm3To4": arm3to4text,
        }

    return results

# #####################
# Rename key variables to align directly with Study Design
# #####################
def renameForAnalysis(dta):
    dta.rename(columns={# 'GovtConfScore':'PreTrust_Govt',
    'TrustInSSAScore': 'PreTrust_SSA',
    'TrustInInternetScore': 'PreTrust_Internet',
                        }, inplace=True)
    return dta

def getSummaryOfCategoricalVars(dta, vars_Categorical, label):
    stuff = None
    for col in vars_Categorical:

        newStuff =  pd.DataFrame(dta[col].value_counts(dropna=False, normalize=True)).reset_index(drop=False)
        newStuff["Var"] = col
        newStuff["Label"] = label
        newStuff.rename(columns = {'index': "Value", col: 'Percent'}, inplace = True)

        if stuff is None:
            stuff = newStuff
        else:
            stuff = stuff.append(newStuff)
    return stuff

def analyzeSummaryStats(dta, writer, scoringVars, primaryOnly):
    # ###############
    # Export summary stats
    # ###############

    # demographicVars = ['trustScore', 'TotalIncome', 'incomeAmount', 'Race', 'race5', 'employment3', 'educYears', 'Married', 'marriedI', 'Age', 'ageYears', 'Gender', 'genderI']
    demographicVars_Numeric = ['incomeAmount', 'educYears','ageYears', 'genderI', 'GovtConfScore', 'PreTrust_SSA', 'PreTrust_Internet', 'RevealedTrust']

    vars_Categorical = ['TotalIncome', 'race5', 'employment3', 'Gender', 'genderI', "surveyArm", "Wave",
                        'fraudExperience_SSA','fraudExperience_Govt','fraudExperience_Biz',
                        'fraudExperience_YN', 'fraudLoss_YN', 'reportFraud_YN', 'CyberTraining']
    allSummaryVars = ["percentCorrect"] + scoringVars + demographicVars_Numeric + vars_Categorical # , "daysFromTrainingToTest"

    summaryStats = dta[allSummaryVars].describe(include = 'all')

    summaryStats.to_excel(writer, sheet_name="summary_FullPop", startrow=0, header=True, index=True)

    summaryTableAll=getSummaryOfCategoricalVars(dta, vars_Categorical, "All data")
    summaryTableAll_fraudLoss_Y=getSummaryOfCategoricalVars(dta.loc[dta.fraudLoss_YN==True].copy(), vars_Categorical, "FraudLoss = Y")
    summaryTableAll_fraudLoss_N=getSummaryOfCategoricalVars(dta.loc[dta.fraudLoss_YN==False].copy(), vars_Categorical, "FraudLoss = N")
    summaryTableAll_reportFraud_Y=getSummaryOfCategoricalVars(dta.loc[dta.reportFraud_YN==True].copy(), vars_Categorical, "ReportFraud = Y")
    summaryTableAll_reportFraud_N=getSummaryOfCategoricalVars(dta.loc[dta.reportFraud_YN==False].copy(), vars_Categorical, "ReportFraud = N")
    summaryTableCombined = summaryTableAll.append([summaryTableAll_fraudLoss_Y, summaryTableAll_fraudLoss_N, summaryTableAll_reportFraud_Y, summaryTableAll_reportFraud_N])
    STC_Wide = pd.pivot(summaryTableCombined, index=("Var", "Value"), columns='Label', values='Percent')

    STC_Wide.to_excel(writer, sheet_name="summary_Cats", startrow=0, header=True, index=True)

    grouped = dta[allSummaryVars].groupby(["surveyArm"])
    summaryStats = grouped.describe().unstack().transpose().reset_index()
    summaryStats.rename(columns={'level_0' :'VarName', 'level_1' :'Metric'}, inplace=True)
    summaryStats.sort_values(['VarName', 'Metric'], inplace=True)
    summaryStats.to_excel(writer, sheet_name="summary_ByArm", startrow=0, header=True, index=False)


    if ~primaryOnly:
        grouped = dta[allSummaryVars].groupby(["surveyArm", "Wave"])
        summaryStats = grouped.describe().unstack().transpose().reset_index()
        summaryStats.rename(columns={'level_0' :'VarName', 'level_1' :'Metric'}, inplace=True)
        summaryStats.sort_values(['Wave','VarName', 'Metric'], inplace=True)
        # grouped.describe().reset_index().pivot(index='name', values='score', columns='level_1')

        summaryStats.to_excel(writer, sheet_name="summary_ByArmAndWave", startrow=0, header=True, index=False)

    # summaryStats.to_csv(dataDir + "RESULTS_" + outputFileName + '.csv')


def analyzePriorTrust(dta, writer):

    # Predictive Analysis: Does prior fraud decrease trust?
    # PreTrustImpostorType ~ β1FraudExperienceImpostorType + β2FraudLossImpostorType + φ Demographics
    resultTables = ols('PreTrust_SSA ~ fraudExperience_SSA + fraudLoss_YN + fraudLoss_Amount + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables #  +  duration_p2_Quantile
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h1_ssa_priorfraud", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h1_ssa_priorfraud", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('PreTrust_Internet ~ fraudExperience_Biz + fraudLoss_YN + fraudLoss_Amount + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables #  +  duration_p2_Quantile
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h1_intrnt_priorfraud", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h1_intrnt_priorfraud", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('GovtConfScore ~ fraudExperience_Biz + fraudExperience_Govt + fraudLoss_YN + fraudLoss_Amount + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables #  +  duration_p2_Quantile
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h1_gvtconf_priorfraud", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h1_gvtconf_priorfraud", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('RevealedTrust ~ fraudExperience_Biz + fraudExperience_Govt + fraudLoss_YN + fraudLoss_Amount + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI', data=dta.loc[~dta.RevealedTrust.isna()]).fit().summary().tables # duration_p2_Quantile
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h1_rlvdtrust_priorfraud", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h1_rlvdtrust_priorfraud", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # Predictive Analysis: What predicts trust?  (I.e., What are the characteristics of people predisposed to (dis)trust)?
    # PreTrustImpostorType ~ β1FraudExperienceImpostorType + β2FraudLossImpostorType + φ Demographics  + GeneralizedTrust + δ OtherPotentialTrustPredictors

    resultTables = ols('PreTrust_SSA ~ GovtConfScore + OnlineShoppingScore + LonelyScore + fraudExperience_SSA + fraudExperience_Govt + '
                       'fraudLoss_YN + fraudLoss_Amount + lIncomeAmount + C(employment3) + '
                       'educYears +  ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables # +  ''duration_p2_Quantile'
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h1b_ssa_personalchar", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h1b_ssa_personalchar", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('RevealedTrust ~ GovtConfScore + OnlineShoppingScore + LonelyScore + fraudExperience_Biz + fraudExperience_Govt + '
                       'fraudLoss_YN + fraudLoss_Amount + lIncomeAmount + C(employment3) + '
                       'educYears +  ageYears + ageYearsSq + genderI', data=dta.loc[~dta.RevealedTrust.isna()]).fit().summary().tables # +  ''duration_p2_Quantile'
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h1b_rvld_personalchar", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h1b_rvld_personalchar", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # Predictions: Low self-control is associated with greater trust in the internet; greater online shopping is associated with greater trust in the internet; more confidence in the future of the US is associated with greater trust in SSA; feeling angry or frustrated with the US government is associated with less trust in SSA.

def analyzeRevealedDistrust(dta, writer):
    # Predictive Analysis: Is prior imposter fraud victimization is associated with greater distrust of legitimate and fake communications

    resultTables = ols('numLabeledFake ~ fraudExperience_YN + fraudLoss_YN + fraudLoss_Amount + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables #  +  duration_p2_Quantile
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h2_totalDistrust", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h2_totalDistrust", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numLabeledFake ~ fraudExperience_SSA + fraudExperience_Biz + fraudExperience_Govt + fraudLoss_YN + fraudLoss_Amount + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables #  +  duration_p2_Quantile
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h2_totalDistrust_ByType", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h2_totalDistrust_ByType", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numFakeLabeledFake ~ fraudExperience_YN + fraudLoss_YN + fraudLoss_Amount + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI +  duration_p2_Quantile', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h2_rightfulDistrust", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h2_rightfulDistrust", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numRealLabeledFake ~ fraudExperience_YN + fraudLoss_YN + fraudLoss_Amount + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables #  +  duration_p2_Quantile
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h2_undueDistrust", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h2_undueDistrust", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


def getGraphDataByArm(dta, varName, varName_SimpleLabel):

    z_95 = 1.960

    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", varName]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_generalinfo", varName]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_tips", varName]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_interactive", varName]

    # Arm 1
    arm1mean = np.mean(order_value_control_group)
    arm1sd = np.std(order_value_control_group)
    arm1se = z_95 * arm1sd / (np.sqrt(len(order_value_control_group)))

    # Effect of Arm 2
    arm2mean = np.mean(order_value_arm2_group)
    arm2sd = np.std(order_value_arm2_group)
    arm2se = z_95 * arm2sd / (np.sqrt(len(order_value_arm2_group)))

    # Effect of Arm 3
    arm3mean = np.mean(order_value_arm3_group)
    arm3sd = np.std(order_value_arm3_group)
    arm3se = z_95 * arm3sd / (np.sqrt(len(order_value_arm3_group)))

    # Effect of Arm 4
    arm4mean = np.mean(order_value_arm4_group)
    arm4sd = np.std(order_value_arm4_group)
    arm4se = z_95 * arm4sd / (np.sqrt(len(order_value_arm4_group)))

    arms = ['1: Control', '2: General Info', '3: Tips', '4: Interactive']
    x_pos = np.arange(len(arms))
    theMeans = [arm1mean, arm2mean, arm3mean, arm4mean]
    theErrors = [arm1se, arm2se, arm3se, arm4se]

    results = pd.DataFrame({'Arm':arms, 'x_pos': x_pos, 'theMeans':theMeans, 'theErrors': theErrors, 'theVar': varName_SimpleLabel})
    return results

def graphMeanByArm(dta, varName, varName_SimpleLabel, yAxisLabel, plotTitle):

    results = getGraphDataByArm(dta, varName, varName_SimpleLabel)

    fig, ax = plt.subplots()
    ax.bar(results.x_pos, results.theMeans, yerr=results.theErrors, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel(yAxisLabel)
    ax.set_xticks(results.x_pos)
    ax.set_xticklabels(results.theArms)
    ax.set_title(plotTitle)
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig('bar_plot_with_error_bars.png')

def graphRCTImpact_IndividualBars(dta, dataDir, outputFileName):
    graphMeanByArm(dta, "percentCorrect_IsReal", "Percent Correct", "Real Messages: % Correct") # Appropriate Trust
    graphMeanByArm(dta, "percentCorrect_IsScam", "Percent Correct", "Scam Messages: % Correct") # Scam ID
    graphMeanByArm(dta, "percentCorrect", "Percent Correct", "All Messages: % Correct")
    graphMeanByArm(dta, "percentCorrect_Email", "Percent Correct", "Emails: % Correct")
    graphMeanByArm(dta, "percentCorrect_Web", "Percent Correct", "Websites: % Correct")
    graphMeanByArm(dta, "percentCorrect_Letter", "Percent Correct", "Letters: % Correct")
    graphMeanByArm(dta, "percentCorrect_Govt", "Percent Correct", "Government Messages: % Correct")
    graphMeanByArm(dta, "percentCorrect_Biz", "Percent Correct", "Business Messages: % Correct")

def graphRCTImpact_GroupedBar(dta, dataDir, outputFileName):
    row1 = getGraphDataByArm(dta, "percentCorrect", "All")
    row2 = getGraphDataByArm(dta, "percentCorrect_IsReal", "Real") # Appropriate Trust
    row3 = getGraphDataByArm(dta, "percentCorrect_IsScam", "Scam") # Scam ID

    allData = pd.concat([row1, row2, row3])
    posPivot= allData.pivot(index='theVar', columns='Arm', values='x_pos')
    meansPivot= allData.pivot(index='theVar', columns='Arm', values='theMeans')
    errorsPivot = allData.pivot(index='theVar', columns='Arm', values='theErrors')
    thePlot = meansPivot.plot(kind='bar', yerr=errorsPivot, rot=0,
                    title = "Percent Correct By Arm",
                    grid = True,
                    xlabel = "",
                    ylabel = "Percent Correct",
                    alpha=0.5, ecolor='black', capsize=5)
    plt.savefig(dataDir + outputFileName + 'all_scam_real.png')


    row4 = getGraphDataByArm(dta, "percentCorrect_Email", "Emails")
    row5 = getGraphDataByArm(dta, "percentCorrect_Web", "Websites")
    row6 = getGraphDataByArm(dta, "percentCorrect_Letter", "Letters")

    allData = pd.concat([row1, row4, row5, row6])
    posPivot= allData.pivot(index='theVar', columns='Arm', values='x_pos')
    meansPivot= allData.pivot(index='theVar', columns='Arm', values='theMeans')
    errorsPivot = allData.pivot(index='theVar', columns='Arm', values='theErrors')
    thePlot = meansPivot.plot(kind='bar', yerr=errorsPivot, rot=0,
                    title = "Percent Correct By Arm",
                    grid = True,
                    xlabel = "",
                    ylabel = "Percent Correct",
                    alpha=0.5, ecolor='black', capsize=10)
    plt.savefig(dataDir + outputFileName + 'all_email_web_letter.png')

    row7 = getGraphDataByArm(dta, "percentCorrect_Govt", "Government")
    row8 = getGraphDataByArm(dta, "percentCorrect_Biz", "Business")

    allData = pd.concat([row1, row7, row8])
    posPivot= allData.pivot(index='theVar', columns='Arm', values='x_pos')
    meansPivot= allData.pivot(index='theVar', columns='Arm', values='theMeans')
    errorsPivot = allData.pivot(index='theVar', columns='Arm', values='theErrors')
    thePlot = meansPivot.plot(kind='bar', yerr=errorsPivot, rot=0,
                    title = "Percent Correct By Arm",
                    grid = True,
                    xlabel = "",
                    ylabel = "Percent Correct",
                    alpha=0.5, ecolor='black', capsize=10)
    plt.savefig(dataDir + outputFileName + 'all_biz_govt.png')

    # fig, ax = plt.subplots()
    # ax.bar(posPivot, meansPivot, yerr=errorsPivot, align='center', alpha=0.5, ecolor='black', capsize=10)
    # ax.set_ylabel("Percent Correct")
    # ax.set_xticks(posPivot)
    # ax.set_xticklabels(results.theArms)
    # ax.set_title()
    # ax.yaxis.grid(True)

    plt.tight_layout()
    plt.savefig('bar_plot_with_error_bars.png')

    # https://stackoverflow.com/questions/23000418/adding-error-bars-to-grouped-bar-plot-in-pandas

def analyzeRCTImpact(dta, writer):


    # ###############
    # RQ1: What is the effect?
    # Experimental Analysis: Does the interactive training help people trust government | online business
    # CorrectTrustImpostorType ~  Arm
    # ###############

    # H3: The interactive training will improve participants’ accuracy of discerning legitimate and fake communications relative to the static training and control conditions. This effect will be consistent for those who have and have not been victimized by an imposter scam.
    row1 = analyzeExperiment_ContinuousVar(dta, "percentCorrect_IsReal") # Appropriate Trust
    row2 = analyzeExperiment_ContinuousVar(dta, "percentCorrect_IsScam") # Scam ID
    row3 = analyzeExperiment_ContinuousVar(dta, "percentCorrect")
    row4 = analyzeExperiment_ContinuousVar(dta, "percentCorrect_Email")
    row5 = analyzeExperiment_ContinuousVar(dta, "percentCorrect_Web")
    row6 = analyzeExperiment_ContinuousVar(dta, "percentCorrect_Letter")
    row7 = analyzeExperiment_ContinuousVar(dta, "percentCorrect_Govt")
    row8 = analyzeExperiment_ContinuousVar(dta, "percentCorrect_Biz")

    pd.DataFrame([row1, row2, row3, row4, row5, row6, row7, row8]).to_excel(writer, sheet_name="h3", startrow=1, header=True, index=True)


    ##############
    # RQ1* Robustness check on result: is the experiment randomized correctly?
    # CorrectTrustImpostorType ~  Arm + PreTrustImpostorType + FraudExperienceImpostorType + FraudLossImpostorType + Demographics  + GeneralizedTrust + OtherPotentialTrustPredictors

    ##############
    # NumCorrect Regression
    # todo -- THIS IS UNLIKELY WHAT WE WANT; THERE MAY BE INTERACTION EFFECTS WE'RE PICKING UP
    resultTables = ols('percentCorrect ~ C(surveyArm) + PreTrust_SSA + PreTrust_Internet + OnlineShoppingScore + fraudExperience_YN + fraudLoss_YN + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables #  +  duration_p2_Quantile
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h3_reg_correct", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h3_reg_correct", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('percentCorrect ~  C(surveyArm) * fraudExperience_YN', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h3_interact_fraudexperience", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h3_interact_fraudexperience", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('percentCorrect ~  C(surveyArm) * fraudExperience_SSA', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h3_interact_fraudSSA", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h3_interact_fraudSSA", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('percentCorrect ~  C(surveyArm) * fraudLoss_YN', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h3_interact_fraudLoss", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h3_interact_fraudLoss", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    # H4: The interactive training does not increase distrust of legitimate communications relative to the to the static training and control conditions.
    resultTables = ols('percentIncorrect_ActuallyReal  ~  C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h4", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h4", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    # Experimental Analysis: What are the characteristics of people who respond to the training?
    # CorrectTrustImpostorType ~  Arm * TreatmentResponsivenessDrivers + Arm  + TreatmentResponsivenessDrivers
    # H5: The interactive training will have a greater effect on discrimination accuracy for older participants and those who engage less frequently in online shopping relative to younger participants and participants who are more frequent online shoppers.

    resultTables = ols('percentCorrect ~  C(surveyArm) * ageYears', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h5_interact_age", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h5_interact_age", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('percentCorrect ~  C(surveyArm) * OnlineShoppingScore', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="h5_interact_online", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="h5_interact_online", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    # Experimental Analysis: Does the interactive trust training increase distrust?
    # IncorrectTrustImpostorType ~  Arm + PreTrustImpostorType + FraudExperienceImpostorType + FraudLossImpostorType + Demographics  + GeneralizedTrust + OtherPotentialTrustPredictors

    # Note -- IncorrectTrustImpostorType == 1 -percentCorrect_Scam
    # BUT distrust - 1-percentCorrect_IsReal

    resultTables = ols('percentCorrect_IsReal ~ C(surveyArm) + PreTrust_SSA + PreTrust_Internet + OnlineShoppingScore + fraudExperience_YN + fraudLoss_YN + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables #  +  duration_p2_Quantile
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r3_reg_realasreal", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r3_reg_realasreal", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('percentCorrect_IsScam ~ C(surveyArm) + PreTrust_SSA + PreTrust_Internet + OnlineShoppingScore + fraudExperience_YN + fraudLoss_YN + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables #  +  duration_p2_Quantile
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r3_reg_scamasscam", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r3_reg_scamasscam", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


def analyzeCorrelations(dta, writer):
    # ##############
    # Correlations
    ################

    indepVars = ['surveyArm', 'daysFromTrainingToTest', 'Wave', 'GovtConfScore', 'PreTrust_SSA', 'PreTrust_Internet', 'OnlineShoppingScore', 'LonelyScore',
                 'incomeAmount', 'race5', 'employment3', 'educYears', 'ageYears','genderI',
                 'fraudExperience_YN', 'fraudLoss_YN', 'duration_p1', 'duration_p1_Quantile', 'duration_p2', 'duration_p2_Quantile', 'Employment']

    depVars = ['numCorrect', 'numFakeLabeledReal', 'numRealLabeledFake']

    dta.Wave = dta.Wave.astype('float64')
    # Look at  Correlations among variables
    allVarsToCorr = depVars + indepVars
    corrMatrix = dta[allVarsToCorr].corr()
    pd.DataFrame(corrMatrix).to_excel(writer, sheet_name="corrMatrix", startrow=1, header=True, index=True)
    # duration_p1 is a proxy for arm, so strange results there.
    # we'd need a fine-tuned var. Let's use p2 instead.  Also, the Quantile shows a much stronger relationship than the raw values (likely since it is not linear in the depvars)
    # Losing money and income and age show a moderate relationship



def analyzeResults(dta, outputFileName, scoringVars, surveyVersion,dataDir,  primaryOnly=True):

    if primaryOnly:
        dta = dta[dta.IsPrimaryWave].copy()

    dta = renameForAnalysis(dta)

    graphRCTImpact_GroupedBar(dta, dataDir, outputFileName)

    ''' Analyze the answers'''
    writer = pd.ExcelWriter(dataDir + 'RESULTS_' + outputFileName + '.xlsx', engine='xlsxwriter')

    analyzeSummaryStats(dta, writer, scoringVars, primaryOnly)
    analyzeCorrelations(dta, writer)

    analyzePriorTrust(dta, writer)
    analyzeRevealedDistrust(dta, writer)
    analyzeRCTImpact(dta, writer)

    # ###############
    # RQ2: Communication Type
    # ###############

    """
    # ###############
    # RQ2: Communication Type
    # ###############
    row1 = analyzeExperiment_ContinuousVar(dta, "numEmailsCorrect")
    row2 = analyzeExperiment_ContinuousVar(dta, "numWebsitesCorrect")
    row3 = analyzeExperiment_ContinuousVar(dta, "numSMSesCorrect")
    row4 = analyzeExperiment_ContinuousVar(dta, "numLettersCorrect")
    pd.DataFrame([row1, row2, row3, row4]).to_excel(writer, sheet_name="r2", startrow=1, header=True, index=True)

    ##############
    # RQ2* Robustness check on Emails result: is the experiment randomized correctly?
    ##############
    # NumEmailsCorrect Regression
    resultTables = ols('numEmailsCorrect ~ C(surveyArm) + daysFromTrainingToTest + GovtConfScore + TrustInSSAScore + TrustInInternetScore + OnlineShoppingScore + LonelyScore + lIncomeAmount + '
                     'C(employment3) + educYears + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r2_reg", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r2_reg", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # ###############
    # RQ3: Time Delay
    # ###############
    resultTables = ols('numCorrect ~ C(surveyArm)*Wave + daysFromTrainingToTest', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r3a_CorrectWaveAndDay_Simple", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r3a_CorrectWaveAndDay_Simple", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numEmailsCorrect ~ C(surveyArm)*Wave + daysFromTrainingToTest', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r3b_EmailWaveAndDay_Simple", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r3b_EmailWaveAndDay_Simple", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # ###############
    # RQ4: Rainloop
    # ###############
    if surveyVersion == '2' or surveyVersion == '3':
        resultTables = ols('NumWithHeadersOpened ~ C(surveyArm)', data=dta).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r4_HeadersOpened", startrow=1, header=False, index=False)
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r4_HeadersOpened",startrow=1 + len(resultTables[0]) + 2, header=False, index=False)
    """


    ########################
    # R5a: What determines fraud susceptibility (whether people get tricked or not)?
    # Ie, false negatives
    ########################
    resultTables = ols('percentIncorrect_ActuallyScam  ~ C(surveyArm) + PreTrust_SSA + PreTrust_Internet + OnlineShoppingScore + fraudExperience_YN + fraudLoss_YN + lIncomeAmount + C(employment3) + educYears +  ageYears + ageYearsSq + genderI +  duration_p2_Quantile', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r5a_prnctFakeLabeledReal", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r5a_prnctFakeLabeledReal", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    """
    ########################
    # R5b: What determines lack of trust?
    ########################
    # Ie, false positive
    resultTables = ols('numRealLabeledFake ~ C(surveyArm) + daysFromTrainingToTest + GovtConfScore + TrustInSSAScore + TrustInInternetScore + OnlineShoppingScore + LonelyScore + lIncomeAmount + '
                       'C(employment3) + educYears + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r5b_numRealLabeledFake", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r5b_numRealLabeledFake", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numLabeledFake ~ C(surveyArm) + daysFromTrainingToTest + GovtConfScore + TrustInSSAScore + TrustInInternetScore + OnlineShoppingScore + LonelyScore + lIncomeAmount + '
                       'C(employment3) + educYears + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_numLabeledFake", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_numLabeledFake", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)
    """
    # ###############
    # H6: Communicaiton Medium
    # ###############
    row1 = analyzeExperiment_ContinuousVar(dta, "percentCorrect")
    row2 = analyzeExperiment_ContinuousVar(dta, "percentCorrect_Email")
    row3 = analyzeExperiment_ContinuousVar(dta, "percentCorrect_Web")
    row4 = analyzeExperiment_ContinuousVar(dta, "percentCorrect_Letter")
    pd.DataFrame([row1, row2, row3, row4]).to_excel(writer, sheet_name="h6_commtype", startrow=1, header=True, index=True)

    # ###############
    # RQ6: Impostor Type
    # ###############
    row1 = analyzeExperiment_ContinuousVar(dta, "numCorrect_Govt")
    row2 = analyzeExperiment_ContinuousVar(dta, "numCorrect_Biz")
    row3 = analyzeExperiment_ContinuousVar(dta, "numEmailsCorrect_Govt")
    row4 = analyzeExperiment_ContinuousVar(dta, "numEmailsCorrect_Biz")
    row5 = analyzeExperiment_ContinuousVar(dta, "numWebsitesCorrect_Govt")
    row6 = analyzeExperiment_ContinuousVar(dta, "numWebsitesCorrect_Biz")
    pd.DataFrame([row1, row2, row3, row4, row5, row6]).to_excel(writer, sheet_name="r6", startrow=1, header=True, index=True)

    # ###############
    # RQ7: Likelihood of being tricked
    # ###############
    dta['isTrickedByFraud'] = dta.numFakeLabeledReal > 0

    dta['isTrickedByAnyGovt'] = dta.numCorrect_Govt < max(dta.numCorrect_Govt)
    dta['isTrickedByAnyBiz'] = dta.numCorrect_Biz < max(dta.numCorrect_Biz)

    dta['isTrickedByAnyGovtEmail'] = dta.numEmailsCorrect_Govt < max(dta.numEmailsCorrect_Govt)
    dta['isTrickedByAnyBizEmail'] = dta.numEmailsCorrect_Biz < max(dta.numEmailsCorrect_Biz)

    dta['isTrickedByAnyGovtWeb'] = dta.numWebsitesCorrect_Govt < max(dta.numWebsitesCorrect_Govt)
    dta['isTrickedByAnyBizWeb'] = dta.numWebsitesCorrect_Biz < max(dta.numWebsitesCorrect_Biz)

    row1 = analyzeExperiment_BinaryVar(dta, "isTrickedByFraud")
    row2 = analyzeExperiment_BinaryVar(dta, "isTrickedByAnyGovt")
    row3 = analyzeExperiment_BinaryVar(dta, "isTrickedByAnyBiz")
    row4 = analyzeExperiment_BinaryVar(dta, "isTrickedByAnyGovtEmail")
    row5 = analyzeExperiment_BinaryVar(dta, "isTrickedByAnyBizEmail")
    pd.DataFrame([row1, row2, row3, row4, row5]).to_excel(writer, sheet_name="r7", startrow=1, header=True, index=True)

    # ###############
    # RQ8: Every Email
    # ###############
    filter_cols = [col for col in dta.columns if col.startswith('Correct_')]
    theRows = []
    for filter_col in filter_cols:
        arow = analyzeExperiment_BinaryVar(dta, filter_col)
        theRows = theRows + [arow]

    pd.DataFrame(theRows).to_excel(writer, sheet_name="r8", startrow=1, header=True, index=True)


    """
    # ##############
    # Scatter Plots
    ################

    import seaborn as sns
    sns.set_theme(style="ticks")

    toPlot = dta[['numCorrect', 'surveyArm', 'daysFromTrainingToTest', 'Wave', 'GovtConfScore', 'PreTrust_SSA', 'PreTrust_Internet', 'OnlineShoppingScore', 'LonelyScore', 'fraudExperience_YN', 'fraudLoss_YN', 'duration_p2_Quantile']]
    sns.pairplot(toPlot, hue="surveyArm")

    # ##############
    # Regressions
    # ##############

    # Sanity Check regression
    resultTables = ols('lIncomeAmount ~ageYears + ageYearsSq + educYears + genderI', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_Sanity", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_Sanity", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # Simple Experiment-Only test
    resultTables = ols('numCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numCorrect_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numCorrect_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numEmailsCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numEmailsCorrect_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numEmailsCorrect_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # Full regression, within each specific wave, with controls
    startRow = 1
    for wave in dta.Wave.unique():
        # worksheet = writer.book.add_worksheet("numCorrect_ByArmAndWave")
        # worksheet.write(startRow, 1, 'Wave ' + str(wave))
        # startRow = startRow + 2
        resultTables = ols('numCorrect ~ C(surveyArm) + lIncomeAmount + ageYears + ageYearsSq + educYears +  genderI', data=dta.loc[dta.Wave==wave]).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numCorrect_ByArmInWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[0]) + 2
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numCorrect_ByArmInWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[1]) + 2

    startRow = 1
    for wave in dta.Wave.unique():
        # worksheet = writer.book.add_worksheet("numEmailsCorrect_ByArmAndWave")
        # worksheet.write(startRow, 1, 'Wave ' + str(wave))
        # startRow = startRow + 2
        resultTables = ols('numEmailsCorrect ~ C(surveyArm) + lIncomeAmount + ageYears + ageYearsSq + educYears +  genderI', data=dta.loc[dta.Wave == wave]).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numEmailsCorrect_ByArmInWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[0]) + 2
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numEmailsCorrect_ByArmInWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[1]) + 2


    resultTables = ols('numLettersCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numLettersCorrect_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numLettersCorrect_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numSMSesCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numSMSesCorrect_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numSMSesCorrect_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numLabeledFake ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numLabeledFake_ByArm", startrow=1, header=False,
                                           index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numLabeledFake_ByArm",
                                           startrow=1 + len(resultTables[0]) + 2, header=False, index=False)
       
    """

    if (surveyVersion in ['2', '3', '10', '11', '14', '15']):
        resultTables = ols('NumWithHeadersOpened ~ C(surveyArm)', data=dta).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="NumHeadersOpened_ByArm", startrow=1, header=False, index=False)
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="NumHeadersOpened_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

        resultTables = ols('NumWithLinksClicked ~ C(surveyArm)', data=dta).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="NumWithLinksClicked_ByArm", startrow=1, header=False, index=False)
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="NumWithLinksClicked_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    """
    resultTables = ols('numFakeLabeledFake ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numFakeLabeledFake_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numFakeLabeledFake_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numRealLabeledReal ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numRealLabeledReal_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numRealLabeledReal_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)
    """

    ## ###########
    # Is there an effect of wave: Additional Exporation
    ##############
    """
    # NumCorrect Regression
    resultTables = ols('numCorrect ~ C(surveyArm)*Wave + daysFromTrainingToTest + GovtConfScore + TrustInSSAScore + TrustInInternetScore + OnlineShoppingScore + LonelyScore + lIncomeAmount + '
                     'C(employment3) + educYears +  ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_CorrectWithWaveAndDays", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_CorrectWithWaveAndDays", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numCorrect ~ C(surveyArm)*Wave + GovtConfScore + TrustInSSAScore + TrustInInternetScore + OnlineShoppingScore + LonelyScore + lIncomeAmount + '
                     'C(employment3) + educYears + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_CorrectWithWave", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_CorrectWithWave", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)
    """
    # ##############
    # Save the processed data
    # ##############
    pd.DataFrame(dta).to_excel(writer, sheet_name="theData", startrow=0, header=True, index=False)
    # dta.to_csv(dataDir + "PROCESSED_" + outputFileName + ".csv")
    writer.save()
    # workbook.close()

    """
        if (debugging):
        
        grouped.agg(["count"])
        grouped.percentCorrect.mean()
        grouped.numCorrect.mean()
        grouped.numReal.mean()
        grouped['Correct_ImportantInformation'].value_counts(dropna=False, normalize=True)
        grouped['Correct_AmazonPayment'].value_counts(dropna=False, normalize=True)
        grouped['Correct_AmazonDelay'].value_counts(dropna=False, normalize=True)
        grouped['Correct_RedCross'].value_counts(dropna=False, normalize=True)
        grouped['Correct_Disability'].value_counts(dropna=False, normalize=True)
        grouped['Correct_ssa_optout'].value_counts(dropna=False, normalize=True)
        grouped['Correct_replacementCard'].value_counts(dropna=False, normalize=True)
        grouped['Correct_annualReminderKLEW'].value_counts(dropna=False, normalize=True)
        grouped['Correct_lt_medicare'].value_counts(dropna=False, normalize=True)
        grouped['Correct_sms_disability'].value_counts(dropna=False, normalize=True)
        grouped['Correct_lt_suspension'].value_counts(dropna=False, normalize=True)
        grouped['Correct_sms_redcross'].value_counts(dropna=False, normalize=True)
    """