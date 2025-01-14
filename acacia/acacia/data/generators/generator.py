import os, urllib2, cgi
import re
import dateutil
import acacia.data.util as util
from django.utils import timezone
from django.core.files.base import File
import pandas as pd

import logging
logger = logging.getLogger(__name__)

def spliturl(url):
    pattern = r'^(?P<scheme>ftp|https?)://(?:(?P<user>\w+)?(?::(?P<passwd>\S+))?@)?(?P<url>.+)'
    try:
        m = re.match(pattern, url)
        return m.groups()
    except:
        return ()

class Generator(object):

    def __init__(self, *args, **kwargs):
        #self.engine = 'c'
        self.engine = 'python'
    
    def read_csv(self, *args, **kwargs):
        kwargs['engine'] = self.engine
        ret = pd.read_csv(*args,**kwargs)
        return ret
    
    def get_header(self,fil):
        return {}

    def get_data(self,fil,**kwargs):
        return []

    def get_handle(self,fil,mode='r'):
        if isinstance(fil, File):
            if fil.closed:
                fil.open(mode)
            return fil
        if hasattr(fil,'readline'):
            return fil
        return open(fil, mode)
    
    def download(self, **kwargs):
        filename = kwargs.get('filename', None)
        content = ''
        start = kwargs.get('start', None)
        callback = kwargs.get('callback', None)
        
        result = {}
        if not 'url' in kwargs:
            logger.error('url for download is undefined')
        else:
            url = kwargs['url']
            scheme, username, passwd, path = spliturl(url)
            username = kwargs.get('username',None) or username
            passwd = kwargs.get('password',None) or passwd
            ftp = scheme == 'ftp'
            if ftp:
                if username != '':
                    if passwd != '':
                        url = 'ftp://%s:%s@%s' % (username, passwd, path)
                    else:
                        url = 'ftp://%s@%s' % (username, path)
            else:
                passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
                passman.add_password(None, url, username, passwd)
                authhandler = urllib2.HTTPBasicAuthHandler(passman)
                opener = urllib2.build_opener(authhandler)
                urllib2.install_opener(opener)

            try:
                response = urllib2.urlopen(url)
            except urllib2.URLError as e:
                logger.exception('ERROR opening {url}: {reason}'.format(url=url,reason=e.reason))
                return result
            if response is None:
                return result
            if ftp:
                # check for directory listing
                content = response.read()
                if util.is_dirlist(content):
                    # download all files in directory listing
                    dirlist = util.get_dirlist(content)
                    tz = timezone.get_current_timezone()
                    for f in dirlist:
                        if start is not None:
                            date = dateutil.parser.parse(f['date'])
                            date = timezone.make_aware(date,tz)
                            if date < start:
                                continue
                        filename = f['file']
                        urlfile = url + '/' + filename
                        try:
                            response = urllib2.urlopen(urlfile)
                            result[filename] = response.read()
                        except urllib2.URLError as e:
                            logger.exception('ERROR opening {url}: {reason}'.format(url=urlfile,reason=e.reason))
                else:
                    filename = filename or os.path.basename(url)
                    result[filename] = content
            else:
                _,params = cgi.parse_header(response.headers.get('Content-Disposition',''))
                filename = filename or params.get('filename','file.txt')
                result[filename] = response.read()

            if callback is not None:
                callback(result)
                
        return result

    def get_parameters(self,fil):
        ''' return dict of all parameters in the datafile '''
        return {}
