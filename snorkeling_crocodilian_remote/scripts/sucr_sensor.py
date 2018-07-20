
import rospy
import sucr_sensor_UI

from sensor_msgs.msg import Imu
from sensor_msgs.msg import Range
from std_msgs.msg import Bool
from std_msgs.msg import Float32

class HuskySensorManager:
	def __init__(self, window_manager):
		self.user_interface = window_manager.sensorUIHandler
		
		self.rosImuSubscriber = rospy.Subscriber("/arduino/imu_data", Imu, self.imuCallback)
		self.rosRangeSubscriber = rospy.Subscriber("/arduino/range_data", Range, self.rangeCallback)
		self.rosLimitSwitchSubscriber = rospy.Subscriber("/arduino/limit_state", Bool, self.limitCallback)
		self.rosArmPositionSubscriber = rospy.Subscriber("/arduino/arm/curr_pos", Float32, self.armCurrPosCallback)

	# IMU callback, runs whenever /arduino/imu_data has new data
	def imuCallback(self, imuData):
		self.currIMUData = imuData
		self.user_interface.updateIMU(imuData)
		
	# Range callback, runs whenever /arduino/range_data has new data
	def rangeCallback(self, rangeData):
		self.currRange = rangeData
		self.user_interface.updateRange(rangeData)

	# Limit switch callback, runs whenever /arduino/limit_state has new data
	# (whenever the limit switch changes state)
	def limitCallback(self, limitData):
		self.currLimitState = limitData
		self.user_interface.updateLimit(limitData)

	# Arm current position callback, runs whenever /arduino/arm/curr_pos has new data
	def armCurrPosCallback(self, armData):
		self.armCurrPos = armData
		self.user_interface.updateArmCurrPos(armData)
