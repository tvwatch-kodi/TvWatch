#-*- coding: utf-8 -*-

import mysql.connector
from resources.lib.util import VSlog, uc

SITE_IDENTIFIER = 'cMySqlDB'
SITE_NAME = 'MySqlDB'

class cMySqlDB:

    def __init__(self):
        try:
            self.db = mysql.connector.connect(host=uc("c3FsMTEuZnJlZW15c3FsaG9zdGluZy5uZXQ="), \
                                              user=uc("c3FsMTEyMTc1NjE="), \
                                              password=uc("V2RmcXJqZmZraw=="), \
                                              database=uc("c3FsMTEyMTc1NjE="), \
                                              connection_timeout=10)
            self.dbcur = self.db.cursor()
            # VSlog("Init cMySqlDB SUCCESS")
        except:
            VSlog("Init cMySqlDB FAIL")

    def __del__(self):
        try:
            self.dbcur.close()
            self.db.close()
            # VSlog("Destroy cMySqlDB SUCCESS")
        except:
            VSlog("Destroy cMySqlDB FAIL")

    def updateIP(self, ip, clientID):
        if ip:
            try:
                ex = """UPDATE mainTable
                        SET ip = %s
                        WHERE id = %s"""
                self.dbcur.execute(ex, (ip, clientID))
                self.db.commit()
                VSlog('SQL UPDATE table Successfully: ip with ' + ip)
            except Exception, e:
                VSlog('SQL ERROR UPDATE table ip: ' + e.message)

    def getContentFromMainTable(self):
        sql_select = "SELECT * FROM mainTable"
        res = []
        try:
            self.dbcur.execute(sql_select)
            res = self.dbcur.fetchall()
        except Exception, e:
            VSlog('SQL ERROR GET table: ' + e.message)
        return res

    def updateXFSS(self, xfss, oldXfss):
        if xfss:
            try:
                ex = """UPDATE serverTable
                        SET xfss = %s
                        WHERE xfss = %s"""
                self.dbcur.execute(ex, (xfss, oldXfss))
                self.db.commit()
                VSlog('SQL UPDATE table Successfully: xfss with ' + xfss)
            except Exception, e:
                VSlog('SQL ERROR UPDATE table xfss: ' + e.message)

    def getContentFromServerTable(self):
        sql_select = "SELECT * FROM serverTable"
        res = []
        try:
            self.dbcur.execute(sql_select)
            res = self.dbcur.fetchall()
        except Exception, e:
            VSlog('SQL ERROR GET table: ' + e.message)
        return res
