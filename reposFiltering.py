# The data was already correctly stopped with repositioning including time.
# For sanity check this is proven with the lines below (sum comes to 0, so no time gap larger than 200ms)

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

df = filterdata.filterFileToDataFrame('UserTestTrackingData/AverageShoes/1/Scenario2_20230403_16440493/0_TrackingData_20230403_16440494.csv')

print((df["SecSinceStart"].diff() > 0.2).sum())
print(df["SecSinceStart"].diff())