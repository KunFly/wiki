
pagehistory.py

This module is used for analyzing wikipedia history page
Use this script for other language except french, need
reset locale information below.
    locale.setlocale(locale.LC_ALL,'fr_FR.utf8')

这个模块被使用来处理维基百科的“历史页面”，目前这个模块只支持法文，
如果需要支持其他语言，请修改本地语言环境
    locale.setlocale(locale.LC_ALL,'fr_FR.utf8')

Manuel:

class PageHistory(page_file)
 - method get_revisions, return iterator for revisions

each revision has:
    id          # int
    date        # w3c standard
    author      # str
    size        # str (int + octets)
    change_size # str (+/- int)
    comment     # str
    minoredit   # bool

Example:

infile = "history.html"
t = PageHistory(infile)
revisions = t.get_revisions()
for revision in revisions:
    print revision.id
    print revision.date

moduleBody.py

This module is used for analyzing dump text part
这个模块被使用来处理维基百科DUMP的文本部分

class Sujet(items_sujet,lvl), items_sujet, type list, is [title,text]; lvl is sujet level
 - get_sub_sujet(lvl)

Example:
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
