import rospy
import sucr_gui
import sucr_input
import sucr_ROS

from std_msgs.msg import Bool
from husky_msgs.msg import HuskyStatus

class HuskyStatusManager:
	def __init__(self, window_manager):
		self.window_manager = window_manager

		self.isEStopped = True;
		self.currStatus = None;

		self.rosStatusSubscriber = rospy.Subscriber("/status", HuskyStatus, self.statusCallback)

	def statusCallback(self, message):
		self.currStatus = message
		
		if self.currStatus.e_stop != self.isEStopped:
			self.window_manager.updateEStop(self.currStatus.e_stop)
			self.isEStopped = self.currStatus.e_stop

		self.window_manager.updateStatus(self.currStatus)
		
