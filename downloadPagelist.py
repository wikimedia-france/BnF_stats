# -*- coding:utf-8 -*-

import codecs, re

nbhtmlpages = 100

header = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="fr" dir="ltr">
<head>
<title>Exporter des pages - Wikisource</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<meta name="generator" content="MediaWiki 1.16wmf4" />
<meta name="robots" content="noindex,nofollow" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="search" type="application/opensearchdescription+xml" href="http://fr.wikisource.org/w/opensearch_desc.php" title="Wikisource (fr)" />
<link rel="copyright" href="http://creativecommons.org/licenses/by-sa/3.0/" />
<link rel="alternate" type="application/atom+xml" title="Flux Atom de Wikisource" href="http://fr.wikisource.org/w/index.php?title=Sp%C3%A9cial:Modifications_r%C3%A9centes&amp;feed=atom" />
<link rel="stylesheet" href="http://bits.wikimedia.org/skins-1.5/vector/main-ltr.css?283u" type="text/css" media="screen" />
<link rel="stylesheet" href="http://bits.wikimedia.org/skins-1.5/common/shared.css?283u" type="text/css" media="screen" />
<link rel="stylesheet" href="http://bits.wikimedia.org/skins-1.5/common/commonPrint.css?283u" type="text/css" media="print" />
<link rel="stylesheet" href="http://bits.wikimedia.org/w/extensions/UsabilityInitiative/css/combined.min.css?117" type="text/css" media="all" />
<link rel="stylesheet" href="http://bits.wikimedia.org/w/extensions/UsabilityInitiative/css/vector/jquery-ui-1.7.2.css?1.7.2y" type="text/css" media="all" />
<link rel="stylesheet" href="http://fr.wikisource.org/w/index.php?title=MediaWiki:Common.css&amp;usemsgcache=yes&amp;ctype=text%2Fcss&amp;smaxage=2678400&amp;action=raw&amp;maxage=2678400" type="text/css" media="all" />
<link rel="stylesheet" href="http://fr.wikisource.org/w/index.php?title=MediaWiki:Print.css&amp;usemsgcache=yes&amp;ctype=text%2Fcss&amp;smaxage=2678400&amp;action=raw&amp;maxage=2678400" type="text/css" media="print" />
<link rel="stylesheet" href="http://fr.wikisource.org/w/index.php?title=MediaWiki:Handheld.css&amp;usemsgcache=yes&amp;ctype=text%2Fcss&amp;smaxage=2678400&amp;action=raw&amp;maxage=2678400" type="text/css" media="handheld" />
<link rel="stylesheet" href="http://fr.wikisource.org/w/index.php?title=MediaWiki:Vector.css&amp;usemsgcache=yes&amp;ctype=text%2Fcss&amp;smaxage=2678400&amp;action=raw&amp;maxage=2678400" type="text/css" media="all" />
<link rel="stylesheet" href="http://fr.wikisource.org/w/index.php?title=-&amp;action=raw&amp;maxage=2678400&amp;gen=css" type="text/css" media="all" />
<script type="text/javascript">
var skin="vector",
stylepath="http://bits.wikimedia.org/skins-1.5",
wgUrlProtocols="http\\:\\/\\/|https\\:\\/\\/|ftp\\:\\/\\/|irc\\:\\/\\/|gopher\\:\\/\\/|telnet\\:\\/\\/|nntp\\:\\/\\/|worldwind\\:\\/\\/|mailto\\:|news\\:|svn\\:\\/\\/",
wgArticlePath="http://fr.wikisource.org/wiki/$1",
wgScriptPath="/w",
wgScriptExtension=".php",
wgScript="http://fr.wikisource.org/w/index.php",
wgVariantArticlePath=false,
wgActionPaths={},
wgServer="http://fr.wikisource.org",
wgCanonicalNamespace="Special",
wgCanonicalSpecialPageName="Export",
wgNamespaceNumber=-1,
wgPageName="Spécial:Exporter",
wgTitle="Exporter",
wgAction="view",
wgArticleId=0,
wgIsArticle=false,
wgUserName=null,
wgUserGroups=null,
wgUserLanguage="fr",
wgContentLanguage="fr",
wgBreakFrames=false,
wgCurRevisionId=0,
wgVersion="1.16wmf4",
wgEnableAPI=true,
wgEnableWriteAPI=true,
wgSeparatorTransformTable=[",	.", " 	,"],
wgDigitTransformTable=["", ""],
wgMainPageTitle="Wikisource:Accueil",
wgFormattedNamespaces={"-2": "Média", "-1": "Spécial", "0": "", "1": "Discussion", "2": "Utilisateur", "3": "Discussion utilisateur", "4": "Wikisource", "5": "Discussion Wikisource", "6": "Fichier", "7": "Discussion fichier", "8": "MediaWiki", "9": "Discussion MediaWiki", "10": "Modèle", "11": "Discussion modèle", "12": "Aide", "13": "Discussion aide", "14": "Catégorie", "15": "Discussion catégorie", "100": "Transwiki", "101": "Discussion Transwiki", "102": "Auteur", "103": "Discussion Auteur", "104": "Page", "105": "Discussion Page", "106": "Portail", "107": "Discussion Portail", "112": "Livre", "113": "Discussion Livre"},
wgNamespaceIds={"média": -2, "spécial": -1, "": 0, "discussion": 1, "utilisateur": 2, "discussion_utilisateur": 3, "wikisource": 4, "discussion_wikisource": 5, "fichier": 6, "discussion_fichier": 7, "mediawiki": 8, "discussion_mediawiki": 9, "modèle": 10, "discussion_modèle": 11, "aide": 12, "discussion_aide": 13, "catégorie": 14, "discussion_catégorie": 15, "transwiki": 100, "discussion_transwiki": 101, "auteur": 102, "discussion_auteur": 103, "page": 104, "discussion_page": 105, "portail": 106, "discussion_portail": 107, "livre": 112, "discussion_livre": 113, "discuter": 1, "discussion_image": 7, "image": 6, "image_talk": 7},
wgSiteName="Wikisource",
wgCategories=[],
wgDBname="frwikisource",
wgMWSuggestTemplate="http://fr.wikisource.org/w/api.php?action=opensearch\x26search={searchTerms}\x26namespace={namespaces}\x26suggest",
wgSearchNamespaces=[0],
wgMWSuggestMessages=["avec suggestions", "sans suggestions"],
wgRestrictionEdit=[],
wgRestrictionMove=[],
wgCollapsibleNavBucketTest=false,
wgCollapsibleNavForceNewVersion=false,
wgVectorPreferences={"collapsiblenav": {"enable": 1}, "editwarning": {"enable": 1}, "simplesearch": {"enable": 1, "disablesuggest": 0}},
wgVectorEnabledModules={"collapsiblenav": true, "collapsibletabs": true, "editwarning": true, "expandablesearch": false, "footercleanup": false, "simplesearch": true},
Geo={"city": "", "country": ""},
wgNoticeProject="wikisource";
</script><script src="http://bits.wikimedia.org/skins-1.5/common/wikibits.js?283u" type="text/javascript"></script>
<script type="text/javascript" src="http://bits.wikimedia.org/skins-1.5/common/jquery.min.js?283u"></script>
<script src="http://bits.wikimedia.org/skins-1.5/common/ajax.js?283u" type="text/javascript"></script>
<script src="http://bits.wikimedia.org/skins-1.5/common/mwsuggest.js?283u" type="text/javascript"></script>
<script src="http://bits.wikimedia.org/w/extensions/UsabilityInitiative/js/plugins.combined.min.js?283u" type="text/javascript"></script>
<script src="http://bits.wikimedia.org/w/extensions/UsabilityInitiative/Vector/Vector.combined.min.js?283u" type="text/javascript"></script>
<script type="text/javascript">mw.usability.addMessages({'vector-collapsiblenav-more':'Plus de langues','vector-editwarning-warning':'Quitter cette page vous fera perdre toutes les modifications que vous avez faites.\nSi vous êtes connecté avec votre compte, vous pouvez retirer cet avertissement dans la section « Fenêtre de modification » de vos préférences.','vector-simplesearch-search':'Rechercher','vector-simplesearch-containing':'contenant...'});</script>
<script src="http://fr.wikisource.org/wiki/Sp%C3%A9cial:BannerController?283u" type="text/javascript"></script>
<!--[if lt IE 7]><style type="text/css">body{behavior:url("http://fr.wikisource.org/w/skins-1.5/vector/csshover.htc")}</style><![endif]-->
<script src="http://fr.wikisource.org/w/index.php?title=-&amp;action=raw&amp;gen=js&amp;useskin=vector&amp;283u" type="text/javascript"></script>

