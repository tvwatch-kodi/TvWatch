#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, VSlog, VSlang, VSerror, VSshowInfo, VSupdate, VScreateDialogSelect
from resources.lib.tmdb import cTMDb
from resources.lib.config import cConfig

try:    import json
except: import simplejson as json

SITE_IDENTIFIER = 'themoviedb_org'
SITE_NAME = '[COLOR orange]TheMovieDB[/COLOR]'
SITE_DESC = 'Base de données video.'

#doc de l'api http://docs.themoviedb.apiary.io/

URL_MAIN = 'https://www.themoviedb.org/'

API_KEY = '92ab39516970ab9d86396866456ec9b6'
API_VERS = '3'
API_URL = URL_MAIN + API_VERS


#FANART_URL = 'https://image.tmdb.org/t/p/original/'


#https://api.themoviedb.org/3/movie/popular?api_key=92ab39516970ab9d86396866456ec9b6

tmdb_session = ''
tmdb_account = ''
oConfig = cConfig()

def start():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', VSlang(30076), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesGeneral', VSlang(30120), 'films.png', oOutputParameterHandler) # Films

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesGeneral', VSlang(30121), 'replay.png', oOutputParameterHandler) # Series

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('topimdb', 'start', 'Top Imdb', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showFolderList', 'Listes TMDB', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'person/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showActors', VSlang(30486), 'actor.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesGeneral():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'movie/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30478), 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'movie/now_playing')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30479), 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'movie/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30480), 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'genre/movie/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreMovie', VSlang(30481), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory(50)

def showSeriesGeneral():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'tv/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', VSlang(30482), 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'tv/on_the_air')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', VSlang(30483), 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'tv/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', VSlang(30484), 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'genre/tv/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreTV', VSlang(30485), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory(50)

def showSearch():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'search/movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', VSlang(30487), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', VSlang(30488), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'search/person')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchActor', VSlang(30489), 'search.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMyTmdb():
    oGui = cGui()
    grab = cTMDb()

    tmdb_session = oConfig.getSetting('tmdb_session')

    if tmdb_session == '':
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'https://')
        oGui.addDir(SITE_IDENTIFIER, 'getToken', VSlang(30305), 'trakt.png', oOutputParameterHandler)
    else :

        #pas de deco possible avec l'api donc on test l'username sinon ont supprime tous
        result = grab.getUrl('account', '1', 'session_id=' + tmdb_session)

        if 'username' in result and result['username']:

            #pas de menu sans ID user c'est con
            oConfig.setSetting('tmdb_account', str(result['id']))

            sUsername = result['username']
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oGui.addText(SITE_IDENTIFIER, (VSlang(30306)) % (sUsername))

            oOutputParameterHandler = cOutputParameterHandler()
            #/account/{account_id}/favorite/movies
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/favorite/movies' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30490), 'films.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            #/account/{account_id}/rated/movies
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/rated/movies' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30491), 'notes.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            #/account/{account_id}/watchlist/movies
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/watchlist/movies' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', VSlang(30492), 'views.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            #/account/{account_id}/favorite/tv
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/favorite/tv' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', VSlang(30493), 'series.png', oOutputParameterHandler)


            oOutputParameterHandler = cOutputParameterHandler()
            #/account/{account_id}/rated/tv
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/rated/tv' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', VSlang(30494), 'notes.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            #/account/{account_id}/watchlist/tv
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/watchlist/tv' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', VSlang(30496), 'views.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            #/account/{account_id}/rated/tv/episodes
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/rated/tv/episodes' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', VSlang(30495), 'notes.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            #/account/{account_id}/lists
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/lists' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showUserLists', VSlang(30497), 'listes.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://')
            oGui.addDir(SITE_IDENTIFIER, 'ouTMyTmdb', VSlang(30309), 'listes.png', oOutputParameterHandler)

        else :

            ouTMyTmdb()

    oGui.setEndOfDirectory()


