# -*- coding:utf-8 -*-

import xml.dom.minidom, codecs, re, time, calendar, math

def createStatistics(xmlFilename,metadataFilename,pageResultsFilename,bookResultsFilename):
    
    """
    Create statistics (see file_format.txt file) on the BnF partnership
    """
    
    # Open the files
    xmlFile = codecs.open(xmlFilename,'r','utf-8')
    metadataFile  = codecs.open(metadataFilename,'r','utf-8')
    pageResultsFile = codecs.open(pageResultsFilename,'w','utf-8')
    bookResultsFile = codecs.open(bookResultsFilename,'w','utf-8')
    
    # Parse the XML
    xmlString = xmlFile.read().encode('utf-8')
    domxml = xml.dom.minidom.parseString( xmlString )
    
    # Get the metadata
    metadatalist = [ re.sub( '\r?\n', '', line ).split(' ') for line in metadataFile.readlines() ]
    idsbnf = dict()
    nbpages = dict()
    for book in metadatalist :
        idsbnf[book[0]] = int(book[1])
        nbpages[book[0]] = int(book[2])
    
    # Initialize the book variables
    books = dict()
    nbgray, nbblue, nbpink, nbyellow, nbgreen = 0, 0, 0, 0, 0
    raw_pink_levenshtein_distances = set()
    raw_yellow_levenshtein_distances = set()
    raw_green_levenshtein_distances = set()
    finer_pink_levenshtein_distances = set()
    finer_yellow_levenshtein_distances = set()
    finer_green_levenshtein_distances = set()
        
    # Remove unneeded pages
    for mediawiki in domxml.getElementsByTagName('mediawiki'):
        for page in mediawiki.getElementsByTagName('page'):
            
            # Get the title
            title = page.getElementsByTagName('title').item(0).firstChild.data.split('/')
            
            # Initialize the page variables
            book = re.sub( 'Page:(.*)', '\1', title[0] )
            pagen = int(title[1])
            idbnf = idsbnf[title[0]]
            pages = nbpages[title[0]]
            usernames = set()
            ips = set()
            first_status = 0
            last_status = 0
            nonlinearity = False
            nbrev = 0
            creation_date = 0
            pink_date = 0
            yellow_date = 0
            green_date = 0
            ocr = False
            
            # OCR?
            textocr = u''
            try:
                os.listdir(str(idbnf)+'/wikisource')
                ocr = True
                ocrfile = codecs.open( '%d/wikisource/X%07d.txt'%(idbnf,page), 'r', 'utf-8' )
                textocr = ocrfile.read()
                ocrfile.close()
            except:
                ocr = False
            
            # Harvest the revisions
            for revision in page.getElementsByTagName('revision'):
                
                # Number of revisions
                nbrev += 1
                
                # Add the contributor to the list
                contributor = revision.getElementsByTagName('contributor').item(0).firstChild.data
                ip = contributor.getElementsByTagName('ip')
                username = contributor.getElementsByTagName('username')
                if ip.length > 0:
                    ip = ip.item(0).firstChild.data
                    ips.add(ip)
                elif username.length > 0:
                    username = username.item(0).firstChild.data
                    usernames.add(username)
                
                # Get the status
                text = revision.getElementsByTagName('text').item(0).firstChild.data
                pagequality = re.search( '<pagequality level="(\d)" user="(.*)" />', text )
                pagequality_level = int(pagequality.group(1))
                pagequality_user  = pagequality.group(2)
                if pagequality_level == 2:   pagequality_level = 1 # problem
                elif pagequality_level == 0: pagequality_level = 2 # gray
                elif pagequality_level == 1: pagequality_level = 3 # pink
                elif pagequality_level == 3: pagequality_level = 4 # yellow
                elif pagequality_level == 4: pagequality_level = 5 # green
                
                if pagequality_level == 3 and (last_status == 4 or last_status == 5):
                    nonlinearity = True
                elif pagequality_level == 4 and last_status == 5:
                    nonlinearity = True
                elif pagequality_level == 5 and last_status == 3:
                    nonlinearity = True
                
                last_status = pagequality_level
                if nbrev == 1:
                    first_status = last_status
                
                # Dates
                date = calendar.timegm( time.strptime( revision.getElementsByTagName('timestamp').item(0).firstChild.data, '%Y-%m-%dT%H:%M:%SZ' ) )
                
                if last_status == 2:
                    gray_status = date
                elif last_status == 3:
                    pink_date = date
                elif last_status == 4:
                    yellow_date = date
                elif last_status == 5:
                    green_date = date
                
                if nbref == 1:
                    creation_date = date
                
                # Levenshtein distance
                if isocr and (last_status == 3 or last_status == 4 or last_status == 5):
                    
                    text = revision.getElementsByTagName('text').item(0).firstChild.data
                    
                    raw_levenshtein_distance = Levenshtein.distance( textocr, text )
                    
                    # Unwikify
                    untext = re.sub( '<noinclude>[\n ]*(.*)[\n ]*</noinclude>(.*)<noinclude>(.*)</noinclude>', '\1\n\2', text, re.DOTALL )
                    untext = re.sub( '\'\'\'(.*)\'\'\'', '\1', untext )
                    untext = re.sub( '\'\'(.*)\'\'', '\1', untext )
                    untext = re.sub( '{{Centré|(.*)}}', '\1', untext )
                    
                    refs = re.search( '<ref.*>(.*)</ref>', untext )
                    for ref in refs:
                        untext = re.sub( '<ref.*>(.*)</ref>', '', untext )
                        untext += '\n'+ref
                    
                    finner_levenshtein_distance = Levenshtein.distance( textocr, untext )
                    
                    
                    if last_status == 3:
                        raw_pink_lev = raw_levenshtein_distance
                        fin_pink_lev = finer_levenshtein_distance
                    elif last_status == 4:
                        raw_yellow_lev = raw_levenshtein_distance
                        fin_yellow_lev = finer_levenshtein_distance
                    elif last_status == 5:
                        raw_green_lev = raw_levenshtein_distance
                        fin_green_lev = finer_levenshtein_distance
            
            # Save result of the page
            #result = '%d %s %d %d %d %d %d %d %s %s %d %d %d %d %d %d %d %d %d %d %d %d\n'%(idbnf, book, pages, page, nbrev, creation_date, first_status, last_status, u'|'.join(usernames), u'|'.join(ips), gray_date, pink_date, yellow_date, green_date, nonlinearity, isocr, raw_pink_lev, raw_yellow_lev, raw_green_lev, fin_pink_lev, fin_yellow_lev, fin_green_lev)
            result_page = (idbnf, book, pages, pagen, nbrev, creation_date, first_status, last_status, u'|'.join(usernames), u'|'.join(ips), gray_date, pink_date, yellow_date, green_date, nonlinearity, isocr, raw_pink_lev, raw_yellow_lev, raw_green_lev, fin_pink_lev, fin_yellow_lev, fin_green_lev)
            
            pageResultsFile.write( u' '.join(result_page) )
            
            if last_status == 1: nbgray = 1
            if last_status == 2: nbblue = 1
            if last_status == 3: nbpink = 1
            if last_status == 4: nbyellow = 1
            if last_status == 5: nbgreen = 1
            
            if idbnf not in books:
                
                books[idbnf] = ( idbnf, book, pages, nbrev, 1, pages-1, nbgray, nbblue, nbpink, nbyellow, nbgreen, len(contributors), len(ips), u'|'.join(usernames), u'|'.join(ips), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 )
                
            else:
                
                ( old_idbnf, old_book, old_pages, old_nbrev, old_created_pages, old_uncreated_pages, old_nbgray, old_nbblue, old_nbpink, old_nbyellow, old_nbgreen, old_nbcontributors, old_nbips, old_usernames, old_ips, old_mean_raw_pink_lev, old_mean_raw_yellow_lev, old_mean_raw_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev, old_mean_fin_pink_lev, old_mean_fir_yellow_lev, old_mean_fin_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev ) = books[idbnf]
                
                old_usernames.update( usernames )
                old_ips.update( ips )
                
                books[idbnf] = ( old_idbnf, old_book, old_pages, old_nbrev+nbrev, old_created_pages+1, old_uncreated_pages-1, old_nbgray+nbgray, old_nbblue+nbblue, old_nbpink+nbpink, old_nbyellow+nbyellow, old_nbgreen+nbgreen, len(old_contributors), len(old_ips), old_contributors, old_ips, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 )
            
            # Add Levenshtein distances to the ensembles
            raw_pink_levenshtein_distances.add( raw_pink_lev )
            raw_yellow_levenshtein_distances.add( raw_yellow_lev )
            raw_green_levenshtein_distances.add( raw_green_lev )
            finer_pink_levenshtein_distances.add( finer_pink_lev )
            finer_yellow_levenshtein_distances.add( finer_yellow_lev )
            finer_green_levenshtein_distances.add( finer_green_lev )
    
    # Compute standard deviations of the Lenvenshtein distances
    for book in books:
        
        ( idbnf, old_book, old_pages, old_nbrev, old_created_pages, old_uncreated_pages, old_nbgray, old_nbblue, old_nbpink, old_nbyellow, old_nbgreen, old_nbcontributors, old_nbips, old_usernames, old_ips, old_mean_raw_pink_lev, old_mean_raw_yellow_lev, old_mean_raw_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev, old_mean_fin_pink_lev, old_mean_fir_yellow_lev, old_mean_fin_green_lev, old_cov_fin_pink_lev, old_cov_fin_yellow_lev, old_cov_fin_green_lev ) = book
        
        # Compute
        mean_raw_pink_lev = mean(raw_pink_levenshtein_distances[idbnf])
        mean_raw_yellow_lev = mean(raw_yellow_levenshtein_distances[idbnf])
        mean_raw_green_lev = mean(raw_green_levenshtein_distances[idbnf])
        cov_raw_pink_lev = standard_deviation(raw_pink_levenshtein_distances[idbnf])
        cov_raw_yellow_lev = standard_deviation(raw_yellow_levenshtein_distances[idbnf])
        cov_raw_green_lev = standard_deviation(raw_green_levenshtein_distances[idbnf])
        
        mean_fin_pink_lev = mean(raw_pink_levenshtein_distances[idbnf])
        mean_fin_yellow_lev = mean(raw_yellow_levenshtein_distances[idbnf])
        mean_fin_green_lev = mean(raw_green_levenshtein_distances[idbnf])
        cov_fin_pink_lev = standard_deviation(raw_pink_levenshtein_distances[idbnf])
        cov_fin_yellow_lev = standard_deviation(raw_yellow_levenshtein_distances[idbnf])
        cov_fin_green_lev = standard_deviation(raw_green_levenshtein_distances[idbnf])
        
        books[idbnf] = ( idbnf, old_book, old_pages, old_nbrev, old_created_pages, old_uncreated_pages, old_nbgray, old_nbblue, old_nbpink, old_nbyellow, old_nbgreen, len(old_contributors), len(old_ips), old_contributors, old_ips, mean_raw_pink_lev, mean_raw_yellow_lev, mean_raw_green_lev, cov_raw_pink_lev, cov_raw_yellow_lev, cov_raw_green_lev, mean_fin_pink_lev, mean_fin_yellow_lev, mean_fin_green_lev, cov_fin_pink_lev, cov_fin_yellow_lev, cov_fin_green_lev )
        
        # Save results for the book
        bookResultsFile.write( u' '.join(books[idbnf]) )
    
    # Close files
    xmlFile.close()
    metadataFile.close()
    pageResultsFile.close()
    bookResultsFile.close()

def mean(rv):
    
    return sum(rv)/len(rv)

def standard_deviation(rv):
    
    m = sum(rv)/len(rv)
    cov = math.sqrt(sum( [ (x-m)**2 for x in rv ] ) / (len(rv)-1))

createStatistics( 'frwikisource-bnf-20101003-medium.xml', 'metadata-stats.txt', 'page-statistics-20101003.txt', 'book-statistics-20101003.txt' )

