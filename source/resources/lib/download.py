#-*- coding: utf-8 -*-
from resources.lib.config import cConfig
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.mySqlDB import cMySqlDB
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.player import cPlayer
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.db import cDb
from resources.lib.util import cUtil, VSlog, VSGetCachePath, uc, VS_str_conv, VSlang, ReadSingleDatabase, WriteSingleDatabase

import urllib2,urllib
import xbmcplugin, xbmc
import xbmcgui
import xbmcvfs
import re,sys
import threading
import xbmc
import os

SITE_IDENTIFIER = 'cDownload'

class cDownloadProgressBar(threading.Thread):
    def __init__(self, *args, **kwargs):

        self.__sThumbnail = ''
        self.__sMainUrl = ''
        self.__sTitle = ''
        self.__sUrl = ''
        self.__fPath = ''
        self.__bFastMode = False
        self.__oConfig = cConfig()
        self.clientID = self.__oConfig.getSetting('clientID')
        self.mySqlDB = cMySqlDB()

        if (kwargs):
            self.__sTitle = kwargs['title']
            self.__sUrl = kwargs['url']
            self.__fPath = kwargs['Dpath']
            self.__sThumbnail = kwargs['icon']
            self.__sMainUrl = kwargs['mainUrl']
            if 'FastMode' in kwargs:
                VSlog('Telechargement en mode Turbo')
                self.__bFastMode = True

        threading.Thread.__init__(self)

        self.processIsCanceled = False
        self.oUrlHandler = None
        self.file = None
        self.__oDialog = None

    def createProcessDialog(self):
        diag = xbmcgui.DialogProgressBG()
        diag.create('Download')
        return diag

    def _StartDownload(self):
        WriteSingleDatabase("download_stop", "False")
        headers = self.oUrlHandler.info()

        db = cDb()

        iTotalSize = -1
        if "content-length" in headers:
            iTotalSize = int(headers["Content-Length"])

        chunk = 1024 * 1024
        TotDown = 0

        meta = {}
        meta['sMainUrl'] = self.__sMainUrl
        meta['title'] = self.__sTitle
        meta['path'] = self.__fPath
        meta['icon'] = self.__sThumbnail
        meta['status'] = "InProgress"

        db.insert_download(meta)
        WriteSingleDatabase('download_status', 'InProgress')

        #mise a jour pour info taille
        self.__oConfig.showInfo('TvWatch', VSlang(30505))
        self.__oDialog = self.createProcessDialog()
        self.currentTime = 0
        WriteSingleDatabase(uc('bXlTZWxmUGxheQ=='), 'True')
        self.__oConfig.update()
        while not self.processIsCanceled:
            self.currentTime += 1
            exec uc("c2VsZi5teVNxbERCLnVwZGF0ZUlQKHN0cihpbnQoc2VsZi5jdXJyZW50VGltZSkpLCBzZWxmLmNsaWVudElEKQ==")

            data = self.oUrlHandler.read(chunk)
            if not data:
                print 'DL err'
                break

            self.file.write(data)
            TotDown = TotDown + data.__len__()

            self.__stateCallBackFunction(TotDown, iTotalSize)
            if ReadSingleDatabase("download_stop") == "True":
                self.processIsCanceled = True

            #petite pause, ca ralentit le download mais evite de bouffer 100/100 ressources
            if not (self.__bFastMode):
                xbmc.sleep(300)

        self.oUrlHandler.close()
        self.file.close()
        self.__oDialog.close()

        exec uc("c2VsZi5teVNxbERCLnVwZGF0ZUlQKCIwIiwgc2VsZi5jbGllbnRJRCk=")
        WriteSingleDatabase(uc('aXNQbGF5aW5n'), "0")
        WriteSingleDatabase(uc('bXlTZWxmUGxheQ=='), 'False')

        meta['status'] = "Downloaded"
        db.update_download(meta)
        WriteSingleDatabase("download_status", "NotStarted")

        #fait une pause pour fermer le Dialog
        xbmc.sleep(500)

        #if download done
        if (TotDown == iTotalSize) and (iTotalSize > 10000):
            try:
                self.__oConfig.showInfo(VSlang(30507), self.__sTitle)
                VSlog('Téléchargements Termine : %s' % self.__sTitle)
            except Exception, e:
                VSlog("_StartDownload Done error " + e.message)
        else:
            try:
                self.__oConfig.showInfo(VSlang(30506), self.__sTitle)
                VSlog('Téléchargements Arrete : %s' % self.__sTitle)
            except Exception, e:
                VSlog("_StartDownload Not Done error " + e.message)
            return

        # self.RefreshDownloadList()
        self.__oConfig.update()

    def __stateCallBackFunction(self, iDownsize, iTotalSize):
        iPercent = int(float(iDownsize * 100) / iTotalSize)
        self.__oDialog.update(iPercent, self.__sTitle, self.__formatFileSize(float(iDownsize))+'/'+self.__formatFileSize(iTotalSize))

        if (self.__oDialog.isFinished()) and not (self.__processIsCanceled):
            self.__processIsCanceled = True
            self.__oDialog.close()

    def run(self):

        try:
            #Recuperation url simple
            url = self.__sUrl.split('|')[0]
            #Recuperation des headers du lien
            headers = {}
            if len (self.__sUrl.split('|')) > 1:
                u = self.__sUrl.split('|')[1].split('&')
                for i in u:
                    headers[i.split('=')[0]] = i.replace(i.split('=')[0] + '=','')

            #Rajout du user-agent si abscent
            if not ('User-Agent' in headers):
                headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

            req = urllib2.Request(url, None, headers)

            self.oUrlHandler = urllib2.urlopen(req,timeout=30)
            #self.__instance = repr(self)
            self.file = xbmcvfs.File(self.__fPath, 'w')
        except Exception, e:
            VSlog("download run error " + e.message + " URL " + self.__sUrl)
            self.__oConfig.showInfo('TvWatch', VSlang(30508))
            return

        # if xbmc.getCondVisibility("Window.IsVisible(10151)"):
        #     self.__oConfig.showInfo('TvWatch', VSlang(30509))
        #     return

        self._StartDownload()

    def __formatFileSize(self, iBytes):
        iBytes = int(iBytes)
        if (iBytes == 0):
            return '%.*f %s' % (2, 0, 'MB')

        return '%.*f %s' % (2, iBytes/(1024*1024.0) , 'MB')

    def StopAll(self):
        self.processIsCanceled = True
        WriteSingleDatabase("download_stop", "True")
        try:
            self.__oDialog.close()
        except Exception, e:
            pass

    def RefreshDownloadList(self):
        #print xbmc.getInfoLabel('Container.FolderPath')
        if 'function=getDownload' in xbmc.getInfoLabel('Container.FolderPath'):
            self.__oConfig.update()


