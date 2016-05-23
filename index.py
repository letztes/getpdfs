#!/usr/bin/python
# -*- coding: utf-8 -*- 

#print "content-type:text/html\n\n"
#print '<a href="/getpdf/">back</a>'

from HTMLParser import HTMLParser
import cgi
import cgitb
import os
import re
import urllib2

from getpdf import *


cgitb.enable()  # for troubleshooting

form = cgi.FieldStorage()

url = form.getvalue('url')

pdf_getter = GetPdf(url)	

parser = pdf_getter.get_parser()

if url and len(url) > 3:
	level1regex = form.getvalue('level1regex')

	if level1regex:
		level2regex = form.getvalue('level2regex')
		
		if level2regex:
			level3regex = form.getvalue('level3regex')
		
			if level3regex:
				level4regex = form.getvalue('level4regex')
				
				if level4regex:
					level5regex = form.getvalue('level5regex')

	else:
		level1regex = 'pdf$'
	response = urllib2.urlopen(url)

	html = response.read()
	
	links = pdf_getter.get_links(html,level1regex)
	
	print 'Downloaded: '
	print links
	print "<br>"
	print '<a href="/getpdf/">Back</a>'
	
	pdf_getter.get_pdfs(links)
		
	#~ for link_string in links:
		#~ time.sleep(1)
		#~ pdf_getter.get_pdfs([link_string])

else:
	print "no url specified"

