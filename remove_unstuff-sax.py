# -*- coding:utf-8 -*-

import codecs, re
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import quoteattr
from xml.sax import make_parser

class TruncateHandler(ContentHandler):
    
    outputXmlFile = None
    titles = []
    inPageOrSiteinfo = False
    buf = u''
    
    def __init__(self,outputXmlFile,titles):
        self.outputXmlFile = outputXmlFile
        self.titles = titles
        self.buf = u''
        self.inPageOrSiteinfo = False
    
    def startElement(self, name, attrs):
        
        if name == 'page' or name == 'siteinfo':
            self.inPageOrSiteinfo = True
            self.buf = u'  <'+name+'>'
        
        elif self.inPageOrSiteinfo:
            self.buf += u'<'+name
            for key in attrs.items():
                self.buf += u' %s=%s'%(key[0],quoteattr(key[1]))
            self.buf += u'>'
        
        elif name == 'mediawiki':
            self.outputXmlFile.write('<mediawiki')
            for key in attrs.items():
                self.outputXmlFile.write(u' %s=%s'%(key[0],quoteattr(key[1])))
            self.outputXmlFile.write(u'>\n')
        
    def characters(self,ch):
        self.buf += ch
    
    def endElement(self,name):
        
        if name == 'page':
            self.inPageOrSiteinfo = False
            self.buf += u'</page>\n'
            title = re.search( 'Page:(.*)/?\d?', re.search('<title>(.*)</title>',self.buf).group(1) ).group(1)
            print title
            if title in self.titles:
                self.outputXmlFile.write(self.buf)
                self.titles.remove(title)
                print '***ADDED***'
        
        elif name == 'siteinfo':
            self.inPageOrSiteinfo = False
            self.buf += u'</siteinfo>\n'
            self.outputXmlFile.write(self.buf)
        
        elif self.inPageOrSiteinfo:
            self.buf += '</'+name+'>'
        
        elif name == 'mediawiki':
            self.outputXmlFile.write('</mediawiki>')

def truncateXML(outputXmlFilename,inputXmlFilename,titlesFilename):
    
    """
    Remove all pages whose the title is not in the titles list
    """
    
    # Open the files
    titlesFile  = codecs.open(titlesFilename,'r','utf-8')
    inputXmlFile = codecs.open(inputXmlFilename,'r','utf-8')
    outputXmlFile = codecs.open(outputXmlFilename,'w','utf-8')
    
    # Get the titles
    titlesArray = [ re.sub( '\r?\n', '', line ) for line in titlesFile.readlines() ]
    
    # Parse the XML
    h = TruncateHandler(outputXmlFile,titlesArray)
    saxparser = make_parser()
    saxparser.setContentHandler(h)
    saxparser.parse( inputXmlFilename )
    
    # Close files
    inputXmlFile.close()
    outputXmlFile.close()
    titlesFile.close()

truncateXML( 'bgwikisource-20100928-pages-meta-history-truncated.xml.test', 'bgwikisource-20100928-pages-meta-history.xml', 'titles.txt' )

