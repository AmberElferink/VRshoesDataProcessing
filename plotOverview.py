import numpy as np
import pandas
from matplotlib import pyplot as plt
import matplotlib.axes._axes as axes
import matplotlib.figure as figure
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from IPython.display import display

# plotVelocities(filterdata.filterFileToDataFrame('0_TrackingData_20230215_17133531.csv'))

xaxisRange = 'SecFromFullStart'
yaxisRange = 'RLHorSpeed'
ystep = 0.5
xstep = 2


pointSetsX = 'SecFromFullStart'
pointSetsY =  ['HeadPosX', 'HeadPosY', 'HeadPosZ', 'HeadRotX', 'HeadRotY', 'HeadRotZ']
labelSets = ['Right Leg horizontal speed', 'Left Leg horizontal speed', 'Locomotion speed', 'PlayerHorSpeed']



def plotOverview(df, title):
    fig, axs = plt.subplots(2)
    fig.suptitle('Vertically stacked subplots')
    dataset = df
    dontShow = dataset['isMoving'] == False #dontShow = False #if you do not want to filter 

    for a in range(axs):
        for i in range(0, len(pointSetsY)):
            axs[a].plot(np.ma.masked_where(dontShow, dataset[pointSetsX]), np.ma.masked_where(dontShow, dataset[pointSetsY[i]]), label = labelSets[i])  
            axs[a].axis('equal')
            axs[a].title(title)
            axs[a].legend()

 # Only do Settings after .plot call!!!!

    ax = plt.gca() #type: axes.Axes

    ax.set_xticks(np.arange(round(min(dataset[xaxisRange])), round(max(dataset[xaxisRange])), step=xstep))
    ax.set_yticks(np.arange(round(min(dataset[yaxisRange])), round(max(dataset[yaxisRange])), step=ystep))
    ax.set_xlabel('X', loc = "right")
    ax.set_ylabel('Y', rotation=0, loc="top")
    ax.set_adjustable("box")
    ax.set_xbound(min(dataset[xaxisRange]), max(dataset[xaxisRange]))
    #ax.set_xbound(min(dataset[xaxisRange]), 24)

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





    ax[a].show()










    dataset = df
    dontShow = dataset['isMoving'] == False #dontShow = False #if you do not want to filter 
    #for calculations, to work with the unfiltered: dataset[~dontShow]


    # colored line plots, multiple subplots
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/multicolored_line.html

    fig, ax = plt.subplots() # type:figure.Figure, axes.Axes

    for i in range(0, len(pointSetsY)):
        plt.plot(np.ma.masked_where(dontShow, dataset[pointSetsX]), np.ma.masked_where(dontShow, dataset[pointSetsY[i]]), label = labelSets[i]) 
        plt.axis('equal')
        plt.title(title)
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
    #ax.set_xbound(min(dataset[xaxisRange]), 24)

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





    plt.show()

