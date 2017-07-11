#Rename the images

import cv2
import os
import sys
from PIL import Image, ExifTags

def number(base_path, base_index, label):
	images = [f for f in os.listdir(base_path) if not f.startswith('.')]
	index = base_index
	for f in images:

		fname = os.path.join(base_path, f)
		sname = os.path.join(base_path, '{}{:08d}.jpg'.format(label, index))
		
		os.rename(fname, sname)
		index += 1
	print 'Done!'
	
if __name__ == '__main__':
	base_path = sys.argv[1]
	base_index = int(sys.argv[2])
	label = sys.argv[3]
	number(base_path, base_index, label)