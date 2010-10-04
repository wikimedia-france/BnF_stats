# -*- coding:utf-8 -*-

import xml.dom.minidom, codecs, re

def truncateXML(outputXmlFilename,inputXmlFilename,titlesFilename):
    
    """
    Remove all pages whose the title is not in the titles list
    """
    
    # Open the files
    titlesFile  = codecs.open(titlesFilename,'r','utf-8')
    inputXmlFile = codecs.open(inputXmlFilename,'r','utf-8')
    outputXmlFile = codecs.open(outputXmlFilename,'w','utf-8')
    
    # Get the titles
    titlesArray = [ line[:-1] for line in titlesFile.readlines() ]
    
    # Parse the XML
    inputXmlString = inputXmlFile.read().encode('utf-8')
    domxml = xml.dom.minidom.parseString( inputXmlString )
    
    # Remove unneeded pages
    for mediawiki in domxml.childNodes:
        if mediawiki.localName == 'mediawiki':
            for page in mediawiki.childNodes:
                if page.localName == 'page':
                    
                    if page.getElementsByTagName('title').item(0).firstChild.data not in titlesArray:
                        oldpage = mediawiki.removeChild(page)
                        oldpage.unlink()
                
                #elif page.localName == 'siteinfo':
                #    oldpage = mediawiki.removeChild(page)
                #    oldpage.unlink()
    
    # Save file
    string = mediawiki.toxml( 'utf-8' ).decode('utf-8')
    string = re.sub( '</page>\n[\n ]*<page>', '</page>\n<page>', string )
    string = re.sub( '</page>\n[\n ]*</mediawiki>', '</page>\n</mediawiki>', string )
    outputXmlFile.write( string )
    
    # Close files
    inputXmlFile.close()
    outputXmlFile.close()
    titlesFile.close()

truncateXML( 'bgwikisource-20100928-pages-meta-history-truncated.xml', 'bgwikisource-20100928-pages-meta-history.xml', 'titles.txt' )