def ouTMyTmdb():
    oConfig.setSetting('tmdb_session', '')
    oConfig.setSetting('tmdb_account', '')

    VSshowInfo(VSlang(30320))
    VSupdate()
    showMyTmdb()
    return

def getContext():
    tmdb_account = oConfig.getSetting('tmdb_account')

    if tmdb_account == "":
        VSerror(VSlang(30498))
        return False, False, False

    disp = []
    lang = []
    fow = []
    yn  = []

    disp.append('vote')
    fow.append('vote')
    yn.append(True)
    lang.append(VSlang(30443))

    disp.append('account/%s/watchlist' % tmdb_account)
    fow.append('watchlist')
    yn.append(True)
    lang.append(VSlang(30444))

    disp.append('account/%s/favorite' % tmdb_account)
    fow.append('favorite')
    yn.append(True)
    lang.append(VSlang(30445))

    disp.append('account/%s/watchlist' % tmdb_account)
    fow.append('watchlist')
    yn.append(False)
    lang.append(VSlang(30446))

    disp.append('account/%s/favorite' % tmdb_account)
    fow.append('favorite')
    yn.append(False)
    lang.append(VSlang(30447))


    ret = VScreateDialogSelect(lang, 'TMDB')

    if ret > -1:
        return disp[ret], fow[ret], yn[ret]
    return False

def getCat():

    disp = ['1','2']
    dialog_select = 'Films', 'Series'

    ret = VScreateDialogSelect(dialog_select, 'TMDB')

    if ret > -1:
        sType = disp[ret]
    return sType


def getAction():
    grab = cTMDb()
    oInputParameterHandler = cInputParameterHandler()

    sAction= ''
    if not sAction:
        sAction, sFow, sYn = getContext()
    if not sAction:
        return

    sCat = oInputParameterHandler.getValue('sCat')
    if not sCat:
        sCat = getCat()
    if not sCat:
        return

    #dans le doute si meta active
    sTMDB = oInputParameterHandler.getValue('sTmdbId')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sEpisode = oInputParameterHandler.getValue('sEpisode')

    sCat = sCat.replace('1', 'movie').replace('2', 'tv')

    if not sTMDB:
        sTMDB = grab.get_idbyname(oInputParameterHandler.getValue('sFileName'), '', sCat)
    if not sTMDB:
        return


    if sAction == 'vote':
        #vote /movie/{movie_id}/rating
        #/tv/{tv_id}/rating
        numboard = xbmcgui.Dialog().numeric(0, 'Min 0.5 - Max 10')
        if numboard != None:
            sAction = '%s/%s/rating' % (sCat, sTMDB)
            sPost = {"value": numboard}
        else :
            return

    else:

        sPost = {"media_type": sCat, "media_id": sTMDB, sFow: sYn}


    data = grab.getPostUrl(sAction, sPost)

    if len(data) > 0:
        VSshowInfo(data['status_message'])

    return

#comme le cat change pour le type ont refait
def getWatchlist():
    grab = cTMDb()

    tmdb_session = oConfig.getSetting('tmdb_session')
    tmdb_account = oConfig.getSetting('tmdb_account')

    if not tmdb_session:
        return

    if not tmdb_account:
        return

    oInputParameterHandler = cInputParameterHandler()


    sCat = oInputParameterHandler.getValue('sCat')
    if not sCat:
        return

    #dans le doute si meta active
    sTMDB = oInputParameterHandler.getValue('sTmdbId')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sEpisode = oInputParameterHandler.getValue('sEpisode')

    sCat = sCat.replace('1', 'movie').replace('2', 'tv')

    if not sTMDB:
        sTMDB = grab.get_idbyname(oInputParameterHandler.getValue('sFileName'), '', sCat)
    if not sTMDB:
        return

    sPost = {"media_type": sCat, "media_id": sTMDB, 'watchlist': True}
    sAction = 'account/%s/watchlist' % tmdb_account

    data = grab.getPostUrl(sAction, sPost)

    if len(data) > 0:
        VSshowInfo(data['status_message'])

    return

