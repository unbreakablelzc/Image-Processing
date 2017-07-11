# Take screenshots of videos

import os
import sys
import numpy as np
import cv2  

def capture_video(base_path, target_path, timeF):
	vc = cv2.VideoCapture(base_path)
	print vc.grab()
	c = 1
	total = 0
  
	if vc.isOpened():  
		rval , frame = vc.read()  
	else:  
		rval = False  
  
	while rval:  
		rval, frame = vc.read()
		if(c%timeF == 0):
			cv2.imwrite(target_path  + '/' + str(c) + '.jpg',frame)
			total += 1
			print str(total) + " screenshot"
		c = c + 1  
		cv2.waitKey(1)  
	vc.release()  
	

if __name__ == "__main__":
	base_path = sys.argv[1]
	target_path = sys.argv[2]
	timeF = int(sys.argv[3])
	capture_video(base_path, target_path, timeF)