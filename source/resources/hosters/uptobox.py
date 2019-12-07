#-*- coding: utf-8 -*-

#
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
# from resources.lib.config import cConfig
from resources.lib.util import VSlog, VSlang

import requests
import urllib2,urllib,xbmcgui,re,xbmc

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'TvWatch'
        self.__sFileName = ''
        self.oPremiumHandler = None
        self.stream = True
        # self.oConfig = cConfig()

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'uptobox'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def __modifyUrl(self, sUrl):
        if (sUrl.startswith('http://')):
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.request()
            sRealUrl = oRequestHandler.getRealUrl()
            self.__sUrl = sRealUrl
            return self.__getIdFromUrl()

        return sUrl;

    def __getKey(self):
        oRequestHandler = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'flashvars.filekey="(.+?)";'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            aResult = aResult[1][0].replace('.','%2E')
            return aResult

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        if "uptobox.com/" in self.__sUrl:
            a = self.__sUrl.find("uptobox.com/") + len("uptobox.com/")
            self.__sUrl = self.__sUrl[a:]
        elif "uptostream.com/iframe/" in self.__sUrl:
            a = self.__sUrl.find("uptostream.com/iframe/") + len("uptostream.com/iframe/")
            self.__sUrl = self.__sUrl[a:]
        elif "uptostream.com/" in self.__sUrl:
            a = self.__sUrl.find("uptostream.com/") + len("uptostream.com/")
            self.__sUrl = self.__sUrl[a:]

    def checkSubtitle(self,sHtmlContent):
        oParser = cParser()

        #On ne charge les sous titres uniquement si vostfr se trouve dans le titre.
        if re.search('<head\s*.+?>\s*<title>[^<>]+VOSTFR[^<>]*<\/title>',sHtmlContent,re.IGNORECASE):

            sPattern = '<track type=[\'"].+?[\'"] kind=[\'"]subtitles[\'"] src=[\'"]([^\'"]+).vtt[\'"] srclang=[\'"].+?[\'"] label=[\'"]([^\'"]+)[\'"]>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
                Files = []
                for aEntry in aResult[1]:
                    url = aEntry[0]
                    label = aEntry[1]
                    url = url + '.srt'

                    if not url.startswith('http'):
                        url = 'http:' + url
                    if 'Forc' not in label:
                        Files.append(url)
                return Files

        return False

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLinkByUserToken(self, url):
        VSlog("getMediaLinkByUserToken")
        self.setUrl(url)
        FILE_CODE = self.__sUrl
        USR_TOKEN = "e84e2bdf19d127b4e624eed2c83bfd871tgrq"
        URL = "https://uptobox.com/api/link"

        PARAMS = {'token':USR_TOKEN, 'file_code':FILE_CODE}

        try:
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()
            result = True, data['data']['dlLink']
        except Exception, e:
            result = False, False
        return result

    def getMediaLink(self):
        return self.getMediaLinkByUserToken(self.__sUrl)
        #dialog3 = xbmcgui.Dialog()
        #ret = dialog3.select('Choissisez votre mode de fonctionnement',['Passer en Streaming (via Uptostream)','Rester en direct (via Uptobox)'])
        # sPlayerMode = self.oConfig.getSetting('playerMode')
        #mode DL
        if sPlayerMode == '0':
            self.stream = False
        #mode stream
        elif sPlayerMode == '1':
            self.__sUrl = self.__sUrl.replace('http://uptobox.com/','http://uptostream.com/iframe/')
        else:
            return False

        #cGui().showInfo('Resolve', self.__sDisplayName, 5)

        #Si premium
        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        if (self.oPremiumHandler.isPremiumModeAvailable()):
            #self.stream = False
            return self.__getMediaLinkByPremiumUser()

        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        VSlog("__getMediaLinkForGuest")
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        SubTitle = ''
        SubTitle = self.checkSubtitle(sHtmlContent)

        if (self.stream):
            api_call = self.GetMedialinkStreaming(sHtmlContent)
        else:
            api_call = self.GetMedialinkDL(sHtmlContent)

        if api_call:
            if SubTitle:
                return True, api_call,SubTitle
            else:
                return True, api_call

        cGui().showInfo(self.__sDisplayName, VSlang(30510) , 5)
        return False, False


    def __getMediaLinkByPremiumUser(self):
        VSlog("__getMediaLinkByPremiumUser")
        if not self.oPremiumHandler.Authentificate():
            VSlog("cannot Authentificate")
            return False, False

        sHtmlContent = self.oPremiumHandler.GetHtml(self.__sUrl)

        SubTitle = ''
        SubTitle = self.checkSubtitle(sHtmlContent)

        if (self.stream):
            api_call = self.GetMedialinkStreaming(sHtmlContent)
        else:
            api_call = self.GetMedialinkDL(sHtmlContent)

        if api_call:
            if SubTitle:

                return True, api_call,SubTitle
            else:
                return True, api_call

        cGui().showInfo(self.__sDisplayName, VSlang(30510) , 5)
        return False, False

    def GetMedialinkDL(self,sHtmlContent):

        if 'You have to wait' in sHtmlContent:
            cGui().showInfo(self.__sDisplayName, 'Limitation active' , 10)
            return False

        # VSlog(sHtmlContent)

        oParser = cParser()
        # sPattern =  '(?s)<form\sname\s*=[\'"]F1[\'"].+?>(.+?)<center>'
        sPattern = '<a href="([^"]+)" class=\'big-button-green-flat mt-4 mb-4\' style="display: inline-block; text-decoration: none;">'
        aResult = oParser.parse(sHtmlContent, sPattern)

        # VSlog(aResult)

        if (aResult[0]):
            return urllib.quote(aResult[1][0], safe=":/")
            sForm = aResult[1][0]

            data = {}
            for match in re.finditer(r'type="hidden"\s+name="(.+?)"\s+value="(.*?)"', sForm):
                key, value = match.groups()
                data[key] = value

            postdata = urllib.urlencode( data )
            headers['Referer'] = self.__sUrl

            sHtmlContent = self.oPremiumHandler.GetHtml(self.__sUrl,postdata)

            sPattern =  '<a href *=[\'"](?!http:\/\/uptostream.+)([^<>]+?)[\'"]\s*>\s*<span class\s*=\s*[\'"]button_upload green[\'"]\s*>' #green khaki
            aResult = oParser.parse(sHtmlContent, sPattern) #ici on get le link a jouer directement

            if (aResult[0]):
                return urllib.quote(aResult[1][0], safe=":/")

        return False

    def GetMedialinkStreaming(self,sHtmlContent):

        oParser = cParser()
        sPattern =  'src":[\'"]([^<>\'"]+)[\'"],"type":[\'"][^\'"><]+?[\'"],"label":[\'"]([0-9]+p)[\'"].+?"lang":[\'"]([^\'"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        stream_url = ''

        if (aResult[0] == True):
            url=[]
            qua=[]

            for aEntry in aResult[1]:
                url.append(aEntry[0])
                tmp_qua = aEntry[1]
                if (aEntry[2]):
                    if 'unknow' not in aEntry[2]:
                        tmp_qua = tmp_qua + ' (' + aEntry[2] + ')'
                qua.append(tmp_qua)

            #Si une seule url
            if len(url) == 1:
                stream_url = url[0]
            #si plus de une
            elif len(url) > 1:
                #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    stream_url = url[ret]
                else:
                    return False
            else:
                return False

            stream_url = urllib.unquote(stream_url)

            if not stream_url.startswith('http'):
                stream_url = 'http:' + stream_url

            return stream_url
        else:
            cGui().showInfo(self.__sDisplayName, VSlang(30510) , 5)
            return False

        return False