def getToken():
    grab = cTMDb()
    return grab.getToken()

def showSearchMovie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        #oGui.setEndOfDirectory()
        return

def showSearchSerie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showSeries(sSearchText)
        #oGui.setEndOfDirectory()
        return

def showSearchActor():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showActors(sSearchText)
        #oGui.setEndOfDirectory()
        return

def showGenreMovie():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl(sUrl)

    total = len(result)
    if (total > 0):
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            sTitle = sTitle.encode("utf-8")
            sUrl = 'genre/' + str(sId) + '/movies'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(sTitle), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenreTV():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    result = grab.getUrl(sUrl)

    total = len(result)
    if (total > 0):
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            sTitle = sTitle.encode("utf-8")
            #sUrl = API_URL + '/genre/' + str(sId) + '/tv'
            sUrl = 'discover/tv'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('genre', sId)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showUserLists():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if (oInputParameterHandler.exist('session_id')):
        term += 'session_id=' +  oInputParameterHandler.getValue('session_id')

    sUrl = oInputParameterHandler.getValue('siteUrl')
    result = grab.getUrl(sUrl, iPage, term)

    total = len(result)
    if (total > 0):
        for i in result['results']:
            sId, sTitle = i['id'], i['name']

            #sUrl = API_URL + '/genre/' + str(sId) + '/tv'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sId)
            oGui.addDir(SITE_IDENTIFIER, 'showLists', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showFolderList():
    oGui = cGui()
    liste = []
    liste.append( ['Top Manga', '31665'] )
    liste.append( ['Top Manga 2', '31695'] )
    liste.append( ['Disney Classic', '338'] )
    liste.append( ['Pixar', '3700'] )
    liste.append( ['Top 50 des plus grands films', '10'] )
    liste.append( ['Marvel', '1'] )
    liste.append( ['DC Comics Universe', '3'] )
    liste.append( ['Les films fascinants ', '43'] )
    liste.append( ['Gagnants des Oscars', '31670'] )
    liste.append( ['Les adaptations', '9883'] )
    liste.append( ['science-fiction', '3945'] )
    liste.append( ['Best séries', '36788'] )
    liste.append( ['Films de Noel', '40944'] )
    #liste.append( ['nom de la liste', 'ID de la liste'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showLists', sTitle, 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    grab = cTMDb()

    POSTER_URL = 'https://image.tmdb.org/t/p/' + 'w342' #possible values: w92|w154|w185|w342|w500|w780|original
    FANART_URL = 'https://image.tmdb.org/t/p/' + 'w1280' #possible values: w300|w780|w1280|original

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')

    if (oInputParameterHandler.exist('sSearch')):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/movie', iPage, 'query=' + sSearch)
        sUrl = ''

    else:

        if (oInputParameterHandler.exist('session_id')):
            term += 'session_id=' +  oInputParameterHandler.getValue('session_id')

        sUrl = oInputParameterHandler.getValue('siteUrl')
        result = grab.getUrl(sUrl, iPage, term)
        #result = grab.getUrl(sUrl, iPage)


    total = len(result)
    if (total > 0):
        total = len(result['results'])
        progress_ = oConfig.createDialog(SITE_NAME)

        for i in result['results']:
            oConfig.updateDialog(progress_, total)
            if progress_.iscanceled():
                break

            sId, sTitle, sOtitle, sThumb, sFanart, sDesc = i['id'], i['title'], i['original_title'], i['poster_path'], i['backdrop_path'], i['overview']
            if sThumb:
                sThumb = POSTER_URL + sThumb
            else:
                sThumb = ''

            sTitle = sTitle.encode("utf-8")
            if sFanart:
                sFanart = FANART_URL + sFanart
            else :
                sFanart = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://tmdb/%s' % sId)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sTmdbId', sId)
            oOutputParameterHandler.addParameter('type', 'film')
            oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

            #oGui.addMovieDB('globalSearch', 'showHosters', sTitle, 'films.png', sThumb, sFanart, oOutputParameterHandler)
            cGui.CONTENT = "movies"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sTitle)
            oGuiElement.setIcon('films.png')
            oGuiElement.setMeta(1)
            oGuiElement.setMetaAddon('true')
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(1)
            oGuiElement.setDescription(sDesc)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oConfig.finishDialog(progress_)

        if (iPage > 0):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            if sSearch:
                oOutputParameterHandler.addParameter('sSearch', sSearch)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + str(iNextPage) + ' >>>[/COLOR]', oOutputParameterHandler)


    #chnagement mode
    oGui.setEndOfDirectory(500)



