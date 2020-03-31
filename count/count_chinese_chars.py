import re
import sys
import zhon
from zhon import hanzi

def count_chinese_chars(input):
	chars_unique = set()
	chars_count = 0
	chars = re.findall('[%s]' % zhon.hanzi.characters, input)
	if not chars:
		return 0, 0
	else:
		for x in chars:
			chars_count = chars_count + 1
			if x not in chars_unique:
				chars_unique.add(x)
		chars_count_unique = len(chars_unique)
		return chars_count_unique, chars_count

def main():
	if len(sys.argv) > 1:
		arg = sys.argv[1]
	else:
		arg = input("Enter text containing Chinese characters: ")
	count = count_chinese_chars(arg)
	print('The input contains ' + str(count[0]) + ' unique Chinese characters out of ' + str(count[1]) + ' in total.')

if __name__ == '__main__':
	main()