</head>
<body class="mediawiki ltr ns--1 ns-special page-Spécial_Exporter skin-vector">
		<div id="mw-page-base" class="noprint"></div>
		<div id="mw-head-base" class="noprint"></div>
		<!-- content -->
		<div id="content">
			<a id="top"></a>
			<div id="mw-js-message" style="display:none;"></div>
						<!-- sitenotice -->
			<div id="siteNotice"><!-- centralNotice loads here --><script type="text/javascript" language="JavaScript">
/* <![CDATA[ */
document.writeln("\x3cdiv id=\"localNotice\"\x3e\x3c/div\x3e");
/* ]]> */
</script></div>
			<!-- /sitenotice -->
						<!-- firstHeading -->
			<h1 id="firstHeading" class="firstHeading">Exporter des pages</h1>
			<!-- /firstHeading -->
			<!-- bodyContent -->
			<div id="bodyContent">
				<!-- tagline -->
				<div id="siteSub">La bibliothèque libre.</div>
				<!-- /tagline -->
				<!-- subtitle -->
				<div id="contentSub"></div>
				<!-- /subtitle -->
																<!-- jumpto -->
				<div id="jump-to-nav">
					Aller à : <a href="#mw-head">Navigation</a>,
					<a href="#p-search">rechercher</a>
				</div>
				<!-- /jumpto -->
								<!-- bodytext -->
				<p>Vous pouvez exporter en XML le texte et l’historique d’une page ou d’un ensemble de pages&nbsp;;
