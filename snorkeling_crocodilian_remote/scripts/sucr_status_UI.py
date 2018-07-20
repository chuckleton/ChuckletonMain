import rospy
import sucr_gui
import Tkinter as tk
from ttk import *

from std_msgs.msg import Bool
from husky_msgs.msg import HuskyStatus

class StatusUIHandler:
	
	def __init__(self, window_manager, statusTab, driveTab, configTab):
		self.window_manager = window_manager
		self.status_tab = statusTab
		self.drive_tab = driveTab
		self.config_tab = configTab
		
		# Read-only button showing whether the e-stop is engaged (GREEN = disengaged, RED = engaged)
		self.eStopButtonVis = tk.Button(self.drive_tab,bg="red",text="E-Stop",height = 14,width=21)
		self.eStopButtonVis.grid(column = 2, row = 10)

		
		# Labels for the status values
		self.uptime_lbl = tk.Label(self.status_tab,text = "Uptime (ms): ")
		self.uptime_lbl.grid(column = 0, row = 1)
		self.uptime_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.uptime_value_lbl.grid(column = 1, row = 1)

		self.loop_freq_lbl = tk.Label(self.status_tab,text = "Loop Freq (hz): ")
		self.loop_freq_lbl.grid(column = 0, row = 2)
		self.loop_freq_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.loop_freq_value_lbl.grid(column = 1, row = 2)

		self.mcu_usr_curr_lbl = tk.Label(self.status_tab,text = "MCU & User Current (A): ")
		self.mcu_usr_curr_lbl.grid(column = 0, row = 3)
		self.mcu_usr_curr_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.mcu_usr_curr_value_lbl.grid(column = 1, row = 3)

		self.l_driver_curr_lbl = tk.Label(self.status_tab,text = "Left Driver Current (A): ")
		self.l_driver_curr_lbl.grid(column = 0, row = 4)
		self.l_driver_curr_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.l_driver_curr_value_lbl.grid(column = 1, row = 4)

		self.r_driver_curr_lbl = tk.Label(self.status_tab,text = "Right Driver Current (A): ")
		self.r_driver_curr_lbl.grid(column = 0, row = 5)
		self.r_driver_curr_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.r_driver_curr_value_lbl.grid(column = 1, row = 5)

		self.battery_voltage_lbl = tk.Label(self.status_tab,text = "Battery Voltage (V): ")
		self.battery_voltage_lbl.grid(column = 0, row = 6)
		self.battery_voltage_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.battery_voltage_value_lbl.grid(column = 1, row = 6)

		self.l_driver_voltage_lbl = tk.Label(self.status_tab,text = "Left Driver Voltage (V): ")
		self.l_driver_voltage_lbl.grid(column = 0, row = 7)
		self.l_driver_voltage_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.l_driver_voltage_value_lbl.grid(column = 1, row = 7)

		self.r_driver_voltage_lbl = tk.Label(self.status_tab,text = "Right Driver Voltage (V): ")
		self.r_driver_voltage_lbl.grid(column = 0, row = 8)
		self.r_driver_voltage_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.r_driver_voltage_value_lbl.grid(column = 1, row = 8)

		self.l_driver_temp_lbl = tk.Label(self.status_tab,text = "Left Driver Temp (C): ")
		self.l_driver_temp_lbl.grid(column = 0, row = 9)
		self.l_driver_temp_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.l_driver_temp_value_lbl.grid(column = 1, row = 9)

		self.r_driver_temp_lbl = tk.Label(self.status_tab,text = "Right Driver Temp (C): ")
		self.r_driver_temp_lbl.grid(column = 0, row = 10)
		self.r_driver_temp_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.r_driver_temp_value_lbl.grid(column = 1, row = 10)

		self.l_motor_temp_lbl = tk.Label(self.status_tab,text = "Left Motor Temp (C): ")
		self.l_motor_temp_lbl.grid(column = 0, row = 11)
		self.l_motor_temp_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.l_motor_temp_value_lbl.grid(column = 1, row = 11)

		self.r_motor_temp_lbl = tk.Label(self.status_tab,text = "Right Motor Temp (C): ")
		self.r_motor_temp_lbl.grid(column = 0, row = 12)
		self.r_motor_temp_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.r_motor_temp_value_lbl.grid(column = 1, row = 12)

		self.capacity_est_lbl = tk.Label(self.status_tab,text = "Capacity Estimate (Wh): ")
		self.capacity_est_lbl.grid(column = 0, row = 13)
		self.capacity_est_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.capacity_est_value_lbl.grid(column = 1, row = 13)

		self.charge_est_lbl = tk.Label(self.status_tab,text = "Charge Estimate (%): ")
		self.charge_est_lbl.grid(column = 0, row = 14)
		self.charge_est_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.charge_est_value_lbl.grid(column = 1, row = 14)

		self.timeout_lbl = tk.Label(self.status_tab,text = "Timeout Status: ")
		self.timeout_lbl.grid(column = 0, row = 15)
		self.timeout_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.timeout_value_lbl.grid(column = 1, row = 15)

		self.lockout_lbl = tk.Label(self.status_tab,text = "Lockout Status: ")
		self.lockout_lbl.grid(column = 0, row = 16)
		self.lockout_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.lockout_value_lbl.grid(column = 1, row = 16)

		self.e_stop_lbl = tk.Label(self.status_tab,text = "E-Stop Status: ")
		self.e_stop_lbl.grid(column = 0, row = 17)
		self.e_stop_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.e_stop_value_lbl.grid(column = 1, row = 17)

		self.ros_pause_lbl = tk.Label(self.status_tab,text = "ROS Pause Status: ")
		self.ros_pause_lbl.grid(column = 0, row = 18)
		self.ros_pause_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.ros_pause_value_lbl.grid(column = 1, row = 18)

		self.no_battery_lbl = tk.Label(self.status_tab,text = "No Battery Status: ")
		self.no_battery_lbl.grid(column = 0, row = 19)
		self.no_battery_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.no_battery_value_lbl.grid(column = 1, row = 19)

		self.current_limit_lbl = tk.Label(self.status_tab,text = "Current Limit Status: ")
		self.current_limit_lbl.grid(column = 0, row = 20)
		self.current_limit_value_lbl = tk.Label(self.status_tab,text = "N/A")
		self.current_limit_value_lbl.grid(column = 1, row = 20)


	def updateEStop(self, eStop_status):
		if not eStop_status:
			self.eStopButtonVis.config(bg="green")
		else:
			self.eStopButtonVis.config(bg="red")

	def updateStatus(self, statusMessage):
		self.uptime_value_lbl.config(text = str(statusMessage.uptime))

		self.loop_freq_value_lbl.config(text = str(statusMessage.ros_control_loop_freq))

		self.mcu_usr_curr_value_lbl.config(text = str(statusMessage.mcu_and_user_port_current))
		self.l_driver_curr_value_lbl.config(text = str(statusMessage.left_driver_current))
		self.r_driver_curr_value_lbl.config(text = str(statusMessage.right_driver_current))

		self.battery_voltage_value_lbl.config(text = str(statusMessage.battery_voltage))
		self.l_driver_voltage_value_lbl.config(text = str(statusMessage.left_driver_voltage))
		self.r_driver_voltage_value_lbl.config(text = str(statusMessage.right_driver_voltage))

		self.l_driver_temp_value_lbl.config(text = str(statusMessage.left_driver_temp))
		self.r_driver_temp_value_lbl.config(text = str(statusMessage.right_driver_temp))
		self.l_motor_temp_value_lbl.config(text = str(statusMessage.left_motor_temp))
		self.r_motor_temp_value_lbl.config(text = str(statusMessage.right_motor_temp))

		self.capacity_est_value_lbl.config(text = str(statusMessage.capacity_estimate))
		self.charge_est_value_lbl.config(text = str(statusMessage.charge_estimate))

		self.timeout_value_lbl.config(text = str(statusMessage.timeout))
		self.lockout_value_lbl.config(text = str(statusMessage.lockout))
		self.e_stop_value_lbl.config(text = str(statusMessage.e_stop))
		self.ros_pause_value_lbl.config(text = str(statusMessage.ros_pause))
		self.no_battery_value_lbl.config(text = str(statusMessage.no_battery))
		self.current_limit_value_lbl.config(text = str(statusMessage.current_limit))