def showSeries(sSearch=''):
    grab = cTMDb()

    POSTER_URL = 'https://image.tmdb.org/t/p/' + 'w342' #possible values: w92|w154|w185|w342|w500|w780|original
    FANART_URL = 'https://image.tmdb.org/t/p/' + 'w1280' #possible values: w300|w780|w1280|original

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')

    if (oInputParameterHandler.exist('sSearch')):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/tv', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        if (oInputParameterHandler.exist('genre')):
            term = 'with_genres=' +  oInputParameterHandler.getValue('genre')

        if (oInputParameterHandler.exist('session_id')):
            term += 'session_id=' +  oInputParameterHandler.getValue('session_id')

        result = grab.getUrl(sUrl, iPage, term)

    oGui = cGui()

    total = len(result)

    if (total > 0):
        total = len(result['results'])
        progress_ = oConfig.createDialog(SITE_NAME)

        for i in result['results']:
            oConfig.updateDialog(progress_, total)
            if progress_.iscanceled():
                break

            sId, sTitle, sOtitle, sThumb, sFanart, sDesc = i['id'], i['name'], i['original_name'], i['poster_path'], i['backdrop_path'], i['overview']
            if sThumb:
                sThumb = POSTER_URL + sThumb
            else:
                sThumb = ''

            if sFanart:
                sFanart = FANART_URL + sFanart
            else :
                sFanart = ''

            sTitle = sTitle.encode("utf-8")

            sSiteUrl = 'tv/' + str(sId)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sFanart', sFanart)
            oOutputParameterHandler.addParameter('sTmdbId', sId)
            #oOutputParameterHandler.addParameter('searchtext', sTitle)
            oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))


            #oGui.addTVDB(SITE_IDENTIFIER, 'showSeriesSaison', sTitle, 'series.png', sThumb, sFanart, oOutputParameterHandler)

            cGui.CONTENT = "tvshows"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName(SITE_IDENTIFIER) # a activer pour  saisons
            #oGuiElement.setSiteName('globalSearch') # a desactiver pour saison
            oGuiElement.setFunction('showSeriesSaison')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sTitle)
            oGuiElement.setIcon('series.png')
            oGuiElement.setMeta(2)
            oGuiElement.setMetaAddon('true')
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(2)
            oGuiElement.setDescription(sDesc)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oConfig.finishDialog(progress_)

        if (iPage > 0):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            if sSearch:
                oOutputParameterHandler.addParameter('sSearch', sSearch)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            if (oInputParameterHandler.exist('genre')):
                oOutputParameterHandler.addParameter('genre', oInputParameterHandler.getValue('genre'))
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Page ' + str(iNextPage) + ' >>>[/COLOR]', oOutputParameterHandler)

    #chnagement mode
    oGui.setEndOfDirectory(500)

