# -*- coding: utf-8 -*-
"""
    System Configuration Vars

    Author: Crash_
    Version: 0.9 (Beta Version)

    This program is intended to resolve "Subscriber" mail service while is available into
    Ghost Blog project.

    There is no warranty for this free software
"""

#If TRUE set all debug notifications implemented as active
DEBUG = False
#If TRUE run as daemon and never stop just use update-rc.d to set in differents user runlevels
#If FALSE you MUST USE Cron&Crontab check README file
ASDAEMON = False
#if ASDAEMON is TRUE set sleep time suggested 60
SLEEPASDAEMON = 60
#Notification on updates not implemented yet
CHECK4UPDATES = True
#Set base URL for links
URL = 'http://127.0.0.1:2368'

#Mail Config This Only Work For SMTP Mails SSL Config, this is what i need but working in other ways
SMTPSERVER = 'mail.myserver.com'
SMTPPORT = '465'
#Right now just html working on plain text
ISHTML = True
#Credential for SMTP
MAILUSER = 'user@myserver.com'
MAILPASS = 'mypass'
#Who is sending the mails?
MAILSENDER = 'newsletter@myserver.com'

#DB Production DEBUG=False
DBSERVERPROD = '127.0.0.1'
DBPORTPROD = '3306'
DBUSERPROD = 'root'
DBPASSPROD = '12345'
DBSCHEMAPROD = 'ghost'

#DB Develop DEBUG=True
DBSERVERDEV = '127.0.0.1'
DBPORTDEV = '3306'
DBUSERDEV = 'root'
DBPASSDEV = '12345'
DBSCHEMADEV = 'ghost'

#DB Mail - Internal Control For Sent Posts
MAILDATABASE = 'ghostsubscribemail'
MAILTABLE = 'mail_news'
GHOSTTABLE = 'posts'

#html color selection
BACKGROUND = '#FFFFFF'
NEWSTITLE = '#000000'
NEWSCOMMENT = '#5882FA'
DIVTITLE = '#A4A4A4'
DIVCONTENT = '#5882FA'