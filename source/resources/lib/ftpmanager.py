#-*- coding: utf-8 -*-
#Primatech.
from resources.lib.config import cConfig
from resources.lib.ftplib import FTP
from resources.lib.util import VSlog,VSerror,uc,VSlang

class cFtpManager:

    def __init__(self):
        try:
            self.ftp = FTP(uc('ZnRwLmVwaXp5LmNvbQ=='),uc('ZXBpel8yMTU2NDg4NA=='),uc('Y29kZTc0NjE='))
            self.oConfig = cConfig()
        except Exception, e:
            VSlog("FtpManager __init__ ERROR: " + e.message)

    def sendDb(self):
        fileDb = self.oConfig.getFileDB()
        command = 'STOR db_' + self.oConfig.getSetting('clientID') + '.db'
        try:
            f = open(fileDb,'rb')
            self.ftp.cwd('/htdocs/db/')
            self.ftp.storbinary(command, f)
            f.close()
            self.ftp.quit()
        except Exception, e:
            VSlog("FtpManager sendDb ERROR: " + e.message)

    def getDb(self):
        fileDb = self.oConfig.getFileDB()
        command = 'RETR db_' + self.oConfig.getSetting('clientID') + '.db'
        try:
            f = open(fileDb,'wb')
            self.ftp.cwd('/htdocs/db/')
            self.ftp.retrbinary(command, f.write)
            f.close()
            self.ftp.quit()
        except Exception, e:
            VSlog("FtpManager getDb ERROR: " + e.message)

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
