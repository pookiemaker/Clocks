# version 1.0 nothing fancy

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock as KivyClock
import time
import serial
#import csac I would love for this to work.


gui = '''
<ContainerBox>:

	GridLayout:
		id: main_box
		rows: 6
		# Row 0 
		GridLayout:
			id: light_box_1
			cols: 4
			Button:
				id: status_0
				text: 'CSAC Status'
				background_color:  (2,0,0,1)
				on_press: root.push_button()
			Button:
				id: status_1
				text: 'CSAC Status'
				background_color:  (2,0,0,1)
				on_press: root.push_button()
			Button:
				id: status_2
				text: 'CSAC Status'
				background_color:  (2,0,0,1)
				on_press: root.push_button()
			Button:
				id: status_3
				text: 'CSAC Status'
				background_color:  (2,0,0,1)
				on_press: root.push_button()
		#Row 1
		GridLayout:
			id: light_box_1
			cols: 4
			Button:
				id: status_4
				text: 'CSAC mode'
				background_color:  (2,0,0,1)
				on_press: root.push_button_readD()
			Button:
				id: status_5
				text: 'CSAC Discp'
				background_color:  (2,0,0,1)
				on_press: root.push_button()
			Button:
				id: status_6
				text: 'Freq Lock WRITE CAUTION'
				background_color:  (2,0,0,1)
				on_press: root.push_button_writeFL()
			Button:
				id: status_7
				text: 'Change Mode'
				background_color:  (2,0,0,1)
				on_press: root.push_button_writeModeD()
		# row 2
		Label:
			id: titlebar
			text: "Big Friendly Button"
		#Row 3
		Button:
			id: status
			text: 'CSAC Disc Lock'
			background_color:  (2,0,0,1)
			on_press: root.push_button()
		#row 4
		Button:
			id: big_button
			text: 'write date to console'
			background_color:  (2,0,0,1)
			on_press: root.push_button()
		# Row 5
		Label:
			id:raw_data
			halign: 'right'
			text: "asdfasf"
		
'''

Builder.load_string(gui)


class ContainerBox(BoxLayout):
	__version__ = "0.0.1"
	__author__ = "pookie"

	# this is the initialiation 
	def __init__(self,**kwargs):
		super(ContainerBox,self).__init__(**kwargs)
		KivyClock.schedule_interval(self.update, 1)


	def push_button(self):
		print(self.ids.keys())
		self.ids.big_button.text = "Dont Push"
		self.ids.big_button.background_color = (1,2,1,1)

	def push_button_readD(self):
		ser.write(b'!M?\r\n')
		data = ser.readline()
		self.ids.status_4.text = 'Disc Value\n   ' + data

	def push_button_writeFL(self):
		ser.write(b'!FL\r\n')
		data = ser.readline()
		print(data)
		data = ser.readline()
		print(data)
		self.ids.status_6.text = 'Freq Steering\n Written\n   '

	def push_button_writeModeD(self):
		ser.write(b'!M?\r\n')
		data = ser.readline()
		print('::'+data+'::')
		if data == '0x0000\r\n':
			ser.write(b'!MD\r\n')
			print('Change to Disc Mode')
			print(ser.readline())
		else:
			ser.write(b'!Md\r\n')
			print('Change to Free Run Mode')
			print(ser.readline())
			print(ser.readline())
			print('------------------')

		print(' Mode supposed to be changing')
		print(data)
		self.ids.status_7.text = 'Changing'



	def update(self,dt):
		# serial read write
		ser.write(b'^\r\n')
		data = ser.readline()		
		print(data)
		self.ids.raw_data.text = data
		data_v = data.split(',')
	
		# CSAC Status [0]
		if data_v[0] == '0':
			self.ids.status_0.background_color = (1,2,1,1)
			self.ids.status_0.text = 'Unit Status \n LOCKED'
		elif data_v[0] == '1':
			self.ids.status_0.background_color = (2,2,1,1)
			self.ids.status_0.text = 'Unit Status \n uWave Freq Steer'
		elif data_v[0] == '2':
			self.ids.status_0.background_color = (2,2,1,1)
			self.ids.status_0.text = 'Unit Status \n uWave Freq Stab'
		elif data_v[0] == '3':
			self.ids.status_0.background_color = (2,2,1,1)
			self.ids.status_0.text = 'Unit Status \n uWave Freq Acq'
		elif data_v[0] == '4':
			self.ids.status_0.background_color = (2,2,1,1)
			self.ids.status_0.text = 'Unit Status \n Laser Power Acq'
		elif data_v[0] == '5':
			self.ids.status_0.background_color = (2,2,1,1)
			self.ids.status_0.text = 'Unit Status \n Laser Current Acq'
		elif data_v[0] == '6':
			self.ids.status_0.background_color = (2,2,1,1)
			self.ids.status_0.text = 'Unit Status \n uWave Power Acq'
		elif data_v[0] == '7':
			self.ids.status_0.background_color = (2,2,1,1)
			self.ids.status_0.text = 'Unit Status \n Heater Equilb'
		elif data_v[0] == '8':
			self.ids.status_0.background_color = (2,2,1,1)
			self.ids.status_0.text = 'Unit Status \n Initial Warmup'
		elif data_v[0] == '9':
			self.ids.status_0.background_color = (2,2,1,1)
			self.ids.status_0.text = 'Unit Status \n Asleep (ULP)'
		else:
			self.ids.status_0.background_color = (2,1,1,1)
			self.ids.status_0.text = 'Unit Status \n BROKEN'
			


		# Phase [10]
		self.ids.status_1.text = 'Steering: ' + data_v[10]
		self.ids.status_1.background_color = (2,2,1,1)
		#print('Steering' + data_v[10])  

		# Phase [12]
		self.ids.status_2.text = 'Phase offset: ' + data_v[12]
		self.ids.status_2.background_color = (2,2,1,1)
		#print('Phase' + data_v[12])  
		

		# Disc Status [13]
		if data_v[13] == '1':
			self.ids.status_3.background_color = (1,2,1,1)
			self.ids.status_3.text = 'Discipline \nLocked'
		elif data_v[13] == '0':
			self.ids.status_3.background_color = (2,2,1,1)
			self.ids.status_3.text = 'Acquiring'
		else:
			self.ids.status_3.background_color = (2,1,1,1)
			self.ids.status_3.text = 'bad'
		#print('test ' + data_v[13] + ' ****')  

		# Mode [3]
		ser.write(b'!M?\r\n')
		data = ser.readline()
		self.ids.status_4.text = 'Mode: ' + data
		self.ids.status_4.background_color = (2,2,1,1)
		#print('Steering' + data_v[10])  

		# Mode [3]
		ser.write(b'!D?\r\n')
		data = ser.readline()
		self.ids.status_5.text = 'Disc Value\n   ' + data
		self.ids.status_5.background_color = (2,2,1,1)
		#print('Steering' + data_v[10])  

		# Freq Latch
		self.ids.status_6.text = 'Freq Latch \n CAUTION'
		self.ids.status_6.background_color = (2,1,1,1)

		# Change Mode
		self.ids.status_7.text = 'Change Mode'
		self.ids.status_7.background_color = (2,2,1,1)



class Test(App):
	def build(self):
		return ContainerBox()



if __name__ == "__main__":
	# setup the serial port
	ser = serial.Serial()
	ser.baudrate = 56700
	ser.port = '/dev/ttyUSB0'
	ser.timeout = 0.1
	# open the serial port
	ser.open()
	ser.isOpen()


	Test().run()



