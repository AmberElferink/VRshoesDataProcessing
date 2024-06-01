# This script loops through all the TrackingData files
# It shows the plot with a slider to adjust the end time so you can see the trajectory growing.
# This is done so the data could be cut when the experiment was over, since sometimes did didn't happen automatically.
# Pressing Space, all data in the file loaded is DELETED after the time of the slider setting. CAREFUL IT TRULY DESTROYS DATA ON DISK
# Clicking cross shows the next plot.

import os
from pathlib import Path

import filterdata

import sys
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



directory = "UserTestTrackingData"

for root, dirs, files in os.walk(directory):
    for filename in files:
        filePath = os.path.join(root, filename)
        filePath = filePath.replace('\\', '/')
        #print(os.path.join(root, filename))
        if(filename.endswith('.csv') and filename.startswith("0_TrackingData")):
            print(filePath)

            df = filterdata.filterFileToDataFrame(filePath)

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

            plotTrajectoryIdx = 1 # 0 is player (including head movement), 1 is locomotionoffset, 2 is physical room position



            # for i in range(0, len(pointSetsX)):
            #     plt.plot(np.ma.masked_where(dontShow, dataset[pointSetsX[i]]), np.ma.masked_where(dontShow, dataset[pointSetsY[i]]), label = labelSets[i]) 
            #     plt.axis('equal')
            #     plt.legend()

            # dataset.plot(x=xaxis, y=yaxis, 
            #     xticks=np.arange(round(min(dataset[xaxisRange])), round(max(dataset[xaxisRange])), step=xstep),
            #     yticks=np.arange(round(min(dataset[yaxisRange])), round(max(dataset[yaxisRange])), step=ystep),
            #     ylabel= yaxis,
            #     )

            # Only do Settings after .plot call!!!!
            # Create the figure and the line that we will manipulate
            fig, ax = plt.subplots()
            trajectoryPlayer, = ax.plot(np.ma.masked_where(dontShow, dataset[pointSetsX[plotTrajectoryIdx]]), np.ma.masked_where(dontShow, dataset[pointSetsY[plotTrajectoryIdx]]), label = labelSets[plotTrajectoryIdx]) 
            fig.text(0.05, 0.95, filePath, fontdict=None)
            plt.axis('equal')
            plt.legend(loc='upper left')
                #line, = ax.plot(np.ma.masked_where(dontShowWithinTime, subSetWithinTime[pointSetsX[i]]), np.ma.masked_where(dontShowWithinTime, subSetWithinTime[pointSetsY[i]]), label = labelSets[i]) 

            # adjust the main plot to make room for the sliders
            fig.subplots_adjust(left=0.25, bottom=0.25)

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


            fig = plt.gcf()
            progressLine = fig.add_axes([0.25, 0.1, 0.65, 0.03])
            progress_slider = Slider(
                ax=progressLine,
                label='Frequency [Hz]',
                valmin=0.1,
                valmax=df["SecFromFullStart"].iloc[-1],
                valinit=df["SecFromFullStart"].iloc[-1],
            )

            currTimeSet = df["SecFromFullStart"].iloc[-1]
            def updateSliderPath(val):
                global currTimeSet
                currTimeSet = val
                subSetWithinTime = dataset[dataset["SecFromFullStart"] <= val]
                dontShowWithinTime = dontShow[dataset["SecFromFullStart"] <= val]
                print(subSetWithinTime)
                if len(subSetWithinTime["SecFromFullStart"]) > 0:
                    # for i in range(0, len(pointSetsX)):
                    trajectoryPlayer.set_xdata(np.ma.masked_where(dontShowWithinTime, subSetWithinTime[pointSetsX[plotTrajectoryIdx]]))
                    trajectoryPlayer.set_ydata(np.ma.masked_where(dontShowWithinTime, subSetWithinTime[pointSetsY[plotTrajectoryIdx]])) 

            def on_press(event):
                print('press', event.key)
                sys.stdout.flush()
                if event.key == ' ':
                    saveFilePath = filePath
                    selectedDf = df[df['SecFromFullStart'] <= currTimeSet]
                    selectedDf.to_csv(saveFilePath, encoding='utf-8')
                    message = "deleted data after " + str(currTimeSet) + " loaded from " + str(filePath) + " and saving to " + str(saveFilePath)
                    fig.text(0.05, 0.05, message, fontdict=None)
                    print(message)
                    fig.canvas.draw()


            progress_slider.on_changed(updateSliderPath)

            fig.canvas.mpl_connect('key_press_event', on_press)


            print("Total time:", df["SecFromFullStart"].iloc[-1]," seconds ")



            plt.show()