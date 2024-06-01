# This scripts shows:
# Playerpos (The path of the headset position), 
# Locomotion offset (virtual locomotion position that creates the offset the user sees purely due to the shoes algorithm), 
# Roompos (the offset of the user in the physical room.)

# It shows this for the file loaded in filterData

import filterdata

import math
import numpy as np
import pandas
from matplotlib import pyplot as plt
import matplotlib.axes._axes as axes
import matplotlib.figure as figure
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from IPython.display import display
from matplotlib.widgets import Button, Slider

df = filterdata.filterFileToDataFrame('UserTestTrackingData/AverageShoes/2/Scenario2_20230404_10371816/0_TrackingData_20230404_10371816.csv')

task1 = df[df['Task'].str.contains("MW")]
task2 = df[df['Task'].str.contains("BW")]
task3 = df[df['Task'].str.contains("CW")]


# with pandas.option_context('display.min_rows', 300, 'display.max_columns', 10):
#     display(df[['isMoving', 'MoveSectionLabels', 'avgMovingSection']].head(300))

dataset = df
dontShow = dataset['isMoving'] == False #dontShow = False #if you do not want to filter 
#for calculations, to work with the unfiltered: dataset[~dontShow]

xaxisRange = 'PlayerX'
yaxisRange = 'PlayerZ'
ystep = 2
xstep = 2

pointSetsX = ['PlayerX', 'LocomotionOffX', 'RoomPosX']
pointSetsY =  ['PlayerZ', 'LocomotionOffZ', 'RoomPosZ']
labelSets = ['Player Position', 'Locomotion Offset', 'RoomPos']



for i in range(0, len(pointSetsX)):
    plt.plot(np.ma.masked_where(dontShow, dataset[pointSetsX[i]]), np.ma.masked_where(dontShow, dataset[pointSetsY[i]]), label = labelSets[i]) 
    plt.axis('equal')
    plt.legend()

# dataset.plot(x=xaxis, y=yaxis, 
#     xticks=np.arange(round(min(dataset[xaxisRange])), round(max(dataset[xaxisRange])), step=xstep),
#     yticks=np.arange(round(min(dataset[yaxisRange])), round(max(dataset[yaxisRange])), step=ystep),
#     ylabel= yaxis,
#     )

# Only do Settings after .plot call!!!!

ax = plt.gca() #type: axes.Axes
ax.set_xticks(np.arange(round(min(dataset[xaxisRange])), round(max(dataset[xaxisRange])), step=xstep))
ax.set_yticks(np.arange(round(min(dataset[yaxisRange])), round(max(dataset[yaxisRange])), step=ystep))
ax.set_xlabel('X', loc = "right")
ax.set_ylabel('Y', rotation=0, loc="top")
ax.set_adjustable("box")
ax.set_xbound(min(dataset[xaxisRange]), max(dataset[xaxisRange]))

# ... and label them with the respective list entries
# ax.set_xticklabels(farmers)
# ax.set_yticklabels(vegetables)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(12)
    #label.set_bbox(dict(facecolor='y', edgecolor='None', alpha=0.7))


# TODO: maybe add minimal movement to prevent the float imprecisions to count?
def totalDistance(xlist, ylist):
    if (len(xlist) != len(ylist)):
        return -1
    sum = 0
    for i in range(1, len(xlist)):
        if type(xlist) == pandas.Series:
            sum += distance(xlist.iloc[i] - xlist.iloc[i - 1], ylist.iloc[i] - ylist.iloc[i - 1])
        else:
            sum += distance(xlist[i] - xlist[i - 1], ylist[i] - ylist[i - 1])
    return sum

def distance(x, y):
    return math.sqrt(x*x + y*y)


if type(dontShow) == pandas.Series:
    for i in range(0, len(pointSetsX)):
        print("Total Distance", labelSets[i], totalDistance(dataset[~dontShow][pointSetsX[i]], dataset.loc[~dontShow][pointSetsY[i]]))
else:
    for i in range(0, len(pointSetsX)):
        print("Total Distance", labelSets[i], totalDistance(dataset[pointSetsX[i]], dataset[pointSetsY[i]]))



# TODO: substract repositioning pieces
# task1Time = task1["SecFromFullStart"].iloc[-1]
# task2Time = task2["SecFromFullStart"].iloc[-1] - task1Time
# task3Time = task3["SecFromFullStart"].iloc[-1] - task2Time

print("Total time:", df["SecFromFullStart"].iloc[-1]," seconds ")



plt.show()