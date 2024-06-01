import filterdata
import genSpeed

dataframes = filterdata.filterFileToDataFrame('UserTestTrackingData/StandingFootVelocity/1/Scenario2_20230403_16213153/0_TrackingData_20230403_16213153.csv')



genSpeed.clearData()
genSpeed.addData('HipAngle', 'Hip')
genSpeed.addData('HeadAngle', 'Head')
genSpeed.addData('StandingAngle', 'StandingAngle')
genSpeed.addData('AvgFeetAngle', 'Avg')


genSpeed.plotSpeed(dataframes, "Title")


# genSpeed.clearData()
# genSpeed.addData('HeadRotY', 'Head')
# genSpeed.addData('LLegRotY', 'LeftFoot')
# genSpeed.addData('RLegRotY', 'RightFoot')
# genSpeed.addData('HipRotY', 'Hip')
# genSpeed.plotSpeed(dataframes, "rawAngles")

