#!/usr/bin/python
# -*- coding: utf-8 -*- 

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
	
	response.close()
	
	links_to_pdfs = []
	
	links1 = pdf_getter.get_links(html,level1regex)

	if not level1regex:
		links_to_pdfs.extend(links1)
	if links1 and level1regex:
		level1regex_compiled = re.compile(level1regex)
		for link1 in links1:

			if re.match(level1regex_compiled, link1):
				response2 = urllib2.urlopen(link1)
				html2 = response2.read()
				links2 = pdf_getter.get_links(html2,level2regex)
				if not level2regex:
					links_to_pdfs.extend(links2)
				
				if links2 and level2regex:
					level2regex_compiled = re.compile(level2regex)
					for link2 in links2:
						if re.match(level2regex_compiled, link2):
							response3 = urllib2.urlopen(link2)
							html3 = response3.read()
							links3 = pdf_getter.get_links(html3,level3regex)
							
							print 'links3: '
							print links3
							if not level3regex:
								links_to_pdfs.extend(links3)
				
							if links3 and level3regex:
								level3regex_compiled = re.compile(level3regex)
								for link3 in links3:
									if re.match(level3regex_compiled, link3):
										response4 = urllib2.urlopen(link3)
										html4 = response4.read()
										links4 = pdf_getter.get_links(html4,level3regex)
										
										print 'links4: '
										print links4
				
										if not level4regex:
											links_to_pdfs.extend(links4)
								
										if links4 and level4regex:
											level4regex_compiled = re.compile(level4regex)
						
	
	pdf_getter.get_pdfs(links_to_pdfs)
	
	print 'Downloaded: '
	print links_to_pdfs
	print "<br>"
	print '<a href="/getpdf/">Back</a>'

else:
	print "no url specified"

