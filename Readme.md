# What is this?
This is a repository to process tracking data from the VR shoes experiment (LINKKKKKK), to plots over time and csv files ready for statistical analysis in R. It can calculate speed plots, calculate csv files for statistical analysis on completionTime and trackerlosses. It also has a function to manually clip the data to the end of the experiment based on the trajectory.

- For statistics processing in R, see (LINNKKKKKKKK).
- For the virtual Unity environment in the user test that gathered the data see (LINNKKKKKKK).

## How to install
Use Anaconda to manage multiple python versions/packages on your pc.
The anaconda environment settings and installed packages are given in anaconda_environment.yaml, 
and can be directly imported via the Anaconda Navigator GUI to create an environment that can run this project.
Python version: 3.10.12

## What is in what file?
### UserTestTrackingData folder
The UserTestTrackingData contains the data for the user from the experiment. 
It's subfolder have data organized as: 
`direction algorithm (locomotion technique / LT) > subject number > Folder with data.`

This folder with data often contains `0_TrackerData` (we use this), and extra files, which are not used in our analysis, but provided by the previous Cannovo et al (2021) work based on each task. The folder also contains a file called `rawTrackers`, which is direct position/rotation data from the trackers in Unity, which can be used to directly replay the tracker motion in Unity for that participant via the AnimateTrackers script.

### filterdata.py
This has functions related to load and process folders or files in UserTestTrackingData to dataframes usable in python. It can also calculates extra variables such as dt's (delta times), speed data based on real tracked data, filtered speed data based on if motion is active or not, and more.
These functions are used to load and preprocess files/folders in other scripts.

### genTrajectory
- genTrajectory.py plots the trajectory of a single trial at once.
- genTrajectory-interactive-trajectory.py plots the trajectory with interactive slider that controls the time, so you can see where the user slowed down/stopped/went fast as well.
- genTrajectory-interactive-trajectory-loopfiles.py this was used to loop through all trials, and manually cut the data in UserTestTrackingData the end of each trial.

### allData.py
Loads all data from UserTestTrackingData, and delivers all csv files and can plot speeds.

### trackingloss.py
This was a test file that can show data relevant to tracking loss for a single data file.
The full csv is calculated in allData.py.

### genVelocity.py

