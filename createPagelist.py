# -*- coding:utf-8 -*-

import codecs, re, wikipedia

pagesFile  = codecs.open('pages.txt','w','utf-8')
metadataFile  = codecs.open('metadata-stats.txt','r','utf-8')

# Get the metadata
metadatalist = [ re.sub( '\r?\n', '', line ).split(' ') for line in metadataFile.readlines() ]
for book in metadatalist :
    
    print book[0]
    for nbpage in range(0,int(book[2])):
        
        pagesFile.write( 'Page:%s/%s\n'%(book[0],nbpage+1) )

pagesFile.close()
metadataFile.close()

