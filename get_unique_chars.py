# hi there
import glob
import re
import zhon
from zhon import hanzi

def get_chars():
# customize "INPUT_DIR" ad libidum (keep "/" at the end)
	INPUT_DIR = './input/'

# reads only .txt-files
	path = INPUT_DIR + '*.txt'
	outfile = open('./output/output-all.txt', "w")
	chars_overall_count = 0
	files = glob.glob(path)

	for name in files:
		input = open(name, 'r')
		chars_in_file_count = 0
		for line in input:
			chars = re.findall('[%s]' % zhon.hanzi.characters, line)
			if not chars:
				continue
			else:
				for x in chars:
					outfile.write(x + "\n")
					chars_in_file_count = chars_in_file_count + 1
		try:
			print('The file "' + re.search('\/([^/]*)(\.txt)', name).group(0)[1:] + '" contains ' + str(chars_in_file_count) + ' characters.')
		except AttributeError:
			print('The file "' + str(name) + '" contains ' + str(chars_in_file_count) + ' characters.')

		chars_overall_count = chars_overall_count + chars_in_file_count

		print('The overall number of characters so far is ' + str(chars_overall_count) + '.\n')
		input.close()
	outfile.close()

def main():
	get_chars()
	outfile = open('./output/output-unique.txt', "w")
	chars_overall_count = 0
	chars_encountered = set()

	for line in open('./output/output-all.txt', "r"):
		chars_overall_count = chars_overall_count + 1
		if line not in chars_encountered:
			outfile.write(line)
			chars_encountered.add(line)
	print('Result:\n' + str(len(chars_encountered)) + ' unique characters out of ' + str(chars_overall_count) + ' overall characters were written to "output-unique.txt"')
	outfile.close()

if __name__ == '__main__':
	main()
# over and out