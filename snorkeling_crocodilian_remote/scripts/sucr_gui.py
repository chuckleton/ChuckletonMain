
import Tkinter as tk
from ttk import *
import datetime

import sucr_input
import sucr_status_UI
import sucr_sensor_UI

import os
import cv2

from husky_msgs.msg import HuskyStatus


# Manages the visual GUI methods
class WindowManager:

	# Initializes the windows of the GUI
	def __init__(self,config):
		self.config = config

		self.window = tk.Tk()

		self.tab_control = Notebook(self.window)
		self.drive_tab = tk.Frame(self.tab_control)
		self.main_tab = tk.Frame(self.tab_control)
		self.status_tab = tk.Frame(self.tab_control)

		self.joyVariable = tk.StringVar()

	# Draws the initial window in the GUI
	def drawWindow(self):
		# Sets up the title and size of the window
		self.window.title = "Snorkeling Crocodilian Rover"
		self.window.geometry('1620x900')

		# Adds tabs to the window
		# Tab used while driving
		self.tab_control.add(self.drive_tab, text = 'Drive')
		# Tab used for setting parameters
		self.tab_control.add(self.main_tab, text = 'Config')
		# Tab used for diagnostic info
		self.tab_control.add(self.status_tab, text = 'Status')

		self.statusUIHandler = sucr_status_UI.StatusUIHandler(self,self.status_tab,self.drive_tab,self.main_tab)
		self.sensorUIHandler = sucr_sensor_UI.SensorUIHandler(self,self.status_tab,self.drive_tab,self.main_tab, self.config)

		# IP Label, may not be needed
		IP_lbl = tk.Label(self.main_tab,text = "IP Address")
		IP_lbl.grid(column = 0, row = 1)
		IP_Entry = tk.Entry(self.main_tab, width = 15)
		IP_Entry.grid(column = 1, row = 1)
		
		# Sets the row the joystick menus start on
		joyMenuStart = 5
		
		# Combobox and label for choosing joystick
		joy_lbl = tk.Label(self.main_tab, text = "Joystick ")
		joy_lbl.grid(column = 0, row = joyMenuStart)
		
		self.joyMenu = Combobox(self.main_tab, textvariable=self.joyVariable, width = 30, state = "readonly")
		self.joyMenu.grid(column = 1, row = joyMenuStart)
		self.joyMenu.bind("<<ComboboxSelected>>", self.joyChanged)

		# Comboboxes and labels for choosing joystick axes
		joyX_lbl = tk.Label(self.main_tab, text = "X-Axis ")
		joyX_lbl.grid(column = 0, row = joyMenuStart+1)
		self.joyXMenu = Combobox(self.main_tab, width = 10, state = "readonly")
		self.joyXMenu.grid(column = 1, row = joyMenuStart+1)
		self.joyXMenu.bind("<<ComboboxSelected>>", self.joyXChanged)

		joyAngular_lbl = tk.Label(self.main_tab, text = "Angular-Axis ")
		joyAngular_lbl.grid(column = 0, row = joyMenuStart+2)
		self.joyAngularMenu = Combobox(self.main_tab, width = 10, state = "readonly")
		self.joyAngularMenu.grid(column = 1, row = joyMenuStart+2)
		self.joyAngularMenu.bind("<<ComboboxSelected>>", self.joyAngularChanged)

		joyDeadman_lbl = tk.Label(self.main_tab, text = "Deadman Button ")
		joyDeadman_lbl.grid(column = 0, row = joyMenuStart+3)
		self.joyDeadmanMenu = Combobox(self.main_tab, width = 10, state = "readonly")
		self.joyDeadmanMenu.grid(column = 1, row = joyMenuStart+3)
		self.joyDeadmanMenu.bind("<<ComboboxSelected>>", self.joyDeadmanChanged)

		joyTurbo_lbl = tk.Label(self.main_tab, text = "Turbo Button ")
		joyTurbo_lbl.grid(column = 0, row = joyMenuStart+4)
		self.joyTurboMenu = Combobox(self.main_tab, width = 10, state = "readonly")
		self.joyTurboMenu.grid(column = 1, row = joyMenuStart+4)
		self.joyTurboMenu.bind("<<ComboboxSelected>>", self.joyTurboChanged)

		joyArm_lbl = tk.Label(self.main_tab, text = "Arm-Axis ")
		joyArm_lbl.grid(column = 0, row = joyMenuStart+5)
		self.joyArmMenu = Combobox(self.main_tab, width = 10, state = "readonly")
		self.joyArmMenu.grid(column = 1, row = joyMenuStart+5)
		self.joyArmMenu.bind("<<ComboboxSelected>>", self.joyArmChanged)

		# Sets the length of the sliders for choosing max speeds
		speedScaleLength = 125

		# Sliders for choosing max speeds for the rover, linear and angular, turbo and normal
		self.setXNormalMax = tk.Scale(self.main_tab, length=speedScaleLength,label="Max Linear Speed (m/s)",orient=tk.VERTICAL,from_=1.0,to=0.2,resolution=0.025,command=self.updateSpeedConfig)
		self.setAngularNormalMax = tk.Scale(self.main_tab, length = speedScaleLength,label="Max Angular Speed (rad/s)",orient=tk.VERTICAL,from_=1.0,to=0.0,resolution=0.025,command=self.updateSpeedConfig)

		self.setXNormalMax.set(self.config.xMax)
		self.setAngularNormalMax.set(self.config.angularMax)

		self.setXNormalMax.grid(column = 6, row = 2)
		self.setAngularNormalMax.grid(column = 7, row = 2)

		self.setXTurboMax = tk.Scale(self.main_tab, length=speedScaleLength,label="Turbo Linear Speed (m/s)",orient=tk.VERTICAL,from_=1.0,to=0.2,resolution=0.025,command=self.updateSpeedConfig)
		self.setAngularTurboMax = tk.Scale(self.main_tab, length = speedScaleLength,label="Turbo Angular Speed (rad/s)",orient=tk.VERTICAL,from_=1.0,to=0.0,resolution=0.025,command=self.updateSpeedConfig)

		self.setXTurboMax.set(self.config.xTurboMax)
		self.setAngularTurboMax.set(self.config.angularTurboMax)

		self.setXTurboMax.grid(column = 6, row = 4)
		self.setAngularTurboMax.grid(column = 7, row = 4)


		# Read-only sliders giving a visual representation of commands currently being sent to the rover
		self.xVisSlider = tk.Scale(self.drive_tab,from_=self.config.xTurboMax,to=-self.config.xTurboMax,orient=tk.VERTICAL,resolution=0.01,state='disabled',label="X-Axis Value",length = 250,sliderlength=10)
		self.xVisSlider.grid(column = 1,row = 9)

		self.angularVisSlider = tk.Scale(self.drive_tab,from_=self.config.angularTurboMax,to=-self.config.angularTurboMax,orient=tk.HORIZONTAL,resolution=0.01,state='disabled',label="Angular-Axis Value",length = 250,sliderlength=10)
		self.angularVisSlider.grid(column = 1,row = 10)


		# Read-only buttons showing whether the deadman and turbo buttons are engaged (RED = DISENGAGED, GREEN = ENGAGED)
		self.deadmanButtonVis = tk.Button(self.drive_tab,bg="red",text="ENABLE",height = 14,width = 21)
		self.turboButtonVis = tk.Button(self.drive_tab,bg="red",text="TURBO",height = 14,width = 21)
		self.deadmanButtonVis.grid(column = 2,row = 9)
		self.turboButtonVis.grid(column = 4,row = 9)

		self.videoFeedPanel = None
		

		self.tab_control.grid(row = 0, column = 0)











	# Activated when a speed control slider is moved, changes the max speeds and changes the visualization sliders to only show a max of the max turbo speed
	def updateSpeedConfig(self, *args):
		self.config.setSpeeds(float(self.setXNormalMax.get()),float(self.setXTurboMax.get()),float(self.setAngularNormalMax.get()),float(self.setAngularTurboMax.get()))

		self.xVisSlider.config(from_=self.config.xTurboMax,to=-self.config.xTurboMax)
		self.angularVisSlider.config(from_=self.config.angularTurboMax,to=-self.config.angularTurboMax)
		

	# Gives a visual display of the joystick, moves the sliders to the current commanded velocity and changes the colors of the turbo and deadman buttons
	def drawJoystick(self, linear, angular, deadman, turbo, arm):
		self.xVisSlider.config(state='normal')
		self.xVisSlider.set(linear)
		self.xVisSlider.config(state='disabled')

		self.angularVisSlider.config(state='normal')
		self.angularVisSlider.set(angular)
		self.angularVisSlider.config(state='disabled')

		self.sensorUIHandler.updateArmSlider(arm)

		if deadman == 1:
			self.deadmanButtonVis.config(bg="green")
		else:
			self.deadmanButtonVis.config(bg="red")
		if turbo == 1:
			self.turboButtonVis.config(bg="green")
		else:
			self.turboButtonVis.config(bg="red")

	# methods called when menus are changed, updates the values of the selected joystick and selected axes and buttons
	def joyXChanged(self, *args):
		self.joy.setXAxis(self.joyXMenu.get())
		self.joyXMenu.selection_clear()

	def joyAngularChanged(self, *args):
		self.joy.setAngularAxis(self.joyAngularMenu.get())
		self.joyAngularMenu.selection_clear()

	def joyDeadmanChanged(self, *args):
		self.joy.setDeadmanButton(self.joyDeadmanMenu.get())
		self.joyDeadmanMenu.selection_clear()

	def joyTurboChanged(self, *args):
		self.joy.setTurboButton(self.joyTurboMenu.get())
		self.joyTurboMenu.selection_clear()

	def joyArmChanged(self, *args):
		self.joy.setArmAxis(self.joyArmMenu.get())
		self.joyArmMenu.selection_clear()

	def joyChanged(self, *args):
		self.joy.updateJoystickName(self.joyMenu.get())
		self.joyMenu.selection_clear()

	# Called from sucr_input.py, updates the list of joysticks to choose from
	def updateJoystickList(self, joy_list):
		self.joyMenu['values'] = joy_list

	# Called from sucr_input.py, updates the list of axes to choose from once a joystick has been selected
	def updateJoystickAxisChoices(self, joyAxisList, joyButtonList):
		self.joyXMenu['values'] = joyAxisList
		self.joyAngularMenu['values'] = joyAxisList
		self.joyArmMenu['values'] = joyAxisList
		self.joyDeadmanMenu['values'] = joyButtonList
		self.joyTurboMenu['values'] = joyButtonList

	# Set the address of the input class
	def setupJoy(self,joy_addr):
		self.joy = joy_addr


	# Camera Feed:
	def updateCameraFeed(self,image,cv_image):
		self.cv_image = cv_image
		if self.videoFeedPanel is None:
			self.videoFeedPanel = tk.Label(self.drive_tab, image = image)
			self.videoFeedPanel.image = image
			self.videoFeedPanel.grid(row = 11, column = 10, padx = 5, pady = 5)

			self.takeImageButton = tk.Button(self.drive_tab,text = "Save Image",command = self.takePic)
			self.takeImageButton.grid(row = 12, column = 10)
		else:
			self.videoFeedPanel.configure(image = image)
			self.videoFeedPanel.image = image

	def takePic(self):
		ts = datetime.datetime.now()
		name = "{}.png".format(ts.strftime("%Y-%m-%d-%H-%M-%S"))
		oldDir = os.getcwd()
		os.chdir(self.config.imagePath)
		cv2.imwrite(name,self.cv_image)
		os.chdir(oldDir)
		
	def updateEStop(self, eStop_status):
		self.statusUIHandler.updateEStop(eStop_status)

	def updateStatus(self, statusMsg):
		self.statusUIHandler.updateStatus(statusMsg)



if __name__ == '__main__':
	window_manager = WindowManager()
	window_manager.drawWindow()
	window_manager.window.mainloop()
