#!/usr/bin/env python3

import re
import glob
import zhon
from zhon import hanzi
import xlsxwriter

INPUT_DIR = './Footnotes/'
OUTPUT_DIR = './Output/'
path = INPUT_DIR + '*.txt'
files = glob.glob(path)

outfile_murks = open('./Output/murks_fnt.txt', 'w')

# xlsx export
workbook = xlsxwriter.Workbook('Bib_fnt.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
worksheet.write(row, col, "type")
col += 1
worksheet.write(row, col, "author")
col += 1
worksheet.write(row, col, "title")
col += 1
worksheet.write(row, col, "publication")
col += 1
worksheet.write(row, col, "publisher")
col += 1
worksheet.write(row, col, "year")
col += 1
worksheet.write(row, col, "url")
col += 1
worksheet.write(row, col, "source")
col += 1
worksheet.write(row, col, "raw")


row = 1
col = 0

for x in files:
	infile = open(x, 'r')
	quelle = re.search('_[^_]*_', x).group(0)[1:-1]

	for line in infile:
		try:
			input = re.search('[^\s①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]*:《[^《》]*》，[^\s]*。', line).group(0)
		except AttributeError:
			print("mir doch egal")
			continue

		outdict = {"type":"", "author":"", "title":"", "publication":"", "publisher":"", "year":"", "url":"", "source":quelle, "entry":"", "raw":input}		

		try:
			if not re.search('^[^《]*〈', input): # book
				outdict["type"] = "book"
				
				try:
					autooor = re.search('^([^《]+)《', input).group(0)[:-1]
					chars = re.findall('[%s]' % zhon.hanzi.characters, autooor)
					if not chars:
						outdict["author"] = autooor 
					else:
						autorstring = ""
						for x in chars:
							autorstring = autorstring + x
						outdict["author"] = autorstring 
				except AttributeError:
					outdict["author"] = "none"
				
				try:
					outdict["entry"] = re.search('《.*', input).group(0)
				except AttributeError:
					outdict["entry"] = "none"
				
				try:
					outdict["title"] = re.search('[^，]*，', outdict["entry"]).group(0)[1:-2]
				except AttributeError:
					outdict["title"] = outdict["entry"]
				
				try:
					outdict["publisher"] = re.search('》.*，[0-9]{4}', outdict["entry"]).group(0)[2:-5]
				except AttributeError:
					outdict["publisher"] = "none"

			else: # article
				outdict["type"] = "paper"
				
				try:
					outdict["author"] = re.search('^([^〈]+)〈', input).group(0)[:-1] 
				except AttributeError:
					outdict["author"] = "none"
					
				try:
					outdict["entry"] = re.search('〈.*', input).group(0)
				except AttributeError:
					outdict["entry"] = "none"
					
				try:
					outdict["title"] = re.search('.[^〉]*〉', outdict["entry"]).group(0)[1:-1]
				except AttributeError:
					outdict["title"] = "none"
					
				try:
					outdict["publication"] = re.search('《[^》]*》', outdict["entry"]).group(0)[1:-1]
					data = re.search('》.*', outdict["entry"]).group(0)[2:]
				except AttributeError:
					outdict["publication"] = 'none'
					data = re.search('〉.*', outdict["entry"]).group(0)[2:]

				try:
					outdict["data"] = re.search('》.*', outdict["entry"]).group(0)[2:]
				except AttributeError:	
					outdict["data"] = re.search('〉.*', outdict["entry"]).group(0)[2:]
			
			if not re.search('\d{4}(年|\.)', outdict["entry"]):
				outdict["year"] = int(re.search('\d{4}', outdict["entry"]).group(0))
			else:
				outdict["year"] = int(re.search('\d{4}(年|\.)', outdict["entry"]).group(0)[:4])
			outdict["url"] = re.search('http[^\s\n;；%]*', input).group(0)
			
		except AttributeError:
			outfile_murks.write('doof gelaufen bei ' + input)

		worksheet.write(row, col, outdict["type"])
		col += 1
		worksheet.write(row, col, outdict["author"])
		col += 1
		worksheet.write(row, col, outdict["title"])
		col += 1
		worksheet.write(row, col, outdict["publication"])
		col += 1
		worksheet.write(row, col, outdict["publisher"])
		col += 1
		worksheet.write(row, col, outdict["year"])
		col += 1
		worksheet.write(row, col, outdict["url"])
		col += 1
		worksheet.write(row, col, outdict["source"])
		col += 1
		worksheet.write(row, col, outdict["raw"])
		col = 0
		row += 1

	infile.close()

workbook.close()

outfile_murks.close()