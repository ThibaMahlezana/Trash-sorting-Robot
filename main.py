# importing libraries
import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter

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

  
	# show video stream
	cv2.imshow('TRASH SORTING ROBOT', frame)
	
	# key to quit
	if cv2.waitKey(1) == ord('q'):
		break

# Clean up
video.release()
cv2.destroyAllWindows()
    
print("[INFO] everything is working fine")
