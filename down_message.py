#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#writer:Qiaoy<TraceurQ@gmail.com>
#V1.0:2012.2.27
#V1.1:2012.2.28 

from BeautifulSoup import BeautifulSoup
import re
import os
import sys
import urllib2
import logging
import xhtml2pdf.pisa as pisa

def exp():
    print "README"
    print "If Html have Chinese you must have the code2000.ttf Because xhtml2pdf just use it"
    print "sudo apt-get install python-BeautifulSoup"
    print "sudo apt-get install python-reportlab"
    print "sudo apt-get install python-html5lib"
    print "sudo apt-get install python-xhtml2pdf"

def down(site):
    value = urllib2.urlopen(site).read()
    soup = BeautifulSoup(value)
    try:
        title = str(re.findall(r"<TITLE>(.*?)</TITLE>",value)[0])
        time = re.findall(r"<HR SIZE=1>\r\n(.*?)\r\n",value)[0].replace(' ','')
        conntext = str(soup.html.body("p")[4])
        conntext = conntext.replace("<span style=\"font-family: \xe5\xae\x8b\xe4\xbd\x93\">","")
        HtmlFile = open("./html/%s.html"%title,"w")
        HtmlFile.write(r'''
            <html>
            <meta charset="utf8"/>  
            <style type='text/css'>  
            @font-face {   
                    font-family: "code2000";   
                    src: url("code2000.ttf")   
            }   
              
            html {   
                 font-family: code2000;   
            }   
            </style>
        ''')
        HtmlFile.write(r'<title>'+title+'</title>')
        HtmlFile.write(r"<h1 align=center>%s</h1>"%title)
        HtmlFile.write(r"<h3 align=center>%s</h3>"%time)
        HtmlFile.write(conntext)
        HtmlFile.write(r'</html>')
        HtmlFile.close()
    except:
        title = None
        exp()
        sys.exit()
    return title

def change(title):
    if title:        
        FileName = os.getcwd()
        HtmlName = FileName + "/html/%s"%title + ".html"
        PdfName = FileName + "/pdf/%s"%title + ".pdf"
        data = open(HtmlName).read()
        result = file(PdfName,"w")
        pdf = pisa.CreatePDF(data,result)
        if not pdf.err:
            pisa.startViewer(PdfName)
            print "%s.pdf is ok"%title
        result.close()
    else:
        exp()
        sys.exit()

if __name__ == "__main__":
    try:
        os.mkdir("html")
        os.mkdir("pdf")
    except:
        pass
    sites = []
    for i in range(2,5):#Change NO. to download the different page 
        page = urllib2.urlopen("http://www.itsec.gov.cn/xwdt/yjdt20/index%d.htm"%i).read()
        url = re.findall(r'href=\"([\d]*.htm)\"',page)
        sites = sites + url
    for site in sites:
        change(down("http://www.itsec.gov.cn/xwdt/yjdt20/%s"%site))
