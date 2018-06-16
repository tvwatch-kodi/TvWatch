#-*- coding: utf-8 -*-
#Primatech.
from resources.lib.db import cDb
from resources.lib.util import VSlog
from resources.lib.config import cConfig
from resources.lib.ftpmanager import cFtpManager

import re
import urllib
import urllib2
import requests
import datetime
import time
try:    import json
except: import simplejson as json

SITE_IDENTIFIER = 'cTvHandler'
SITE_NAME = 'TVHANDLER'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
headers = { 'User-Agent' : UA }

class cTvHandler:

    def __init__(self, MODE):
        self.key = "QVRoTFgyMVJOUS9DQlFZMDZnSmE5dz09"

        self.tokens = []
        self.ids = []
        self.url = ''
        self.mode = MODE
        if self.mode == 1:
            self.url = 'http://swiftstreamz.com/SwiftLive/'
        elif self.mode == 2:
            self.url = 'http://swiftstream.aprolibro.com/apps/'

        if self.isResetCheck():
            cDb().del_valide()
            cFtpManager().sendDb()


    def generateToken(self):
        URL = 'http://swiftstream.aprolibro.com/apps/get_application.php?key=' + self.key
        req = urllib2.Request(URL, None, headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
        response.close()

        try:
            self.tokens.append(result['DATA'][0]['HelloLogin'])
            self.tokens.append(result['DATA'][0]['LiveTvLogin'])
            self.tokens.append(result['DATA'][0]['loginUrl'])
            self.tokens.append(result['DATA'][0]['loginUrlNew'])
            self.tokens.append(result['DATA'][0]['nexgtvToken'])

            self.ids.append(result['DATA'][0]['PasswordHello'])
            self.ids.append(result['DATA'][0]['PasswordLiveTv'])
            self.ids.append(result['DATA'][0]['Password'])
            self.ids.append(result['DATA'][0]['PasswordNew'])
            self.ids.append(result['DATA'][0]['nexgtvPass'])
        except Exception, e:
            VSlog("ERROR " + str(e.message))

        token = ''
        for i in range(5):
            url = self.tokens[i]
            user, password = self.ids[i].split(':')
            res = requests.get(url, auth=(user, password))
            if res.status_code == 200:
                token = res.text
                break
        return token

    def getCategories(self):
        url = ''
        if self.mode == 1:
            url = self.url + 'api.php'
        elif self.mode == 2:
            url = self.url + 'beoutq.php'
        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
        response.close()
        return result['LIVETV']

    def getChannels(self, cid):
        url = ''
        if self.mode == 1:
            url = self.url + 'api.php'
        elif self.mode == 2:
            url = self.url + 'beoutq.php'
        url += '?cat_id=' + cid
        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
        response.close()
        return result['LIVETV']

    def testUrl(self, url):
        oDb = cDb()
        match = oDb.get_valideFromUrl(url)
        if match != None:
            if match[2] == '1':
                return True
            elif match[2] == '0':
                return False
        code = 0
        try:
            res = requests.get(url, timeout = 0.5)
            code = res.status_code
        except Exception, e:
            VSlog("ERROR " + str(e.message))
        if code == 200:
            oDb.insert_valide(url, '1')
            return True
        else:
            oDb.insert_valide(url, '0')
        return False

    #bug python
    def __strptime(self, date, format):
        try:
            date = datetime.datetime.strptime(date, format)
        except TypeError:
            date = datetime.datetime(*(time.strptime(date, format)[0:6]))
        return date

    def isResetCheck(self):
        oConfig = cConfig()
        test_time = oConfig.getSetting('test_time')

        if not (test_time):
            oConfig.setSetting('test_time', str(datetime.datetime.now()))
            #On force la maj avec une date a la con
            test_time = '2000-09-23 10:59:50.877000'

        if (test_time):
            time_sleep = datetime.timedelta(days=1)
            time_now = datetime.datetime.now()
            time_service = self.__strptime(test_time, "%Y-%m-%d %H:%M:%S.%f")
            if (time_now - time_service > time_sleep):
                oConfig.setSetting('test_time', str(datetime.datetime.now()))
                VSlog('Reset Check URL NOW')
                return True
            else:
                VSlog('Reset Check URL le : ' + str(time_sleep + time_service))
                return False
