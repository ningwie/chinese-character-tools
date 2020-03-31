import os
import re

liste = open('2big5_chars.txt')
dict = {}

for line in liste:
	big5 = line[:4]
	char = line[4:5]
	dict[big5] = char

for x in dict:
	print(x + " " + dict[x])
	
for filename in os.listdir("./Downloads"):
	if filename.startswith("A"):
		try:
			big5 = filename[:4]
			print(big5)
			os.rename(filename, dict[big5])
		except KeyError:
	 		print(filename)
# 	except FileNotFoundError:
# 		print("ups")

liste.close()