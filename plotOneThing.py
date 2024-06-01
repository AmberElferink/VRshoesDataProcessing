import filterdata
import genVelocity

dataframes = filterdata.filterFileToDataFrame('UserTestTrackingData/StandingFootVelocity/1/Scenario2_20230403_16213153/0_TrackingData_20230403_16213153.csv')



genVelocity.clearData()
genVelocity.addData('HipAngle', 'Hip')
genVelocity.addData('HeadAngle', 'Head')
genVelocity.addData('StandingAngle', 'StandingAngle')
genVelocity.addData('AvgFeetAngle', 'Avg')


genVelocity.plotVelocities(dataframes, "Title")


# genVelocity.clearData()
# genVelocity.addData('HeadRotY', 'Head')
# genVelocity.addData('LLegRotY', 'LeftFoot')
# genVelocity.addData('RLegRotY', 'RightFoot')
# genVelocity.addData('HipRotY', 'Hip')
# genVelocity.plotVelocities(dataframes, "rawAngles")

