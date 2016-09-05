# -*- coding: utf-8 -*-
import linecache
import sys

from dbmodel import database
from utils import config

"""
    Ghost Database Model

    Author: Crash_
    Version: 0.9 (Beta Version)

    This program is intended to resolve "Subscriber" mail service while is available into
    Ghost Blog project.

    There is no warranty for this free software

    Parameters to execute: "NONE" check config file in utils/ folder
"""


class DBGhostPosts:

    def __init__(self):
        self.url = config.URL
        self.mydb = database.DBM()
        self.debug = config.DEBUG
        self.maildatabase = config.MAILDATABASE
        self.mailtable = config.MAILTABLE
        if config.DEBUG:
            self.ghostdatabase = config.DBSCHEMADEV
        else:
            self.ghostdatabase = config.DBSCHEMAPROD
        self.ghosttable = config.GHOSTTABLE

    def subscribemail_empty(self):
        query = 'SELECT * FROM ' + self.maildatabase + "." + self.mailtable + ' LIMIT 1'
        if self.debug:
            print query
        try:
            res = self.mydb.executeQryGetRow(query)
            if res is None:
                return True
            else:
                return False
        except:
            self.PrintException()

    def initialize_subscribemail(self):
        query = 'SELECT uuid, DATE_FORMAT(updated_at, "%Y-%m-%d %H:%i:%s"), DATE_FORMAT(min(published_at), "%Y-%m-%d %H:%i:%s") FROM ' + self.ghostdatabase + '.' + self.ghosttable
        if self.debug:
            print query
        try:
            res = self.mydb.executeQryGetRow(query)
            if res is None:
                return False
            else:
                uuid = res[0]
                updated_at = res[1]
                published_at = res[2]
                query = "INSERT INTO " + self.maildatabase + "." + self.mailtable + "(uuid, updated_at, published_at) values ('" + uuid + "', '" + updated_at + "', '" + published_at + "')"
                return self.mydb.executeQry(query)
        except:
            self.PrintException()

    def get_recent_published_post(self, permalinks):
        listposts = []
        query = 'SELECT DATE_FORMAT(max(' + self.maildatabase + '.' + self.mailtable + '.published_at), "%Y-%m-%d %H:%i:%s") FROM ' + self.maildatabase + '.' + self.mailtable
        if self.debug:
            print query
        try:
            res = self.mydb.executeQryGetCell(query)
            query = 'SELECT ' + self.ghostdatabase + '.' + self.ghosttable + '.uuid, DATE_FORMAT(' + \
            self.ghostdatabase + '.' + self.ghosttable + '.updated_at, "%Y-%m-%d %H:%i:%s"), DATE_FORMAT(' + \
            self.ghostdatabase + '.' + self.ghosttable + '.published_at, "%Y-%m-%d %H:%i:%s"),' + \
            self.ghostdatabase + '.' + self.ghosttable + '.slug, ' + self.ghostdatabase + '.' + \
            self.ghosttable + '.html, ' + self.ghostdatabase + '.' + self.ghosttable + '.markdown, ' + \
            self.ghostdatabase + '.' + self.ghosttable + '.title FROM ' + self.ghostdatabase + '.' + self.ghosttable + \
            ' WHERE ' + self.ghostdatabase + '.' + self.ghosttable + '.published_at > "' + res + '"'
            if self.debug:
                print query
            res = self.mydb.executeQryGetRows(query)
            if res is None:
                if self.debug:
                    print("No new posts...")
                return False
            else:
                for i in range(len(res)):
                    post = {}
                    if self.debug:
                        print("New post founded now working...")
                    post['uuid'] = res[i][0]
                    post['updated_at'] = res[i][1]
                    post['published_at'] = res[i][2]
                    post['link'] = self.build_permalink(permalinks, res[i][3], post['published_at'])
                    post['markdown'] = res[i][5]
                    post['title'] = res[i][6]
                    if post['uuid'] is None and post['updated_at'] is None and post['published_at'] is None:
                        if self.debug:
                            print("No valid row maybe NULL...")
                        return False
                    listposts.append(post)
                return listposts
        except:
            self.PrintException()
            return None

    def build_permalink(self, permalink, slug, published_at):
        if permalink.find('year') > -1 and permalink.find('month') > -1 and permalink.find('day') > -1:
            dateuri = published_at.split(' ')[0].split('-')
            return (self.url + '/' + dateuri[0] + '/' + dateuri[1] + '/' + dateuri[2] + '/' + slug)
        else:
            return (self.url + '/' + slug)

    def mark_post_as_sent(self, listposts):
        for j in range(len(listposts)):
            query = 'INSERT INTO ' + self.maildatabase + '.' + self.mailtable + '(uuid, updated_at, published_at) values ("' + listposts[j]['uuid'] + '", "' + \
            listposts[j]['updated_at'] + '", "' + listposts[j]['published_at'] + '")'
            if self.debug:
                print query
            self.mydb.executeQry(query)

    def get_ghost_settings(self):
        logoquery = 'SELECT ' + self.ghostdatabase + '.settings.value FROM ' + self.ghostdatabase + '.settings WHERE STRCMP(' + self.ghostdatabase + '.settings.key,"logo")=0'
        titlequery = 'SELECT ' + self.ghostdatabase + '.settings.value FROM ' + self.ghostdatabase + '.settings WHERE STRCMP(' + self.ghostdatabase + '.settings.key,"title")=0'
        permalinksquery = 'SELECT ' + self.ghostdatabase + '.settings.value FROM ' + self.ghostdatabase + '.settings WHERE STRCMP(' + self.ghostdatabase + '.settings.key,"permalinks")=0'
        if self.debug:
            print logoquery
            print titlequery
            print permalinksquery
        settings = {}
        try:
            logo = self.mydb.executeQryGetCell(logoquery)
            settings['logo'] = logo
            title = self.mydb.executeQryGetCell(titlequery)
            settings['title'] = title
            permalinks = self.mydb.executeQryGetCell(permalinksquery)
            settings['permalinks'] = permalinks

            if logo is None and title is None:
                return False
            else:
                return settings
        except:
            self.PrintException()

    def get_list_subscribers(self):
        query = 'SELECT ' + self.ghostdatabase + '.subscribers.email FROM ' + self.ghostdatabase + '.subscribers WHERE STRCMP(' + self.ghostdatabase + '.subscribers.status,"subscribed")=0'
        if self.debug:
            print query
        res = self.mydb.executeQryGetRows(query)
        return res

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