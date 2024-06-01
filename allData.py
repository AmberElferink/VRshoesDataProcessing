## -------------------- WHAT IS THIS FILE? ---------------------------------
## This file is able to process all data from all trials in UserTestTrackingData, can create each csv, and executes filters 
## and data implementations from other files to combine to one big data frame that can do everything.
## uncomment lines in each csv segment to overwrite that particular csv.
## if you want to plot images of the speeds, look at the end of the file on how to do it, 
## or see genSpeed.py to plot for specific files.
## if working with new data, set your seperator ; or , for example, and header files first in filterdata.py
## then first run it through genTrajectory-interactive-trajectory-loopfiles.py to cut the data after the end experiment

import filterdata
import genSpeed
import directions

import pandas
import numpy as np


def calculateAverages(dfs, onlyMoving):
    for i in range(0, len(dfs["df"])):
        avgPlayerSpeed, avgLocSpeed = genSpeed.calcAvgLocomotionSpeed(dfs['df'][i], onlyMoving)
        dfs['avgLocSpeed'].append(avgLocSpeed)
        dfs['avgPlayerSpeed'].append(avgPlayerSpeed)


# This will contain all dataframes, for each subjectnr, and locomotion technique, 
# and also calculates some calculated variables over the entire trial such as average 
# velocities, and of course the dataframe df for the trial itself.
dataframes = {'lt': [], 'subjectnr': [], 'df': [], 'avgLocSpeed':[], 'avgPlayerSpeed':[]}

# Loads and organizes the dataframes, and calculates some extra columns for further processing
# If new data, set your seperator and header of the data files in filterData before executing!
# Enable verbal to see what is happening.
filterdata.verbal = False
filterdata.LoadAndFilterFolder("UserTestTrackingData", dataframes["df"], dataframes["subjectnr"], dataframes['lt'])

#this way you dont have to loop through dataframes
allcontainingDataFrame = pandas.concat(dataframes['df'], axis=0)
# print(allcontainingDataFrame)

completionTimeDataFrame = pandas.DataFrame(columns = ['completionTime', 'LocomotionTechnique', 'SubjectNr'])


##################### CREATE TIME SPENT CSV #########################
for idf, df in enumerate(dataframes["df"]):
    new_row = {'completionTime': df['SecFromFullStart'].iloc[-1],'LocomotionTechnique':df["LocomotionTechnique"][0], 'SubjectNr':df["SubjectNr"][0]}
    completionTimeDataFrame = completionTimeDataFrame.append(new_row, ignore_index=True)
    #completionTimeDataFrame.to_csv("completionTime.csv", encoding='utf-8') # uncomment to overwrite csv
###########################################################################




####################### ANALYZE NR OF TRACKING LOSSES TO CSV ##############
trackerlossdataframe = pandas.DataFrame(columns = ['NrTrackerlosses', 'LocomotionTechnique', 'SubjectNr'])
timeThreshold = 0.2 # in seconds time a trackerloss should be active before it is counted here

for idf, df in enumerate(dataframes["df"]):
    #count number of tracker losses
    # log all sections of data where the trackers are not working
    sectionList, sectionNr, sectionNrToFirstLastIdx = filterdata.BoolSectionDef(df["AllTrackersWorking"], False) 

    # calculate time difference between end and start of te section with tracker loss
    sectionNrToTimeTaken = {}
    sectionNrToThresholdedTimeTaken = {}
    for i in range(1, sectionNr): 
        sectionNrToTimeTaken[i] = df["SecSinceStart"][sectionNrToFirstLastIdx[i][1]] - df["SecSinceStart"][sectionNrToFirstLastIdx[i][0]]
        if sectionNrToTimeTaken[i] > timeThreshold:
            sectionNrToThresholdedTimeTaken[i] = sectionNrToTimeTaken[i]
    new_row = {'NrTrackerlosses':len(sectionNrToThresholdedTimeTaken), 'LocomotionTechnique':df["LocomotionTechnique"][0], 'SubjectNr':df["SubjectNr"][0]}
    trackerlossdataframe = trackerlossdataframe.append(new_row, ignore_index=True)
    #trackerlossdataframe.to_csv("trackerloss_analysis2.csv", encoding='utf-8') # uncomment to overwrite csv
####################################################################


######################### Preprocessing for direction analysis. This was not further used in the thesis since it gave redundant results, and resulted in confusion for readers ##############################
directionDataframe = allcontainingDataFrame[[
    "SubjectNr", 
    "LocomotionTechnique", 
    "SecSinceStart", 
    "StandingAngle", 
    "HipAngle", 
    "HeadAngle", 
    "AvgFeetAngle", 
    "AllTrackersWorking", 
    "LocomotionOffX", 
    "LocomotionOffY", 
    "LocomotionOffZ",
    "isMoving"
    ]].copy()
#print(directionDataframe)
#directionDataframe.to_csv("direction_analysis.csv", encoding='utf-8') # uncomment to overwrite csv
#######################################################################################


calculateAverages(dataframes, True)
print(pandas.DataFrame(data=dataframes))

for df in dataframes["df"]:
    directions.processDirections(df)
    dtlist = np.diff(df['SecSinceStart'])
    dtlist = np.insert(dtlist, 0, 0, 0)
    df['dt'] = dtlist * 100 - 2.25


# What variables would you like to plot over time? You can see any
genSpeed.clearData()
#genSpeed.addData('PlayerHorSpeed', 'Player speed')
#genSpeed.addData('LLegPosY', "Left leg height")
#genSpeed.addData('RLegPosY', "Right leg height")
genSpeed.addData('LLHorSpeed', "Left Foot horizontal")
genSpeed.addData('RLHorSpeed', "Right Foot horizontal")
genSpeed.addData('EWMA_Left_Non_Abs', "EWMA Left Foot horizontal")
genSpeed.addData('EWMA_Right_Non_Abs', "EWMA Right Foot horizontal")
genSpeed.addData('LocomotionSpeed', 'Locomotion speed')
#genSpeed.addData('dirAngleRad', 'world direction radians')
#genSpeed.addData('LeftFootPitch', 'Left foot pitch')
#genSpeed.addData('AllTrackersWorking', 'All trackers working')
#genSpeed.addData('dt', 'deltaTime logging (centi seconds)')
#genSpeed.addData('headAngleRad', 'Head rotation')
#genSpeed.addData('StandingLeadingFootNr', 'right: 1.5, left: -1.5, none: 0')


#genSpeed.multipleSpeedPlots(dataframes, "StandingFootVelocity")



# Uncommenting this will plot all in succession, meaning you will get 80 popups, clicking through them one by one!!!
# You can also just input one of them replacing the for loop below, or plot in genSpeed.py
# for i in range(0, len(dfs)):
#     genSpeed.plotSpeed(dfs[i], "LT: " + locomotionTechniques[i] + "Subject: " + subjectNrs[i])

