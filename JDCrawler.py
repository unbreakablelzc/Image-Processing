import requests
from bs4 import BeautifulSoup
import os
import urllib2,socket
 
class Picture():
 
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        self.base_url = 'http://list.jd.com/list.html?cat=737,794,798&jth=yi'
        self.base_path = os.path.dirname(__file__)
 
    def makedir(self, name):
        path = os.path.join(self.base_path, name)
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            print("File has been created.")
        else:
            print('OK!The file is existed. You do not need create a new one.')
        os.chdir(path)
 
    def request(self, url):
        r = requests.get(url, headers=self.headers)
        return r
 
    def get_img(self, page):
        r = self.request(self.base_url + str(page))
        plist = BeautifulSoup(r.text, 'lxml').find('div', id='plist')
        item = plist.find_all('li', class_='gl-item')
        print(len(item))
        self.makedir('pictures')
        num = 0
        for i in item:
            num += 1
            imglist = i.find('div', class_='p-img')
            print(num)
            img = imglist.find('img')
            print('This is %s picture' %num)
            if img.get('src'):
                url = 'https:' + img.get('src')
                fileName = img.get('src').split('/')[-1]
                #urllib2.urlretrieve(url, filename=fileName)
                img = urllib2.urlopen(url).read()
                f = open(fileName, 'wb')
                f.write(img)
 
            elif img.get('data-lazy-img'):
                url = 'https:' + img.get('data-lazy-img')
                fileName = img.get('data-lazy-img').split('/')[-1]
                #urllib2.urlretrieve(url, filename=fileName)
                img = urllib2.urlopen(url).read()
                f = open(fileName, 'wb')
                f.write(img)
 
 
 
if __name__ == '__main__':
    picture = Picture()
    for i in range(2): 
        picture.get_img(i+1)