def showSeriesSaison():
    oGui = cGui()
    grab = cTMDb()

    POSTER_URL = 'https://image.tmdb.org/t/p/' + 'w342' #possible values: w92|w154|w185|w342|w500|w780|original
    FANART_URL = 'https://image.tmdb.org/t/p/' + 'w1280' #possible values: w300|w780|w1280|original

    oInputParameterHandler = cInputParameterHandler()

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')

    sId = oInputParameterHandler.getValue('sId')
    if sId == False:
        sId = sUrl.split('/')[-1]

    if sFanart == False:
        sFanart = ''


    #recherche la serie complete
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sMovieTitle)
    #oOutputParameterHandler.addParameter('type', 'serie')
    #oOutputParameterHandler.addParameter('searchtext', sMovieTitle)
    oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sMovieTitle))

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName('globalSearch')
    oGuiElement.setFunction('searchMovie')
    oGuiElement.setTitle(VSlang(30414))
    oGuiElement.setCat(2)
    oGuiElement.setIcon("searchtmdb.png")
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    #oGui.addDir('cHome', 'showSearch', VSlang(30414), 'searchtmdb.png', oOutputParameterHandler)
    #fin

    result = grab.getUrl(sUrl)

    total = len(result)

    if (total > 0):

        total = len(result['seasons'])
        progress_ = oConfig.createDialog(SITE_NAME)

        for i in result['seasons']:
            oConfig.updateDialog(progress_, total)
            if progress_.iscanceled():
                break

            sdate, sNbreEp, sIdSeason, sThumb, SSeasonNum = i['air_date'], i['episode_count'], i['id'], i['poster_path'], i['season_number']

            if sThumb:
                sThumb = POSTER_URL + sThumb
            else:
                sThumb = ''

            sTitle = 'Saison ' + str(SSeasonNum) + ' (' + str(sNbreEp) + ')'

            sUrl = 'tv/' + sId + '/season/' + str(SSeasonNum)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sSeason', SSeasonNum)
            oOutputParameterHandler.addParameter('sFanart', sFanart)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)


            #oGui.addTVDB(SITE_IDENTIFIER, 'showSeriesEpisode', sTitle, 'series.png', sThumb, sFanart, oOutputParameterHandler)

            cGui.CONTENT = "tvshows"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sTmdbId)
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showSeriesEpisode')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sMovieTitle)
            oGuiElement.setIcon('series.png')
            oGuiElement.setMeta(2)
            oGuiElement.setMetaAddon('true')
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(7)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oConfig.finishDialog(progress_)

    #chnagement mode
    oGui.setEndOfDirectory(500)

def showSeriesEpisode():
    grab = cTMDb()

    POSTER_URL = 'https://image.tmdb.org/t/p/' + 'w342' #possible values: w92|w154|w185|w342|w500|w780|original
    FANART_URL = 'https://image.tmdb.org/t/p/' + 'w1280' #possible values: w300|w780|w1280|original

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')

    sSeason = oInputParameterHandler.getValue('sSeason')
    #sId = oInputParameterHandler.getValue('sId')
    if sSeason == False:
        sSeason = sUrl.split('/')[-1]

    if sFanart == False:
        sFanart = ''

    oGui = cGui()

    #recherche saison complete
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sMovieTitle)
    #oOutputParameterHandler.addParameter('type', 'serie')
    search = '%s S%02d' % (sMovieTitle, int(sSeason))
    #oOutputParameterHandler.addParameter('searchtext', search)
    oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(search))


    oGuiElement = cGuiElement()
    oGuiElement.setSiteName('globalSearch')
    oGuiElement.setFunction('searchMovie')
    oGuiElement.setTitle(VSlang(30415))
    oGuiElement.setCat(2)
    oGuiElement.setIcon("searchtmdb.png")
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    #oGui.addDir('cHome', 'showSearch', VSlang(30415), 'searchtmdb.png', oOutputParameterHandler)
    #fin

    result = grab.getUrl(sUrl)

    total = len(result)
    if (total > 0):
        total = len(result['episodes'])
        progress_ = oConfig.createDialog(SITE_NAME)

        for i in result['episodes']:
            oConfig.updateDialog(progress_, total)
            if progress_.iscanceled():
                break

            #sId, sTitle, sOtitle, sThumb, sFanart = i['id'], i['name'], i['original_name'], i['poster_path'], i['backdrop_path']
            sdate, sIdEp, sEpNumber, sName, sThumb, SResume = i['air_date'], i['id'], i['episode_number'], i['name'], i['still_path'], i['overview']

            sName = sName.encode("utf-8")
            if sName == '':
                sName = sMovieTitle

            if sThumb:
                sThumb = POSTER_URL + sThumb
            else:
                sThumb = ''

            #sTitle = '[COLOR coral]S' + sSeason + 'E' + str(sEpNumber) + '[/COLOR] - ' + sName
            sTitle = 'S%s E%s %s' % (sSeason, str(sEpNumber) , sName)

            sExtraTitle = ' S' + "%02d" % int(sSeason) + 'E' + "%02d" % int(sEpNumber)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sMovieTitle + '|' + sExtraTitle) #Pour compatibilite Favoris
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
            oOutputParameterHandler.addParameter('sSeason', sSeason)
            oOutputParameterHandler.addParameter('sEpisode', sEpNumber)
            oOutputParameterHandler.addParameter('type', 'serie')
            oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sMovieTitle))

            #oGui.addTVDB('globalSearch', 'showHosters', sTitle, 'series.png', sThumb, sFanart, oOutputParameterHandler)

            cGui.CONTENT = "tvshows"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sTmdbId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sMovieTitle)
            oGuiElement.setIcon('series.png')
            oGuiElement.setMeta(2)
            oGuiElement.setMetaAddon('true')
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(2)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oConfig.finishDialog(progress_)

    #tchnagement mode
    oGui.setEndOfDirectory(500)

