'''
Created on Dec 9, 2015

@author: theo
'''
from PIL import Image
from PIL.ExifTags import TAGS
import urllib
from cStringIO import StringIO

class Exif:

    @classmethod
    def from_file(cls,f):
        exif = Image.open(f)._getexif()
        return {TAGS.get(tag,tag): value for tag, value in exif.items()}

    @classmethod
    def from_url(cls, url):
        return Exif.from_file(StringIO(urllib.urlopen(url).read()))

if __name__ == '__main__':
    imagefile = r'/home/theo/git/acaciadata/iom/media/eecc4c3f-6eeb-45a1-a7f5-640d3515e512.jpg'
    print Exif.from_file(imagefile)
    url = r'https://akvoflow-90.s3.amazonaws.com/images/eecc4c3f-6eeb-45a1-a7f5-640d3515e512.jpg'
    print Exif.from_url(url)

    