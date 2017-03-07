#! /usr/bin/env python
# -*- encoding=utf8 -*-

from pyExcelerator import *
from xml.etree import ElementTree as ET
import xlrd
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

title_name = ["k", "zh", "en"]


def xlsToXml(xlsFile,outfile):
    bk = xlrd.open_workbook(xlsFile)
    fh = open(outfile, "w+")
    fh.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    fh.write("<root>")
    for _sheet  in bk.sheets():
        if _sheet.name not in ("firstName" ,"familyName"):
            break
        nrows = _sheet.nrows
        ncols = _sheet.ncols
        for i in xrange(3, nrows):
            _c_dict = {}
            for j in range(0, len(title_name)):
                _c_dict[title_name[j]] =_sheet.row(i)[j].value 
    
            fh.write("<i>")
            for _title in title_name:
                    fh.write("<%s>%s</%s>" %(_title, _c_dict[_title], _title))
            fh.write("</i>")

    fh.write("</root>")
    fh.close()

def xmlToXls(xmlFile, outfile):
    fh = open(xmlFile)
    data = fh.read()
    fh.close()
    w = Workbook()
    xmlData = ET.fromstring(data)
    _sheet_tables = {}
    for _d in xmlData:
        _c_dict = {}
        for _c in _d.getchildren():
            _c_dict[_c.tag] = _c.text if _c.text else ""
    
        split_name_list = _c_dict["k"].split("_")
        if split_name_list[-1].isdigit():
            split_name_list.remove(split_name_list[-1])
            sheet_name = "_".join(split_name_list)
        else:
            sheet_name = "Other"
        if sheet_name not in _sheet_tables:
            _sheet_tables[sheet_name] = {"name":w.add_sheet(sheet_name), "number":3}
            for i in range(0,len(title_name)):
                _sheet_tables[sheet_name]["name"].write(2,i,title_name[i])
    
        for i in range(0,len(title_name)):
            _sheet_tables[sheet_name]["name"].write(_sheet_tables[sheet_name]["number"],i,_c_dict.get(title_name[i], ""))
        _sheet_tables[sheet_name]["number"] += 1
        
    w.save(outfile)

if __name__ == "__main__":
    xmlFile = sys.argv[1]
    if xmlFile.endswith("string_all.txt"):
        xmlToXls(xmlFile, "multiLanguage.xls")
    elif xmlFile.endswith("string_update.txt"):
        xmlToXls(xmlFile, "multiLanguage_update.xls")
    elif xmlFile.endswith("multiLanguage.xls"):
        xlsToXml(xmlFile, "string_all.txt")
    elif xmlFile.endswith("multiLanguage_update.xls"):
        xlsToXml(xmlFile, "string_name.txt")
    else:
        print "输入文件错误\n %s" % xmlFile
        sys.exit(1)
