#-*- coding: utf-8 -*-
#Primatech.
from resources.lib.config import cConfig
from resources.lib.ftplib import FTP
from resources.lib.util import VSlog,VSerror,uc,VSlang
import os
import time

class cFtpManager:

    def __init__(self):
        try:
            self.ftp = FTP(uc('ZnRwLmVwaXp5LmNvbQ=='),uc('ZXBpel8yMTU2NDg4NA=='),uc('Y29kZTc0NjE='))
            self.ftp.sendcmd("TYPE i")
            self.oConfig = cConfig()
        except Exception, e:
            VSlog("FtpManager __init__ ERROR: " + e.message)

    def getmTimeLocalDB(self, fileDb):
        t = time.localtime(os.path.getmtime(fileDb))
        year = t[0]
        month = t[1]
        day = t[2]
        hour = t[3]
        min = t[4]
        sec = t[5]
        timestamp = sec
        timestamp += min * 100
        timestamp += hour * 10000
        timestamp += day * 1000000
        timestamp += month * 100000000
        timestamp += year * 10000000000
        return timestamp

    def sendDb(self):
        fileDb = self.oConfig.getFileDB()
        fileDbServer = 'db_' + self.oConfig.getSetting('clientID') + '.db'

        try:
            do = False
            if ((os.path.exists(fileDb)) and (fileDbServer in self.ftp.nlst())):
                timestamp_s = self.ftp.voidcmd('MDTM /htdocs/db/'+fileDbServer)[4:].strip()
                timestamp_l = self.getmTimeLocalDB(fileDb)
                if int(timestamp_l) > int(timestamp_s):
                    do = True
            else:
                do = True
            if do:
                command = 'STOR ' + fileDbServer
                f = open(fileDb,'rb')
                self.ftp.cwd('/htdocs/db/')
                self.ftp.storbinary(command, f)
                f.close()
                self.ftp.quit()
        except Exception, e:
            VSlog("FtpManager sendDb ERROR: " + e.message)
            self.ftp.quit()

    def getDb(self):
        fileDb = self.oConfig.getFileDB()
        fileDbServer = 'db_' + self.oConfig.getSetting('clientID') + '.db'

        try:
            do = False
            if ((os.path.exists(fileDb)) and (fileDbServer in self.ftp.nlst())):
                timestamp_s = self.ftp.voidcmd('MDTM /htdocs/db/'+fileDbServer)[4:].strip()
                timestamp_l = self.getmTimeLocalDB(fileDb)
                if int(timestamp_l) < int(timestamp_s):
                    do = True
            else:
                do = True
            if do:
                command = 'RETR ' + fileDbServer
                f = open(fileDb,'wb')
                self.ftp.cwd('/htdocs/db/')
                self.ftp.retrbinary(command, f.write)
                f.close()
                self.ftp.quit()
        except Exception, e:
            VSlog("FtpManager getDb ERROR: " + e.message)
            self.ftp.quit()

    def sendLogs(self):
        fileLog = self.oConfig.getLogFile()
        command = 'STOR log_' + self.oConfig.getSetting('clientID') + '.log'
        try:
            f = open(fileLog,'rb')
            self.ftp.cwd('/htdocs/logs/')
            self.ftp.storbinary(command, f)
            f.close()
            self.ftp.quit()
        except Exception, e:
            VSlog("FtpManager sendLogs ERROR: " + e.message)
            self.ftp.quit()
