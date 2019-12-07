#-*- coding: utf-8 -*-
# Primatech.

#
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.player import cPlayer
from resources.lib.db import cDb
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.util import VSlog

class cHosterGui:

    SITE_NAME = 'cHosterGui'

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oHoster, sMediaUrl, sThumbnail, protectedLink, sQual, bGetRedirectUrl = False):
        cConfig().log('showHoster')

        params = {}

        params['sHosterIdentifier'] = oHoster.getPluginIdentifier()
        params['sMediaUrl'] = sMediaUrl
        params['sMainUrl'] = protectedLink
        params['sItemUrl'] = sMediaUrl
        params['sFileName'] = oHoster.getFileName()
        params['title'] = oHoster.getDisplayName()
        params['sThumbnail'] = sThumbnail
        params['sQual'] = sQual
        params['sType'] = "tvshow"

        #existe dans le menu krypton 17
        # if not util.isKrypton():
        #     oGui.createContexMenuWatch(oGuiElement, oOutputParameterHandler)

        return self.play(params)

    def checkHoster(self, sHosterUrl):
        VSlog('checkHoster')
        #securitee
        if (not sHosterUrl):
            return False

        #Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]

        #Recuperation du host
        try:
            sHostName = sHosterUrl.split('/')[2]
        except:
            sHostName = sHosterUrl

        #L'user a active l'url resolver ?
        if cConfig().getSetting('UserUrlResolver') == 'true':
            import urlresolver
            hmf = urlresolver.HostedMediaFile(url=sHosterUrl)
            if hmf.valid_url():
                tmp = self.getHoster('resolver')
                RH = sHosterUrl.split('/')[2]
                RH = RH.replace('www.','')
                tmp.setRealHost( RH[:3].upper() )
                return tmp

        #Gestion classique
        if ('uptostream' in sHostName):
            # return self.getHoster('uptostream')
            return self.getHoster('uptobox')

        #Lien telechargeable a convertir en stream
        if ('uptobox' in sHostName):
            return self.getHoster('uptobox')

        #Si aucun hebergeur connu on teste les liens directs
        if (sHosterUrl[-4:] in '.mp4.avi.flv.m3u8.webm'):
            return self.getHoster('lien_direct')

        return False

    def getHoster(self, sHosterFileName):
        exec "from resources.hosters." + sHosterFileName + " import cHoster"
        return cHoster()

    def play(self, params = {}):
        VSlog("play hoster")
        # oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        protectedLink = oInputParameterHandler.getValue('protectedLink')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sTitle = oInputParameterHandler.getValue('title')
        sThumbnail = oInputParameterHandler.getValue('sThumbnail')
        sQual = ''
        sMainUrl = ''
        sType = ''

        if params != {}:
            sHosterIdentifier = params['sHosterIdentifier']
            sMediaUrl = params['sMediaUrl']
            protectedLink = params['sItemUrl']
            sMainUrl = params['sMainUrl']
            sFileName = params['sFileName']
            sTitle = params['title']
            sThumbnail = params['sThumbnail']
            sQual = params['sQual']
            sType = params['sType']

        if not sTitle:
            sTitle = sFileName

        VSlog("Hoster - play " + sMediaUrl)

        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        sHosterName = oHoster.getDisplayName()
        # cConfig().showInfo(sHosterName, 'Resolve')

        try:
            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink()

            if aLink[0]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(self.SITE_NAME)
                oGuiElement.setMediaUrl(aLink[1])
                oGuiElement.setTitle(sTitle)
                oGuiElement.setFileName(sTitle)
                oGuiElement.setThumbnail(sThumbnail)
                #oGuiElement.setTitle(oHoster.getFileName())
                if sType == 'tvshow':
                    oGuiElement.setMeta(2)
                else:
                    oGuiElement.setMeta(1)
                oGuiElement.getMetadonne()
                # oGuiElement.getInfoLabel()

                oPlayer = cPlayer()

                #sous titres ?
                if len(aLink) > 2:
                    oPlayer.AddSubtitles(aLink[2])

                playParams = {}
                playParams['guiElement'] = oGuiElement
                playParams['title'] = sFileName
                playParams['sUrlToPlay'] = aLink[1]
                # playParams['sItemUrl'] = protectedLink #dl protect
                playParams['sItemUrl'] = sMediaUrl #uptobox
                playParams['sMainUrl'] = sMainUrl
                playParams['sQual'] = sQual
                playParams['sThumbnail'] = sThumbnail
                playParams['tv'] = 'False'

                if not cConfig().testUrl(sThumbnail):
                    playParams['sThumbnail'] = oGuiElement.getThumbnail()

                return oPlayer.run(playParams)
            else:
                VSlog("ERROR: Fichier introuvable")
                return False

        except Exception, e:
            VSlog("ERROR: Fichier introuvable")
            VSlog('play Hoster Erreur ' + e.message)
            return False

    def addToPlaylist(self):
        cConfig().log('addToPlaylist')
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        VSlog("Hoster - play " + sMediaUrl)
        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if (aLink[0] == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
            oGuiElement.setTitle(oHoster.getFileName())

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oGui.showInfo('Playlist', str(oHoster.getFileName()), 5)
            return

        oGui.setEndOfDirectory()

    def __getRedirectUrl(self, sUrl):
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