def showActors(sSearch = ''):
    oGui = cGui()
    grab = cTMDb()

    POSTER_URL = 'https://image.tmdb.org/t/p/' + 'w342' #possible values: w92|w154|w185|w342|w500|w780|original
    FANART_URL = 'https://image.tmdb.org/t/p/' + 'w1280' #possible values: w300|w780|w1280|original

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')

    if (oInputParameterHandler.exist('sSearch')):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        #format obligatoire evite de modif le format de l'url dans la lib >> _call
        #a cause d'un ? pas ou il faut pour ça >> invalid api key
        result = grab.getUrl(sUrl,iPage,'query=' + sSearch)

    else:
        result = grab.getUrl(sUrl, iPage)

    total = len(result)

    if (total > 0):
        total = len(result['results'])
        progress_ = oConfig.createDialog(SITE_NAME)

        #récup le nombre de page pour NextPage
        nbrpage = result['total_pages']

        for i in result['results']:
            oConfig.updateDialog(progress_, total)
            if progress_.iscanceled():
                break

            sName, sThumb = i['name'], i['profile_path']

            if sThumb:
                sThumb = POSTER_URL + sThumb
            else:
                sThumb = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            sName = sName.encode('utf-8')

            oOutputParameterHandler.addParameter('siteUrl', 'person/' + str(i['id']) + '/movie_credits')
            #oGui.addMovieDB(SITE_IDENTIFIER, 'showFilmActor', '[COLOR red]'+str(sName)+'[/COLOR]', '', sThumb, '', oOutputParameterHandler)
            sTitle = '[COLOR red]' + str(sName) + '[/COLOR]'

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showFilmActor')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sName)
            oGuiElement.setIcon('actors.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setCat(7)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oConfig.finishDialog(progress_)

        if (int(iPage) < int(nbrpage)):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()

            #ajoute param sSearch pour garder le bon format d'url avec grab url
            if sSearch:
                oOutputParameterHandler.addParameter('sSearch', sSearch)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showActors', '[COLOR teal]Page ' + str(iNextPage) + ' >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory(500)

def showFilmActor():
    oGui = cGui()
    grab = cTMDb()

    POSTER_URL = 'https://image.tmdb.org/t/p/' + 'w342' #possible values: w92|w154|w185|w342|w500|w780|original
    FANART_URL = 'https://image.tmdb.org/t/p/' + 'w1280' #possible values: w300|w780|w1280|original

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')

    result = grab.getUrl(sUrl, iPage)

    total = len(result)
    if (total > 0):
        total = len(result['cast'])
        progress_ = oConfig.createDialog(SITE_NAME)

        for i in result['cast']:
            oConfig.updateDialog(progress_, total)
            if progress_.iscanceled():
                break


            sId, sTitle, sThumb, sFanart, sDesc = i['id'], i['title'], i['poster_path'], i['backdrop_path'], i['overview']


            try:
                #sTitle = unicodedata.normalize('NFKD', sTitle).encode('ascii', 'ignore')
                sTitle = sTitle.encode("utf-8")

            except: sTitle = "Aucune information"

            try:
                sThumb = POSTER_URL + sThumb
            except:
                sThumb = ''

            try:
                sFanart = FANART_URL + sFanart
            except :
                sFanart = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://tmdb/%s' % sId)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sTmdbId', sId)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('type', 'film')
            oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

            #oGui.addMovieDB('globalSearch', 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
            cGui.CONTENT = "movies"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sTitle)
            oGuiElement.setIcon('actors.png')
            oGuiElement.setMeta(1)
            oGuiElement.setMetaAddon('true')
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(1)
            oGuiElement.setDescription(sDesc)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oConfig.finishDialog(progress_)
         #pas de paramettre de page
        # if (iPage > 0):
            # iNextPage = int(iPage) + 1
            # oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', sUrl)
            # oOutputParameterHandler.addParameter('page', iNextPage)
            # oGui.addDir(SITE_IDENTIFIER, 'showFilmActor', '[COLOR teal]Page ' + str(iNextPage) + ' >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory(500)


