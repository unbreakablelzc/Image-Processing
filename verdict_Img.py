import MySQLdb
import hashlib
import os
import sys
import cv2
from os.path import islink, join
from time import localtime, strftime
from PIL import Image, ExifTags

HOST = "localhost"
USER = "root"
PWD = "1234"
DB = "TESTDB"
EXCLUDE_DIR = ['.git']

def connect():
	db = MySQLdb.connect(HOST,USER,PWD,DB)
	return db

def create_table():
	db = connect()
	cursor = db.cursor()
	
	sql = """CREATE TABLE IF NOT EXISTS IMAGES (
	PATH CHAR(200) NOT NULL,
	MTIME CHAR(20),
	SHA1 CHAR(100) NOT NULL
	)"""
	
	cursor.execute(sql)
	db.close()

def insert_image(img_path, mtime, sha1):
	db = connect()
	cursor = db.cursor()
	
	sql = """INSERT INTO IMAGES (
	PATH, MTIME, SHA1)
	VALUES('%s', '%s', '%s')""" % \
	(img_path, mtime, sha1)
	
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	
	db.close()

def search_image(img_path, sname):
	res = True
	img_size = os.path.getsize(img_path)
	db = connect()
	cursor = db.cursor()
	sha1 = cal_sha1(img_path, img_size)
	sha12 = cal_shal_resize(img_path, sname)
	
	sql = """SELECT * FROM IMAGES
	WHERE SHA1 = '%s' OR SHA1 = '%s'""" % \
	(sha1, sha12)
	
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:			
			path = row[0]
			mtime = row[1]
			sha1 = row[2]
			print str(img_path) + " already exists in the Database.."
			res = False # if exists, change res to False
	except:
		print "Error: unable to fetch data"	
	db.close()
	return res

def cal_sha1(img_path, img_size):
	#date = strftime('%Y/%m/%d %H:%M:%S', localtime(os.path.getmtime(filepath)))
	with open(img_path, 'rb') as openfile: 
		while True:
			data = openfile.read(img_size)
			if not data:
				break
			xhash = hashlib.sha1()
			xhash.update(data)
	return xhash.hexdigest()

def cal_shal_resize(img_path, sname):
	img = Image.open(img_path)
	width, height = img.size
	img2 = img.copy()
	if (width > 640 or height > 480) and width > height :	
		img2 = img2.resize((640, 480))
		img_size2 = 640 * 480
	elif (width > 640 or height > 480) and width < height :
		img2 = img2.resize((480, 640))
		img_size2 = 480 * 640
	else:
		img_size2 = 256 * 256
	img2.save(sname)
	sha1 = cal_sha1(sname, img_size2)
	return sha1

def verdict(dirpath, copy_path):
	ent = [e for e in os.listdir(dirpath)
			if (not e in EXCLUDE_DIR) and (not islink(join(dirpath, e)))]
	index = 0
	for e in ent:
		fullpath = os.path.join(dirpath, e)
		_fullpath = fullpath.replace('\\', '\\\\')
		#print _fullpath
		if os.path.isdir(fullpath):
			verdict(fullpath, copy_path)
		else:
			sname = os.path.join(copy_path, '{:08d}.jpg'.format(index))
			_, ext = os.path.splitext(e)
			if(ext.lower() == '.jpg'):
				img_size = os.path.getsize(fullpath)
				sha1 = cal_sha1(fullpath, img_size)
				mtime = strftime('%Y/%m/%d %H:%M:%S', localtime(os.path.getmtime(fullpath)))
				if(search_image(_fullpath, sname)):
					insert_image(_fullpath, mtime, sha1)
		index += 1
		
if __name__ == "__main__":
	dirpath = sys.argv[1]
	copy_path = sys.argv[2]
	_dirpath = dirpath.replace('\\', '\\\\')
	create_table()
	verdict(dirpath, copy_path)