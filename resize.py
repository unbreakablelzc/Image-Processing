#Resize the images to 256*256

import cv2
import os
import sys
from PIL import Image, ExifTags
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def generate_fg2(fname, outshape):
    fg = cv2.imread(fname, cv2.IMREAD_COLOR)
    fg = cv2.resize(fg, outshape)
    return fg
	
def resize(base_path):
	images = [f for f in os.listdir(base_path) if not f.startswith('.')]
	for f in images:
		fname = os.path.join(base_path, f)
		fg = cv2.imread(fname, cv2.IMREAD_COLOR)
		fg = generate_fg2(fname, (256, 256))
		cv2.imwrite(fname, fg)
	print 'Done!'
        
	
if __name__ == '__main__':
	base_path = sys.argv[1]
	resize(base_path)