def showLists():
    grab = cTMDb()

    POSTER_URL = 'https://image.tmdb.org/t/p/' + 'w342' #possible values: w92|w154|w185|w342|w500|w780|original
    FANART_URL = 'https://image.tmdb.org/t/p/' + 'w1280' #possible values: w300|w780|w1280|original

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')

    sUrl = oInputParameterHandler.getValue('siteUrl')


    result = grab.getUrl('list/' + sUrl, iPage, '')

    oGui = cGui()

    total = len(result)

    if (total > 0):
        total = len(result['items'])
        progress_ = oConfig.createDialog(SITE_NAME)

        for i in result['items']:
            oConfig.updateDialog(progress_, total)
            if progress_.iscanceled():
                break

            sId, sType, sThumb, sFanart, sVote, sDesc = i['id'], i['media_type'], i['poster_path'], i['backdrop_path'], i['vote_average'], i['overview']

            if sThumb:
                sThumb = POSTER_URL + sThumb
            else:
                sThumb = ''

            if sFanart:
                sFanart = FANART_URL + sFanart
            else :
                sFanart = ''

            sTitle = "None"

            if 'name' in i:
                sTitle = i['name'].encode("utf-8")
            if 'title' in i:
                sTitle = i['title'].encode("utf-8")

            sDisplayTitle = "%s (%s)" % (sTitle, sVote)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://tmdb/%s' % sId)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sFanart', sFanart)
            oOutputParameterHandler.addParameter('sTmdbId', sId)
            #oOutputParameterHandler.addParameter('searchtext', sTitle)
            oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

            #oGui.addTVDB(SITE_IDENTIFIER, 'showSeriesSaison', sTitle, 'series.png', sThumb, sFanart, oOutputParameterHandler)

            cGui.CONTENT = "movies"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sDisplayTitle)
            oGuiElement.setFileName(sTitle)
            oGuiElement.setIcon('series.png')
            if sType == 'movie':
                oGuiElement.setMeta(1)
                oGuiElement.setCat(1)
            elif sType == 'tv':
                oGuiElement.setMeta(2)
                oGuiElement.setCat(2)
            oGuiElement.setMetaAddon('true')
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setDescription(sDesc)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oConfig.finishDialog(progress_)

    oGui.setEndOfDirectory(500)


def __checkForNextPage(sHtmlContent):
    sPattern = "<span class='page-numbers current'>.+?</span><a class='page-numbers' href='([^<]+)'>.+?</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