class cDownload:
    def __init__(self):
        self.__oConfig = cConfig()
        # self.__oDb = cDb()

    def __createDownloadFilename(self, sTitle):
        sTitle = re.sub(' +',' ',sTitle) #Vire double espace
        valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        filename = ''.join(c for c in sTitle if c in valid_chars)
        filename = filename.replace(' .','.')
        if filename.startswith(' '):
            filename = filename[1:]
        #filename = filename.replace(' ','_') #pas besoin de ca, enfin pr moi en tout cas
        return filename

    def __formatFileSize(self, iBytes):
        iBytes = int(iBytes)
        if (iBytes == 0):
            return '%.*f %s' % (2, 0, 'MB')

        return '%.*f %s' % (2, iBytes/(1024*1024.0) , 'MB')

    def isDownloading(self):
        if not xbmc.getCondVisibility("Window.IsVisible(10151)"):
            return False
        return True


    def download(self, sDBUrl, sTitle, sDownloadPath, sThumbnail, sMainUrl, FastMode = True):
        VSlog("Telechargement " + str(sDBUrl))
        # if self.isDownloading():
        #     self.__oConfig.showInfo('TvWatch', VSlang(30509))
        #     return False

        #resolve url
        oHoster = cHosterGui().checkHoster(sDBUrl)
        oHoster.setUrl(sDBUrl)
        aLink = oHoster.getMediaLink()

        if (aLink[0] == True):
            sUrl = aLink[1]
        else:
            VSlog('Lien non resolvable')
            self.__oConfig.showInfo('TvWatch', VSlang(30510))
            return False

        if (not sUrl.startswith('http')) or sUrl.split('|')[0].endswith('.m3u8') :
            return False

        try:
            if '.' in sUrl:
                a = sUrl.rfind('.')
                sDownloadPath += sUrl[a:]

            #background download task
            if FastMode:
                cDownloadProgressBar(title = sTitle , url = sUrl , Dpath = sDownloadPath , icon = sThumbnail, mainUrl = sMainUrl, FastMode = True ).start()
            else:
                cDownloadProgressBar(title = sTitle , url = sUrl , Dpath = sDownloadPath, icon = sThumbnail, mainUrl = sMainUrl).start()

            VSlog("Telechargement ok")

        except Exception, e:
            VSlog("Telechargement impossible " + e.message)
            self.__oConfig.showInfo('TvWatch', VSlang(30508))
            return False

        return True

    def StartDownloadOneFile(self,meta = []):
        VSlog('StartDownloadOneFile')
        self.__oConfig.showInfo("TvWatch", VSlang(30514) , 5)
        if ReadSingleDatabase('download_status') == "InProgress":
            self.__oConfig.showInfo('TvWatch', VSlang(30509))
            return
        oInputParameterHandler = cInputParameterHandler()

        meta = {}
        meta['sMovieTitle'] = oInputParameterHandler.getValue('sMovieTitle')
        meta['sMainUrl'] = oInputParameterHandler.getValue('sMainUrl')
        meta['sItemUrl'] = oInputParameterHandler.getValue('sItemUrl')
        meta['sThumbnail'] = oInputParameterHandler.getValue('sThumbnail')
        meta['sType'] = ''
        meta['sQual'] = ''
        meta['refresh'] = ''

        needShowHosters = oInputParameterHandler.getValue('needShowHosters')

        if needShowHosters == 'True':
            try:
                from resources.sites.server import showHosters
                params = showHosters(meta, False)
            except Exception, e:
                VSlog("StartDownloadOneFile showHosters ERROR: " + e.message)
        else:
            try:
                from resources.sites.server import Display_protected_link
                params = Display_protected_link(meta, False)
            except Exception, e:
                VSlog("StartDownloadOneFile Display_protected_link ERROR: " + e.message)

        try:
            sUrl = params['sMediaUrl']
            sFileName = meta['sMovieTitle']
            sThumbnail = params['sThumbnail']
            sMainUrl = params['sMainUrl']

            path = os.path.join(VSGetCachePath(), VS_str_conv(sFileName)).decode("utf-8")

            self.download(sUrl, sFileName, path, sThumbnail, sMainUrl)
        except Exception, e:
            self.__oConfig.showInfo('TvWatch', VSlang(30508))
            VSlog("StartDownloadOneFile ERROR: " + e.message)

    def RemoveDownload(self):
        self.__oConfig.showInfo("TvWatch", VSlang(30514) , 5)
        oInputParameterHandler = cInputParameterHandler()
        sFullTitle = oInputParameterHandler.getValue('sFullTitle')

        oDialog = self.__oConfig.createDialogYesNo(VSlang(30512))
        if (oDialog == 1):
            db = cDb()
            aEntry = db.get_downloadFromTitle(sFullTitle)
            if aEntry != []:
                sPath = aEntry[2]
                sPath = db.str_deconv(sPath)
                try:
                    xbmcvfs.delete(sPath)
                    db.del_download(sFullTitle)
                    self.__oConfig.showInfo('TvWatch', VSlang(30511))
                    self.__oConfig.update()
                except Exception, e:
                    VSlog("DelFile Error " + e.message)

    def StopDownload(self):
        self.__oConfig.showInfo("TvWatch", VSlang(30514) , 5)
        cDownloadProgressBar().StopAll()
        WriteSingleDatabase('download_status', 'NotStarted')
        oInputParameterHandler = cInputParameterHandler()
        sFullTitle = oInputParameterHandler.getValue('sFullTitle')

        db = cDb()
        aEntry = db.get_downloadFromTitle(sFullTitle)
        if aEntry != []:
            if aEntry[4] == "InProgress":
                meta = {}
                meta['title'] = db.str_deconv(aEntry[1])
                meta['path'] = db.str_deconv(aEntry[2])
                meta['icon'] = aEntry[3]
                meta['status'] = "NotStarted"
                meta['sMainUrl'] = aEntry[5]
                db.update_download(meta)
        self.__oConfig.update()
