# Note: raw out of Unity, there was an extra line on top of the data with some info on thresholds and stuff, and it had ; as delimiter
# Then later this was overwritten of TrackerData files by pandas for setting the times users reached the end and discarding the rest of the data.
# So if you get a "KeyError", make sure that the below settings are correct:
# If straight from Unity (not a 0_TrackerData file in UserTestTrackingData in the python folder), set sep=";", header = 1
# If from the files here ( a 0_TrackerData file in UserTestTrackingData in the python folder), set sep=",", header = 0

import pandas
import math
from IPython.display import display
import os
from pathlib import Path
import numpy as np


pandas.set_option('display.max_rows', 500)

verbal = True

def importFile(fileName):
    print("reading " + fileName)
    return pandas.read_csv(fileName,  sep=",",header=0,index_col=False, dtype = {
"Task": str,
"Timestamp": str,
"SecSinceStart": float,
"PlayerX": float,
"PlayerY": float,
"PlayerZ": float,
"LocomotionOffX": float,
"LocomotionOffY": float,
"LocomotionOffZ": float,
"PlayerRotX": float,
"PlayerRotY": float,
"PlayerRotZ": float,
"HeadPosX": float,
"HeadPosY": float,
"HeadPosZ": float,
"HeadRotX": float,
"HeadRotY": float,
"HeadRotZ": float,
"PlayerHorSpeed": float,
"LHandPosX": float,
"LHandPosY": float,
"LHandPosZ": float,
"LHandRotX": float,
"LHandRotY": float,
"LHandRotZ": float,
"RHandPosX": float,
"RHandPosY": float,
"RHandPosZ": float,
"RHandRotX": float,
"RHandRotY": float,
"RHandRotZ": float,
"LLegPosX": float,
"LLegPosY": float,
"LLegPosZ": float,
"LLegRotX": float,
"LLegRotY": float,
"LLegRotZ": float,
"LLHorSpeed": float,
"RLegPosX": float,
"RLegPosY": float,
"RLegPosZ": float,
"RLegRotX": float,
"RLegRotY": float,
"RLegRotZ": float,
"RLHorSpeed": float,
"HipPosX": float,
"HipPosY": float,
"HipPosZ": float,
"HipRotX": float,
"HipRotY": float,
"HipRotZ": float,
"HipHorSpeed": float,
"DirectionRotX": float,
"DirectionRotY": float,
"DirectionRotZ": float,
"AllTrackersWorking": bool,
"TrackersNotWorking": str,
"RightLifted": bool,
"RightStanding": bool,
"LeftLifted": bool,
"LeftStanding": bool,
"StandingLeadingFoot": str,
"LiftedLeadingFoot": str,
"GWAngle": float,
"LocomotionSpeed": float,
"EWMA_Right": float,
"EWMA_Left": float,
"LAvgVelAngle": float,
"RAvgVelAngle": float,
"LAvgVelMag": float,
"RAvgVelMag": float,
"LiftedAngle": float,
"StandingAngle": float,
"HipAngle": float,
"HeadAngle": float,
"AvgFeetAngle": float
})

pandas.set_option('display.max_columns', None)

def LoadAndFilterFolder(directory, dataFrameArray, subjectNrArray, conditionArray):
    # iterate over files in
    # that directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filePath = os.path.join(root, filename)
            #print(os.path.join(root, filename))
            if(filename.endswith('.csv') and filename.startswith("0_TrackingData")):
                subjectNr = os.path.basename(Path(filePath).parents[1])
                locomotionTechnique = os.path.basename(Path(filePath).parents[2])
                if verbal:
                    print("append ", filePath, "subjectNr", subjectNr, " Locomotion Method", locomotionTechnique)
                dataFrameArray.append(filterFileToDataFrame(filePath))
                dataFrameArray[-1]["SubjectNr"] = int(subjectNr)
                dataFrameArray[-1]["LocomotionTechnique"] = locomotionTechnique
                conditionArray.append(locomotionTechnique)
                subjectNrArray.append(subjectNr)
    return dataFrameArray, subjectNrArray, conditionArray


# if the column options are "right", "left",  or "none", this sets right to 1, left to -1, and none to 0.
def nrColBasedOnLeftRight(df, namedCol):
    if namedCol in df.columns:
        conditions = [
        (df[namedCol] == "right"),
        (df[namedCol] == "left"),
        (df[namedCol] == "none")
        ]

        # create a list of the values we want to assign for each condition
        values = [1.5, -1.5, 0]

        # create a new column and use np.select to assign values to it using our lists as arguments
        return np.select(conditions, values)
    else:
        return 0


