#Filter images which is > 256*256

import cv2
import os
import sys
from PIL import Image, ExifTags
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def filter(base_path, target_path):
	images = [f for f in os.listdir(base_path) if not f.startswith('.')]	
	total = 0
	filtered = 0
	for f in images:
		
		skip = False
		fname = os.path.join(base_path, f)
		sname = os.path.join(target_path, f)
		
		img = Image.open(fname).convert('RGB')
		width, height = img.size
		if width > 255 and height > 255:
				img2 = img.copy()
				img2.save(sname)
				filtered += 1
		total += 1
		print 'Process {0}({1}) images'.format(total, filtered)
if __name__ == '__main__':
	images_folder = sys.argv[1]
	target_folder = sys.argv[2]
	filter(images_folder, target_folder)