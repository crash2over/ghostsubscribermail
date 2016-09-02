# -*- coding: utf-8 -*-
import smtplib
import linecache
import sys
import re
from utils import config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
    Mail Unit, just prepare mail and send it

    Author: Crash_
    Version: 0.9 (Beta Version)

    This program is intended to resolve "Subscriber" mail service while is available into
    Ghost Blog project.

    There is no warranty for this free software

    Parameters to execute: "NONE" check config file in utils/ folder
"""


class MyMail:

    def __init__(self, recipient, subject, listposts, logo):
        self.recipient = recipient
        self.subject = subject
        self.listposts = listposts
        self.logo = logo
        self.ishtml = config.ISHTML
        self.debug = config.DEBUG
        self.mailserver = config.SMTPSERVER
        self.mailport = config.SMTPPORT
        self.mailuser = config.MAILUSER
        self.mailpass = config.MAILPASS
        self.mailsender = config.MAILSENDER

    def sendMail(self):
        # Create message container - the correct MIME type is multipart/alternative.
        part = None
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.mailsender
        msg['To'] = self.recipient
        msg.preamble = """
        Your mail reader does not support the report format.
        Please visit us <a href="http://cubemelink.com.mx">online</a>!"""
        try:
            print("Ready to send mail to... " + self.recipient)
            if self.ishtml:
                # Record the MIME types of both parts - text/plain and text/html.
                myhtml = self.get_header_html() + self.get_body()
                part = MIMEText(myhtml, 'html')
                if self.debug:
                    myhtmltmp = (myhtml[:100] + '...') if len(myhtml) > 100 else (myhtml + '...')
                    print myhtmltmp
            else:
                self.data += "\nCheck more in: " + self.link
                part = MIMEText(self.data, 'plain')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part)

            # Send the message via local SMTP server.
            s = smtplib.SMTP_SSL(self.mailserver, self.mailport)
            s.login(self.mailuser, self.mailpass)
            # sendmail function takes 3 arguments: sender's address, recipient's address
            # and message to send - here it is sent as one string.
            s.sendmail(self.mailsender, self.recipient, msg.as_string())
            s.quit()
            if self.debug:
                print("Mail sent...")
            return True
        except:
            self.PrintException()
            return False

    def get_header_html(self):
        css = """
        <head>
            <style type="text/css">
                a {
                    color: #E1F5A9;
                    font-size: 70%;
                }

                a:visited {
                    color: white;
                }

                a:hover {
                    color: orange;
                }
            </style>
        </head>
        """
        return css

    def get_body(self):
        postlen = len(self.listposts)
        body = '<body>' \
        '    <div style="background-color: ' + config.BACKGROUND + '; color:white;">\n' \
        '        <div style="padding:50px; color:white;">\n' \
        '            <img src="' + self.logo + '" height="50" width="240" align="center">\n' \
        '            <div class="container">\n' \
        '                <h1 style="color: ' + config.NEWSTITLE + ';">Newsletter For: ' + self.recipient.split('@', 1)[0] + '</h1>\n' \
        '                <h2 style="color: ' + config.NEWSCOMMENT + ';">Check The Last Posts: </h2><br>\n'
        for i in range(postlen):
            body += self.get_posts_divs(self.listposts[i]['title'], self.listposts[i]['markdown'], self.listposts[i]['link'])
        body += '        <br><br><br><br>\n' \
        '                <p style="color: #E1F5A9;font-size: 90%;pointer-events: none;cursor: default;"><b>Copyright © ViajandoConAlas.com.mx</b></p>\n' \
        '            </div>\n' \
        '        </div>\n' \
        '    </div>\n' \
        '</body>\n'
        return body

    def get_posts_divs(self, title, markdown, link):
        content = self.reegex_utf8decode(markdown)
        content = (content[:150] + '...') if len(content) > 150 else (content + '...')
        title = self.reegex_utf8decode(title)
        div = '           <li><h3 style="color: ' + config.DIVTITLE + ';">' + title + '</h3></li>\n' \
        '                <div style="color: ' + config.DIVCONTENT + ';width: 40em;overflow: hidden;border: 2px solid #CEECF5 !important;padding: 15px;width: 400px;font-size: 90%;">\n' \
        '                    <b>' + content + '</b><br><br>\n' \
        '                    <a href="' + link + '" style="font-size: 70%;color=white;"> Check More About This Here </a>\n' \
        '                </div>\n'
        return div

    def regex_utf8decode(self, markdown):
        nomarkdowns = re.sub('[!#$\[\]\(\)]', '', markdown)
        nourl = re.sub('((/)+[\\w\\d:#@%/;$()~_?\\+-=\\\\\\.&]*)', '', re.sub('((http|https):+(/)+[\\w\\d:#@%/;$()~_?\\+-=\\\\\\.&]*)', '', nomarkdowns))
        no2encode = nourl.decode('utf-8').encode('raw_unicode_escape').decode('utf-8')
        return no2encode.encode('ascii', 'xmlcharrefreplace')

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