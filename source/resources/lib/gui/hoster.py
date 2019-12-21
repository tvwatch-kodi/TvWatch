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
from resources.lib.util import VSlog, VSerror

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

        # if ('streamz.' in sHostName):
        #     return self.getHoster('streamz')
        # if ('streamax' in sHostName):
        #     return self.getHoster('streamax')
        # if ('livestream' in sHostName):
        #     return self.getHoster('lien_direct')
        # if ('gounlimited' in sHostName):
        #     return self.getHoster('gounlimited')
        # if ('xdrive' in sHostName):
        #     return self.getHoster('xdrive')
        # if ('facebook' in sHostName):
        #     return self.getHoster('facebook')
        # if ('cloudcartel' in sHostName):
        #     return self.getHoster('cloudcartel')
        # if ('mixdrop.' in sHostName):
        #     return self.getHoster('mixdrop')
        # if ('mixloads' in sHostName):
        #     return self.getHoster('mixloads')
        # if ('vidoza.' in sHostName):
        #     return self.getHoster('vidoza')
        # if (('youtube' in sHostName) or ('youtu.be' in sHostName)):
        #     return self.getHoster('youtube')
        # if ('rutube' in sHostName):
        #     return self.getHoster('rutube')
        # if ('vk.com' in sHostName):
        #     return self.getHoster('vk')
        # if ('vkontakte' in sHostName):
        #     return self.getHoster('vk')
        # if ('vkcom' in sHostName):
        #     return self.getHoster('vk')
        # if ('megawatch' in sHostName):
        #     return self.getHoster('megawatch')
        # if ('playvidto' in sHostName):
        #     return self.getHoster('vidto')
        # if ('vidtodo.' in sHostName):
        #     return self.getHoster('vidtodo')
        # if ('vidstodo.' in sHostName):
        #     return self.getHoster('vidtodo')
        # if ('vidzi' in sHostName):
        #     return self.getHoster('vidzi')
        # if ('vcstream' in sHostName):
        #     return self.getHoster('vidcloud')
        # if ('filetrip' in sHostName):
        #     return self.getHoster('filetrip')
        # if (('dailymotion' in sHostName) or ('dai.ly' in sHostName)):
        #     if 'stream' in sHosterUrl:
        #         return self.getHoster('lien_direct')
        #     else:
        #         return self.getHoster('dailymotion')
        # if ('filez.' in sHostName):
        #     return self.getHoster('flashx')
        # if ('mystream' in sHostName) or ('mstream' in sHostName):
        #     return self.getHoster('mystream')
        # if ('streamingentiercom/videophp?type=speed' in sHosterUrl):
        #     return self.getHoster('speedvideo')
        # if ('speedvideo' in sHostName):
        #     return self.getHoster('speedvideo')
        # if ('speedvid' in sHostName):
        #     return self.getHoster('speedvid')
        # #if (('netu' in sHostName) or ('hqq' in sHostName)):
        #    # return self.getHoster('netu')
        # if ('upstream' in sHostName):
        #     return self.getHoster('upstream')
        # if ('mail.ru' in sHostName):
        #     return self.getHoster('mailru')
        # if ('onevideo' in sHostName):
        #     return self.getHoster('onevideo')
        # if ('googlevideo' in sHostName):
        #     return self.getHoster('googlevideo')
        # if ('picasaweb' in sHostName):
        #     return self.getHoster('googlevideo')
        # if ('googleusercontent' in sHostName):
        #     return self.getHoster('googlevideo')
        # if ('playreplay' in sHostName):
        #     return self.getHoster('playreplay')
        # if ('flashx' in sHostName):
        #     return self.getHoster('flashx')
        # if (('ok.ru' in sHostName) or ('odnoklassniki' in sHostName)):
        #     return self.getHoster('ok_ru')
        # if ('vimeo.com' in sHostName):
        #     return self.getHoster('vimeo')
        # # if ('openload' in sHostName):
        #     # return self.getHoster('openload')
        # if ('prostream' in sHostName):
        #     return self.getHoster('prostream')
        # if ('vidfast' in sHostName):
        #     return self.getHoster('vidfast')
        # if (('thevideo.' in sHostName) or ('video.tt' in sHostName) or ('vev.io' in sHostName)):
        #     return self.getHoster('thevideo_me')
        # if ('uqload.' in sHostName):
        #     return self.getHoster('uqload')
        # if ('letwatch' in sHostName):
        #     return self.getHoster('letwatch')
        # if ('letsupload' in sHostName):
        #     return self.getHoster('letsupload')
        # if ('filepup' in sHostName):
        #     return self.getHoster('filepup')
        # if ('vimple.ru' in sHostName):
        #     return self.getHoster('vimple')
        # if ('wstream.' in sHostName):
        #     return self.getHoster('wstream')
        # if ('watchvideo' in sHostName):
        #      return self.getHoster('watchvideo')
        # if ('drive.google.com' in sHostName):
        #     return self.getHoster('googledrive')
        # if ('docs.google.com' in sHostName):
        #     return self.getHoster('googledrive')
        # if ('vidwatch' in sHostName):
        #     return self.getHoster('vidwatch')
        # if ('up2stream' in sHostName):
        #     return self.getHoster('up2stream')
        # if ('vidbm.' in sHostName):
        #     return self.getHoster('vidbm')
        # if ('tune' in sHostName):
        #     return self.getHoster('tune')
        # if ('vidup' in sHostName):
        #     return self.getHoster('vidup')
        # if ('vidbull' in sHostName):
        #     return self.getHoster('vidbull')
        # if ('vidlox' in sHostName):
        #     return self.getHoster('vidlox')
        # if ('stagevu' in sHostName):
        #     return self.getHoster('stagevu')
        # if (('movshare' in sHostName) or ('wholecloud' in sHostName)):
        #     return self.getHoster('wholecloud')
        # if ('gorillavid' in sHostName):
        #     return self.getHoster('gorillavid')
        # if ('daclips' in sHostName):
        #     return self.getHoster('daclips')
        # if ('estream' in sHostName) and not ('widestream' in sHostName):
        #     return self.getHoster('estream')
        # if ('hdvid' in sHostName):
        #     return self.getHoster('hdvid')
        # #if ('streamango' in sHostName):
        # #    return self.getHoster('streamango')
        # #if ('streamcherry' in sHostName):
        # #    return self.getHoster('streamango')
        # if ('vshare' in sHostName):
        #     return self.getHoster('vshare')
        # if ('giga' in sHostName):
        #     return self.getHoster('giga')
        # if ('vidbom' in sHostName):
        #     return self.getHoster('vidbom')
        # if ('upvid.' in sHostName):
        #     return self.getHoster('upvid')
        # if (('cloudvid' in sHostName ) or ('clipwatching.' in sHostName)):#meme code
        #     return self.getHoster('cloudvid')
        # if ('megadrive' in sHostName):
        #     return self.getHoster('megadrive')
        # if ('downace' in sHostName):
        #     return self.getHoster('downace')
        # if ('clickopen' in sHostName):
        #     return self.getHoster('clickopen')
        # if ('iframe-secured' in sHostName):
        #     return self.getHoster('iframe_secured')
        # if ('iframe-secure' in sHostName):
        #     return self.getHoster('iframe_secure')
        # if ('goo.gl' in sHostName or 'bit.ly' in sHostName or 'streamcrypt.net' in sHostName or 'opsktp.com' in sHosterUrl):
        #     return self.getHoster('allow_redirects')
        # if ('jawcloud' in sHostName):
        #     return self.getHoster('jawcloud')
        # if ('kvid' in sHostName):
        #     return self.getHoster('kvid')
        # if ('soundcloud' in sHostName):
        #     return self.getHoster('soundcloud')
        # if ('mixcloud' in sHostName):
        #     return self.getHoster('mixcloud')
        # if ('ddlfr' in sHostName):
        #     return self.getHoster('ddlfr')
        # if ('pdj' in sHostName):
        #     return self.getHoster('pdj')
        # if ('vidzstore' in sHostName):
        #     return self.getHoster('vidzstore')
        # if ('hd-stream' in sHostName):
        #     return self.getHoster('hd_stream')
        # if ('rapidstream' in sHostName):
        #     return self.getHoster('rapidstream')
        # if ('beeload' in sHostName):
        #     return self.getHoster('beeload')
        # if ('verystream.' in sHostName):
        #     return self.getHoster('verystream')
        # if ('archive.' in sHostName):
        #     return self.getHoster('archive')
        # if ('freshstream' in sHostName):
        #     return self.getHoster('freshstream')
        # if ('jetload' in sHostName):
        #     return self.getHoster('jetload')
        # if ('french-vid' in sHostName or 'fembed.' in sHostName or 'yggseries' in sHostName or 'sendvid' in sHostName or 'vfsplayer' in sHostName):
        #     return self.getHoster('frenchvid')
        # if ('flix555' in sHostName):
        #     return self.getHoster('flix555')
        # if ('onlystream' in sHostName or 'gotochus' in sHostName):
        #     return self.getHoster('onlystream')
        #
        # #Lien telechargeable a convertir en stream
        # if ('1fichier' in sHostName):
        #     return self.getHoster('onefichier')
        # if ('uplea.com' in sHostName):
        #     return self.getHoster('uplea')
        # if ('uploaded' in sHostName or 'ul.to' in sHostName):
        #     return self.getHoster('uploaded')
        #
        # if ('kaydo.ws' in sHostName):
        #     return self.getHoster('lien_direct')

        #Si aucun hebergeur connu on teste les liens directs
        if (sHosterUrl[-4:] in '.mp4.avi.flv.m3u8.webm'):
            return self.getHoster('lien_direct')
        #Cas special si parametre apres le lien_direct
        if (sHosterUrl.split('?')[0][-4:] in '.mp4.avi.flv.m3u8.webm'):
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
                VSerror("Fichier introuvable")
                return False

        except Exception, e:
            VSerror("Fichier introuvable")
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
