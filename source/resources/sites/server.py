#-*- coding: utf-8 -*-

from resources.lib.config import cConfig
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.favourite import cFav
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, VSlog, VSlang, VScreateDialogOK, VS_show_busy_dialog, VSwriteInFile
from resources.lib.db import cDb
from resources.lib.tvHandler import cTvHandler
from resources.lib.player import cPlayer
from resources.lib.config import GestionCookie

import urllib,re,urllib2
import xbmc, xbmcgui, xbmcplugin
import random

# UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = { 'User-Agent' : UA }

SITE_IDENTIFIER = 'server'
SITE_NAME = '[COLOR violet]TvWatch[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_HOST = 'https://www.annuaire-telechargement.com/'

def GetURL_MAIN():
    oRequestHandler = cRequestHandler(URL_HOST)
    oRequestHandler.request()
    URL = oRequestHandler.getRealUrl()
    if not URL:
        URL = URL_HOST
    return URL

URL_MAIN = GetURL_MAIN()
URL_DECRYPT =  'www.dl-protect1.com'

URL_IMAGE = 'http://www.zone-image.com/'

URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN  + 'index.php?', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

TV_EN_DIRECT = (URL_MAIN + 'tv/', 'showTvGroup')

MOVIE_NEWS = (URL_MAIN + 'nouveaute/', 'showMovies') # films (derniers ajouts)
MOVIE_EXCLUS = (URL_MAIN + 'exclus/', 'showMovies') # exclus (films populaires)
MOVIE_3D = (URL_MAIN + 'films-bluray-3d/', 'showMovies') # films en 3D
MOVIE_HD = (URL_MAIN + 'films-bluray-hd/', 'showMovies') # films en HD
MOVIE_HDLIGHT = (URL_MAIN + 'x265-x264-hdlight/', 'showMovies') # films en x265 et x264
MOVIE_VOSTFR = (URL_MAIN + 'filmsenvostfr/', 'showMovies') # films VOSTFR
MOVIE_4K = (URL_MAIN + 'film-ultra-hd-4k/', 'showMovies') # films "4k"

MOVIE_ANIME = (URL_MAIN + 'dessins-animes/', 'showMovies') # dessins animes

SERIE_VFS = (URL_MAIN + 'series-vf/', 'showMovies') # serie VF
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showMovies') # serie VOSTFR

ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies') # Anime VF
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies') # Anime VOSTFR

DOC_NEWS = (URL_MAIN + 'documentaires-gratuit/', 'showMovies') # docs
DOC_DOCS = ('http://', 'load')

SPORT_SPORTS = (URL_MAIN + 'sport/', 'showMovies') # sports
TV_NEWS = (URL_MAIN + 'emissions-tv/', 'showMovies') # dernieres emissions tv
SPECT_NEWS = (URL_MAIN + 'spectacles/', 'showMovies') # dernieres spectacles
CONCERT_NEWS = (URL_MAIN + 'concerts/', 'showMovies') # dernieres concerts
AUTOFORM_VID = (URL_MAIN + 'autoformations-videos/', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', 'http://primatech/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', VSlang(30076), 'search.png', oOutputParameterHandler) # Recherche

    oGui.addDir(SITE_IDENTIFIER, 'continueToWatch', '[B][COLOR khaki]' + VSlang(30424) + '[/COLOR][/B]', 'mark.png', oOutputParameterHandler) # Continuer à regarder

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showTheMovieDB', 'The Movie DB', 'host.png', oOutputParameterHandler) # The Movie DB

    # oOutputParameterHandler = cOutputParameterHandler()
    # oGui.addDir(SITE_IDENTIFIER, 'showTopIMDB', 'Top IMDB', 'host.png', oOutputParameterHandler) # The Movie DB

    # oOutputParameterHandler = cOutputParameterHandler()
    # LiveTV = '1'
    # oOutputParameterHandler.addParameter('mode', LiveTV)
    # oGui.addDir(SITE_IDENTIFIER, 'showTvGroup', VSlang(30469), 'replay.png', oOutputParameterHandler) # LiveTV

    # oOutputParameterHandler = cOutputParameterHandler()
    # SportsTV = '2'
    # oOutputParameterHandler.addParameter('mode', SportsTV)
    # oGui.addDir(SITE_IDENTIFIER, 'showTvGroup', VSlang(30471), 'replay.png', oOutputParameterHandler) # SportsTV

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showFilms', VSlang(30120), 'films.png', oOutputParameterHandler) # Films

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', VSlang(30121), 'replay.png', oOutputParameterHandler) # Series

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30112), 'doc.png', oOutputParameterHandler) # Documentaires

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('sItemUrl', TV_NEWS[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30117), 'tv.png', oOutputParameterHandler) # TV replay

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', SPECT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30425), 'host.png', oOutputParameterHandler) # Spectacles

    #TODO
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('sItemUrl', 'http://primatech')
    # oGui.addDir('cFav', 'getFavourites', VSlang(30423), 'star.png', oOutputParameterHandler) # Ma liste

    oGui.addDir(SITE_IDENTIFIER, 'getDownload', VSlang(30145), 'mark.png', oOutputParameterHandler) # Fichiers téléchargé

    oOutputParameterHandler = cOutputParameterHandler()
    if (cConfig().getSetting('home_update') == 'true'):
        oGui.addDir(SITE_IDENTIFIER, 'showUpdate', "[COLOR skyblue]"+VSlang(30418)+"[/COLOR]", 'update.png', oOutputParameterHandler)
    else:
        oGui.addDir(SITE_IDENTIFIER, 'checkUpdate', VSlang(30473), 'update.png', oOutputParameterHandler)

    oGui.setEndOfDirectory(50)

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showTvGroup():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    mode = int(oInputParameterHandler.getValue('mode'))

    tv = cTvHandler(mode)
    catLists = tv.getCategories()
    found = False
    cat = ''
    for i in catLists:
        if 'SPORTS' in i['category_name']:
            for i in tv.getChannels(i['cid']):
                if 'FR' in i['channel_title'].upper():
                    cat = i['cid']
                    found = True
                    break
            if found:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('cid', cat)
                oOutputParameterHandler.addParameter('mode', str(mode))
                icon = 'https://www.airysat.com/blog/wp-content/uploads/2017/04/bein-france-iptv.jpg'
                oGui.addTV(SITE_IDENTIFIER, 'showBeinFR', 'BEIN FR', '', icon, '', oOutputParameterHandler)
                break
    for i in catLists:
        if 'World Cup' not in i['category_name']:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('cid', i['cid'])
            oOutputParameterHandler.addParameter('mode', str(mode))
            icon = tv.url + 'images/' + i['category_image']
            oGui.addTV(SITE_IDENTIFIER, 'showChannels', i['category_name'], '', icon, '', oOutputParameterHandler)

    if mode == 1:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sItemUrl', TV_NEWS[0])
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30117), 'tv.png', oOutputParameterHandler) # TV replay
    oGui.setEndOfDirectory(50)

