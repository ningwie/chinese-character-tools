import binascii

in_file = open('big5.txt')
out_file = open('chars.txt', 'w')

for line in in_file:
    try:
        input_char = line[:-1]
        char_binary_hex = input_char.encode('utf-8')
        char_binary = binascii.unhexlify(char_binary_hex)
        output = char_binary.decode('big5')
        out_file.write(output + "\n")
    except binascii.Error:
        out_file.write(input_char + "is not a valid character code in Big5.\n")
        
in_file.close()
out_file.close()