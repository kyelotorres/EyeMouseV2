# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import moveMouse
from moveMouse import *
def drawBound(image, boundarys):
   for boundary in boundarys:
      if boundary:
         cv2.circle(drawing, boundary, 3, (0,255,255), -1)

#initialize global variables a,w,d,x which is the boundary variables
a=(0,0)
w=(0,0)
d=(0,0)
s=(0,0)
t = False

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

# allow the camera to warmup
time.sleep(2.0)

#create rectangular kernel of size 5x5
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	#take image and turn gray
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	#take gray and put it threw a threshold filter
	retval, thresholded = cv2.threshold(gray, 5, 255, 0)

	#take thresholded that only sees black and find contours
	im2, contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	drawing = np.copy(image)
	cv2.drawContours(drawing, contours, -1, (255, 0, 0), 2)

	for contour in contours:
		#finds the area of the contour
		area = cv2.contourArea(contour)

		if area < 300 or area > 2000:
			continue

		#creates a bounded box around the contour return x,y,w,h
		(x,y),radius = cv2.minEnclosingCircle(contour)
		center = ( int(x),int(y) )
		radius = int(radius)

		extend = area / (3.14152*radius**2)
		if extend < 0.4:
			continue
#		print("area:"+str(area)+"    extend:"+str(extend))
		cv2.circle(drawing,center,radius,(0,0,255),2)
		print("a:"+str(a)+ " w:"+str(w)+" d:"+str(d)+" s:"+str(s) + " " +str(t))
		#calculate center of the contour and draw a dot
		m = cv2.moments(contour)
		if m['m00'] != 0:

			x = int(m['m10'] / m['m00'])
			y = int(m['m01'] / m['m00'])
			center = (x,y)
			cv2.circle(drawing, center, 3, (0,255,255), -1)

		input =  cv2.waitKey(1) & 0xFF
		#if a,d,w,s pressed, place bound there
		if input == ord('a'):
			a = (x,y)
		elif input == ord('w'):
			w = (x,y)
		elif input == ord('d'):
			d = (x,y)
		elif input == ord('s'):
			s = (x,y)
		elif input == ord('x'):
			t = True
		else:
			pass
		if t:
			moveMouse(x,y,d,a,w,s)
	drawBound(drawing,[d,a,w,s])
	#show the altered frame
	cv2.imshow("Frame", cv2.flip(drawing,1) )

	#ask for users input for 1 ms and convert it to 8 bit integer
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == 27:
		break