le résultat peut alors être importé dans un autre wiki utilisant le logiciel MediaWiki via la <a href="http://fr.wikisource.org/wiki/Sp%C3%A9cial:Importer" title="Spécial:Importer">page d’importation</a>.
</p><p>Pour exporter des pages, entrez leurs titres dans la boîte de texte ci-dessous, à raison d’un titre par ligne. Sélectionnez si vous désirez ou non la version actuelle avec toutes les anciennes versions, avec les lignes de l’historique de la page, ou simplement la page actuelle avec des informations sur la dernière modification.
</p><p>Dans ce dernier cas vous pouvez aussi utiliser un lien, tel que <a href="http://fr.wikisource.org/wiki/Sp%C3%A9cial:Exporter/Wikisource:Accueil" title="Spécial:Exporter/Wikisource:Accueil">Spécial:Exporter/Wikisource:Accueil</a> pour la page <a href="http://fr.wikisource.org/wiki/Wikisource:Accueil" title="Wikisource:Accueil">Wikisource:Accueil</a>.
</p><form method="post" action="http://fr.wikisource.org/w/index.php?title=Sp%C3%A9cial:Exporter&amp;action=submit"><label for="catname">Ajouter les pages de la catégorie :</label>&nbsp;<input name="catname" size="40" value="" id="catname" />&nbsp;<input type="submit" value="Ajouter" name="addcat" /><br /><textarea name="pages" cols="40" rows="10">"""

footer = u"""</textarea><br /><input name="curonly" type="checkbox" value="1" checked="checked" id="curonly" />&nbsp;<label for="curonly">Exporter uniquement la version courante, sans l’historique complet</label><br /><input name="templates" type="checkbox" value="1" id="wpExportTemplates" />&nbsp;<label for="wpExportTemplates">Inclure les modèles</label><br /><input name="wpDownload" type="checkbox" value="1" checked="checked" id="wpDownload" />&nbsp;<label for="wpDownload">Enregistrer dans un fichier</label><br /><input type="submit" value="Exporter" accesskey="s" /></form><div class="printfooter">
Récupérée de « <a href="http://fr.wikisource.org/wiki/Sp%C3%A9cial:Exporter">http://fr.wikisource.org/wiki/Sp%C3%A9cial:Exporter</a> »</div>
				<!-- /bodytext -->
								<!-- catlinks -->
				<div id='catlinks' class='catlinks catlinks-allhidden'></div>				<!-- /catlinks -->
												<div class="visualClear"></div>
			</div>
			<!-- /bodyContent -->
		</div>
		<!-- /content -->
		<!-- header -->
		<div id="mw-head" class="noprint">
			
