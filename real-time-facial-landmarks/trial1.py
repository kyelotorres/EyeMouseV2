# USAGE
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
import cv2
import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
 
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Only keep the black part of the image and create a contour of black region
	retval, thresholded = cv2.threshold(gray, 30, 255, 0)
	thresholded, contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) #finds contours from image thresholded

	# detect faces in the grayscale frame
	rects = detector(gray, 0)

	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		LeftEyeCheck = 0
		RightEyeCheck = 0

		for contour in contours:
			area = cv2.contourArea(contour) #area of contour shape
			bounding_box = cv2.boundingRect(contour) #bound contour with rectangle and return x,y,w,h
			if (area / (bounding_box[2]*bounding_box[3])) < 0.4:
				continue

			m = cv2.moments(contour)
			if m['m00'] != 0:
            			center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))   #standard equation for Cx, Cy
			#if the center of position is in eye range then draw circle
			if (LeftEyeCheck == 0):
				if (shape[36][0] < center[0] < shape[39][0]) & (shape[37][1] < center[1] < shape[41][1]): #left eye
					cv2.circle(frame, center, 4, (255, 0, 0), -1)
					LeftEyeCheck = 1
			if (RightEyeCheck == 0):
				if (shape[42][0] < center[0] < shape[45][0]) &  (shape[43][1] < center[1] < shape[47][1]):
                                        cv2.circle(frame, center, 4, (255, 0, 0), -1)
                                        RightEyeCheck = 1
		# loop over the (x, y)-coordinates of the eyes for the facial landmarks
		# and draw them on the image
		for (x, y) in shape[36:48]:
			cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
		# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == 27:
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
