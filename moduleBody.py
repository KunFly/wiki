#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
This module is used for analyzing dump text part

这个模块被使用来处理维基百科DUMP的文本部分

git clone https://github.com/KunFly/wiki.git
"""
__author__ = "JIN Kun"
__licence__ = "GPL"
__version__ = "0.1"
__email__ = "kun.jin@univ-bpclermont.fr"

import re
import sys
import codecs

def analyze_list(t,lvl=2):
    exp = re.compile("\n?={%s}([^=].+[^=])={%s}\n"%(lvl,lvl))
    l = exp.split(t)
    t_def = None
    if len(l) % 2 != 0:
        t_def = l[0]
        ll = l[1:]
    else:
        ll = l
    new_ll = zip(ll[0::2], ll[1::2])
    return t_def, new_ll

class Sujet:
    def __init__(self, l, lvl=1):
        self.title = l[0].strip()
        self.text = l[1].strip()
        self.main_text = None
        self.list_sujets = None

        lvl += 1
        self.main_text,self.list_sujets = analyze_list(self.text,lvl)

    def get_sub_sujet(self,lvl=2):
        for s_title, s_text in self.list_sujets:
            item_sujet = [s_title,s_text]
            yield Sujet(item_sujet, lvl)

if __name__ == "__main__":
    arg = sys.argv[1]
    inf = codecs.open("body-text.txt","r","utf-8")
    intext = inf.read()
    list_text = ["Histoire de la logique",intext]
    f = Sujet(list_text,lvl=1)
    print f.title
    print f.main_text
    for sub_l2 in f.get_sub_sujet(lvl=2):
        print sub_l2.title
        for sub_l3 in sub_l2.get_sub_sujet(lvl=3):
            print "\t",sub_l3.title
            for sub_l4 in sub_l3.get_sub_sujet(lvl=4):
                print "\t\t",sub_l4.title
