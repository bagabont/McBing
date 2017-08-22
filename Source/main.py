#!/usr/bin/python

from appscript import *
from datetime import datetime, timedelta
from urllib2 import urlopen
from xml.dom import minidom
from os.path import expanduser
import rumps
import random
import thread
import objc


class Image:
    def __init__(self, name, url, copyright):
        self.name = name
        self.url = url
        self.copyright = copyright


def set_mac_background(filename):
    se = app('System Events')
    desktops = se.desktops.display_name.get()
    for d in desktops:
        desk = se.desktops[its.display_name == d]
        desk.picture.set(mactypes.File(filename))
    return


def get_bing_image(index):
    # Getting the XML File
    data = urlopen('http://www.bing.com/HPImageArchive.aspx?format=xml&idx=' + str(index) + '&n=1&mkt=ru-RU')
    xml = minidom.parse(data)

    # Parsing the XML File
    element = xml.getElementsByTagName('url')[0]
    copyright = xml.getElementsByTagName('copyright')[0].firstChild.nodeValue

    url = 'http://www.bing.com' + element.firstChild.nodeValue
    name = xml.getElementsByTagName('startdate')[0].firstChild.nodeValue
    imageUrl = url.replace('_1366x768', '_1920x1200')
    return Image(name, imageUrl, copyright)


def get_file_name(index):
    now = datetime.today() - timedelta(days=index)

    file_name = now.strftime('bing_%d-%m-%Y')
    return file_name


def get_wallpaper(index):
    image = get_bing_image(index)

    wallpaper_path = expanduser('~/Wallpapers/') + 'bing_' + image.name + '.jpg'
    pic = urlopen(image.url)

    with open(wallpaper_path, 'wb') as localFile:
        localFile.write(pic.read())

    set_mac_background(wallpaper_path)
    NSDictionary = objc.lookUpClass("NSDictionary")
    date = datetime.strptime(image.name, '%Y%m%d').date().strftime("%Y-%m-%d")
    rumps.notification("Bing Wallpaper", date, image.copyright, data=NSDictionary())


class BingWallpaper(rumps.App):
    @rumps.clicked("Today")
    def next_wallpaper(self):
        thread.start_new_thread(get_wallpaper, (0,))

    @rumps.clicked("Random")
    def random_wallpaper(self):
    	indices = range(0, 21)
    	random.shuffle(indices)
    	idx = indices[0]
        thread.start_new_thread(get_wallpaper, (idx,))

if __name__ == "__main__":
    BingWallpaper("BW").run()
