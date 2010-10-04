# -*- coding:utf-8 -*-

import codecs, re, calendar, time, math, os, os.path, Levenshtein
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import quoteattr
from xml.sax import make_parser

class PageStatisticsHandler(ContentHandler):
    
    idsbnf = []
    nbpages = []
    pageResultsFile = None
    bookResultsFile = None
    
    # Page statistics
    idbnf = 0
    book = u''
    pages = 0
    pagen = 0
    nbrev = 0
    creation_date = 0
    first_status = 0
    last_status = 0
    usernames = set()
    ips = set()
    gray_date = 0
    pink_date = 0
    yellow_date = 0
    green_date = 0
    nonlinearity = False
    isocr = False
    raw_pink_lev = 0
    fin_pink_lev = 0
    raw_yellow_lev = 0
    fin_yellow_lev = 0
    raw_green_lev = 0
    fin_green_lev = 0
    nbnonbotcontribs = 0
    
    # Book statistics
    books = dict()
    raw_pink_levenshtein_distances = dict()
    raw_yellow_levenshtein_distances = dict()
    raw_green_levenshtein_distances = dict()
    finer_pink_levenshtein_distances = dict()
    finer_yellow_levenshtein_distances = dict()
    finer_green_levenshtein_distances = dict()
    
    # User statistics
    userstats = dict()
    
    # Temporary data
    buf = u''
    date = 0
    textocr = u''
    
    def __init__(self,idsbnf,nbpages,pageResultsFile):
        
        # Input data and output files
        self.idsbnf = idsbnf
        self.nbpages = nbpages
        self.pageResultsFile = pageResultsFile
        
        # Page statistics
        self.idbnf = 0
        self.book = u''
        self.pages = 0
        self.pagen = 0
        self.nbrev = 0
        self.creation_date = 0
        self.first_status = 0
        self.last_status = 0
        self.usernames = set()
        self.ips = set()
        self.gray_date = 0
        self.pink_date = 0
        self.yellow_date = 0
        self.green_date = 0
        self.nonlinearity = False
        self.isocr = False
        self.raw_pink_lev = 0
        self.fin_pink_lev = 0
        self.raw_yellow_lev = 0
        self.fin_yellow_lev = 0
        self.raw_green_lev = 0
        self.fin_green_lev = 0
        self.nbnonbotcontribs = 0
        
        # Book statistics
        self.books = dict()
        self.nbgray, self.nbblue, self.nbpink, self.nbyellow, self.nbgreen = 0, 0, 0, 0, 0
        self.raw_pink_levenshtein_distances = dict()
        self.raw_yellow_levenshtein_distances = dict()
        self.raw_green_levenshtein_distances = dict()
        self.finer_pink_levenshtein_distances = dict()
        self.finer_yellow_levenshtein_distances = dict()
        self.finer_green_levenshtein_distances = dict()
        
        # User statistics
        userstats = dict()
        
        # Temporary data
        self.buf = u''
        self.date = 0
        self.textocr = u''
    
    def startElement(self, name, attrs):
        
        self.buf = u''
        
        if name == 'revision':
            self.date = 0
        
        elif name == 'page':
            self.book = u''
            self.pagen = 0
            self.idbnf = 0
            self.pages = 0
            self.last_status = -1
            self.creation_date = 0
            self.gray_date = 0
            self.pink_date = 0
            self.yellow_date = 0
            self.green_date = 0
            self.nbrev = 0
    
    def characters(self,ch):
        
        self.buf += ch
    
    def endElement(self,name):
        
        if name == 'page':
            
            # Page statistics
            
            result_page = ( str(self.idbnf), re.sub(' ','_',self.book), str(self.pages), str(self.pagen), str(self.nbrev), str(self.creation_date), str(self.first_status), str(self.last_status), re.sub(' ','_',u'|'.join(self.usernames)), re.sub(' ','_',u'|'.join(self.ips)), str(self.gray_date), str(self.pink_date), str(self.yellow_date), str(self.green_date), str(self.nonlinearity), str(self.isocr), str(self.raw_pink_lev), str(self.raw_yellow_lev), str(self.raw_green_lev), str(self.fin_pink_lev), str(self.fin_yellow_lev), str(self.fin_green_lev) )
            
            self.pageResultsFile.write( u' '.join(result_page) )
            self.pageResultsFile.write( u'\n' )
            
            # Book statistics
            nbgray, nbblue, nbpink, nbyellow, nbgreen = 0, 0, 0, 0, 0
            
            if self.last_status == 1: nbblue = 1
            elif self.last_status == 2: nbgray = 1
            elif self.last_status == 3: nbpink = 1
            elif self.last_status == 4: nbyellow = 1
            elif self.last_status == 5: nbgreen = 1
            
            if self.idbnf not in self.books:
                
                self.books[self.idbnf] = ( self.idbnf, self.book, self.pages, self.nbrev, 1, self.pages-1, nbblue, nbgray, nbpink, nbyellow, nbgreen, len(self.usernames), len(self.ips), self.usernames, self.ips, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, self.nbnonbotcontribs, 0 )
            
            else:
                
                ( old_idbnf, old_book, old_pages, old_nbrev, old_created_pages, old_uncreated_pages, old_nbgray, old_nbblue, old_nbpink, old_nbyellow, old_nbgreen, old_nbusernames, old_nbips, old_usernames, old_ips, old_mean_raw_pink_lev, old_mean_raw_yellow_lev, old_mean_raw_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev, old_mean_fin_pink_lev, old_mean_fir_yellow_lev, old_mean_fin_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev, old_nbnonbotcontribs, old_percentnonbotcontribs ) = self.books[self.idbnf]
                
                old_usernames.update( self.usernames )
                old_ips.update( self.ips )
                
                self.books[self.idbnf] = ( old_idbnf, old_book, old_pages, old_nbrev+self.nbrev, old_created_pages+1, old_uncreated_pages-1, old_nbgray+nbgray, old_nbblue+nbblue, old_nbpink+nbpink, old_nbyellow+nbyellow, old_nbgreen+nbgreen, len(old_usernames), len(old_ips), old_usernames, old_ips, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, old_nbnonbotcontribs+self.nbnonbotcontribs, old_percentnonbotcontribs )
            
            # Add Levenshtein distances to the ensembles
            if self.idbnf not in self.raw_pink_levenshtein_distances: self.raw_pink_levenshtein_distances[self.idbnf] = set()
            if self.idbnf not in self.raw_yellow_levenshtein_distances: self.raw_yellow_levenshtein_distances[self.idbnf] = set()
            if self.idbnf not in self.raw_green_levenshtein_distances: self.raw_green_levenshtein_distances[self.idbnf] = set()
            if self.idbnf not in self.finer_pink_levenshtein_distances: self.finer_pink_levenshtein_distances[self.idbnf] = set()
            if self.idbnf not in self.finer_yellow_levenshtein_distances: self.finer_yellow_levenshtein_distances[self.idbnf] = set()
            if self.idbnf not in self.finer_green_levenshtein_distances: self.finer_green_levenshtein_distances[self.idbnf] = set()
            
            self.raw_pink_levenshtein_distances[self.idbnf].add( self.raw_pink_lev )
            self.raw_yellow_levenshtein_distances[self.idbnf].add( self.raw_yellow_lev )
            self.raw_green_levenshtein_distances[self.idbnf].add( self.raw_green_lev )
            self.finer_pink_levenshtein_distances[self.idbnf].add( self.fin_pink_lev )
            self.finer_yellow_levenshtein_distances[self.idbnf].add( self.fin_yellow_lev )
            self.finer_green_levenshtein_distances[self.idbnf].add( self.fin_green_lev )
            
        elif name == 'title':
            
            title = self.buf.split('/')
            self.book = re.search( 'Page:(.*)', title[0] ).group(1)
            self.pagen = int(title[1])
            self.idbnf = int(self.idsbnf[self.book])
            self.pages = self.nbpages[self.book]
            
            print self.book+'/'+str(self.pagen)
            
            # OCR?
            textocr = u''
            if os.path.exists( 'data/ocr/%07d'%self.idbnf ):
                self.isocr = True
                ocrfile = codecs.open( 'data/ocr/%07d/wikisourcepages/X%07d.ws.txt'%(self.idbnf,self.pagen), 'r', 'utf-8' )
                self.textocr = ocrfile.read()
                ocrfile.close()
                
                #print '----------------------------------------------------------------------'
                #print 'Texte OCR'
                #print '---------'
                #print self.textocr
            else:
                self.isocr = False
        
        elif name == 'revision':
            
            self.nbrev += 1
        
        elif name == 'timestamp':
            
            self.date = calendar.timegm( time.strptime( self.buf, '%Y-%m-%dT%H:%M:%SZ' ) )
            self.creation_date = self.date
        
        elif name == 'username':
            
            user = self.buf
            self.usernames.add(user)
            
            # User statistics
            if user not in self.userstats:
                self.userstats[user] = (0,set())
            
            (old_nbcontribs,old_timestamps) = self.userstats[user]
            old_timestamps.add(self.date)
            
            self.userstats[user] = (old_nbcontribs+1,old_timestamps)
            
            if not re.search( 'bot', user, re.IGNORECASE ):
                self.nbnonbotcontribs += 1
            
        
        elif name == 'ip':
            
            user = self.buf
            self.ips.add(user)
            
            # User statistics
            if user not in self.userstats:
                self.userstats[user] = (0,set())
            
            (old_nbcontribs,old_timestamps) = self.userstats[user]
            old_timestamps.add(self.date)
            
            self.userstats[user] = (old_nbcontribs+1,old_timestamps)
            
            self.nbnonbotcontribs += 1
        
        elif name == 'text':
            
            # Get the status
            text = self.buf
            pagequality = re.search( '<pagequality level="(\d)" user="(.*)" />', text )
            pagequality_level = -1
            pagequality_user = u''
            if not pagequality == None:
                pagequality_level = int(pagequality.group(1))
                pagequality_user  = pagequality.group(2)
            if pagequality_level == 2:   pagequality_level = 1 # problem
            elif pagequality_level == 0: pagequality_level = 2 # gray
            elif pagequality_level == 1: pagequality_level = 3 # pink
            elif pagequality_level == 3: pagequality_level = 4 # yellow
            elif pagequality_level == 4: pagequality_level = 5 # green
            
            if pagequality_level == 3 and (self.last_status == 4 or self.last_status == 5):
                self.nonlinearity = True
            elif pagequality_level == 4 and self.last_status == 5:
                self.nonlinearity = True
            elif pagequality_level == 5 and self.last_status == 3:
                self.nonlinearity = True
            
            self.last_status = pagequality_level
            if self.nbrev == 0:
                self.first_status = self.last_status
            
            if self.last_status == 2 and self.gray_date == 0:
                self.gray_date = self.date
            elif self.last_status == 3 and self.pink_date == 0:
                self.pink_date = self.date
            elif self.last_status == 4 and self.yellow_date == 0:
                self.yellow_date = self.date
            elif self.last_status == 5 and self.green_date == 0:
                self.green_date = self.date  
            
            if self.isocr and (self.last_status == 3 or self.last_status == 4 or self.last_status == 5):
                
                #print '----------------------------------------------------------------------'
                #print 'Raw text'
                #print '--------'
                #print text
                
                raw_levenshtein_distance = Levenshtein.distance( self.textocr, text )
                
                # Unwikify
                #untext = re.sub( '<noinclude>[\n ]*(.*)[\n ]*</noinclude>(.*)<noinclude>(.*)</noinclude>', '\1\n\2', text, re.DOTALL )
                resuntext = re.search( '<noinclude>.*</noinclude>(.*)<noinclude>.*</noinclude>', text, re.DOTALL )
                if not resuntext == None:
                    untext = resuntext.group(1)
                
                resuntext = re.search( '\'\'\'(.*)\'\'\'', untext )
                if not resuntext == None:
                    untext = resuntext.group(1)
                
                resuntext = re.search( '\'\'(.*)\'\'', untext )
                if not resuntext == None:
                    untext = resuntext.group(1)
                
                #refs = re.findall( '<ref.*>(.*)</ref>', untext )
                #untext = re.sub( '<ref.*>(.*)</ref>', '', untext )
                #if not refs == None:
                #    for ref in refs:
                #        untext += '\n'+ref
                
                #print '----------------------------------------------------------------------'
                #print 'Finer text'
                #print '----------'
                #print untext
                
                finer_levenshtein_distance = Levenshtein.distance( self.textocr, untext )
                
                if self.last_status == 3:
                    self.raw_pink_lev = raw_levenshtein_distance
                    self.fin_pink_lev = finer_levenshtein_distance
                elif self.last_status == 4:
                    self.raw_yellow_lev = raw_levenshtein_distance
                    self.fin_yellow_lev = finer_levenshtein_distance
                elif self.last_status == 5:
                    self.raw_green_lev = raw_levenshtein_distance
                    self.fin_green_lev = finer_levenshtein_distance
            
            