def showChannels():
    oGui = cGui()
    endOfDir = False

    oInputParameterHandler = cInputParameterHandler()
    cid = oInputParameterHandler.getValue('cid')
    mode = int(oInputParameterHandler.getValue('mode'))

    tv = cTvHandler(mode)
    channelsList = tv.getChannels(cid)

    total = len(channelsList)
    dialog = cConfig().createDialog(SITE_NAME)
    for i in channelsList:
        cConfig().updateDialog(dialog, total)
        if dialog.iscanceled():
            break
        url = i['channel_url'].replace('\\','')
        url = url.replace('/media/','/cdn/')
        title = i['channel_title']
        icon = tv.url + 'images/' + i['channel_thumbnail']
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('url', url)
        oOutputParameterHandler.addParameter('title', title)
        oOutputParameterHandler.addParameter('icon', icon)
        oOutputParameterHandler.addParameter('mode', str(mode))

        url += tv.generateToken().replace('eMeeea/1.0.0.','')
        if cConfig().testUrl(url):
            oGui.addTV(SITE_IDENTIFIER, 'playChannel', i['channel_title'], '', icon, '', oOutputParameterHandler)
            endOfDir = True
    cConfig().finishDialog(dialog)
    if endOfDir:
        oGui.setEndOfDirectory(50)

def showBeinFR():
    oGui = cGui()
    endOfDir = False

    oInputParameterHandler = cInputParameterHandler()
    cid = oInputParameterHandler.getValue('cid')
    mode = int(oInputParameterHandler.getValue('mode'))

    tv = cTvHandler(mode)

    for i in tv.getChannels(cid):
        title = i['channel_title']
        if ('BEIN' in title.upper()) and ('FR' in title.upper()):
            url = i['channel_url'].replace('\\','')
            url = url.replace('/media/','/cdn/')
            icon = tv.url + 'images/' + i['channel_thumbnail']
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('url', url)
            oOutputParameterHandler.addParameter('title', title)
            oOutputParameterHandler.addParameter('icon', icon)
            oOutputParameterHandler.addParameter('mode', str(mode))

            url += tv.generateToken().replace('eMeeea/1.0.0.','')
            if cConfig().testUrl(url):
                oGui.addTV(SITE_IDENTIFIER, 'playChannel', i['channel_title'], '', icon, '', oOutputParameterHandler)
                endOfDir = True
    if endOfDir:
        oGui.setEndOfDirectory(50)

def playChannel():
    oInputParameterHandler = cInputParameterHandler()
    url = oInputParameterHandler.getValue('url')
    title = oInputParameterHandler.getValue('title')
    icon = oInputParameterHandler.getValue('icon')
    mode = int(oInputParameterHandler.getValue('mode'))

    tv = cTvHandler(mode)
    url += tv.generateToken().replace('eMeeea/1.0.0.','')

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle(title)
    oGuiElement.setMediaUrl(url)
    oGuiElement.setThumbnail(icon)

    playParams = {}
    playParams['guiElement'] = oGuiElement
    playParams['title'] = title
    playParams['sUrlToPlay'] = url
    playParams['sItemUrl'] = url
    playParams['sMainUrl'] = url
    playParams['sQual'] = ''
    playParams['tv'] = 'True'
    playParams['sThumbnail'] = icon

    cPlayer(1).run(playParams)

def showFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30426), 'news.png', oOutputParameterHandler) #Nouveautés

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', MOVIE_EXCLUS[0])
    oOutputParameterHandler.addParameter('movie', "True")
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30427), 'sport.png', oOutputParameterHandler) #Populaires

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('sItemUrl', MOVIE_GENRES[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30428), 'hd.png', oOutputParameterHandler) #Blu-rays

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30429), 'hd.png', oOutputParameterHandler) #Films 3D

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30430), 'hd.png', oOutputParameterHandler) #Films HDLight

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30431), 'hd.png', oOutputParameterHandler) #Films 4K

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30432), 'animes.png', oOutputParameterHandler) #Dessins Animés

    oGui.setEndOfDirectory(50)

def showSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30433), 'vf.png', oOutputParameterHandler) #Séries VF

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30434), 'vostfr.png', oOutputParameterHandler) #Séries VOSTFR

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30435), 'animes.png', oOutputParameterHandler) #Dessins Animés VF

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sItemUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30436), 'animes.png', oOutputParameterHandler) #Dessins Animés VOSTFR

    oGui.setEndOfDirectory(50)