<!-- 0 -->
<div id="p-personal" class="">
	<h5>Outils personnels</h5>
	<ul>
					<li  id="pt-prefswitch-link-anon"><a href="http://fr.wikisource.org/w/index.php?title=Sp%C3%A9cial:UsabilityInitiativePrefSwitch&amp;from=Sp%C3%A9cial%3AExporter" title="En savoir plus sur les nouvelles fonctionnalités" class="no-text-transform">Nouvelles fonctionnalités</a></li>
					<li  id="pt-login"><a href="http://fr.wikisource.org/w/index.php?title=Sp%C3%A9cial:Connexion&amp;returnto=Sp%C3%A9cial:Exporter" title="Vous êtes encouragé(e) à vous identifier ; ce n’est cependant pas obligatoire. [o]" accesskey="o">Créer un compte ou se connecter</a></li>
			</ul>
</div>

<!-- /0 -->
			<div id="left-navigation">
				
<!-- 0 -->
<div id="p-namespaces" class="vectorTabs">
	<h5>Espaces de noms</h5>
	<ul>
					<li  id="ca-special" class="selected"><a href="http://fr.wikisource.org/wiki/Sp%C3%A9cial:Exporter" ><span>Page spéciale</span></a></li>
			</ul>
</div>

<!-- /0 -->

<!-- 1 -->
<div id="p-variants" class="vectorMenu emptyPortlet">
		<h5><span>Variantes</span><a href="#"></a></h5>
	<div class="menu">
		<ul>
					</ul>
	</div>
</div>

<!-- /1 -->
			</div>
			<div id="right-navigation">
				
<!-- 0 -->
<div id="p-views" class="vectorTabs emptyPortlet">
	<h5>Affichages</h5>
	<ul>
			</ul>
</div>

<!-- /0 -->

<!-- 1 -->
<div id="p-cactions" class="vectorMenu emptyPortlet">
	<h5><span>Actions</span><a href="#"></a></h5>
	<div class="menu">
		<ul>
					</ul>
	</div>
</div>

<!-- /1 -->

<!-- 2 -->
<div id="p-search">
	<h5><label for="searchInput">Rechercher</label></h5>
	<form action="http://fr.wikisource.org/w/index.php" id="searchform">
		<input type='hidden' name="title" value="Spécial:Recherche"/>
				<div id="simpleSearch">
			<input id="searchInput" name="search" type="text"  title="Rechercher dans Wikisource [f]" accesskey="f"  value="" />
			<button id="searchButton" type='submit' name='button'  title="Rechercher les pages comportant ce texte."><img src="http://bits.wikimedia.org/skins-1.5/vector/images/search-ltr.png?283u" alt="Rechercher" /></button>
		</div>
			</form>
</div>

<!-- /2 -->
			</div>
		</div>
		<!-- /header -->
		<!-- panel -->
			<div id="mw-panel" class="noprint">
				<!-- logo -->
					<div id="p-logo"><a style="background-image: url(http://upload.wikimedia.org/wikisource/fr/b/bc/Wiki.png);" href="http://fr.wikisource.org/wiki/Wikisource:Accueil"  title="Page principale"></a></div>
				<!-- /logo -->
				
<!-- SEARCH -->

<!-- /SEARCH -->

<!-- Lire -->
<div class="portal" id='p-Lire'>
	<h5>Lire</h5>
	<div class="body">
				<ul>
					<li id="n-Accueil"><a href="http://fr.wikisource.org/wiki/Wikisource:Accueil">Accueil</a></li>
					<li id="n-Index.C2.A0des.C2.A0auteurs"><a href="http://fr.wikisource.org/wiki/Wikisource:Index_des_auteurs">Index des auteurs</a></li>
					<li id="n-Portails"><a href="http://fr.wikisource.org/wiki/Cat%C3%A9gorie:Portails">Portails</a></li>
					<li id="n-Aide.C2.A0au.C2.A0lecteur"><a href="http://fr.wikisource.org/wiki/Aide:Aide_au_lecteur">Aide au lecteur</a></li>
					<li id="n-Texte.C2.A0au.C2.A0hasard"><a href="http://fr.wikisource.org/wiki/Sp%C3%A9cial:Page_au_hasard">Texte au hasard</a></li>
				</ul>
			</div>
</div>

<!-- /Lire -->