def AddExtraColls(df):
    df['RoomPosX'] = df['PlayerX'] - df['LocomotionOffX']
    df['RoomPosZ'] = df['PlayerZ'] - df['LocomotionOffZ']
    df['SecFromFullStart'] = CalcTotalTime(df)
    df['EWMA_Left_Non_Abs'] = ListEWMA(df['LLHorSpeed'], 0.82)
    df['EWMA_Right_Non_Abs'] = ListEWMA(df['RLHorSpeed'], 0.82)
    df['EWMA_Both_Non_Abs'] = (df['EWMA_Left_Non_Abs'] + df['EWMA_Right_Non_Abs'] ) / 2

    # Filtering the sections where the person is moving, and afterwards filter out the parts where the person is moving backwards.
    df['isMoving'] = df['LocomotionSpeed'] > 0.05
    # label each section where the person is moving with a different letter
    df['MoveSectionLabels'], nrSections, sectionNrToIdxStartStop = BoolSectionDef(df['isMoving'], True)

    df['StandingLeadingFootNr'] = nrColBasedOnLeftRight(df, 'StandingLeadingFoot')
    df['LiftedLeadingFootNr'] = nrColBasedOnLeftRight(df, 'LiftedLeadingFoot')


    #  calculate the average speed over the whole duration of a letter. Also throw it away if a section is shorter than 1.5 seconds
    df['avgMovingSection'] = 0

    #This filters out data with moving back to center or too short motion areas
    # for sectionNr in range(1, max(df['MoveSectionLabels'])):
    #     sectionMask = df['MoveSectionLabels'] == sectionNr
    #     if df[sectionMask]['SecFromFullStart'].iloc[-1] - df[sectionMask]['SecFromFullStart'].iloc[0] < 0.5: #This part breaks for one file, so commented it out
    #         # moving section too short, throw away
    #         if verbal:
    #             print("remove too short moving section", sectionNr)
    #         df.loc[sectionMask, 'isMoving'] = False 
    #         df.loc[sectionMask, 'MoveSectionLabels'] = 0
        
    #     # if average speed < 0, shuffling backwards, set to False in isMoving
    #     averageSpeed = df.loc[sectionMask, 'avgMovingSection'] = df[sectionMask]['EWMA_Both_Non_Abs'].mean(axis=0) *5 
    #     if averageSpeed < 0:
    #         if verbal:
    #             print("remove backward moving section", sectionNr)
    #         df.loc[sectionMask, 'isMoving'] = False 
    #         df.loc[sectionMask, 'MoveSectionLabels'] = 0
    return df



def CalcTotalTime(df): # this was because the timer started again when a task was completed, this function makes sure to continue counting.
    totalOffset = 0
    SecFromFullStart = []
    SecFromFullStart.append(df['SecSinceStart'][0])
    for i in range(1, len(df['SecSinceStart'] )):
        if(df['SecSinceStart'][i] < df['SecSinceStart'][i-1]):
            totalOffset += df['SecSinceStart'][i-1]
        SecFromFullStart.append(totalOffset + df['SecSinceStart'][i])
    return SecFromFullStart



# returns new exponentially weighted average
def EWMA(prevAverage, newValue, rho):
    return rho * prevAverage + ((1-rho) * newValue)

# returns EWMA list based on another list
def ListEWMA(list, rho):
    average = 0
    EWMA_List = []
    for i in range(0, len(list)):
        average = EWMA(average, list[i], rho)
        EWMA_List.append(average)
    return EWMA_List


# for a mask with multiple rows of 11110001111. It labels: 11110002222 etc
# numberToLabelSection in the above example is 1, so all 1's will be treated as sections, (0 and any other nuumber will not)
# if instead the 0/False sections are to be labeled, use that as argument
def BoolSectionDef(list, valueToLabelSection):
    currSign = list[0]
    sectionNr = 0
    sectionNrList = []

    currSectionStartIdx = 0
    sectionNrToFirstLastIdx = {} # will contain first id and last id of current section

    if list[0] == valueToLabelSection:
        sectionNr = 1
    for i in range(0, len(list)):
        if list[i] != currSign:
            if list[i] == valueToLabelSection: # >0 means tracking is working, this is a new section with broken tracking
                sectionNr +=1
                currSectionStartIdx = i
            else: # value goes to label that should not be added as section, add this as section end
                sectionNrToFirstLastIdx[sectionNr] = [currSectionStartIdx, i]
        currSign = list[i]

        if list[i] > valueToLabelSection:
            sectionNrList.append(sectionNr)
        else:
            sectionNrList.append(0)
    return sectionNrList, sectionNr, sectionNrToFirstLastIdx

def filterFileToDataFrame(fileName):
    df = importFile(fileName)
    df = AddExtraColls(df)
    return df



# with pandas.option_context('display.min_rows', 300, 'display.max_columns', 10):
#     display(df[['isMoving', 'MoveSectionLabels', 'avgMovingSection']].head(300))








