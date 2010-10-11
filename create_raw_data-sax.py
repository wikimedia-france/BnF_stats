# -*- coding:utf-8 -*-

import codecs, re, calendar, time, math, os, os.path, Levenshtein, urllib, xml.dom.minidom
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import quoteattr
from xml.sax import make_parser

class PageStatisticsHandler(ContentHandler):
    
    idsbnf = []
    nbpages = []
    pageResultsFile = None
    bookResultsFile = None
    blacklistTitles = []
    
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
    raw_pink_lev = -1
    fin_pink_lev = -1
    raw_yellow_lev = -1
    fin_yellow_lev = -1
    raw_green_lev = -1
    fin_green_lev = -1
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
    
    def __init__(self,idsbnf,nbpages,blacklistTitles,pageResultsFile):
        
        # Input data and output files
        self.idsbnf = idsbnf
        self.nbpages = nbpages
        self.pageResultsFile = pageResultsFile
        self.blacklistTitles = []
        
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
        self.raw_pink_lev = -1
        self.fin_pink_lev = -1
        self.raw_yellow_lev = -1
        self.fin_yellow_lev = -1
        self.raw_green_lev = -1
        self.fin_green_lev = -1
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
            self.raw_pink_lev = -1
            self.fin_pink_lev = -1
            self.raw_yellow_lev = -1
            self.fin_yellow_lev = -1
            self.raw_green_lev = -1
            self.fin_green_lev = -1
            self.nbnonbotcontribs = 0
    
    def characters(self,ch):
        
        self.buf += ch
    
    def endElement(self,name):
        
        if name == 'page':
            
            if self.book in self.blacklistTitles or self.book+'/'+str(self.pagen) in self.blacklistTitles:
                return
            
            # Page statistics
            
            result_page = [ str(self.idbnf), re.sub(' ','_',self.book), str(self.pages), str(self.pagen), str(self.nbrev), str(self.creation_date), str(self.first_status), str(self.last_status), str(len(self.usernames)), str(len(self.ips)), re.sub(' ','_',u'|'.join(self.usernames)), re.sub(' ','_',u'|'.join(self.ips)), str(self.gray_date), str(self.pink_date), str(self.yellow_date), str(self.green_date), str(self.nonlinearity), str(self.isocr), str(self.raw_pink_lev), str(self.raw_yellow_lev), str(self.raw_green_lev), str(self.fin_pink_lev), str(self.fin_yellow_lev), str(self.fin_green_lev) ]
            
            if len(self.usernames) == 0:
                result_page[10] = '|'
            if len(self.ips) == 0:
                result_page[11] = '|'
            
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
                
                self.books[self.idbnf] = ( self.idbnf, self.book, self.pages, self.nbrev, 1, self.pages-1, nbblue, nbgray, nbpink, nbyellow, nbgreen, len(self.usernames), len(self.ips), self.usernames, self.ips, self.isocr, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, self.nbnonbotcontribs, 0.0 )
            
            else:
                
                ( old_idbnf, old_book, old_pages, old_nbrev, old_created_pages, old_uncreated_pages, old_nbgray, old_nbblue, old_nbpink, old_nbyellow, old_nbgreen, old_nbusernames, old_nbips, old_usernames, old_ips, old_isocr, old_mean_raw_pink_lev, old_mean_raw_yellow_lev, old_mean_raw_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev, old_min_mean_raw_pink_lev, old_min_mean_raw_yellow_lev, old_min_mean_raw_green_lev, old_max_mean_raw_pink_lev, old_max_mean_raw_yellow_lev, old_max_mean_raw_green_lev, old_mean_fin_pink_lev, old_mean_fir_yellow_lev, old_mean_fin_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev, old_min_mean_fin_pink_lev, old_min_mean_fin_yellow_lev, old_min_mean_fin_green_lev, old_max_mean_fin_pink_lev, old_max_mean_fin_yellow_lev, old_max_mean_fin_green_lev, old_nbnonbotcontribs, old_percentnonbotcontribs ) = self.books[self.idbnf]
                
                old_usernames.update( self.usernames )
                old_ips.update( self.ips )
                
                self.books[self.idbnf] = ( old_idbnf, old_book, old_pages, old_nbrev+self.nbrev, old_created_pages+1, old_uncreated_pages-1, old_nbgray+nbgray, old_nbblue+nbblue, old_nbpink+nbpink, old_nbyellow+nbyellow, old_nbgreen+nbgreen, len(old_usernames), len(old_ips), old_usernames, old_ips, old_isocr, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, old_nbnonbotcontribs+self.nbnonbotcontribs, old_percentnonbotcontribs )
            
            # Add Levenshtein distances to the ensembles
            if self.idbnf not in self.raw_pink_levenshtein_distances: self.raw_pink_levenshtein_distances[self.idbnf] = []
            if self.idbnf not in self.raw_yellow_levenshtein_distances: self.raw_yellow_levenshtein_distances[self.idbnf] = []
            if self.idbnf not in self.raw_green_levenshtein_distances: self.raw_green_levenshtein_distances[self.idbnf] = []
            if self.idbnf not in self.finer_pink_levenshtein_distances: self.finer_pink_levenshtein_distances[self.idbnf] = []
            if self.idbnf not in self.finer_yellow_levenshtein_distances: self.finer_yellow_levenshtein_distances[self.idbnf] = []
            if self.idbnf not in self.finer_green_levenshtein_distances: self.finer_green_levenshtein_distances[self.idbnf] = []
            
            if self.raw_pink_lev != -1 : self.raw_pink_levenshtein_distances[self.idbnf].append( self.raw_pink_lev )
            if self.raw_yellow_lev != -1 : self.raw_yellow_levenshtein_distances[self.idbnf].append( self.raw_yellow_lev )
            if self.raw_green_lev != -1 : self.raw_green_levenshtein_distances[self.idbnf].append( self.raw_green_lev )
            if self.fin_pink_lev != -1 : self.finer_pink_levenshtein_distances[self.idbnf].append( self.fin_pink_lev )
            if self.fin_yellow_lev != -1 : self.finer_yellow_levenshtein_distances[self.idbnf].append( self.fin_yellow_lev )
            if self.fin_green_lev != -1 : self.finer_green_levenshtein_distances[self.idbnf].append( self.fin_green_lev )
        
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
            
            if self.book in self.blacklistTitles or self.book+'/'+str(self.pagen) in self.blacklistTitles:
                return
            
            self.nbrev += 1
        
        elif name == 'timestamp':
            
            if self.book in self.blacklistTitles or self.book+'/'+str(self.pagen) in self.blacklistTitles:
                return
            
            self.date = calendar.timegm( time.strptime( self.buf, '%Y-%m-%dT%H:%M:%SZ' ) )
            self.creation_date = self.date
        
        elif name == 'username':
            
            if self.book in self.blacklistTitles or self.book+'/'+str(self.pagen) in self.blacklistTitles:
                return
            
            user = self.buf
            self.usernames.add(user)
            
            # User statistics
            if user not in self.userstats:
                self.userstats[user] = (0,False,[])
            
            (old_nbcontribs,old_ip,old_timestamps) = self.userstats[user]
            old_timestamps.append(self.date)
            
            self.userstats[user] = (old_nbcontribs+1,False,old_timestamps)
            
            if not re.search( 'bot', user, re.IGNORECASE ):
                self.nbnonbotcontribs += 1
            
        
        elif name == 'ip':
            
            if self.book in self.blacklistTitles or self.book+'/'+str(self.pagen) in self.blacklistTitles:
                return
            
            user = self.buf
            self.ips.add(user)
            
            # User statistics
            if user not in self.userstats:
                self.userstats[user] = (0,True,[])
            
            (old_nbcontribs,old_ip,old_timestamps) = self.userstats[user]
            old_timestamps.append(self.date)
            
            self.userstats[user] = (old_nbcontribs+1,True,old_timestamps)
            
            self.nbnonbotcontribs += 1
        
        elif name == 'text':
            
            if self.book in self.blacklistTitles or self.book+'/'+str(self.pagen) in self.blacklistTitles:
                return
            
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
                #print 'raw lev dist=%d'%raw_levenshtein_distance
                
                # Unwikify
                #untext = re.sub( '<noinclude>[\n ]*(.*)[\n ]*</noinclude>(.*)<noinclude>(.*)</noinclude>', '\1\n\2', text, re.DOTALL )
                resuntext = re.search( '<noinclude>.*?</noinclude>(.*)<noinclude>.*?</noinclude>', text, re.DOTALL )
                if not resuntext == None:
                    untext = resuntext.group(1)
                
                bold = re.findall( "'''(.*?)'''", untext, re.DOTALL )
                for res in bold:
                    untext = re.sub( protect_regex("'''(%s)'''"%res), "\\1", untext )
                
                italics = re.findall( "''(.*?)''", untext, re.DOTALL )
                for res in italics:
                    untext = re.sub( protect_regex("''(%s)''"%res), "\\1", untext )
                
                refs = re.findall( "<ref(.*?)>(.*?)</ref>", untext, re.DOTALL )
                for res in refs:
                    #print '***'
                    #print res
                    #print "\n"
                    untext = re.sub( protect_regex("<ref%s>%s</ref>"%res), "", untext )
                    untext += '\n'+res[1]
                
                #print '----------------------------------------------------------------------'
                #print 'Finer text'
                #print '----------'
                #print untext
                
                finer_levenshtein_distance = Levenshtein.distance( self.textocr, untext )
                
                #print 'finer lev dist=%d'%finer_levenshtein_distance
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
    h = PageStatisticsHandler(idsbnf,nbpages,[],pageResultsFile)
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
    global_nbusernames = []
    global_nbips = []
    global_usernames = set()
    global_ips = set()
    global_isocr = 0
    global_nbnonbotcontribs = 0
    global_percentnonbotcontribs = 0
    
    global_mean_raw_pink_lev = []
    global_mean_raw_yellow_lev = []
    global_mean_raw_green_lev = []
    global_cov_raw_pink_lev = []
    global_cov_raw_yellow_lev = []
    global_cov_raw_green_lev = []
    
    global_mean_fin_pink_lev = []
    global_mean_fin_yellow_lev = []
    global_mean_fin_green_lev = []
    global_cov_fin_pink_lev = []
    global_cov_fin_yellow_lev = []
    global_cov_fin_green_lev = []
    
    # Create book statistics
    for k in h.books:
        
        ( idbnf, old_book, old_pages, old_nbrev, old_created_pages, old_uncreated_pages, old_nbgray, old_nbblue, old_nbpink, old_nbyellow, old_nbgreen, old_nbusernames, old_nbips, old_usernames, old_ips, old_isocr, old_mean_raw_pink_lev, old_mean_raw_yellow_lev, old_mean_raw_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev, old_min_mean_raw_pink_lev, old_min_mean_raw_yellow_lev, old_min_mean_raw_green_lev, old_max_mean_raw_pink_lev, old_max_mean_raw_yellow_lev, old_max_mean_raw_green_lev, old_mean_fin_pink_lev, old_mean_fir_yellow_lev, old_mean_fin_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev, old_min_mean_fin_pink_lev, old_min_mean_fin_yellow_lev, old_min_mean_fin_green_lev, old_max_mean_fin_pink_lev, old_max_mean_fin_yellow_lev, old_max_mean_fin_green_lev, old_nbnonbotcontribs, old_percentnonbotcontribs ) = h.books[k]
        
        # Compute
        mean_raw_pink_lev = int(mean(h.raw_pink_levenshtein_distances[idbnf]))
        mean_raw_yellow_lev = int(mean(h.raw_yellow_levenshtein_distances[idbnf]))
        mean_raw_green_lev = int(mean(h.raw_green_levenshtein_distances[idbnf]))
        cov_raw_pink_lev = int(standard_deviation(h.raw_pink_levenshtein_distances[idbnf]))
        cov_raw_yellow_lev = int(standard_deviation(h.raw_yellow_levenshtein_distances[idbnf]))
        cov_raw_green_lev = int(standard_deviation(h.raw_green_levenshtein_distances[idbnf]))
        
        mean_fin_pink_lev = int(mean(h.finer_pink_levenshtein_distances[idbnf]))
        mean_fin_yellow_lev = int(mean(h.finer_yellow_levenshtein_distances[idbnf]))
        mean_fin_green_lev = int(mean(h.finer_green_levenshtein_distances[idbnf]))
        cov_fin_pink_lev = int(standard_deviation(h.finer_pink_levenshtein_distances[idbnf]))
        cov_fin_yellow_lev = int(standard_deviation(h.finer_yellow_levenshtein_distances[idbnf]))
        cov_fin_green_lev = int(standard_deviation(h.finer_green_levenshtein_distances[idbnf]))
        
        min_mean_raw_pink_lev = mine(h.raw_pink_levenshtein_distances[idbnf])
        min_mean_raw_yellow_lev = mine(h.raw_yellow_levenshtein_distances[idbnf])
        min_mean_raw_green_lev = mine(h.raw_green_levenshtein_distances[idbnf])
        max_mean_raw_pink_lev = maxe(h.raw_pink_levenshtein_distances[idbnf])
        max_mean_raw_yellow_lev = maxe(h.raw_yellow_levenshtein_distances[idbnf])
        max_mean_raw_green_lev = maxe(h.raw_green_levenshtein_distances[idbnf])
        
        min_mean_fin_pink_lev = mine(h.finer_pink_levenshtein_distances[idbnf])
        min_mean_fin_yellow_lev = mine(h.finer_yellow_levenshtein_distances[idbnf])
        min_mean_fin_green_lev = mine(h.finer_green_levenshtein_distances[idbnf])
        max_mean_fin_pink_lev = maxe(h.finer_pink_levenshtein_distances[idbnf])
        max_mean_fin_yellow_lev = maxe(h.finer_yellow_levenshtein_distances[idbnf])
        max_mean_fin_green_lev = maxe(h.finer_green_levenshtein_distances[idbnf])
        
        #if k == 5085:
        #    print h.finer_pink_levenshtein_distances[idbnf]
        #    print h.finer_yellow_levenshtein_distances[idbnf]
        #    print h.finer_green_levenshtein_distances[idbnf]
        
        percentnonbotcontribs = float(old_nbnonbotcontribs)/float(old_nbrev)*100
        
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
        global_nbusernames.append(old_nbusernames)
        global_nbips.append(old_nbips)
        global_usernames.update(old_usernames)
        global_ips.update(old_ips)
        global_nbnonbotcontribs += old_nbnonbotcontribs
        
        if old_isocr:
            global_isocr += 1
        
        global_mean_raw_pink_lev.append(mean_raw_pink_lev)
        global_mean_raw_yellow_lev.append(mean_raw_yellow_lev)
        global_mean_raw_green_lev.append(mean_raw_green_lev)
        global_cov_raw_pink_lev.append(cov_raw_pink_lev)
        global_cov_raw_yellow_lev.append(cov_raw_yellow_lev)
        global_cov_raw_green_lev.append(cov_raw_green_lev)
        
        global_mean_fin_pink_lev.append(mean_fin_pink_lev)
        global_mean_fin_yellow_lev.append(mean_fin_yellow_lev)
        global_mean_fin_green_lev.append(mean_fin_green_lev)
        global_cov_fin_pink_lev.append(cov_fin_pink_lev)
        global_cov_fin_yellow_lev.append(cov_fin_yellow_lev)
        global_cov_fin_green_lev.append(cov_fin_green_lev)
        
        h.books[idbnf] = [ str(idbnf), re.sub(' ','_',old_book), str(old_pages), str(old_nbrev), str(old_created_pages), str(old_uncreated_pages), str(old_nbgray), str(old_nbblue), str(old_nbpink), str(old_nbyellow), str(old_nbgreen), str(len(old_usernames)), str(len(old_ips)), re.sub(' ','_',u'|'.join(old_usernames)), re.sub(' ','_',u'|'.join(old_ips)), str(old_isocr), str(mean_raw_pink_lev), str(mean_raw_yellow_lev), str(mean_raw_green_lev), str(cov_raw_pink_lev), str(cov_raw_yellow_lev), str(cov_raw_green_lev), str(min_mean_raw_pink_lev), str(min_mean_raw_yellow_lev), str(min_mean_raw_green_lev), str(max_mean_raw_pink_lev), str(max_mean_raw_yellow_lev), str(max_mean_raw_green_lev), str(mean_fin_pink_lev), str(mean_fin_yellow_lev), str(mean_fin_green_lev), str(cov_fin_pink_lev), str(cov_fin_yellow_lev), str(cov_fin_green_lev), str(min_mean_fin_pink_lev), str(min_mean_fin_yellow_lev), str(min_mean_fin_green_lev), str(max_mean_fin_pink_lev), str(max_mean_fin_yellow_lev), str(max_mean_fin_green_lev), str(old_nbnonbotcontribs), str(percentnonbotcontribs) ]
        
        if len(old_usernames) == 0:
            h.books[idbnf][13] = '|'
        if len(old_ips) == 0:
            h.books[idbnf][14] = '|'
        
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
    
    min_global_mean_raw_pink_lev = mine(global_mean_raw_pink_lev)
    min_global_mean_raw_yellow_lev = mine(global_mean_raw_yellow_lev)
    min_global_mean_raw_green_lev = mine(global_mean_raw_green_lev)
    max_global_mean_raw_pink_lev = maxe(global_mean_raw_pink_lev)
    max_global_mean_raw_yellow_lev = maxe(global_mean_raw_yellow_lev)
    max_global_mean_raw_green_lev = maxe(global_mean_raw_green_lev)
    
    min_global_mean_fin_pink_lev = mine(global_mean_fin_pink_lev)
    min_global_mean_fin_yellow_lev = mine(global_mean_fin_yellow_lev)
    min_global_mean_fin_green_lev = mine(global_mean_fin_green_lev)
    max_global_mean_fin_pink_lev = maxe(global_mean_fin_pink_lev)
    max_global_mean_fin_yellow_lev = maxe(global_mean_fin_yellow_lev)
    max_global_mean_fin_green_lev = maxe(global_mean_fin_green_lev)
    
    if len(global_usernames) == 0:
        global_usernames = ['|']
    if len(global_ips) == 0:
        global_ips = ['|']
    
    alleResultsFile.write( u' '.join( ( str(global_nbbooks), str(global_pages), str(float(global_pages)/float(global_nbbooks)), str(global_nbrev), str(global_created_pages), str(global_uncreated_pages), str(global_nbgray), str(global_nbblue), str(global_nbpink), str(global_nbyellow), str(global_nbgreen), str(mean(global_nbusernames)), str(mean(global_nbips)), re.sub(' ','_',u'|'.join(global_usernames)), re.sub(' ','_',u'|'.join(global_ips)), str(global_isocr), str(mean_global_mean_raw_pink_lev), str(mean_global_mean_raw_yellow_lev), str(mean_global_mean_raw_green_lev), str(mean_global_cov_raw_pink_lev), str(mean_global_cov_raw_yellow_lev), str(mean_global_cov_raw_green_lev), str(min_global_mean_raw_pink_lev), str(min_global_mean_raw_yellow_lev), str(min_global_mean_raw_green_lev), str(max_global_mean_raw_pink_lev), str(max_global_mean_raw_yellow_lev), str(max_global_mean_raw_green_lev), str(mean_global_mean_fin_pink_lev), str(mean_global_mean_fin_yellow_lev), str(mean_global_mean_fin_green_lev), str(mean_global_cov_fin_pink_lev), str(mean_global_cov_fin_yellow_lev), str(mean_global_cov_fin_green_lev), str(min_global_mean_fin_pink_lev), str(min_global_mean_fin_yellow_lev), str(min_global_mean_fin_green_lev), str(max_global_mean_fin_pink_lev), str(max_global_mean_fin_yellow_lev), str(max_global_mean_fin_green_lev), str(global_nbnonbotcontribs), str(float(global_nbnonbotcontribs)/float(global_nbrev)*100) ) ) )
    
    global_nbcontributors = 0
    global_editcount = []
    global_nbcontribs = []
    global_min_timestamp = []
    global_max_timestamp = []
    global_quartile_1 = []
    global_quartile_2 = []
    global_quartile_3 = []
    
    # Write user statistics
    for user in h.userstats:
        
        (nbcontribs,ip,timestamps) = h.userstats[user]
        global_nbcontributors += 1
        global_nbcontribs.append(nbcontribs)
        
        print user
        
        # Get the editcount
        editcount = 0
        if not ip:
            xmlString = urllib.urlopen('http://fr.wikisource.org/w/api.php?action=query&list=allusers&auprop=editcount&aulimit=1&format=xml&aufrom='+urllib.quote(user.encode('utf-8'))).read()
            domxml = xml.dom.minidom.parseString( xmlString )
            editcount = int(domxml.getElementsByTagName('u').item(0).getAttribute('editcount'))
            global_editcount.append(editcount)
        
        # Sort timestamps
        timestamps.sort()
        min_timestamp = min(timestamps)
        max_timestamp = max(timestamps)
        quartile_1 = timestamps[int(len(timestamps)*float(1)/float(4))]
        quartile_2 = timestamps[int(len(timestamps)*float(1)/float(2))]
        quartile_3 = timestamps[int(len(timestamps)*float(3)/float(4))]
        
        global_min_timestamp.append(min_timestamp)
        global_max_timestamp.append(max_timestamp)
        global_quartile_1.append(quartile_1)
        global_quartile_2.append(quartile_2)
        global_quartile_3.append(quartile_3)
        
        str_timestamps = [ str(t) for t in timestamps ]
        userResultsFile.write( u' '.join( ( user, str(editcount), str(nbcontribs), u'|'.join(str_timestamps), str(min_timestamp), str(max_timestamp), str(quartile_1), str(quartile_2), str(quartile_3) ) ) )
        userResultsFile.write( u'\n' )
        
        time.sleep(1)
    
    # Global user stats
    
    alleResultsFile.write( '\n' )
    alleResultsFile.write( u' '.join( ( str(global_nbcontributors), str(int(mean(global_editcount))), str(int(mean(global_nbcontribs))), str(int(mean(global_min_timestamp))), str(int(mean(global_max_timestamp))), str(int(mean(global_quartile_1))), str(int(mean(global_quartile_2))), str(int(mean(global_quartile_3))), str(int(standard_deviation(global_quartile_1))), str(int(standard_deviation(global_quartile_2))), str(int(standard_deviation(global_quartile_3))) ) ) )
    
    # Close files
    metadataFile.close()
    pageResultsFile.close()
    bookResultsFile.close()
    userResultsFile.close()
    alleResultsFile.close()

