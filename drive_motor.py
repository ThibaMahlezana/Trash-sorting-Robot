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

def collect_object_steps(pos_y):
    # collect the object
    seek(pos_y)
    drop(160)
    grab(90)
    pick(160)
    deseek(pos_y)

def drop_object_steps():
    # drop the object
    drop(150)
    release(90)
    pick(150)

def getPosX(x_center):
    
    if x_center < 160:
        pos_x = 90
    
    elif x_center >= 160 and x_center < 320:
        pos_x = 67
    
    elif x_center >= 320 and x_center < 480:
        pos_x = 45
        
    elif x_center >= 480 and x_center < 640:
        pos_x = 22
    
    print(pos_x)
    print(x_center)
    
    return pos_x

def getPosY(y_center):
    
    if y_center < 120:
        pos_y = 22
    
    elif y_center >= 120 and y_center < 240:
        pos_y = 45
    
    elif y_center >= 240 and y_center < 360:
        pos_y = 67
        
    elif y_center >= 360 and y_center < 480:
        pos_y = 90
        
    return pos_y

def collect_paper(x_center, y_center):
    pos_x = getPosX(x_center)
    pos_y = getPosY(y_center)
    
    # approach an object
    move_left(pos_x)
    
    # collect the object
    collect_object_steps(pos_y)
    move_right(pos_x)
    
    #drop the object
    move_left(90)
    drop_object_steps()
    move_right(90)

def collect_metal(x_center, y_center):
    pos_x = getPosX(x_center)
    pos_y = getPosY(y_center)
    
    # approach an object
    move_left(pos_x)
    
    # collect the object
    collect_object_steps(pos_y)
    move_right(pos_x)
    
    #drop the object
    move_left(135)
    drop_object_steps()
    move_right(135)


def collect_plastic(x_center, y_center):
    pos_x = getPosX(x_center)
    pos_y = getPosY(y_center)
    
    # approach an object
    move_left(pos_x)
    
    # collect the object
    collect_object_steps(pos_y)
    move_right(pos_x)
    
    #drop the object
    move_left(180)
    drop_object_steps()
    move_right(180)


