import cv2
import numpy as np
from networktables import NetworkTables

def show_webcam():
	ip = "roboRIO-670-frc.local"
        NetworkTables.initialize(server=ip)
        table = NetworkTables.getTable("knuckles_vision")
	lower = np.array([0,0,234])
	upper = np.array([180,252,255])
	cam = cv2.VideoCapture(0)
	while True:
		ret_val, img = cam.read()
	        maxX = 0
        	maxY = 0
	        maxW = 0    
        	maxH = 0
	        ret_val, img = cam.read()
        	threshed_img = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), lower, upper)          
        	contours, hierarchy = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
       		for c in contours:
                	x, y, w, h = cv2.boundingRect(c)
                	if w*h > maxW*maxH:
                        	maxW = w
                        	maxH = h
                        	maxX = x
                        	maxY = y
		degreesPerPixel=0.04765625
		targetX=640
		rectMidX=maxX+(maxW/2)
		rads = degreesPerPixel*(targetX - rectMidX)
		table.putNumber('angle', rads)
		table.putNumber('x', maxX)
		table.putNumber('y', maxY)
		table.putNumber('w', maxW)
		table.putNumber('h', maxH)
		cv2.rectangle(img, (maxX, maxY), (maxX+maxW, maxY+maxH), (0, 225, 0), 2)	
		cv2.imshow('my webcam', img)
		if cv2.waitKey(1) == 27:
			break
	cv2.destroyAllWindows()

def main():
	show_webcam()

if __name__ == '__main__':
	main()
