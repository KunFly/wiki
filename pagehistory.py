#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
This module is used for analyzing wikipedia history page
Use this script for other language except french, need
reset locale information below.
"""

__author__ = "JIN Kun"
__licence__ = "GPL"
__version__ = "0.1"
__email__ = "kun.jin@univ-bpclermont.fr"

from lxml.html.soupparser import parse
from lxml import etree
import sys
import re
from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL,'fr_FR.utf8')

class PageHistory:

    def __init__(self, page):
        self.page = page

    def get_revisions(self):
        root = parse(self.page).getroot()
        list_rev = root.xpath("//ul[@id='pagehistory']/li")
        for rev in list_rev:
            yield Revision(rev)

class Revision:

    def __init__(self, rev):

        self.rev = rev
        self.id = None # int
        self.date = None # w3c standard
        self.author = None # str
        self.size = None # str (int + octets)
        self.change_size = None # str (+/- int)
        self.comment = None # str
        self.minoredit = None # bool
        for element in self.rev:
            try:
                ele_class = element.attrib["class"]
            except:
                continue
            if ele_class == "mw-changeslist-date":
                self.set_id(element.attrib["href"])
                self.set_date(element.text)
            elif ele_class == "history-user":
                self.set_author(element[0].text)
            elif ele_class == "minoredit":
                self.set_minoredit()
            elif ele_class == "history-size":
                self.set_size(element.text)
            elif (ele_class == "mw-plusminus-neg" 
                  or 
                  ele_class == "mw-plusminus-pos"
                  or
                  ele_class == "mw-plusminus-null"):
                self.set_change_size(element.text)
            elif ele_class == "comment":
                self.set_comment(element)

    def set_id(self,url): 
        exp = re.compile("(?<==)\d+$",re.U)
        self.id = exp.search(url).group(0)
    def get_id(self): return self.id

    def set_date(self,date_string):
        date_format_in =  u"%d %B %Y à %H:%M".encode("utf-8")
        date_format_out = u"%Y-%m-%dT%H:%M".encode("utf-8")
        date_string_in = date_string.encode("utf-8")
        date_string = datetime.strptime(date_string_in, date_format_in)
        self.date = unicode(date_string.strftime(date_format_out))
    def get_date(self): return self.date

    def set_author(self,author): self.author = unicode(author)
    def get_author(self): return self.author

    def set_minoredit(self): self.minoredit = True
    def get_minoredit(self): return self.minoredit

    def set_size(self,size): self.size = unicode(size)
    def get_size(self): return self.size

    def set_change_size(self, size): self.change_size = unicode(size)
    def get_change_size(self): return self.change_size

    def set_comment(self, element):
        self.comment = "".join(element.xpath(".//text()"))
    def get_comment(self): return self.comment

if __name__ == "__main__":
    infile = sys.argv[1]
    t = PageHistory(infile)
    revisions = t.get_revisions()
    for revision in revisions:
        print revision.date

