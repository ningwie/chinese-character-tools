# Dings zu Dings. Zeichen in html table schreiben

import binascii

in_file = open('chars.txt')
out_file = open('table.html', 'w')

out_file.write("""
<html>
<table>
""")

output = """
	<tr>
		<td><a href="Downloads/***.png">%%%</a></td>
		<td><a href="http://stroke-order.learningweb.moe.edu.tw/mobiles/practice.rbt?big5Code=***">***</td>
	</tr>
"""

for line in in_file:
    try:
        input_char = line[0:1]
        trans_big = input_char.encode('big5')
        trans_hex = binascii.hexlify(trans_big)
        trans_int = int(trans_hex, 16)
        out_big = '{:X}'.format(trans_int)
    except UnicodeEncodeError:
        out_big = "Sorry, not in MOE data"
    char_tc = line[0:1]
    out1 = output.replace("%%%", char_tc)
    out2 = out1.replace("***", out_big)
    out_file.write(out2 + "\n")

out_file.write("""
</table>
</html>
""")

in_file.close()
out_file.close()