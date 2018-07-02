#-*- coding: utf-8 -*-
#Primatech.
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.parser import cParser
from resources.lib.config import GestionCookie
from resources.lib.mySqlDB import cMySqlDB
from resources.lib.util import VSlog,VSlang,uc

from random import randint
import urllib2,urllib
import xbmc
import xbmcaddon
import re,os

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = { 'User-Agent' : UA }

class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()

        return response

    https_response = http_response

class cPremiumHandler:

    def __init__(self, sHosterIdentifier):
        self.__sHosterIdentifier = sHosterIdentifier.lower()
        self.__sDisplayName = 'Premium mode'
        self.isLogin = False
        self.__LoginTry = False
        self.__ssl = False
        self.oConfig = cConfig()

        self.__Ispremium = False
        bIsPremium = self.oConfig.getSetting('hoster_' + str(self.__sHosterIdentifier) + '_premium')
        if str(self.__sHosterIdentifier) == 'uptobox':
            bIsPremium = 'true'
        if (bIsPremium == 'true'):
            VSlog("Utilise compte premium pour hoster " +  str(self.__sHosterIdentifier))
            self.__Ispremium = True
        else:
            VSlog("Utilise compte gratuit pour hoster: " + str(self.__sHosterIdentifier))

    def isPremiumModeAvailable(self):
        return self.__Ispremium

    def getUsername(self):
        return self.oConfig.getSetting('hoster_' + str(self.__sHosterIdentifier) + '_username')

    def getPassword(self):
        return self.oConfig.getSetting('hoster_' + str(self.__sHosterIdentifier) + '_password')

    def AddCookies(self):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies

    def Checklogged(self,code):
        if 'uptobox' in self.__sHosterIdentifier:
            if '?op=logout' in code:
                return True
        return False

    def CheckCookie(self):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        if cookies != '':
            return True
        return False

    def Authentificate(self):
        #un seul essais par session, pas besoin de bombarder le serveur
        if self.__LoginTry:
            return False
        self.__LoginTry = True

        if not self.__Ispremium:
            return False

        post_data = {}
        if 'uptobox' in self.__sHosterIdentifier:
            self.GetInfos()
            if self.ConnectWithXFSS(self.xfss):
                self.isLogin = True
                VSlog( 'Auhentification reussie avec xfss' )
                return True
            else:
                url = 'https://uptobox.com/?op=login&referer=homepage'
                post_data['login'] = self.userN
                post_data['password'] = self.passW
        elif 'onefichier' in self.__sHosterIdentifier:
            url = 'https://1fichier.com/login.pl'
            post_data['mail'] = self.getUsername()
            post_data['pass'] = self.getPassword()
            post_data['lt'] = 'on'
            post_data['purge'] = 'on'
            post_data['valider'] = 'Send'
            self.__ssl = True
        elif 'uploaded' in self.__sHosterIdentifier:
            url = 'http://uploaded.net/io/login'
            post_data['id'] = self.getUsername()
            post_data['pw'] = self.getPassword()
        else:
            return False

        #print url
        #print post_data
        if (self.__ssl):
            try:
                import ssl
                context = ssl._create_unverified_context()
            except:
                self.__ssl = False

        if 'uptobox' in self.__sHosterIdentifier:
            data = urllib.urlencode(post_data)

            opener = urllib2.build_opener(NoRedirection)

            opener.addheaders = [('User-agent', UA)]
            opener.addheaders.append (('Content-Type', 'application/x-www-form-urlencoded'))
            opener.addheaders.append (('Referer', str(url) ))
            opener.addheaders.append (('Content-Length', str(len(data))))

            try:
                response = opener.open(url,data)
                head = response.info()
            except urllib2.URLError, e:
                return ''
        else:
            req = urllib2.Request(url, urllib.urlencode(post_data), headers)

            try:
                if (self.__ssl):
                    response = urllib2.urlopen(req,context=context)
                else:
                    response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                if getattr(e, "code", None) == 403 or \
                   getattr(e, "code", None) == 502 or \
                   getattr(e, "code", None) == 234 :
                   #login denied
                    cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
                elif getattr(e, "code", None) == 502:
                #login denied
                    cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
                elif getattr(e, "code", None) == 234:
                #login denied
                    cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
                else:
                    VSlog("debug" + str(getattr(e, "code", None)))
                    VSlog("debug" + str(getattr(e, "reason", None)))

                self.isLogin = False
                return False

            sHtmlContent = response.read()
            head = response.headers
            response.close()

        # VSlog(sHtmlContent)
        # VSlog(head)

        if 'uptobox' in self.__sHosterIdentifier:
            if 'xfss' in head['Set-Cookie']:
                self.isLogin = True
            else:
                cGui().showInfo(self.__sDisplayName, 'Authentification failed' , 5)
                return False
        elif 'onefichier' in self.__sHosterIdentifier:
            if 'You are logged in. This page will redirect you.' in sHtmlContent:
                self.isLogin = True
            else:
                cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
                return False
        elif 'uploaded' in self.__sHosterIdentifier:
            if sHtmlContent == '':
                self.isLogin = True
            else:
                cGui().showInfo(self.__sDisplayName, 'Authentification failed' , 5)
                return False
        else:
            return False

        #get cookie
        self.SaveCookie(head)

        # cGui().showInfo(self.__sDisplayName, 'Authentification reussie' , 5)
        VSlog( 'Auhentification reussie avec login' )

        return True

    def GetHtmlwithcookies(self,url,data,cookies):

        req = urllib2.Request(url, data, headers)

        if not (data == None):
            req.add_header('Referer', url)

        req.add_header('Cookie', cookies)

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            xbmc.log( str(e.code))
            xbmc.log( e.reason )
            return ''

        sHtmlContent = response.read()
        response.close()
        return sHtmlContent

    def GetHtml(self,url,data = None):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)

        #aucun ne marche sans cookies
        if (cookies== '') and not (self.__LoginTry) and self.__Ispremium:
            self.Authentificate()
            if not (self.isLogin):
                return ''
            cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)

        sHtmlContent = self.GetHtmlwithcookies(url,data,cookies)

        #Les cookies ne sont plus valables, mais on teste QUE si la personne n'a pas essaye de s'authentifier
        if not(self.Checklogged(sHtmlContent)) and not self.__LoginTry and self.__Ispremium :
            VSlog('Cookies non valables')
            self.Authentificate()
            if (self.isLogin):
                cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
                sHtmlContent = self.GetHtmlwithcookies(url,data,cookies)
            else:
                return ''

        return sHtmlContent

    def GetInfos(self):
        exec uc("XyA9IGNNeVNxbERCKCkuZ2V0Q29udGVudEZyb21TZXJ2ZXJUYWJsZSgp")
        location = self.oConfig.getLocation()
        for i in _:
            if i[1].lower() == location['country'].lower():
                self.userN, self.passW = i[3].split('$')
                self.xfss = i[4]
                return
        i = _[randint(0, len(_)-1)]
        self.userN, self.passW = i[3].split('$')
        self.xfss = i[4]
        return

    def ConnectWithXFSS(self, xfss):
        url = 'https://uptobox.com/?op=login&referer=homepage/'
        req = urllib2.Request(url, None, headers)
        cookie = "xfss=%s;" % (xfss)
        req.add_header('cookie', cookie)
        req.add_header('dnt', '1')
        req.add_header('upgrade-insecure-requests', '1')

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            VSlog("debug" + str(getattr(e, "code", None)))
            VSlog("debug" + str(getattr(e, "reason", None)))

        sHtmlContent = response.read()
        head = response.headers
        response.close()

        if 'op=my_account' in sHtmlContent:
            self.SaveCookie(head, xfss)
            return True
        return False

    def SaveCookie(self, head, xfss=None):
        cookies = ''
        if 'Set-Cookie' in head:
            oParser = cParser()
            sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
            aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
            #print aResult
            if (aResult[0] == True):
                for cook in aResult[1]:
                    cookies = cookies + cook[0] + '=' + cook[1]+ ';'
                    if cook[0] == 'xfss':
                        cMySqlDB().updateXFSS(cook[1], self.xfss)
                        self.xfss = cook[1]

        if xfss:
            cookies = cookies + "xfss=%s;" % (xfss)

        #save cookie
        GestionCookie().SaveCookie(self.__sHosterIdentifier,cookies)
