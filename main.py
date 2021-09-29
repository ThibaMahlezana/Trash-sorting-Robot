# importing libraries
import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter
from drive_motor import *

model_url = "detect.tflite"
labels_url = "labelmap.txt"

# loading the model
interpreter = Interpreter(model_url)

# loading the labels
with open(labels_url, 'r') as f:
    labels = [line.strip() for line in f.readlines()]
    
# take care of empty labels (first line)
if labels[0] == '???':
    del(labels[0])

# allocating model tensors
interpreter.allocate_tensors()

# getting model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

video = cv2.VideoCapture(0)
imW = video.get(cv2.CAP_PROP_FRAME_WIDTH)
imH = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

def draw_lines():
    cv2.putText(frame, '120', (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.line(frame, (0, 120), (640, 120), (0, 0, 255), 1)
    cv2.putText(frame, '240', (50, 230), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.line(frame, (0, 240), (640, 240), (0, 0, 255), 1)
    cv2.putText(frame, '360', (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.line(frame, (0, 360), (640, 360), (0, 0, 255), 1)
    
 
print(imW)
print(imH)

num_paper = 0
num_metal = 0
num_plastic = 0

while True:
    # grab frame from video stream
    ret, frame = video.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)

    # prfroming detection
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # retrieve detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects

    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > 0.6) and (scores[i] <= 1.0)):
            # Get bounding box coordinates and draw box
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
            
            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 4)
            # Draw label
            object_name = labels[int(classes[i])]
            label = '%s: %d%%' % (object_name, int(scores[i]*100))
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) 
            label_ymin = max(ymin, labelSize[1] + 10)
            cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            
            # Draw circle
            x_center = (xmax + xmin) / 2
            y_center = (ymax + ymin) / 2
             
            #cv2.putText(frame, 'center: (x = %d%, y = %d%)' % (int(x_center), int(y_center)), (int(x_center + 20), int(y_center)), cv2.FONT_HERSHEY_SIMPLEX, 
            #       0.6, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.circle(frame, (int(x_center), int(y_center)), 10, (0, 0, 255), 1)
            
            # calculate detections for memory
            if object_name == 'paper':
                num_paper = num_paper + 1
                
            if object_name == 'metal':
                num_metal = num_metal + 1
                
            if object_name == 'plastic':
                num_plastic = num_plastic + 1
    
    # collect detected trash object
    if num_paper > 35:
        num_paper = 0
        print('collecting paper ...')
        collect_paper(x_center, y_center)
        
    if num_metal > 35:
        num_metal = 0
        print('collecting metal ...')
        collect_metal(x_center, y_center)
        
    if num_plastic > 35:
        num_plastic = 0
        print('collecting plastic ...')
        collect_plastic(x_center, y_center)

    # draw horizontal lines
    draw_lines()

    # show video stream
    cv2.imshow('TRASH SORTING ROBOT', frame)

    # key to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
video.release()
cv2.destroyAllWindows()
    
print("[INFO] everything is working fine")
