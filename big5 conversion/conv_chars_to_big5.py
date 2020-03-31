# read lines from file and transform them, one by one, to Big5 codes and write them out to a new file

import binascii

in_file = open('chars.txt', 'r')
out_file = open('big5.txt', 'w')

for line in in_file:
    try:
        input_char = line[0:1]
        char_binary = input_char.encode('big5')
        char_binary_hex = binascii.hexlify(char_binary)
        char_int = int(char_binary_hex, 16)
        output = '{:X}'.format(char_int)
        out_file.write(output + "\n")
    except UnicodeEncodeError:
        out_file.write(input_char + "\n")
        
in_file.close()
out_file.close()