<!-- Contribuer -->
<div class="portal" id='p-Contribuer'>
	<h5>Contribuer</h5>
	<div class="body">
				<ul>
					<li id="n-portal"><a href="http://fr.wikisource.org/wiki/Wikisource:Scriptorium" title="À propos du projet">Scriptorium</a></li>
					<li id="n-help"><a href="http://fr.wikisource.org/wiki/Aide:Aide" title="Aide">Aide</a></li>
					<li id="n-Communaut.C3.A9"><a href="http://fr.wikisource.org/wiki/Wikisource:Portail_communautaire">Communauté</a></li>
					<li id="n-Livre-au-hasard"><a href="http://fr.wikisource.org/wiki/Sp%C3%A9cial:Random/Livre">Livre au hasard</a></li>
					<li id="n-recentchanges"><a href="http://fr.wikisource.org/wiki/Sp%C3%A9cial:Modifications_r%C3%A9centes" title="Liste des modifications récentes sur le wiki [r]" accesskey="r">Modif. récentes</a></li>
					<li id="n-sitesupport"><a href="http://meta.wikimedia.org/wiki/Special:GeoLite" title="Aidez-nous">Faire un don</a></li>
				</ul>
			</div>
</div>

<!-- /Contribuer -->

<!-- TOOLBOX -->
<div class="portal" id="p-tb">
	<h5>Boîte à outils</h5>
	<div class="body">
		<ul>
																																							<li id="t-specialpages"><a href="http://fr.wikisource.org/wiki/Sp%C3%A9cial:Pages_sp%C3%A9ciales" title="Liste de toutes les pages spéciales [q]" accesskey="q">Pages spéciales</a></li>
													</ul>
	</div>
</div>

<!-- /TOOLBOX -->

<!-- LANGUAGES -->

<!-- /LANGUAGES -->
			</div>
		<!-- /panel -->
		<!-- footer -->
		<div id="footer">
																		<ul id="footer-places">
																	<li id="footer-places-privacy"><a href="http://fr.wikisource.org/wiki/Wikisource:Confidentialit%C3%A9" title="Wikisource:Confidentialité">Politique de confidentialité</a></li>
																							<li id="footer-places-about"><a href="http://fr.wikisource.org/wiki/Wikisource:%C3%80_propos" title="Wikisource:À propos">À propos de Wikisource</a></li>
																							<li id="footer-places-disclaimer"><a href="http://fr.wikisource.org/wiki/Wikisource:Avertissements_g%C3%A9n%C3%A9raux" title="Wikisource:Avertissements généraux">Avertissements</a></li>
															</ul>
										<ul id="footer-icons" class="noprint">
								<li id="footer-icon-poweredby"><a href="http://www.mediawiki.org/"><img src="http://bits.wikimedia.org/skins-1.5/common/images/poweredby_mediawiki_88x31.png" height="31" width="88" alt="Powered by MediaWiki" /></a></li>
												<li id="footer-icon-copyright"><a href="http://wikimediafoundation.org/"><img src="/images/wikimedia-button.png" width="88" height="31" alt="Wikimedia Foundation"/></a></li>
							</ul>
			<div style="clear:both"></div>
		</div>
		<!-- /footer -->
		<!-- fixalpha -->
		<script type="text/javascript"> if ( window.isMSIE55 ) fixalpha(); </script>
		<!-- /fixalpha -->
		
<script type="text/javascript">if (window.runOnloadHook) runOnloadHook();</script>
		<!-- Served by srv212 in 0.071 secs. -->			</body>
</html>"""

metadataFile  = codecs.open('metadata-stats.txt','r','utf-8')

# Get the metadata
htmlpage = 1
nblineofhtmlpage = 0
nblinesperhtmlpage = int(580000/nbhtmlpages)
metadatalist = [ re.sub( '\r?\n', '', line ).split(' ') for line in metadataFile.readlines() ]
for book in metadatalist :
    
    print book[0]
    for nbpage in range(0,int(book[2])):
        
        if nblineofhtmlpage % nblinesperhtmlpage == 0:
            pagesFile  = codecs.open('pages-export%d.htm'%(htmlpage),'w','utf-8')
            pagesFile.write( header )
        
        pagesFile.write( 'Page:%s/%s\n'%(book[0],nbpage+1) )
        
        nblineofhtmlpage += 1
        
        if nblineofhtmlpage % nblinesperhtmlpage == 0:
            pagesFile.write( footer )
            pagesFile.close()
            htmlpage += 1

metadataFile.close()

