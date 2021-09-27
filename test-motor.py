from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
import time

def move_forward(angle, channel):	
	for i in range(0, angle, 5):
		kit.servo[channel].angle = i
		time.sleep(0.04)

def move_backwards(angle, channel):
	for i in reversed(range(0, angle, 5)):
		kit.servo[channel].angle = i
		time.sleep(0.04)

def move_left(angle):
	move_forward(angle, 0)

def move_right(angle):
	move_backwards(angle, 0)
		
def drop(angle):
	move_forward(angle, 1)

def pick(angle):
	move_backwards(angle, 1)

def seek(angle):
	move_forward(angle, 2)
	
def deseek(angle):
	move_backwards(angle, 2)

def grab(angle):
	move_forward(angle, 4)
	
def release(angle):
	move_backwards(angle, 4)

def collect_object_steps():
	# collect the object
	seek(90)
	drop(150)
	grab(90)
	pick(150)
	deseek(90)

def drop_object_steps():
	# drop the object
	drop(150)
	release(90)
	pick(150)
	

def collect_paper():
	collect_object_steps()
	
	move_left(90)
	drop_object_steps()
	move_right(90)

def collect_metal():
	collect_object_steps()
	
	move_left(135)
	drop_object_steps()
	move_right(135)


def collect_plastic():
	collect_object_steps()
	
	move_left(180)
	drop_object_steps()
	move_right(180)

#collect_paper()
#collect_metal()
collect_plastic()

'''
def collect_metal():
	move_forward(135, 0)
	move_backwards(135, 0)

def collect_plastic():
	move_forward(180, 0)
	move_backwards(180, 0)
'''