def showGenre(basePath):
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + basePath + '?genrelist[]=1'] )
    liste.append( ['Animation',URL_MAIN +  basePath + '?genrelist[]=2'] )
    liste.append( ['Arts Martiaux',URL_MAIN +  basePath + '?genrelist[]=3'] )
    liste.append( ['Aventure',URL_MAIN +  basePath + '?genrelist[]=4'] )
    liste.append( ['Biopic',URL_MAIN +  basePath + '?genrelist[]=5'] )
    liste.append( ['Comédie Dramatique',URL_MAIN +  basePath + '?genrelist[]=7'] )
    liste.append( ['Comédie Musicale',URL_MAIN +  basePath + '?genrelist[]=8'] )
    liste.append( ['Comédie',URL_MAIN +  basePath + '?genrelist[]=9'] )
    liste.append( ['Divers',URL_MAIN +  basePath + '?genrelist[]=10'] )
    liste.append( ['Documentaires',URL_MAIN +  basePath + '?genrelist[]=11'] )
    liste.append( ['Drame',URL_MAIN +  basePath + '?genrelist[]=12'] )
    liste.append( ['Epouvante Horreur',URL_MAIN +  basePath + '?genrelist[]=13'] )
    liste.append( ['Espionnage',URL_MAIN +  basePath + '?genrelist[]=14'] )
    liste.append( ['Famille',URL_MAIN +  basePath + '?genrelist[]=15'] )
    liste.append( ['Fantastique',URL_MAIN +  basePath + '?genrelist[]=16'] )
    liste.append( ['Guerre',URL_MAIN +  basePath + '?genrelist[]=17'] )
    liste.append( ['Historique',URL_MAIN +  basePath + '?genrelist[]=18'] )
    liste.append( ['Musical',URL_MAIN +  basePath + '?genrelist[]=19'] )
    liste.append( ['Péplum',URL_MAIN +  basePath + '?genrelist[]=6'] )
    liste.append( ['Policier',URL_MAIN +  basePath + '?genrelist[]=20'] )
    liste.append( ['Romance',URL_MAIN +  basePath + '?genrelist[]=21'] )
    liste.append( ['Science Fiction',URL_MAIN +  basePath + '?genrelist[]=22'] )
    liste.append( ['Thriller',URL_MAIN +  basePath + '?genrelist[]=23'] )
    liste.append( ['Western',URL_MAIN +  basePath + '?genrelist[]=24'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sItemUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory(500)

def showMovies(sSearch = ''):
    oGui = cGui()
    bGlobal_Search = False
    view = 500
    movie = "False"
    oParser = cParser()
    aResult = None

    if sSearch:
        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch=sSearch.replace(URL_SEARCH[0],'')

        sHtmlContent, aResult = searchOnServer(sSearch)

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('sItemUrl')
        try:
            movie = oInputParameterHandler.getValue('movie')
        except:
            pass
        sUrl = fixUrl(sUrl)
        #request = urllib2.Request(sUrl, None, headers)
        #sPattern = '<div style="height:[0-9]{3}px;"> *<a href="([^"]+)"><img class="[^"]+?" data-newsid="[^"]+?" src="([^<"]+)".+?<div class="[^"]+?" style="[^"]+?"> *<a href="[^"]+?"> ([^<]+?)<'
        sPattern = '<div style="height:[0-9]{3}px;">\s*<a href="([^"]+)"><img class="[^"]+?" data-newsid="[^"]+?" src="([^<"]+)".+?<a href="[^"]+" *>([^<]+)<'
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        aResult = oParser.parse(sHtmlContent, sPattern)

    #VSlog(aResult)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER,'[COLOR khaki]' + VSlang(30438) + '[/COLOR]')
        view = 50
    elif (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            sTitle = str(aEntry[2])
            sUrl2 = aEntry[0]

            #Si recherche et trop de resultat, on nettoye
            #31/12/17 Ne fonctionne plus ?
            # if sSearch and total > 2:
            #     if cUtil().CheckOccurence(sSearch, sTitle) == 0:
            #         continue

            if 'http' in aEntry[1]:
                sThumbnail = aEntry[1]
            else:
                sThumbnail = URL_IMAGE+aEntry[1]

            sIcon = ''
            if sSearch:
                if not cConfig().testUrl(sThumbnail):
                    sIcon = 'none.png'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMainUrl', str(sUrl2))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            # Peut ne plus fonctionner !! (Fonctionne au 04/02/2018)
            # sThumbnail = sThumbnail.replace("zone-telechargement.ws","zone-telechargement1.com")
            # sThumbnail = sThumbnail.replace("https://ww1.zone-telechargement","https://www.zone-telechargement")

            sDisplayTitle = sTitle

            if 'films-gratuit' in sUrl2 or '4k' in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, sIcon, sThumbnail, '', oOutputParameterHandler)
            elif movie != "True":
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, sIcon, sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sItemUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR white]'+VSlang(30472)+'[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory(view)


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="navigation" align="center" >.+?<a href="([^"]+)">Suivant</a></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        #print aResult
        return aResult[1][0]

    return False

def showMoviesLinks(params = {}):
    VSlog('showMoviesLinks')

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sMainUrl = oInputParameterHandler.getValue('sMainUrl')

    if params != {}:
        sMovieTitle = params['sMovieTitle']
        sThumbnail = params['sThumbnail']
        sMainUrl = params['sMainUrl']

    sItemUrl = sMainUrl

    sItemUrl = fixUrl(sItemUrl)
    oRequestHandler = cRequestHandler(sItemUrl)
    sHtmlContent = oRequestHandler.request()

    year = ""
    if sHtmlContent == '':
        showMovies(sMovieTitle)
    else:
        year = findYearInHTML(sHtmlContent)

    #Affichage du menu
    oGui = cGui()
    oGui.addText(SITE_IDENTIFIER,'[COLOR khaki]' + VSlang(30443) + '[/COLOR]')

    #on recherche d'abord la qualité courante
    oParser = cParser()
    sPattern = '<div style="[^"]+?"> *Qualité (.+?)<\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    sQual = ''
    if (aResult[0]):
        sQual = aResult[1][0]
        sTitle = sMovieTitle + ' [COLOR skyblue]' + sQual + '[/COLOR]'

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sItemUrl', sItemUrl)
        oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
        oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
        oOutputParameterHandler.addParameter('status', 'NotStarted')
        oOutputParameterHandler.addParameter('needShowHosters', 'True')

        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler, \
                      meta=True, isFolder=True, year=year, download=True)

    #on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)<\/b><\/span><span style="color:#.{6}"><b>([^<]+)<\/b><\/span>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sQual = aEntry[1] + " |" + aEntry[2].replace("(","").replace(")","")
            sTitle = sMovieTitle + ' [COLOR skyblue]' + sQual + '[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sItemUrl', URL_MAIN[:-1] + aEntry[0])
            oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oOutputParameterHandler.addParameter('status', 'NotStarted')
            oOutputParameterHandler.addParameter('needShowHosters', 'True')

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler, \
                          meta=True, isFolder=True, year=year, download=True)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory(50)

