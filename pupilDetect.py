# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(2.0)

#create rectangular kernel of size 5x5
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	#take image and turn gray
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	#take gray and put it threw a threshold filter
	retval, thresholded = cv2.threshold(gray, 1, 255, 0)

	#take thresholded that only sees black and find contours
	im2, contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	drawing = np.copy(image)
	cv2.drawContours(drawing, contours, -1, (255, 0, 0), 2)

	for contour in contours:
		#finds the area of the contour
		area = cv2.contourArea(contour)
		#creates a bounded box around the contour return x,y,w,h
		bounding_box = cv2.boundingRect(contour)
		#create extend variable which is the area of the contour / the area of the bounded_box
		extend = area / (bounding_box[2]*bounding_box[3])

		# jump to next iteration if extend > 0.8:
		if extend > 0.5:
			continue
		#if the area of the contour is not within a certain range, skip
		if area < 100 or area > 2000:
			continue
		#calculate center of the contour and draw a dot
		m = cv2.moments(contour)
		if m['m00'] != 0:
			center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
			cv2.circle(drawing, center, 3, (0,255,0), -1)
		#fit an ellipse around the contour and draw it
		try:
			ellipse = cv2.fitEllipse(contour)
			cv2.ellipse(drawing,box=ellipse,color=(0,255,0))
		except:
			pass

	# show the altered frame
	cv2.imshow("Frame", drawing)

	#ask for users input for 30 ms and convert it to 8 bit integer
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == 27:
		break