def mean(rv):
    
    if len(rv) == 0:
        return -1
    else:
        return float(sum(rv))/len(rv)

def mine(rv):
    
    if len(rv) == 0:
        return -1
    else:
        return min(rv)

def maxe(rv):
    
    if len(rv) == 0:
        return 0
    else:
        return max(rv)

def standard_deviation(rv):
    
    m = mean(rv)
    if len(rv) == 0:
        return 0
    else:
        return math.sqrt(sum( [ (float(x)-m)**2 for x in rv ] ) / len(rv))

def protect_regex(string):
    
    res = re.sub( '\(', '\\(', string )
    res = re.sub( '\)', '\\)', res )
    res = re.sub( '\|', '\\|', res )
    res = re.sub( '\[', '\\[', res )
    res = re.sub( '\]', '\\]', res )
    res = re.sub( '\{', '\\{', res )
    res = re.sub( '\}', '\\}', res )
    res = re.sub( '\.', '\\.', res )
    res = re.sub( '\*', '\\*', res )
    res = re.sub( '\?', '\\?', res )
    res = re.sub( '\+', '\\+', res )
    res = re.sub( '\^', '\\^', res )
    res = re.sub( '\\[0-9AbBdDsSwWZ]', '\\\\0', res )
    return res

createStatistics( 'frwikisource-bnf-20101003-page.xml', 'metadata-stats.txt', 'frwikisource-statistics-20101003-page.txt', 'frwikisource-statistics-20101003-book.txt', 'frwikisource-statistics-20101003-20101011-user.txt', 'frwikisource-statistics-20101003-20101011-alle.txt' )

