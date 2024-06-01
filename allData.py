import filterdata
import genVelocity
import directions

import pandas
import numpy as np

def calculateAverages(dfs, onlyMoving):
    for i in range(0, len(dfs["df"])):
        avgPlayerSpeed, avgLocSpeed = genVelocity.calcAvgLocomotionVel(dfs['df'][i], onlyMoving)
        dfs['avgLocVel'].append(avgLocSpeed)
        dfs['avgPlayerVel'].append(avgPlayerSpeed)



dataframes = {'lt': [], 'subjectnr': [], 'df': [], 'avgLocVel':[], 'avgPlayerVel':[]}

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

calculateAverages(dataframes, True)
print(pandas.DataFrame(data=dataframes))

for df in dataframes["df"]:
    directions.processDirections(df)
    dtlist = np.diff(df['SecSinceStart'])
    dtlist = np.insert(dtlist, 0, 0, 0)
    df['dt'] = dtlist * 100 - 2.25


# What would you like to plot?
genVelocity.clearData()
#genVelocity.addData('PlayerHorSpeed', 'Player speed')
#genVelocity.addData('LLegPosY', "Left leg height")
#genVelocity.addData('RLegPosY', "Right leg height")
genVelocity.addData('LLHorSpeed', "Left Foot horizontal")
genVelocity.addData('EWMA_Left_Non_Abs', "EWMA Left Foot horizontal")
genVelocity.addData('EWMA_Right_Non_Abs', "EWMA Right Foot horizontal")
genVelocity.addData('RLHorSpeed', "Right Foot horizontal")
genVelocity.addData('LocomotionSpeed', 'Locomotion speed')
#genVelocity.addData('dirAngleRad', 'world direction radians')
#genVelocity.addData('LeftFootPitch', 'Left foot pitch')
#genVelocity.addData('AllTrackersWorking', 'All trackers working')
#genVelocity.addData('dt', 'deltaTime logging (centi seconds)')
#genVelocity.addData('headAngleRad', 'Head rotation')
#genVelocity.addData('StandingLeadingFootNr', 'right: 1.5, left: -1.5, none: 0')


#genVelocity.multipleVelocityPlots(dataframes, "StandingFootVelocity")



# Uncommenting this will plot all in succession, meaning you will get 80 popups!!!. You can also just input one of them replacing the for loop below.
# for i in range(0, len(dfs)):
#     genVelocity.plotVelocities(dfs[i], "LT: " + locomotionTechniques[i] + "Subject: " + subjectNrs[i])