def showSeriesLinks(params = {}):
    VSlog('showSeriesLinks')
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sMainUrl = oInputParameterHandler.getValue('sMainUrl')

    if params != {}:
        sMovieTitle = params['sMovieTitle']
        sThumbnail = params['sThumbnail']
        sMainUrl = params['sMainUrl']

    sItemUrl = sMainUrl

    sMovieTitle = sMovieTitle.replace('[COMPLETE]','').strip()
    sMovieTitle = sMovieTitle.replace('COMPLETE','').strip()

    sItemUrl = fixUrl(sItemUrl)
    oRequestHandler = cRequestHandler(sItemUrl)
    sHtmlContent = oRequestHandler.request()

    year = ""
    if sHtmlContent == '':
        showMovies(sMovieTitle)
    else:
        year = findYearInHTML(sHtmlContent)

    sPattern = '<meta property="og:title" content="Game of Thrones - Saison 7 COMPLETE">'
    if sPattern in sHtmlContent:
        a = sHtmlContent.find(sPattern) + len('<meta property="og:title" content="')
        b = sHtmlContent[a:].find('">')
        sMovieTitle = sHtmlContent[a:a+b]

    #on recherche d'abord la qualité courante
    sPattern = '<div style="[^"]+?">.+?Qualité (.+?)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    sQual = ''
    if (aResult[1]):
        sQual = aResult[1][0]

    sDisplayTitle = sMovieTitle + ' [COLOR skyblue]' + sQual + '[/COLOR]'

    seasons = []
    meta = {}
    meta['sItemUrl'] = sItemUrl
    meta['sMovieTitle'] = sMovieTitle
    meta['sThumbnail'] = sThumbnail
    meta['sQual'] = sQual
    meta['sDisplayTitle'] = sDisplayTitle
    meta['season'] = '0'
    if 'Saison ' in sMovieTitle:
        try:
            meta['season'] = sMovieTitle[sMovieTitle.find('Saison ')+7:].replace('COMPLETE','').strip()
            nb = int(meta['season'])
        except:
            meta['season'] = '0'
    seasons.append(meta)

    #on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    #sPattern1 = '<a href="([^"]+)"><span class="otherquality">([^<]+)<'
    sPattern1 = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)<\/b><\/span><span style="color:#.{6}"><b>([^<]+)<\/b><\/span>'
    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    total = 0
    dialog = None
    if (aResult1[0] == True):
        for aEntry in aResult1[1]:
            sQual = aEntry[1] + " |" + aEntry[2].replace("(","").replace(")","")
            sDisplayTitle = sMovieTitle + ' [COLOR skyblue]' + sQual + '[/COLOR]'
            sItemUrl = URL_MAIN + 'telecharger-series' + aEntry[0]

            meta = {}
            meta['sItemUrl'] = sItemUrl
            meta['sMovieTitle'] = sMovieTitle
            meta['sThumbnail'] = sThumbnail
            meta['sQual'] = sQual
            meta['sDisplayTitle'] = sDisplayTitle
            meta['season'] = '0'
            if 'Saison ' in sMovieTitle:
                try:
                    meta['season'] = sMovieTitle[sMovieTitle.find('Saison ')+7:].replace('COMPLETE','').strip()
                except:
                    meta['season'] = '0'
            seasons.append(meta)

    #on regarde si dispo d'autres saisons
    sHtmlContent2 = CutSais(sHtmlContent)
    #sPattern2 = '<a href="([^"]+)"><span class="otherquality">([^<]+)<'
    sPattern2 = '<a href="([^"]+)"><span class="otherquality">([^<]+)<b>([^<]+)<span style="color:#.{6}">([^<]+)<\/span><span style="color:#.{6}">([^<]+)<\/b><\/span>'
    aResult2 = oParser.parse(sHtmlContent2, sPattern2)

    if (aResult2[0] == True):
        total = len(aResult2[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult2[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            sQual = aEntry[3].strip() + " | " + aEntry[4].replace("(","").replace(")","").strip()
            sTitle = aEntry[1] + aEntry[2] + ' [COLOR skyblue]' + sQual + '[/COLOR]'
            if ' Saison ' in sMovieTitle:
                sTitle = sMovieTitle[:sMovieTitle.find(' Saison ')] + " " +sTitle
                sMovieTitle = sMovieTitle[:sMovieTitle.find('Saison')]
                sMovieTitle += 'Saison '
                sMovieTitle += aEntry[2]
            sItemUrl = URL_MAIN + 'telecharger-series' + aEntry[0]

            meta = {}
            meta['sItemUrl'] = sItemUrl
            meta['sMovieTitle'] = sMovieTitle
            meta['sThumbnail'] = sThumbnail
            meta['sQual'] = sQual
            meta['sDisplayTitle'] = sTitle
            meta['season'] = '0'
            if 'Saison ' in sMovieTitle:
                try:
                    meta['season'] = sMovieTitle[sMovieTitle.find('Saison ')+7:].replace('COMPLETE','').strip()
                except:
                    meta['season'] = '0'
            seasons.append(meta)
        cConfig().finishDialog(dialog)

    stop = True
    seasons, currentSeason, currentEpisode = sortSeasonsAndGetCurrentSeason(seasons)
    if currentSeason != 0:
        oGui.addText(SITE_IDENTIFIER,'[COLOR khaki]' + VSlang(30446) + '[/COLOR]')
        stop = False
    else:
        oGui.addText(SITE_IDENTIFIER,'[COLOR khaki]' + VSlang(30444) + '[/COLOR]')
    for season in seasons:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sItemUrl', season['sItemUrl'])
        oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', season['sMovieTitle'])
        oOutputParameterHandler.addParameter('sThumbnail', season['sThumbnail'])
        oOutputParameterHandler.addParameter('sQual', season['sQual'])
        oOutputParameterHandler.addParameter('currentEpisode', str(currentEpisode))
        oOutputParameterHandler.addParameter('currentSeason', str(currentSeason))
        if currentSeason == int(season['season']):
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', season['sDisplayTitle'], '', season['sThumbnail'], '', oOutputParameterHandler, meta=True, year=year)
        else:
            if not stop:
                oGui.addText(SITE_IDENTIFIER,'[COLOR khaki]' + VSlang(30445) + '[/COLOR]')
                stop = True
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', season['sDisplayTitle'], '', season['sThumbnail'], '', oOutputParameterHandler, meta=True, year=year)

    oGui.setEndOfDirectory(50)

def showHosters(params = {}, playNow = True):# recherche et affiche les hotes
    VSlog('showHosters')

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('sItemUrl')
    sMainUrl = oInputParameterHandler.getValue('sMainUrl')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    if params != {}:
        sMovieTitle = params['sMovieTitle']
        sUrl = params['sItemUrl']
        sMainUrl = params['sMainUrl']
        sThumbnail = params['sThumbnail']

    sUrl = fixUrl(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    #Si ca ressemble aux lien premiums on vire les liens non premium
    meta = {}
    meta['sItemUrl'] = ExtractUptoboxLinksForMovies(sHtmlContent)
    meta['sMainUrl'] = sMainUrl
    meta['sMovieTitle'] = sMovieTitle
    meta['sThumbnail'] = sThumbnail
    meta['sType'] = 'movie'
    meta['sQual'] = 'osef'
    meta['refresh'] = "False"

    res = {}
    try:
        res = Display_protected_link(meta, playNow)
    except Exception, e:
        VSlog("showHosters ERROR: " + e.message)
    return res

def showSeriesHosters():# recherche et affiche les hotes
    VSlog('showSeriesHosters')

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de paramettre
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sItemUrl = oInputParameterHandler.getValue('sItemUrl')
    sMainUrl = oInputParameterHandler.getValue('sMainUrl')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sQual = oInputParameterHandler.getValue('sQual')
    currentEpisode = oInputParameterHandler.getValue('currentEpisode')
    currentSeason = oInputParameterHandler.getValue('currentSeason')

    sItemUrl = fixUrl(sItemUrl)
    oRequestHandler = cRequestHandler(sItemUrl)
    sHtmlContent = oRequestHandler.request()

    Links = ExtractUptoboxLinksForTvShows(sHtmlContent)

    episodes = []
    if (len(Links) > 0):
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in Links:
            cConfig().updateDialog(dialog, len(Links))

            if dialog.iscanceled():
                break

            sName = aEntry[1]
            sName = sName.replace('Télécharger','')
            sName = sName.replace('pisodes','pisode')
            sItemUrl = aEntry[0]

            # if sName != '' and sName.find('pisode') != -1:
            sTitle = sMovieTitle + ' ' + sName
            sTitle = sTitle.replace('[COMPLETE]','').strip()
            sTitle = sTitle.replace('COMPLETE','').strip()
            sDisplayTitle = sTitle

            meta = {}
            meta['sItemUrl'] = sItemUrl
            meta['sMovieTitle'] = sTitle
            meta['sDisplayTitle']= sDisplayTitle
            meta['sThumbnail'] = sThumbnail
            meta['sType'] = 'tvshow'
            meta['sQual'] = sQual
            meta['refresh'] = "False"
            meta['episode'] = '0'
            if "Episode" in sTitle:
                episode = sTitle[sTitle.find("Episode")+7:].split(" ")
                meta['episode'] = episode[1]
                episodes.append(meta)
                if "Saison" in sTitle:
                    season = sTitle[sTitle.find("Saison")+6:sTitle.find("Episode")].split(" ")
                    try:
                        if int(currentSeason) != int(season[1]):
                            currentEpisode = '0'
                    except Exception, e:
                        VSlog("Issue on showSeriesHosters (season): " + e.message)
                        currentEpisode = '0'
            elif "Episode" not in sTitle and "Saison" not in sTitle:
                episodes.append(meta)

        for i in range(len(episodes)):
            try:
                if int(episodes[i]['episode']) == int(currentEpisode):
                    episodes.insert(0, episodes[i])
                    del episodes[i+1]
                    break
            except Exception, e:
                VSlog("Issue on showSeriesHosters (episode): " + e.message)
                break

        stop = True
        if int(currentEpisode) != 0:
            oGui.addText(SITE_IDENTIFIER,'[COLOR khaki]' + VSlang(30446) + '[/COLOR]')
            stop = False
        else:
            oGui.addText(SITE_IDENTIFIER,'[COLOR khaki]' + VSlang(30447) + '[/COLOR]')
        for episode in episodes:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sItemUrl', episode['sItemUrl'])
            oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', episode['sMovieTitle'])
            oOutputParameterHandler.addParameter('sThumbnail', episode['sThumbnail'])
            oOutputParameterHandler.addParameter('sType', episode['sType'])
            oOutputParameterHandler.addParameter('sQual', episode['sQual'])
            oOutputParameterHandler.addParameter('refresh', episode['refresh'])
            oOutputParameterHandler.addParameter('status', 'NotStarted')

            oGui.addTV(SITE_IDENTIFIER, 'Display_protected_link', episode['sDisplayTitle'], '', episode['sThumbnail'], '', \
                      oOutputParameterHandler, meta=True, isFolder=True, download=True)
            if not stop:
                oGui.addText(SITE_IDENTIFIER,'[COLOR khaki]' + VSlang(30448) + '[/COLOR]')
                stop = True

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory(50)

    # if len(episodes) == 1:
    #     params = {}
    #     params['sItemUrl'] = episodes[0]['sItemUrl']
    #     params['sMainUrl'] = sMainUrl
    #     params['sMovieTitle'] = episodes[0]['sMovieTitle']
    #     params['sThumbnail'] = episodes[0]['sThumbnail']
    #     params['sType'] = episodes[0]['sType']
    #     params['sQual'] = episodes[0]['sQual']
    #     params['refresh'] = episodes[0]['refresh']
    #
    #     try:
    #         Display_protected_link(params)
    #     except Exception, e:
    #         VSlog("showSeriesHosters ERROR: " + e.message)
    # else:
    #     oGui.setEndOfDirectory(50)

def showStreamingHosters():# recherche et affiche les hotes
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('sItemUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sUrl = fixUrl(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<iframe.+?src="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(sUrl))

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            #print sHosterUrl

            sDisplayTitle = sMovieTitle

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                # cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory(50)

def Display_protected_link(params = {}, playNow = True):
    VSlog('Display_protected_link')
    if playNow:
        VS_show_busy_dialog()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('sItemUrl')
    sMainUrl = oInputParameterHandler.getValue('sMainUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sType = oInputParameterHandler.getValue('sType')
    sQual = oInputParameterHandler.getValue('sQual')
    refresh = oInputParameterHandler.getValue('refresh')

    if params != {}:
        sUrl = params['sItemUrl']
        sMainUrl = params['sMainUrl']
        sMovieTitle = params['sMovieTitle']
        sThumbnail = params['sThumbnail']
        sType = params['sType']
        sQual = params['sQual']
        refresh = params['refresh']

    oParser = cParser()

    #Est ce un lien dl-protect ?
    if URL_DECRYPT in sUrl:
        sHtmlContent = DecryptDlProtecte(sUrl)

        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotecte = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = '<div class="lienet"><a href="(.+?)">'
                aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)

        else:
            oDialog = VScreateDialogOK(VSlang(30458))
            aResult_dlprotecte = (False, False)

    #Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotecte = (True, [sUrl])

    if aResult_dlprotecte[0]:
        episode = 1
        for aEntry in aResult_dlprotecte[1]:
            sHosterUrl = aEntry
            sTitle = sMovieTitle
            if len(aResult_dlprotecte[1]) > 1:
                sTitle = sMovieTitle + ' episode ' + str(episode)

            sDisplayTitle = sTitle

            oHosterGui = cHosterGui()

            episode+=1
            oHoster = oHosterGui.checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)

                playParams = {}
                playParams['sHosterIdentifier'] = oHoster.getPluginIdentifier()
                playParams['sMediaUrl'] = sHosterUrl
                playParams['sItemUrl'] = sUrl
                playParams['sMainUrl'] = sMainUrl
                playParams['sFileName'] = sTitle
                playParams['title'] = sDisplayTitle
                playParams['sThumbnail'] = sThumbnail
                playParams['sQual'] = sQual
                playParams['refresh'] = refresh
                playParams['sType'] = sType

                if playNow:
                    oHosterGui.play(playParams)
                    if refresh == "True":
                        cGui().updateDirectory()
                else:
                    return playParams
    # cConfig().showInfo('TvWatch', VSlang(30513))

def prepareNextEpisode(sMovieTitle, sQual, sType):
    VSlog("Début prepareNextEpisode")
    if sType == 'tvshow':
        params = getNextEpisode(sMovieTitle, sQual)
        if params != {}:
            try:
                res = Display_protected_link(params, False)
            except Exception, e:
                VSlog("prepareNextEpisode ERROR: " + e.message)
            VSlog("Fin prepareNextEpisode")
            return res
    return None

def playUrl(playParams):
    cHosterGui().play(playParams)

def getNextEpisode(title, sQual, nextSeason = False):
    VSlog('getNextEpisode: current ' + title)

    try:
        quality, language = sQual.lower().replace(" ","").split("|")
        if "720p" in quality:
            quality = "720p"
        elif "1080p" in quality:
            quality = "1080p"
        if "french" in language:
            language = "french"
        VSlog("quality: %s language: %s" % (quality, language))
    except Exception, e:
        quality = 'somerandomstring'
        language = 'somerandomstring'
        VSlog("getNextEpisode ERROR: " + e.message)

    sSearch = title[:(title.lower().find("episode"))].strip()
    sHtmlContent, aResult = searchOnServer(sSearch, titleonly=True)

    sMainUrl = ''
    if (aResult[0] == True):
        sSeason = None
        sSeasonNum = 0
        if "Saison " in title:
            sSeason = title[title.find("Saison"):title.find(" Episode")]
            try:
                try:
                    sSeasonNum = int(title[title.find("Saison ")+7:title.find(" Episode")])
                except:
                    sSeasonNum = 0
            except Exception, e:
                VSlog('getNextEpisode ERROR : ' + e.message)

        sEpisode = None
        if "Episode " in title:
            sEpisode = title[title.find("Episode"):]

        for aEntry in aResult[1]:
            sMovieTitle = aEntry[2]
            sUrl = aEntry[0]
            sMainUrl = sUrl
            if 'http' in aEntry[1]:
                foundThumbnail = aEntry[1]
            else:
                foundThumbnail = URL_MAIN+aEntry[1]

            if sSeason in sMovieTitle:
                VSlog("Saison OK")
                qualAndLang = False
                if (quality in sUrl.replace("-","")) and (language in sUrl.replace("-","")):
                    qualAndLang = True
                if qualAndLang:
                    VSlog("Quality and Language OK")

                    sUrl = fixUrl(sUrl)
                    oRequestHandler = cRequestHandler(sUrl)
                    sHtmlContent = oRequestHandler.request()

                    Links = ExtractUptoboxLinksForTvShows(sHtmlContent)

                    if (len(Links) > 0):
                        getNextOne = False
                        params = {}
                        for aEntry in Links:
                            foundUrl = None
                            foundTitle = None
                            sName = aEntry[1]
                            sName = sName.replace('Télécharger','')
                            sName = sName.replace('pisodes','pisode')
                            sUrl2 = aEntry[0]

                            if sName != '' and sName.find('pisode') != -1:
                                sTitle = sMovieTitle + ' ' + sName
                                sTitle = sTitle.replace('[COMPLETE]','').strip()
                                sTitle = sTitle.replace('COMPLETE','').strip()
                                sDisplayTitle = sTitle
                                foundUrl = sUrl2
                                foundTitle = sTitle

                            if getNextOne:
                                params['sItemUrl'] = foundUrl
                                params['sMainUrl'] = sMainUrl
                                params['sMovieTitle'] = foundTitle
                                params['sThumbnail'] = foundThumbnail
                                params['sType'] = "tvshow"
                                params['sQual'] = sQual
                                params['refresh'] = "True"
                                break

                            if sEpisode in foundTitle:
                                if nextSeason:
                                    params['sItemUrl'] = foundUrl
                                    params['sMainUrl'] = sMainUrl
                                    params['sMovieTitle'] = foundTitle
                                    params['sThumbnail'] = foundThumbnail
                                    params['sType'] = "tvshow"
                                    params['sQual'] = sQual
                                    params['refresh'] = "True"
                                    break
                                else:
                                    getNextOne = True

                        if params != {}:
                            VSlog('getNextEpisode: target ' + foundTitle)
                            return params
                            break
                        elif not nextSeason:
                            title = title[:title.find("Saison")]
                            title += "Saison " + str(sSeasonNum+1) + " Episode 1"
                            getNextEpisode(title, sQual, True)
                            break

        # sNextPage = __checkForNextPage(sHtmlContent)
        # if (sNextPage != False):
        #     oOutputParameterHandler = cOutputParameterHandler()
        #     oOutputParameterHandler.addParameter('sItemUrl', sNextPage)
        #     oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    return {}

def continueToWatch():
    VSlog("continueToWatch")
    oGui = cGui()
    oDb = cDb()
    oConfig = cConfig()
    dialog = oConfig.createDialog(SITE_NAME)
    matchedrow = oDb.get_history()
    matchedrow.reverse()
    for aEntry in matchedrow:
        oConfig.updateDialog(dialog, len(matchedrow))
        if dialog.iscanceled():
            break

        sUrl = aEntry[1]
        sMainUrl = aEntry[2]
        sRawtitle = aEntry[3]
        sRawtitle = oDb.str_deconv(sRawtitle)
        sTitle = aEntry[4]
        sTitle = oDb.str_deconv(sTitle)
        sThumbnail = aEntry[5]
        sType = aEntry[6]
        sQual = aEntry[7]

        status = 'NotStarted'
        aEntryDl = oDb.get_downloadFromTitle(sTitle)
        if aEntryDl != []:
            status = aEntryDl[4]

        # VSlog(aEntry)

        correctedURL = correctUrl(sMainUrl)
        if correctedURL != '':
            sMainUrl = URL_MAIN + correctedURL

        sFullTitle = sTitle

        if "Episode " in sTitle:
            sTitle = sTitle[:sTitle.find("Episode ")].rstrip()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sItemUrl', sUrl)
        oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sFullTitle', sFullTitle)
        oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
        oOutputParameterHandler.addParameter('sType', sType)
        oOutputParameterHandler.addParameter('sRawtitle', sRawtitle)
        oOutputParameterHandler.addParameter('sQual', sQual)
        oOutputParameterHandler.addParameter('refresh', "True")
        oOutputParameterHandler.addParameter('status', status)

        sDisplayTitle = sTitle

        if sType == 'tvshow':
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler, continueToWatchFolder = True, isFolder=True)
        else:
            oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler, continueToWatchFolder = True, isFolder=True)

    oConfig.finishDialog(dialog)
    if len(matchedrow) == 0:
        oGui.addText(SITE_IDENTIFIER,'[COLOR khaki]' + VSlang(30449) + '[/COLOR]')
        oGui.setEndOfDirectory(50)
    else:
        oGui.setEndOfDirectory(500)

def getDownload():
    VSlog("getDownload")
    oGui = cGui()
    oDb = cDb()
    oConfig = cConfig()
    dialog = oConfig.createDialog(SITE_NAME)
    matchedrow = oDb.get_download()
    matchedrow.reverse()
    for aEntry in matchedrow:
        oConfig.updateDialog(dialog, len(matchedrow))
        if dialog.iscanceled():
            break

        sTitle = aEntry[1]
        sTitle = oDb.str_deconv(sTitle)
        sPath = aEntry[2]
        sPath = oDb.str_deconv(sPath)
        sThumbnail = aEntry[3]
        status = aEntry[4]
        sMainUrl = aEntry[5]

        sFullTitle = sTitle

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sFullTitle', sFullTitle)
        oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
        oOutputParameterHandler.addParameter('sPath', sPath)
        oOutputParameterHandler.addParameter('status', status)

        sDisplayTitle = sTitle

        oGui.addMovie(SITE_IDENTIFIER, 'playDownload', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler, downloadFolder = True, isFolder=True)

    oConfig.finishDialog(dialog)
    if len(matchedrow) == 0:
        oGui.addText(SITE_IDENTIFIER,'[COLOR khaki]' + VSlang(30504) + '[/COLOR]')
        oGui.setEndOfDirectory(50)
    else:
        oGui.setEndOfDirectory(500)

def playDownload():
    oInputParameterHandler = cInputParameterHandler()
    sMainUrl = oInputParameterHandler.getValue('sMainUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sFullTitle = oInputParameterHandler.getValue('sFullTitle')
    sPath = oInputParameterHandler.getValue('sPath')
    status = oInputParameterHandler.getValue('status')

    try:
        xlistitem = xbmcgui.ListItem( sMovieTitle, iconImage=sThumbnail, path=sPath)
    except:
        xlistitem = xbmcgui.ListItem( sMovieTitle, iconImage=sThumbnail, )
    xlistitem.setInfo( "video", { "Title": sMovieTitle } )

    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()
    playlist.add( sPath, xlistitem )

    xbmcPlayer = xbmc.Player(  )
    xbmcPlayer.play(playlist)

def playContinueToWatch(sFullTitle):
    oDb = cDb()
    aEntry = oDb.get_historyFromTitle(sFullTitle)
    # VSlog(aEntry)

    if aEntry:
        sUrl = aEntry[1]
        sMainUrl = aEntry[2]
        sRawtitle = aEntry[3]
        sRawtitle = oDb.str_deconv(sRawtitle)
        sTitle = aEntry[4]
        sTitle = oDb.str_deconv(sTitle)
        sThumbnail = aEntry[5]
        sType = aEntry[6]
        sQual = aEntry[7]

        params = {}
        params['sItemUrl'] = sUrl
        params['sMainUrl'] = sMainUrl
        params['sMovieTitle'] = sTitle
        params['sThumbnail'] = sThumbnail
        params['sType'] = sType
        params['sQual'] = sQual
        params['refresh'] = "True"

        try:
            Display_protected_link(params)
        except Exception, e:
            VSlog("playContinueToWatch ERROR: " + e.message)

def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Qualités également disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''

def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Saisons également disponibles pour cette saison:</h3>(.+?)<h3>Qualités également disponibles pour cette saison:</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    return ''

#keep Premium links only
def CutPremiumlinks(sHtmlContent):
    if 'premium' in sHtmlContent.lower():
        a = sHtmlContent.lower().find('premium')
        sHtmlContent = sHtmlContent[a:]
    return sHtmlContent

def ExtractUptoboxLinks(sHtmlContent):
    #Recupere les liens Uptobox uniquement
    Links = []
    if 'uptobox' in sHtmlContent.lower():
        a = sHtmlContent.lower().find('uptobox')
        aa = a
        sHtmlContent = sHtmlContent[a:]
        stop = False
        while not stop:
            if 'href="' in sHtmlContent:
                a = sHtmlContent.find('href="') + 6
            if 'font-weight:bold' in sHtmlContent:
                aa = sHtmlContent.find('font-weight:bold') + 16
            if a < aa:
                b = sHtmlContent[a:].find('">')
                c = sHtmlContent[a+b:].find('</a>')
                link = sHtmlContent[a:a+b]
                name = sHtmlContent[a+b+2:a+b+c]
                Links.append([link, name])
                sHtmlContent = sHtmlContent[a+b+c+2:]
            else:
                stop = True
    return Links

def ExtractUptoboxLinksForTvShows(sHtmlContent):
    LinksGroup = []
    while 'uptobox' in sHtmlContent.lower():
        a = sHtmlContent.lower().find('uptobox')
        sHtmlContent = sHtmlContent[a:]
        if '</div>' in sHtmlContent[:len('uptobox')+10]:
            LinksGroup.append(ExtractUptoboxLinks(sHtmlContent))
        sHtmlContent = sHtmlContent[7:]

    max = 0
    Links = []
    for l in LinksGroup:
        if len(l) > max:
            max = len(l)
            Links = l

    return Links

def ExtractUptoboxLinksForMovies(sHtmlContent):
    LinksGroup = []
    while 'uptobox' in sHtmlContent.lower():
        a = sHtmlContent.lower().find('uptobox')
        sHtmlContent = sHtmlContent[a:]
        if '</div>' in sHtmlContent[:len('uptobox')+10]:
            LinksGroup.append(ExtractUptoboxLinks(sHtmlContent))
        sHtmlContent = sHtmlContent[7:]

    min = 10000
    Links = []
    for l in LinksGroup:
        if len(l) < min and len(l) > 0:
            min = len(l)
            Links = l

    link = ''
    if len(Links) > 0:
        link = Links[0][0]

    return link

def DecryptDlProtecte(url):
    VSlog('DecryptDlProtecte : ' + url)

    url = url.replace('https', 'http')

    if not (url):
        return ''

    # 1ere Requete pour recuperer le cookie
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    cookies = GestionCookie().Readcookie('www_dl-protect1_com')
    #VSlog( 'cookie'  + str(cookies))

    #Tout ca a virer et utiliser oRequestHandler.addMultipartFiled('sess_id':sId,'upload_type':'url','srv_tmp_url':sTmp) quand ca marchera
    multipart_form_data = {'submit':'continuer','submit':'Continuer'}
    data, headersMulti = encode_multipart(multipart_form_data, {})

    #2 eme requete pour avoir le lien
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(oRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addHeaderEntry('Host', 'www.dl-protect1.com')
    oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Content-Length', headersMulti['Content-Length'])
    oRequestHandler.addHeaderEntry('Content-Type', headersMulti['Content-Type'])
    oRequestHandler.addHeaderEntry('Cookie', cookies)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')

    oRequestHandler.addParametersLine(data)

    sHtmlContent = oRequestHandler.request()

    return sHtmlContent

#******************************************************************************
#from http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/

"""Encode multipart form data to upload files via POST."""

def encode_multipart(fields, files, boundary = None):
    r"""Encode dict of form fields and dict of files as multipart/form-data.
    Return tuple of (body_string, headers_dict). Each value in files is a dict
    with required keys 'filename' and 'content', and optional 'mimetype' (if
    not specified, tries to guess mime type or uses 'application/octet-stream').

    >>> body, headers = encode_multipart({'FIELD': 'VALUE'},
    ...                                  {'FILE': {'filename': 'F.TXT', 'content': 'CONTENT'}},
    ...                                  boundary='BOUNDARY')
    >>> print('\n'.join(repr(l) for l in body.split('\r\n')))
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FIELD"'
    ''
    'VALUE'
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FILE"; filename="F.TXT"'
    'Content-Type: text/plain'
    ''
    'CONTENT'
    '--BOUNDARY--'
    ''
    >>> print(sorted(headers.items()))
    [('Content-Length', '193'), ('Content-Type', 'multipart/form-data; boundary=BOUNDARY')]
    >>> len(body)
    193
    """

    import mimetypes
    import random
    import string

    _BOUNDARY_CHARS = string.digits

    def escape_quote(s):
        return s.replace('"', '\\"')

    if boundary is None:
        boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(15))
    lines = []

    for name, value in fields.items():
        lines.extend((
            '-----------------------------{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
            '',
            str(value),
            '-----------------------------{0}--'.format(boundary),
            '',
        ))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(
                    escape_quote(name), escape_quote(filename)),
            'Content-Type: {0}'.format(mimetype),
            '',
            value['content'],
        ))

    body = '\r\n'.join(lines)

    headers = {
        'Content-Type': 'multipart/form-data; boundary=---------------------------{0}'.format(boundary),
        'Content-Length': str(len(body)),
    }

    return (body, headers)

def showUpdate():
    try:
        from resources.lib.about import cAbout
        cAbout().checkdownload()
    except:
        pass
    return

def checkUpdate():
    try:
        from resources.lib.about import cAbout
        if not cAbout().checkupdate():
            cConfig().showInfo("TvWatch", VSlang(30474))
    except:
        pass
    return

def showTheMovieDB():
    try:
        from themoviedb_org import start
        start()
    except Exception, e:
        VSlog('ERROR showTheMovieDB: '+e.message)
    return

def showTopIMDB():
    try:
        from topimdb import start
        start()
    except Exception, e:
        VSlog('ERROR showTopIMDB: '+e.message)
    return

def sortSeasonsAndGetCurrentSeason(seasons):
    db = cDb()
    res = db.get_historyFromTitle(seasons[0]['sMovieTitle'])
    currentSeason = 0
    currentEpisode = 0
    stop = False
    while not stop:
        stop = True
        for i in range(len(seasons)-1):
            if int(seasons[i]['season']) > int(seasons[i+1]['season']):
                seasons[i], seasons[i+1] = seasons[i+1], seasons[i]
                stop = False

    if res:
        ind = 0
        for i in range(len(seasons)):
            title = db.str_deconv(res[4])
            titleCp = title
            if "Episode " in title:
                title = title[:title.find("Episode ")].rstrip()
            if title == seasons[i]['sMovieTitle']:
                try:
                    currentEpisode = int(titleCp[titleCp.find("Episode ")+8:].replace(" ",""))
                except:
                    currentEpisode = 0
                currentSeason = int(seasons[i]['season'])
                seasons[ind], seasons[i] = seasons[i], seasons[ind]
                ind += 1
    return seasons, currentSeason, currentEpisode

def fixUrl(url):
    url = url.replace("://","")
    url = URL_MAIN + url[url.find("/")+1:]
    return url

def correctUrl(url):
    if '//' in url:
        a = url.find('//')
        url = url[a+2:]
        if '/' in url:
            a = url.find('/')
            return url[a+1:]
    return ''

def searchOnServer(sSearch, titleonly=False):
    query_args = ( ( 'do' , 'search' ) , ('subaction' , 'search' ) , ('story' , sSearch ) )
    if titleonly:
        query_args = ( ( 'do' , 'search' ) , ('subaction' , 'search' ) , ('story' , sSearch ) , ('titleonly' , '3' ))

    sPattern = '<a href="([^"]+)" *><img class="mainimg.+?src="([^"]+)"(?:.|\s)+?<a href=".+?" *>([^"]+)</a>'
    data = urllib.urlencode(query_args)
    oRequestHandler = cRequestHandler(URL_SEARCH[0])
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParametersLine(data)
    oRequestHandler.addParameters('User-Agent', UA)
    oRequestHandler.addParameters('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    oRequestHandler.addParameters('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addParameters('Accept-Encoding','gzip, deflate, br')
    oRequestHandler.addParameters('Referer', URL_MAIN)
    oRequestHandler.addParameters('Content-Type','application/x-www-form-urlencoded')
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    return sHtmlContent, aResult

def findYearInHTML(sHtmlContent):
    year = ""
    if sHtmlContent != '':
        sHtmlContent = sHtmlContent.replace(" ", "")
        if "Datedesortie:" in sHtmlContent:
            a = sHtmlContent.find("Datedesortie:") + 13
            sHtmlContent = sHtmlContent[a:]
            found = 0
            count = 0
            for char in sHtmlContent:
                count += 1
                if char.isdigit():
                    found += 1
                    if found == 4:
                        year = sHtmlContent[count-4:count]
                        VSlog("YEAR found: "+year)
                        break
                    if count > 30:
                        break
    return year
