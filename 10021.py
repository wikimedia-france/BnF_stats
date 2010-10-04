# -*- coding:utf-8 -*-

header = u"""<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.4/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.4/ http://www.mediawiki.org/xml/export-0.4.xsd" version="0.4" xml:lang="fr">
  <siteinfo>
    <sitename>Wikisource</sitename>
    <base>http://fr.wikisource.org/wiki/Wikisource:Accueil</base>
    <generator>MediaWiki 1.16wmf4</generator>
    <case>first-letter</case>
    <namespaces>
      <namespace key="-2" case="first-letter">Média</namespace>
      <namespace key="-1" case="first-letter">Spécial</namespace>
      <namespace key="0" case="first-letter" />
      <namespace key="1" case="first-letter">Discussion</namespace>
      <namespace key="2" case="first-letter">Utilisateur</namespace>
      <namespace key="3" case="first-letter">Discussion utilisateur</namespace>
      <namespace key="4" case="first-letter">Wikisource</namespace>
      <namespace key="5" case="first-letter">Discussion Wikisource</namespace>
      <namespace key="6" case="first-letter">Fichier</namespace>
      <namespace key="7" case="first-letter">Discussion fichier</namespace>
      <namespace key="8" case="first-letter">MediaWiki</namespace>
      <namespace key="9" case="first-letter">Discussion MediaWiki</namespace>
      <namespace key="10" case="first-letter">Modèle</namespace>
      <namespace key="11" case="first-letter">Discussion modèle</namespace>
      <namespace key="12" case="first-letter">Aide</namespace>
      <namespace key="13" case="first-letter">Discussion aide</namespace>
      <namespace key="14" case="first-letter">Catégorie</namespace>
      <namespace key="15" case="first-letter">Discussion catégorie</namespace>
      <namespace key="100" case="first-letter">Transwiki</namespace>
      <namespace key="101" case="first-letter">Discussion Transwiki</namespace>
      <namespace key="102" case="first-letter">Auteur</namespace>
      <namespace key="103" case="first-letter">Discussion Auteur</namespace>
      <namespace key="104" case="first-letter">Page</namespace>
      <namespace key="105" case="first-letter">Discussion Page</namespace>
      <namespace key="106" case="first-letter">Portail</namespace>
      <namespace key="107" case="first-letter">Discussion Portail</namespace>
      <namespace key="112" case="first-letter">Livre</namespace>
      <namespace key="113" case="first-letter">Discussion Livre</namespace>
    </namespaces>
  </siteinfo>
"""

footer = u"""</mediawiki>
"""

import codecs, re

xmlResult = codecs.open( 'frwikisource-bnf-20101003.xml', 'w', 'utf-8' )

for f in range(0,99):
    
    file = codecs.open( 'data/Wikisource-99-%02d.xml'%(f+1), 'r', 'utf-8' )
    
    sfile = file.read()
    
    if not re.search( '<mediawiki .*>', sfile ):
        print 'error 1: %s'%(f+1)
    if not re.search( '</mediawiki>', sfile ):
        print 'error 2: %s'%(f+1)
    
    sfile = re.sub( header, "", sfile )
    sfile = re.sub( footer, "", sfile )
    
    xmlResult.write( sfile )
    
    file.close()

xmlResult.close()

