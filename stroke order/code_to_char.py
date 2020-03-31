# for file in folder get chars

import glob
import re

def main():
	INPUT_DIR = './pre-input/'
	path = INPUT_DIR + '*.txt'
	files = glob.glob(path)

	for name in files:
		input = open(name, 'r')
		out_name = './input/' + re.search('\/([^/]*)(\.txt)', name).group(0)[1:]
		out_file = open(out_name, 'w')

		for line in input:
			code = re.findall('[U][+][A-Z|0-9]{4,}', line)
			if not code:
				continue
			else:
				for x in code:
					char = chr(int(x[2:], 16))
					out_file.write(char + '\t' + x + '\n')
		
		out_file.close()
		input.close()

if __name__ == '__main__':
	main()