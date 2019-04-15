#-*- coding: utf-8 -*-
#Primatech.
from resources.lib.config import cConfig
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.ftpmanager import cFtpManager
from resources.lib.util import VSlog, ReadSingleDatabase, WriteSingleDatabase

import StorageServer
import os, sys
import urllib
import xbmc
import base64

SITE_IDENTIFIER = 'cDb'
SITE_NAME = 'DB'

try:
    from sqlite3 import dbapi2 as sqlite
    VSlog('SQLITE 3 as DB engine')
except:
    from pysqlite2 import dbapi2 as sqlite
    VSlog('SQLITE 2 as DB engine')

class cDb:
    def __init__(self, ftp = True):
        self.oConfig = cConfig()
        self.enableFtp = ftp
        try:
            if self.enableFtp:
                self.ftp = cFtpManager()
                VSlog("Retrieve DB from server")
                self.ftp.getDb()
            DB = self.oConfig.getFileDB()
            self.db = sqlite.connect(DB)
            self.dbcur = self.db.cursor()
        except Exception, e:
            VSlog('cDb ERROR in Constructor: ' + str(e.message))

    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.db.close()
            if self.enableFtp:
                VSlog("sendDb to server")
                self.ftp.sendDb()
                self.ftp.quit()
        except Exception, e:
            VSlog('cDb ERROR in Destructor: ' + str(e.message))

    def lockDB(self):
        if ReadSingleDatabase("dbLock") == "Locked":
            raise Exception('DB is already locked')

    def unlockDB(self):
        WriteSingleDatabase("dbLock", "Unlocked")

    def createTables(self):
        # self.dropTables()
        try:
            self.lockDB()
            ''' Create table '''
            sql_create = "CREATE TABLE IF NOT EXISTS history ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""sItemUrl TEXT, ""mainUrl TEST, ""rawtitle TEXT, ""title TEXT, ""icon TEXT, ""type TEXT, ""quality TEXT, ""UNIQUE(rawtitle)"");"
            self.dbcur.execute(sql_create)

            sql_create = "CREATE TABLE IF NOT EXISTS resume ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""timepoint TEXT, ""UNIQUE(title)"");"
            self.dbcur.execute(sql_create)

            sql_create = "CREATE TABLE IF NOT EXISTS watched ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""site TEXT, ""UNIQUE(title, site)"");"
            self.dbcur.execute(sql_create)

            sql_create = "CREATE TABLE IF NOT EXISTS favorite ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""siteurl TEXT, ""site TEXT, ""fav TEXT, ""cat TEXT, ""icon TEXT, ""fanart TEXT, ""UNIQUE(title, site)"");"
            self.dbcur.execute(sql_create)

            sql_create = "CREATE TABLE IF NOT EXISTS download2 ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""path TEXT, ""icon TEXT, ""status TEXT, ""mainUrl TEXT, ""UNIQUE(title)"");"
            self.dbcur.execute(sql_create)

            sql_create = "CREATE TABLE IF NOT EXISTS valide ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""url TEXT, ""ok TEXT, ""UNIQUE(url)"");"
            self.dbcur.execute(sql_create)

            VSlog('Table initialized')

            self.unlockDB()

        except Exception, e:
            VSlog('cDb ERROR in createTables: ' + str(e.message))

    def dropTables(self):
        try:
            self.lockDB()
            self.dbcur.execute("DROP TABLE IF EXISTS %s" %('history'))
            self.dbcur.execute("DROP TABLE IF EXISTS %s" %('resume'))
            self.dbcur.execute("DROP TABLE IF EXISTS %s" %('watched'))
            self.dbcur.execute("DROP TABLE IF EXISTS %s" %('favorite'))
            self.dbcur.execute("DROP TABLE IF EXISTS %s" %('downloaded'))
            self.dbcur.execute("DROP TABLE IF EXISTS %s" %('valide'))
            VSlog('Tables dropped successfully')
            self.unlockDB()
        except:
            VSlog("deleteTable FAIL")

    #Ne pas utiliser cette fonction pour les chemins
    # def str_conv2(self, data):
    #     if isinstance(data, str):
    #         # Must be encoded in UTF-8
    #         data = data.decode('utf8')
    #     import unicodedata
    #     data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
    #     data = data.decode('string-escape') #ATTENTION : provoque des bugs pour les chemins a cause du caractere '/'
    #     return data

    def str_conv(self, data):
        data = data.rstrip()
        data = base64.b16encode(data)
        return data

    def str_deconv(self, data):
        data = base64.b16decode(data)
        data = data.rstrip()
        return data

    #***********************************
    #   Resume fonctions
    #***********************************

    def insert_resume(self, meta):
        title = self.str_conv(meta['title'])
        timepoint = meta['timepoint']
        try:
            self.lockDB()
            ex = "INSERT INTO resume (title, timepoint) VALUES (?, ?)"
            self.dbcur.execute(ex, (title, timepoint))
            self.db.commit()
            VSlog('SQL INSERT resume Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR INSERT resume: ' + str(e.message))
            if 'UNIQUE constraint failed' in str(e.message):
                self.update_resume(meta)

    def update_resume(self, meta):
        title = self.str_conv(meta['title'])
        timepoint = meta['timepoint']
        try:
            self.lockDB()
            ex = "UPDATE resume SET timepoint = '%s' WHERE title = '%s'" % (timepoint, title)
            self.dbcur.execute(ex)
            self.db.commit()
            VSlog('SQL UPDATE resume Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR UPDATE resume: ' + str(e.message))

    def get_resume(self, meta):
        title = self.str_conv(meta['title'])
        sql_select = "SELECT * FROM resume WHERE title = '%s'" % (title)
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.unlockDB()
            if not matchedrow:
                matchedrow = []
            return matchedrow
        except Exception, e:
            VSlog('SQL ERROR EXECUTE resume: ' + str(e.message))
            return []

    def del_resume(self, title):
        title = self.str_conv(title)
        sql_delete = "DELETE FROM resume WHERE title = '%s'" % (title)
        try:
            self.lockDB()
            self.dbcur.execute(sql_delete)
            self.db.commit()
            VSlog('SQL DELETE resume Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR DELETE resume: ' + str(e.message))

    #***********************************
    #   Watched fonctions
    #***********************************

    def insert_watched(self, meta):
        title = self.str_conv(meta['title'])
        site = urllib.quote_plus(meta['site'])
        ex = "INSERT INTO watched (title, site) VALUES (?, ?)"
        try:
            self.lockDB()
            self.dbcur.execute(ex, (title,site))
            self.db.commit()
            VSlog('SQL INSERT watched Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR INSERT watched: ' + str(e.message))

    def get_watched(self, meta):
        count = 0
        site = urllib.quote_plus(meta['site'])
        sql_select = "SELECT * FROM watched WHERE site = '%s'" % (site)
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.unlockDB()
            if matchedrow:
                count = 1
            return count
        except Exception, e:
            VSlog('SQL ERROR EXECUTE watched: ' + str(e.message))
            return None

    def del_watched(self, meta):
        site = urllib.quote_plus(meta['site'])
        sql_select = "DELETE FROM watched WHERE site = '%s'" % (site)
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            self.db.commit()
            self.unlockDB()
            return False, False
        except Exception, e:
            VSlog('SQL ERROR DELETE watched: ' + str(e.message))
            return False, False

    #***********************************
    #   Favoris fonctions
    #***********************************

    def insert_favorite(self, meta):
        title = self.str_conv(meta['title'])
        VSlog(meta['siteurl'])
        siteurl = urllib.quote_plus(meta['siteurl'])
        sIcon = meta['icon']
        try:
            self.lockDB()
            ex = "INSERT INTO favorite (title, siteurl, site, fav, cat, icon, fanart) VALUES (?, ?, ?, ?, ?, ?, ?)"
            self.dbcur.execute(ex, (title,siteurl, meta['site'],meta['fav'],meta['cat'],sIcon,meta['fanart']))
            self.db.commit()
            VSlog('SQL INSERT favorite Successfully')
            self.oConfig.showInfo(meta['title'], 'Enregistré avec succés')
            self.unlockDB()
        except Exception, e:
            if 'UNIQUE constraint failed' in str(e.message):
                self.oConfig.showInfo(meta['title'], 'Item déjà présent dans votre Liste')
            VSlog('SQL ERROR INSERT favorite: ' + str(e.message))
            pass

    def get_favorite(self):
        sql_select = "SELECT * FROM favorite"
        matchedrow = []
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.unlockDB()
            if not matchedrow:
                matchedrow = []
        except Exception, e:
            VSlog('SQL ERROR EXECUTE favorite: ' + str(e.message))
        return matchedrow


    def del_favorite(self):
        oInputParameterHandler = cInputParameterHandler()
        if (oInputParameterHandler.exist('sCat')):
            sql_delete = "DELETE FROM favorite WHERE cat = '%s'" % (oInputParameterHandler.getValue('sCat'))

        if(oInputParameterHandler.exist('sMovieTitle')):
            siteUrl = oInputParameterHandler.getValue('siteUrl')
            sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
            siteUrl = urllib.quote_plus(siteUrl)
            title = self.str_conv(sMovieTitle)
            title = title.replace("'", r"''")
            sql_delete = "DELETE FROM favorite WHERE siteurl = '%s' AND title = '%s'" % (siteUrl,title)

        if(oInputParameterHandler.exist('sAll')):
            sql_delete = "DELETE FROM favorite;"

        try:
            self.lockDB()
            self.dbcur.execute(sql_delete)
            self.db.commit()
            self.oConfig.showInfo('TvWatch', 'Favoris supprimé')
            self.unlockDB()
            return False, False
        except Exception, e:
            VSlog('SQL ERROR EXECUTE favorite: ' + str(e.message))
            return False, False

    def writeFavourites(self):
        oInputParameterHandler = cInputParameterHandler()
        sTitle = oInputParameterHandler.getValue('sTitle')
        sId = oInputParameterHandler.getValue('sId')
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sFav = oInputParameterHandler.getValue('sFav')

        if (oInputParameterHandler.exist('sCat')):
            sCat = oInputParameterHandler.getValue('sCat')
        else:
            sCat = '5'

        sUrl = urllib.quote_plus(sUrl)
        fav_db = self.__sFile
        watched = {}
        if not os.path.exists(fav_db):
            file(fav_db, "w").write("%r" % watched)

        if os.path.exists(fav_db):
            watched = eval(open(fav_db).read() )
            watched[sUrl] = watched.get(sUrl) or []

            #add to watched
            if not watched[sUrl]:
                #list = [sFav, sUrl];
                watched[sUrl].append(sFav)
                watched[sUrl].append(sId)
                watched[sUrl].append(sTitle)
                watched[sUrl].append(sCat)
            else:
                watched[sUrl][0] = sFav
                watched[sUrl][1] = sId
                watched[sUrl][2] = sTitle
                watched[sUrl][3] = sCat

        file(fav_db, "w").write("%r" % watched)
        self.oConfig.showInfo('Marque-Page', sTitle)

    #***********************************
    #   history fonctions
    #***********************************

    def insert_history(self, meta):
        title = meta['title']
        sItemUrl = meta['sItemUrl']
        sMainUrl = meta['mainUrl']
        sIcon = meta['icon']
        sType = meta['type']
        sQuality = meta['quality']
        sRawtitle = title
        title = self.str_conv(title)
        if sType == 'tvshow' and 'Saison' in sRawtitle:
            sRawtitle = sRawtitle[:sRawtitle.find('Saison')]
        sRawtitle = self.str_conv(sRawtitle)
        try:
            self.lockDB()
            ex = "INSERT INTO history (title, sItemUrl, mainUrl, icon, type, rawtitle, quality) VALUES (?, ?, ?, ?, ?, ?, ?)"
            self.dbcur.execute(ex, (title, sItemUrl, sMainUrl, sIcon, sType, sRawtitle, sQuality))
            self.db.commit()
            VSlog('SQL INSERT history Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR INSERT history: ' + str(e.message))
            if 'UNIQUE constraint failed' in str(e.message):
                self.update_history(meta)

    def update_history(self, meta):
        title = meta['title']
        sItemUrl = meta['sItemUrl']
        sMainUrl = meta['mainUrl']
        sIcon = meta['icon']
        sType = meta['type']
        sQuality = meta['quality']
        sRawtitle = title
        title = self.str_conv(title)
        if sType == 'tvshow' and 'Saison' in sRawtitle:
            sRawtitle = sRawtitle[:sRawtitle.find('Saison')]
        sRawtitle = self.str_conv(sRawtitle)
        try:
            self.lockDB()
            ex = "UPDATE history SET title='%s', sItemUrl='%s', mainUrl='%s', type='%s', icon='%s', quality='%s' WHERE rawtitle='%s'" \
            % (title, sItemUrl, sMainUrl, sType, sIcon, sQuality, sRawtitle)
            self.dbcur.execute(ex)
            self.db.commit()
            VSlog('SQL UPDATE history Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL UPDATE history: ' + str(e.message))


    def get_history(self):
        sql_select = "SELECT * FROM history"
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.unlockDB()
            if not matchedrow:
                matchedrow = []
            return matchedrow
        except Exception, e:
            VSlog('SQL ERROR GET history: ' + str(e.message))
            return []

    def get_historyFromTitle(self, title):
        sRawtitle = title
        if 'Saison' in title:
            sRawtitle = title[:title.find('Saison')]
        sRawtitle = self.str_conv(sRawtitle)
        sql_select = "SELECT * FROM history WHERE rawtitle = '%s'" % (sRawtitle)
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchone()
            self.unlockDB()
            if not matchedrow:
                matchedrow = []
            return matchedrow
        except Exception, e:
            VSlog('SQL ERROR GET history: ' + str(e.message))
            return []

    def del_history(self, title):
        sRawtitle = title
        if 'Saison' in title:
            sRawtitle = title[:title.find('Saison')]
        sRawtitle = self.str_conv(sRawtitle)
        sql_delete = "DELETE FROM history WHERE rawtitle = '%s'" % (sRawtitle)
        try:
            self.lockDB()
            self.dbcur.execute(sql_delete)
            self.db.commit()
            VSlog('SQL DELETE history Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR DELETE history: ' + str(e.message))

    #***********************************
    #   valide fonctions
    #***********************************

    def insert_valide(self, url, ok):
        if '?wmsAuthSign' in url:
            url = url[:url.find('?wmsAuthSign')]
        # url = urllib.quote_plus(url)
        try:
            self.lockDB()
            ex = "INSERT INTO valide (url, ok) VALUES (?, ?)"
            self.dbcur.execute(ex, (url,ok))
            self.db.commit()
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR INSERT valide: ' + str(e.message))

    def get_valideFromUrl(self, url):
        if '?wmsAuthSign' in url:
            url = url[:url.find('?wmsAuthSign')]
        # url = urllib.quote_plus(url)
        sql_select = "SELECT * FROM valide WHERE url = '%s'" % (url)
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchone()
            self.unlockDB()
            return matchedrow
        except Exception, e:
            VSlog('SQL ERROR GET valide: ' + str(e.message))
            return None

    def get_valide(self):
        sql_select = "SELECT * FROM valide"
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.unlockDB()
            return matchedrow
        except Exception, e:
            VSlog('SQL ERROR GET valide: ' + str(e.message))
            return None

    def del_valide(self):
        sql_delete = "DELETE FROM valide"
        try:
            self.lockDB()
            self.dbcur.execute(sql_delete)
            self.db.commit()
            VSlog('SQL DELETE valide Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR valide history: ' + str(e.message))

    #***********************************
    #   downloaded fonctions
    #***********************************

    def insert_download(self, meta):
        mainUrl = meta['sMainUrl']
        title = meta['title']
        path = meta['path']
        sIcon = meta['icon']
        status = meta['status']
        # sRawtitle = title
        title = self.str_conv(title)
        path = self.str_conv(path)
        # if sType == 'tvshow' and 'Saison' in sRawtitle:
        #     sRawtitle = sRawtitle[:sRawtitle.find('Saison')]
        # sRawtitle = self.str_conv(sRawtitle)
        try:
            self.lockDB()
            ex = "INSERT INTO downloaded (title, path, icon, status, mainUrl) VALUES (?, ?, ?, ?, ?)"
            self.dbcur.execute(ex, (title, path, sIcon, status, mainUrl))
            self.db.commit()
            VSlog('SQL INSERT downloaded Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR INSERT downloaded: ' + str(e.message))
            if 'UNIQUE constraint failed' in str(e.message):
                self.update_download(meta)

    def update_download(self, meta):
        mainUrl = meta['sMainUrl']
        title = meta['title']
        path = meta['path']
        sIcon = meta['icon']
        status = meta['status']
        # sRawtitle = title
        title = self.str_conv(title)
        path = self.str_conv(path)
        # if sType == 'tvshow' and 'Saison' in sRawtitle:
        #     sRawtitle = sRawtitle[:sRawtitle.find('Saison')]
        # sRawtitle = self.str_conv(sRawtitle)
        try:
            self.lockDB()
            ex = "UPDATE downloaded SET icon='%s', status='%s', mainUrl='%s' WHERE title='%s' AND path='%s'" % (sIcon, status, mainUrl, title, path)
            self.dbcur.execute(ex)
            self.db.commit()
            VSlog('SQL UPDATE downloaded Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL UPDATE downloaded: ' + str(e.message))


    def get_download(self):
        sql_select = "SELECT * FROM downloaded"
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.unlockDB()
            if not matchedrow:
                matchedrow = []
            return matchedrow
        except Exception, e:
            VSlog('SQL ERROR GET downloaded: ' + str(e.message))
            return []

    def get_downloadFromTitle(self, title):
        # sRawtitle = title
        # if 'Saison' in title:
        #     sRawtitle = title[:title.find('Saison')]
        title = self.str_conv(title)
        sql_select = "SELECT * FROM downloaded WHERE title = '%s'" % (title)
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchone()
            self.unlockDB()
            if not matchedrow:
                matchedrow = []
            return matchedrow
        except Exception, e:
            VSlog('SQL ERROR GET downloaded: ' + str(e.message))
            return []

    def get_downloadFromStatus(self, status):
        sql_select = "SELECT * FROM downloaded WHERE status = '%s'" % (status)
        try:
            self.lockDB()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchone()
            self.unlockDB()
            if not matchedrow:
                matchedrow = []
            return matchedrow
        except Exception, e:
            VSlog('SQL ERROR GET downloaded: ' + str(e.message))
            return []

    def del_downloadByStatus(self, status):
        sql_delete = "DELETE FROM downloaded WHERE status = '%s'" % (status)
        try:
            self.lockDB()
            self.dbcur.execute(sql_delete)
            self.db.commit()
            VSlog('SQL DELETE downloaded Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR DELETE downloaded: ' + str(e.message))

    def del_download(self, title):
        # sRawtitle = title
        # if 'Saison' in title:
        #     sRawtitle = title[:title.find('Saison')]
        title = self.str_conv(title)
        sql_delete = "DELETE FROM downloaded WHERE title = '%s'" % (title)
        try:
            self.lockDB()
            self.dbcur.execute(sql_delete)
            self.db.commit()
            VSlog('SQL DELETE downloaded Successfully')
            self.unlockDB()
        except Exception, e:
            VSlog('SQL ERROR DELETE downloaded: ' + str(e.message))