def createStatistics(xmlFilename,metadataFilename,pageResultsFilename,bookResultsFilename,userResultsFilename,alleResultsFilename):
    
    """
    Create statistics (see file_format.txt file) on the BnF partnership
    """
    
    # Open the files
    metadataFile  = codecs.open(metadataFilename,'r','utf-8')
    pageResultsFile = codecs.open(pageResultsFilename,'w','utf-8')
    bookResultsFile = codecs.open(bookResultsFilename,'w','utf-8')
    userResultsFile = codecs.open(userResultsFilename,'w','utf-8')
    alleResultsFile = codecs.open(alleResultsFilename,'w','utf-8')
    
    # Get the titles
    metadata = [ re.sub( '\r?\n', '', line ).split(' ') for line in metadataFile.readlines() ]
    idsbnf = dict()
    nbpages = dict()
    for book in metadata:
        key = re.sub('_',' ',book[0])
        idsbnf[key] = int(book[1])
        nbpages[key] = int(book[2])
    
    # Parse the XML
    h = PageStatisticsHandler(idsbnf,nbpages,pageResultsFile)
    saxparser = make_parser()
    saxparser.setContentHandler(h)
    saxparser.parse( xmlFilename )
    
    global_nbbooks = 0
    global_pages = 0
    global_nbrev = 0
    global_created_pages = 0
    global_uncreated_pages = 0
    global_nbgray = 0
    global_nbblue = 0
    global_nbpink = 0
    global_nbyellow = 0
    global_nbgreen = 0
    global_nbusernames = set()
    global_nbips = set()
    global_usernames = set()
    global_ips = set()
    global_nbnonbotcontribs = 0
    global_percentnonbotcontribs = 0
    
    global_mean_raw_pink_lev = set()
    global_mean_raw_yellow_lev = set()
    global_mean_raw_green_lev = set()
    global_cov_raw_pink_lev = set()
    global_cov_raw_yellow_lev = set()
    global_cov_raw_green_lev = set()
    
    global_mean_fin_pink_lev = set()
    global_mean_fin_yellow_lev = set()
    global_mean_fin_green_lev = set()
    global_cov_fin_pink_lev = set()
    global_cov_fin_yellow_lev = set()
    global_cov_fin_green_lev = set()
    
    # Create book statistics
    for k in h.books:
        
        ( idbnf, old_book, old_pages, old_nbrev, old_created_pages, old_uncreated_pages, old_nbgray, old_nbblue, old_nbpink, old_nbyellow, old_nbgreen, old_nbusernames, old_nbips, old_usernames, old_ips, old_mean_raw_pink_lev, old_mean_raw_yellow_lev, old_mean_raw_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev, old_mean_fin_pink_lev, old_mean_fir_yellow_lev, old_mean_fin_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev, old_nbnonbotcontribs, old_percentnonbotcontribs ) = h.books[k]
        
        # Compute
        mean_raw_pink_lev = int(mean(h.raw_pink_levenshtein_distances[idbnf]))
        mean_raw_yellow_lev = int(mean(h.raw_yellow_levenshtein_distances[idbnf]))
        mean_raw_green_lev = int(mean(h.raw_green_levenshtein_distances[idbnf]))
        cov_raw_pink_lev = int(standard_deviation(h.raw_pink_levenshtein_distances[idbnf]))
        cov_raw_yellow_lev = int(standard_deviation(h.raw_yellow_levenshtein_distances[idbnf]))
        cov_raw_green_lev = int(standard_deviation(h.raw_green_levenshtein_distances[idbnf]))
        
        mean_fin_pink_lev = int(mean(h.raw_pink_levenshtein_distances[idbnf]))
        mean_fin_yellow_lev = int(mean(h.raw_yellow_levenshtein_distances[idbnf]))
        mean_fin_green_lev = int(mean(h.raw_green_levenshtein_distances[idbnf]))
        cov_fin_pink_lev = int(standard_deviation(h.raw_pink_levenshtein_distances[idbnf]))
        cov_fin_yellow_lev = int(standard_deviation(h.raw_yellow_levenshtein_distances[idbnf]))
        cov_fin_green_lev = int(standard_deviation(h.raw_green_levenshtein_distances[idbnf]))
        
        percentnonbotcontribs = old_nbnonbotcontribs/old_nbrev
        
        # Global stats
        global_nbbooks += 1
        global_pages += old_pages
        global_nbrev += old_nbrev
        global_created_pages += old_created_pages
        global_uncreated_pages += old_uncreated_pages
        global_nbgray += old_nbgray
        global_nbblue += old_nbblue
        global_nbpink += old_nbpink
        global_nbyellow += old_nbyellow
        global_nbgreen += old_nbgreen
        global_nbusernames.add(old_nbusernames)
        global_nbips.add(old_nbips)
        global_usernames.update(old_usernames)
        global_ips.update(old_ips)
        global_nbnonbotcontribs += old_nbnonbotcontribs
        
        global_mean_raw_pink_lev.add(mean_raw_pink_lev)
        global_mean_raw_yellow_lev.add(mean_raw_yellow_lev)
        global_mean_raw_green_lev.add(mean_raw_green_lev)
        global_cov_raw_pink_lev.add(cov_raw_pink_lev)
        global_cov_raw_yellow_lev.add(cov_raw_yellow_lev)
        global_cov_raw_green_lev.add(cov_raw_green_lev)
        
        global_mean_fin_pink_lev.add(mean_fin_pink_lev)
        global_mean_fin_yellow_lev.add(mean_fin_yellow_lev)
        global_mean_fin_green_lev.add(mean_fin_green_lev)
        global_cov_fin_pink_lev.add(cov_fin_pink_lev)
        global_cov_fin_yellow_lev.add(cov_fin_yellow_lev)
        global_cov_fin_green_lev.add(cov_fin_green_lev)
        
        h.books[idbnf] = ( str(idbnf), re.sub(' ','_',old_book), str(old_pages), str(old_nbrev), str(old_created_pages), str(old_uncreated_pages), str(old_nbgray), str(old_nbblue), str(old_nbpink), str(old_nbyellow), str(old_nbgreen), str(len(old_usernames)), str(len(old_ips)), re.sub(' ','_',u'|'.join(old_usernames)), re.sub(' ','_',u'|'.join(old_ips)), str(mean_raw_pink_lev), str(mean_raw_yellow_lev), str(mean_raw_green_lev), str(cov_raw_pink_lev), str(cov_raw_yellow_lev), str(cov_raw_green_lev), str(mean_fin_pink_lev), str(mean_fin_yellow_lev), str(mean_fin_green_lev), str(cov_fin_pink_lev), str(cov_fin_yellow_lev), str(cov_fin_green_lev), str(old_nbnonbotcontribs), str(percentnonbotcontribs) )
        
        # Save results for the book
        bookResultsFile.write( u' '.join(h.books[idbnf]) )
        bookResultsFile.write( u'\n' )
    
    mean_global_mean_raw_pink_lev = int(mean(global_mean_raw_pink_lev))
    mean_global_mean_raw_yellow_lev = int(mean(global_mean_raw_yellow_lev))
    mean_global_mean_raw_green_lev = int(mean(global_mean_raw_green_lev))
    mean_global_cov_raw_pink_lev = int(mean(global_cov_raw_pink_lev))
    mean_global_cov_raw_yellow_lev = int(mean(global_cov_raw_yellow_lev))
    mean_global_cov_raw_green_lev = int(mean(global_cov_raw_green_lev))
    
    mean_global_mean_fin_pink_lev = int(mean(global_mean_fin_pink_lev))
    mean_global_mean_fin_yellow_lev = int(mean(global_mean_fin_yellow_lev))
    mean_global_mean_fin_green_lev = int(mean(global_mean_fin_green_lev))
    mean_global_cov_fin_pink_lev = int(mean(global_cov_fin_pink_lev))
    mean_global_cov_fin_yellow_lev = int(mean(global_cov_fin_yellow_lev))
    mean_global_cov_fin_green_lev = int(mean(global_cov_fin_green_lev))
    
    alleResultsFile.write( u' '.join( ( str(global_nbbooks), str(global_pages), str(global_pages/global_nbbooks), str(global_nbrev), str(global_created_pages), str(global_uncreated_pages), str(global_nbgray), str(global_nbblue), str(global_nbpink), str(global_nbyellow), str(global_nbgreen), str(mean(global_nbusernames)), str(mean(global_nbips)), re.sub(' ','_',u'|'.join(global_usernames)), re.sub(' ','_',u'|'.join(global_ips)), str(mean_global_mean_raw_pink_lev), str(mean_global_mean_raw_yellow_lev), str(mean_global_mean_raw_green_lev), str(mean_global_cov_raw_pink_lev), str(mean_global_cov_raw_yellow_lev), str(mean_global_cov_raw_green_lev), str(mean_global_mean_fin_pink_lev), str(mean_global_mean_fin_yellow_lev), str(mean_global_mean_fin_green_lev), str(mean_global_cov_fin_pink_lev), str(mean_global_cov_fin_yellow_lev), str(mean_global_cov_fin_green_lev), str(global_nbnonbotcontribs), str(global_nbnonbotcontribs/global_nbrev) ) ) )
    
    # Write user statistics
    for user in h.userstats:
        
        (nbcontribs,timestamps) = h.userstats[user]
        str_timestamps = [ str(t) for t in timestamps ]
        userResultsFile.write( u' '.join( ( user, str(nbcontribs), u'|'.join(str_timestamps) ) ) )
        userResultsFile.write( u'\n' )
    
    # Close files
    metadataFile.close()
    pageResultsFile.close()
    bookResultsFile.close()
    userResultsFile.close()
    alleResultsFile.close()

def mean(rv):
    
    return sum(rv)/len(rv)

def standard_deviation(rv):
    
    m = sum(rv)/len(rv)
    if len(rv) == 0:
        return None
    elif len(rv) == 1:
        return 0
    else:
        return math.sqrt(sum( [ (x-m)**2 for x in rv ] ) / (len(rv)-1))

createStatistics( 'frwikisource-bnf-20101003-page.xml', 'metadata-stats.txt', 'frwikisource-statistics-20101003-page.txt', 'frwikisource-statistics-20101003-book.txt', 'frwikisource-statistics-20101003-user.txt', 'frwikisource-statistics-20101003-alle.txt' )

