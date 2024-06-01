import filterdata

import pandas
import numpy as np

# this contains the logic to see tracking losses and times for a single file. This was further implemented to loop over all data in allData.py because that was easier.

df = filterdata.filterFileToDataFrame('UserTestTrackingData/StandingFootVelocity/1/Scenario2_20230403_16213153/0_TrackingData_20230403_16213153.csv')
timeThreshold = 0.2 # in seconds time a trackerloss should be active before it is counted here

trackerlossdataframe = pandas.DataFrame(columns = ['NrTrackerlosses', 'LocomotionTechnique', 'SubjectNr'])



# log all sections of data where the trackers are not working
sectionList, sectionNr, sectionNrToFirstLastIdx = filterdata.BoolSectionDef(df["AllTrackersWorking"], False) 

print(df)

# calculate time difference between end and start of te section with tracker loss
sectionNrToTimeTaken = {}
sectionNrToThresholdedTimeTaken = {}
for i in range(1, sectionNr): 
    sectionNrToTimeTaken[i] = df["SecSinceStart"][sectionNrToFirstLastIdx[i][1]] - df["SecSinceStart"][sectionNrToFirstLastIdx[i][0]]
    if sectionNrToTimeTaken[i] > timeThreshold:
        sectionNrToThresholdedTimeTaken[i] = sectionNrToTimeTaken[i]

print("tracker loss number with time of lost connection behind it in seconds")
print(sectionNrToTimeTaken)
print("same, but filtered to contain only tracker losses above the time length of the threshold set above")
print(sectionNrToThresholdedTimeTaken)
print("number of trackerlosses above the time threshold for this file")
print(len(sectionNrToThresholdedTimeTaken))

# For this, LocomotionTechnique is needed which is only created when loading an entire folder. Therefore this was continued in alldata.
# new_row = {'NrTrackerlosses':len(sectionNrToThresholdedTimeTaken), 'LocomotionTechnique':df["LocomotionTechnique"][0], 'SubjectNr':df["SubjectNr"][0]}
# trackerlossdataframe = trackerlossdataframe.append(new_row, ignore_index=True)