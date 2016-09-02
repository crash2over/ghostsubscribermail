# -*- coding: utf-8 -*-
import MySQLdb
import linecache
import sys
from utils import config

"""
    Database Unit Generic Queries

    Author: Crash_
    Version: 0.9 (Beta Version)

    This program is intended to resolve "Subscriber" mail service while is available into
    Ghost Blog project.

    There is no warranty for this free software

    Parameters to execute: "NONE" check config file in utils/ folder
"""


class DBM:

    def __init__(self):
        self.debug = config.DEBUG

        if config.DEBUG:
            self._ServerDB = config.DBSERVERDEV
            self._PortDB = config.DBPORTDEV
            self._UserDB = config.DBUSERDEV
            self._PassDB = config.DBPASSDEV
            self._SchemaDB = config.DBSCHEMADEV
        else:
            self._ServerDB = config.DBSERVERPROD
            self._PortDB = config.DBPORTPROD
            self._UserDB = config.DBUSERPROD
            self._PassDB = config.DBPASSPROD
            self._SchemaDB = config.DBSCHEMAPROD

    def __connect(self):
        try:
            db = MySQLdb.connect(host=self._ServerDB, port=int(self._PortDB), user=self._UserDB, passwd=self._PassDB, db=self._SchemaDB)
            db.set_character_set('utf8')
            return db
        except:
            self.PrintException()
            return None

    def executeQryGetRows(self, qry):
        try:
            db = self.__connect()
            cursor = db.cursor()
            cursor.execute(qry)
            lista = cursor.fetchall()
            rows = cursor.rowcount
            if rows == 0:
                if self.debug:
                    print("Row count on executeQryGetRows(): " + str(rows))
                lista = None
            db.commit()
            db.close()
        except:
            lista = None
            if self.debug:
                self.PrintException()
        return lista

    def executeQryGetRow(self, qry):
        try:
            db = self.__connect()
            cursor = db.cursor()
            cursor.execute(qry)
            lista = cursor.fetchone()
            rows = cursor.rowcount
            if rows == 0:
                if self.debug:
                    print("Row count on executeQryGetRow(): " + str(rows))
                lista = None
            db.commit()
            db.close()
        except:
            lista = None
            if self.debug:
                self.PrintException()
        return lista

    def executeQry(self, qry):
        res = True
        try:
            db = self.__connect()
            cursor = db.cursor()
            cursor.execute(qry)
            db.commit()
            db.close()
        except:
            res = False
            if self.debug:
                print qry
                self.PrintException()
        return res

    def executeQryGetCell(self, qry):
        try:
            db = self.__connect()
            cursor = db.cursor()
            cursor.execute(qry)
            lista = cursor.fetchone()
            if lista is not None:
                cell = lista[0]
            else:
                cell = None
            db.commit()
            db.close()
        except:
            cell = None
            if self.debug:
                self.PrintException()
        return cell

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
