# What is this?
This is a repository to process tracking data from the VR shoes experiment (LINKKKKKK to full paper), to plots over time and csv files ready for statistical analysis in R. It can calculate speed plots, calculate csv files for statistical analysis on completionTime and trackerlosses. It also has a function to manually clip the data to the end of the experiment based on the trajectory.

- [Processing tracker data Github](https://github.com/AmberElferink/VRshoesDataProcessing) is this project: Processing tracking data from Unity to plots and csv files ready for statistic analysis.
- [VR shoes R statistics processing Github](https://github.com/AlexisDerumigny/Reproducibility-VR-Project). For statistics processing in R.
- [VR shoes Unity Environment Github](https://github.com/AmberElferink/LocomotionEvaluation). For the virtual Unity environment in the user test that the users walked in and gathered the tracking data.


## Raw User Experience data / Questionnaires

- [Raw Data Consent form + demographics + Habituation questions Google Spreadsheet](https://docs.google.com/spreadsheets/d/18L1FDxcECkfh0YWAIcpaJXAqzQvc4uHcm83MKERbGXg/edit?usp=sharing)
- [Raw Data UX answers for each trial](https://docs.google.com/spreadsheets/d/1mwZUULM_gU6-xjh3AGX8X6qKFkpROcqetkRowhyOwM8/edit?usp=sharing)
- [Raw SSQ scores and calculation](https://docs.google.com/spreadsheets/d/1Z6ZEOBB_HKG5OKnwlWWeoUAu6VnMPOgTiw3vIsVPwAk/edit?usp=sharing)
- [Google Sheets algorithm design iterations with Pilot data](https://docs.google.com/spreadsheets/d/19XF_UmUEpfjw7bddJwMBGtok1HHl3Nf5debJBxfp_nA/edit?usp=sharing)


If you want to use the questionnaire in your own experiment, you can copy the form for your own use with the following links:
- [Consent form + demographics + Habituation Google Form ](https://docs.google.com/forms/d/16HUnzGaGV9iMNdykEuPBm8y9UqQQHBMW23HlNOklhPY/copy)
- [UX questions for each trial Google Form](https://docs.google.com/forms/d/1SUaqCdrhtiCeiOQPW767yPz0z7UIzTfgg31t2_o47Wo/copy)


## How to install
Use Anaconda to manage multiple python versions/packages on your pc.
The anaconda environment settings and installed packages are given in anaconda_environment.yaml, 
and can be directly imported via the Anaconda Navigator GUI to create an environment that can run this project.
Python version: 3.10.12.
I opened the folder in VScode, but you can use an editor of your choosing.
If using VScode, I recommend installing the Python, Python Debugger, and Pylance extensions. Set the Anaconda environment there as interpreter Ctrl+Shift+P,

## What is in what file?



## Tracking processing
From the python scripts, the csv files are generated for further processing in R. Below describes the raw files, and the python files to generate the plots and these csvs.

### UserTestTrackingData folder
The UserTestTrackingData contains the data for the user from the experiment. 
It's subfolder have data organized as: 
`direction algorithm (locomotion technique / LT) > subject number > Folder with data.`

This folder with data often contains `0_TrackerData` (we use this), and extra files, which are not used in our analysis, but provided by the previous Cannovo et al (2021) work based on each task. While 0_TrackerData contains all tracker data for postprocessing needs, the folder also contains a file called `rawTrackers`, which is direct position/rotation data from the trackers in Unity, which can be used to directly replay the tracker motion in Unity for that participant via the AnimateTrackers script in Unity.

### Loading an individual file
Note, in some files only a single data file is loaded (for example genTrajectory): `df = filterdata.filterFileToDataFrame('UserTestTrackingData/AverageShoes/2/Scenario2_20230404_10371816/0_TrackingData_20230404_10371816.csv')`. In that case, you can get the path if you are working in VScode, by navigating to the file you want to load > Right click > Copy Relative path, paste it, and REPLACE \ by /. If you don't, it will throw an error not explaining what is wrong!

### Loading multiple/all files
This is handled by filterdata.py, and called in allData.py. See examples there :)

### filterdata.py
This has functions related to load and process folders or files in UserTestTrackingData to dataframes usable in python. It can also calculates extra variables such as dt's (delta times), speed data based on real tracked data, filtered speed data based on if motion is active or not, and more.
These functions are used to load and preprocess files/folders in other scripts.

### genTrajectory
- genTrajectory.py plots the trajectory of a single trial at once.
- genTrajectory-interactive-trajectory.py plots the trajectory with interactive slider that controls the time, so you can see where the user slowed down/stopped/went fast as well.
- genTrajectory-interactive-trajectory-loopfiles.py this was used to loop through all trials, and manually cut the data in UserTestTrackingData the end of each trial.

### allData.py
Loads all data from UserTestTrackingData, and delivers all csv files and can plot speeds.
Near the end of the file, we print all collumn names. Each column is explained further below.
```
print("column headers:")
print("\n".join(allcontainingDataFrame.columns.values.tolist()))
```
Uncomment the relevant lines to overwrite the .csv files you want.

### trackingloss.py
This was a test file that can show data relevant to tracking loss for a single data file.
The full csv is calculated in allData.py.

- col `AllTrackersWorking` shows what trackers were and were not working properly.
- col `TrackersNotWorking` contains name indicators of the trackers that were not working at the moment.

### genSpeed.py
This has functions to plot speeds and variables over time. You can add columns to this.


## Definitions of columns
To get any of this data, go to allData.py and process the data there: `allcontainingDataFrame['MyColName']`, with more examples on how to filter in allData.py.

#### General cols in allcontainingDataFrame (in allData.py):
- col `SecSinceStart` is seconds since the start of the task in the trial. Since we don't consider tasks important, there is also `SecFromFullStart` in calculates the seconds from the start of the full trial.

- `SubjectNr`: subject number
- `LocomotionTechnique`: condition (algorithm direction technique) used: AverageFoot, St
- `Task`: from Cannovo et al (2021), they had multiple tasks: MW: MultiStraightLineWalking in the museum, BW: Backwards walking (we let user walk this forwards), and CW: Curved walking in the hallway.
- `Timestamp`: Time and date during the trial.

#### Position/Rotation tracked related
- `PlayerX`, `PlayerY`, `PlayerZ`: virtual player head position in world space, including the offset with respect to the center of the real room (taking roomscale walking into account, as well as locomotion offset from the algorithm). X and Z are the horizontal range, and Y is up.
- `LocomotionOffX`, `LocomotionOffY`, `LocomotionOffZ`: virtual player position in world space, only considering the locomotion offset from the algorithm, and not wandering from the center of the room.
- - `RoomPosX`, `RoomPosZ`: Horizontal position offset from the startingpoint in the physical room.
- `PlayerRotX`, `PlayerRotY`, `PlayerRotZ`: rotation of player in virtual space, includes physical head orientation and locomotion orientation. Double check if this is true from log in Unity, not sure anymore since it is not used in analysis due to dropping direction analysis (see directions.py).
- `HeadPosX`, `HeadPosY`, `HeadPosZ`: Head position in room space.
- `HeadRotX`, `HeadRotY`, `HeadRotZ`: Head rotation in room space.
- `LHandPosX`, `LHandPosY`, `LHandPosZ`, `LHandRotX`, `LHandRotY`, `LHandRotZ`, `RHandPosX`, `RHandPosY`, `RHandPosZ`, `RHandRotX`, `RHandRotY`, `RHandRotZ`: From original work Cannovo that used controllers in hands. Our participants were not tracked on the hands, so this is not used.
- `LLegPosX`, `LLegPosY`, `LLegPosZ`, `LLegRotX`, `LLegRotY`, `LLegRotZ`, `RLegPosX`, `RLegPosY`, `RLegPosZ`, `RLegRotX`, `RLegRotY`, `RLegRotZ`: Raw tracker positions and rotations of the left and right legs.
- `HipPosX`, `HipPosY`, `HipPosZ`, `HipRotX`, `HipRotY`, `HipRotZ`: Raw tracker positions and rotations of hip tracker.


#### Speed (calculation) related
- `PlayerHorSpeed` and `LocomotionSpeed`: PlayerHorSpeed also includes motion of the user moving physically from the center of the room, while LocomotionSpeed only considers the speed from the tracker calculation. Was calculated in unity from derivation of PlayerX/Z.
- `LLHorSpeed`, `RLHorSpeed`, `HipHorSpeed`: calculated in Unity from deriving `LLPosX`, `LLPosZ`, and similar for the others in Unity.
- `DirectionRotX` `DirectionRotY`, `DirectionRotZ`: Locomotion rotation result from algorithm in euler angles.
- `RightLifted`, `RightStanding`, `LeftLifted`, `LeftStanding`: True when that leg is standing/lifting according to our algorithm.
- `StandingLeadingFootNr`, `LiftedLeadingFootNr`: To plot standing/leading foot over time in plots, left/right standing/lifted can be given numbers to display these booleans in the plots with speed data. This is done in filterdata.py.
- `StandingLeadingFoot`, `LiftedLeadingFoot`: What foot is actually used to use standingFoot/liftedFoot choices, since sometimes two feet are on the ground at the same time.
- `EWMA_Right`, `EWMA_Left`: Exponentially Weighted Mean Average during the algorithms movement calculation, but recalculated in python from LLHorSpeed and RLHorSpeed.
- `EWMA_Left_Non_Abs`, `EWMA_Right_Non_Abs`, `EWMA_Both_Non_Abs`: EWMA without the absolute call so you can see what it does signed.
- `isMoving`: some things, such as average walking speed, you only want to run over periods where someone was actually walking. This is a boolean mask that can be used to include/exclude data based on this criterium. It's currently calculated and the threshold is set within filterdata.py.
- `MoveSectionLabels`: label each section where the person is moving with a different letter. This was handy for some calculations, such as avgMovingSection.
- `avgMovingSection`: calculate the average speed over the whole duration of a letter. Also throw it away if a section is shorter than 1.5 seconds

#### Angle related:
We decided to abandon the objective analysis of angles, since it caused confusion and did not contribute.
- `LAvgVelAngle`, `RAvgVelAngle`: Angle of left/right foot velocity vector.
- `LAvgVelMag`, `RAvgVelMag`: magnitude of the velocity vector (speed) of the left/right foot.
- `LiftedAngle`, `StandingAngle`: angle of the current leading lifted/standing foot.
- `HipAngle`, `HeadAngle`, `AvgFeetAngle`: Angles of direction conditions.
- `GWAngle`: don't remember, and it's not used in current analysis since we don't analyze directions anymore.
