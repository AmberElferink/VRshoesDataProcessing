import filterdata
import math
import numpy as np
import pandas as pd
import genSpeed

#df = filterdata.filterFileToDataFrame('0_TrackingData_20230215_17133531.csv')

# (angle + a) % 360 - 180. a can be set if the interesting part of the angle is usually at the wrapping around value (sometimes 5 degrees, sometimes 355 degrees)
def processDirections(df):
    #df['TargetPosY'] = df['TargetPosY'] % 360 - 180 #np.where(df['TargetPosY'] >= 180, df['TargetPosY'] - 360, df['TargetPosY'])
    df['DirectionRotY'] = (df['DirectionRotY'] -90) % 360 - 180
    df['dirAngleRad'] = df['DirectionRotY'] * math.pi / 180

    df['HeadRotY'] = (df['HeadRotY'] + 90)% 360 - 180
    df['headAngleRad'] = df['HeadRotY'] * math.pi / 180

    df['LLegRotZ'] = (df['LLegRotZ'] + 90 )% 360 - 180
    df['LeftFootPitch'] = df['LLegRotZ'] * math.pi / 180
    

    return df
