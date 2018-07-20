import rospy
import sucr_gui
import sucr_input
import sucr_ROS

from PIL import Image as PImage
from PIL import ImageTk
import imutils
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ImageStream:
	def __init__(self, window_manager):
		self.window_manager = window_manager
		self.bridge = CvBridge()

		self.cameraSubsciber = rospy.Subscriber("/usb_cam/image_raw", Image, self.cameraCallback)

	def cameraCallback(self, image):
		try:
			orig_cv_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
			cv_image = imutils.resize(orig_cv_image, width = 700)
			
			display_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
			display_image = PImage.fromarray(display_image)
			display_image = ImageTk.PhotoImage(display_image)

			self.window_manager.updateCameraFeed(display_image,orig_cv_image)
		except CvBridgeError as e:
			print(e)
