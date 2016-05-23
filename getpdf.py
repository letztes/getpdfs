#!/usr/bin/python
# -*- coding: utf-8 -*- 

print "content-type:text/html\n\n"

from HTMLParser import HTMLParser
import os
import re
import time
import urllib2
from urlparse import *

	
class MyHTMLParser(HTMLParser):
	
    def reset(self):
        HTMLParser.reset(self)
        self.links      = []

    def handle_starttag(self, tag, attrs):
		
		# Only parse the 'anchor' tag.
		if tag == "a":
			
			for name, value in attrs:
				
				if name == "href":
					if value[0] == '/':
						absolute=urljoin(self.url, value)
						self.links.append(absolute)
					else:
						self.links.append(value)

class GetPdf:
	def __init__(self, url):
		self.url = url
		self.output_directory = '/tmp/'
		self.parser = MyHTMLParser()
		self.parser.url = url
		
		
	def get_pdfs(self, links):
			
		for url in links:
			
			if 'pdf' not in url:
				continue
			
			time.sleep(1)
			
			file_name = url.split('/')[-1]
			
			response = urllib2.urlopen(url)

			file_handle = open(self.output_directory + file_name, 'wb')
			
			file_size = int(response.info().getheaders("Content-Length")[0])

			if file_size > 500000000:
				print "File " + file_size + " is bigger than 500 MB. Skipping."
				continue
			
			# progressbar via ajax like in http://stackoverflow.com/a/22776

			file_handle.write(response.read())

	def get_links(self,html,regex_string=None):
		
		if regex_string is None:
			regex_string = '.*pdf'
		
		if regex_string is None:
			return
		
		self.parser.feed(html)
			
		regex_compiled = re.compile(regex_string)
		links = []
		
		for link_string in list(self.parser.links):
			if re.match(regex_compiled, link_string):
				links.append(link_string)
		
		self.parser.reset()
		
		return links
		
	def get_parser(self):
		parser = MyHTMLParser()
		return parser
