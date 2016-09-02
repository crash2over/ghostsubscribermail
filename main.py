# -*- coding: utf-8 -*-
import linecache
import sys
import time
from dbmodel import ghostposts
from utils import config
from control import mail

"""
    Main unit for interface between Ghost Blog and Python SMTP

    Author: Crash_
    Version: 0.9 (Beta Version)
    Contact: crash@cubemelink.com.mx

    This program is intended to resolve "Subscriber" mail service while is available into
    Ghost Blog project.

    There is no warranty for this free software

    Parameters to execute: "NONE" check config file in utils/ folder
"""


class Main:

    def __init__(self):
        self.debug = config.DEBUG
        self.asdaemon = config.ASDAEMON
        self.ghost = ghostposts.DBGhostPosts()

    def main(self):
        try:
            if self.asdaemon:
                while True:
                    self.just_doit()
                    time.sleep(config.SLEEPASDAEMON)
            else:
                self.just_doit()
        except:
            self.PrintException()

    def just_doit(self):
        print("*****************************************************")
        #Check if mail service db is empty
        if self.ghost.subscribemail_empty():
            #if empty then init, first post is a dummy
            self.ghost.initialize_subscribemail()
        self.send_mail(self.ghost.get_recent_published_post())
        print("*****************************************************")

    def send_mail(self, listposts):
        okmail = False
        try:
            if listposts:
                settings = self.ghost.get_ghost_settings()
                subscribers = self.ghost.get_list_subscribers()
                if subscribers:
                    print("Starting Mail Working: " + time.strftime("%c"))
                    for i in range(len(subscribers)):
                        recipient = subscribers[i][0]
                        mymail = mail.MyMail(recipient, 'Newsletter From ' + settings['title'], listposts, config.URL + '/' + settings['logo'])
                        okmail = mymail.sendMail()
                    if okmail:
                        self.ghost.mark_post_as_sent(listposts)
                    print("Ending Mail Working: " + time.strftime("%c"))
        except:
            self.PrintException()

    def PrintException(self):
        """
            PrintException(self) method:
                Print errors in these class... debuggin function... use with try and except
        """
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

if __name__ == "__main__":
    main = Main()
    main.main()
