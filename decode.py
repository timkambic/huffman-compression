# /**
# * Copyright (c) 2018 University of Ljubljana, Faculty of Electrical Engineering.
# * All rights reserved. Licensed under the Academic Free License version 3.0.
# * 
# * @author Tim Kambič 
# * @version 16/05/2018
# *
# * Koda, ki dekodira vhodno datoteko, ki je bila kodirana po Hufmanovem kodu, kodna tabela je shranjena v prvi vrstici kodirane datoteke. 
# * UPORABA: python3 decode.py inputfile outputfile
# */


import sys


if len(sys.argv) is not 3:
	print("Usage is decode.py inputfile outputfile ")
	sys.exit()
else:
	INPUT_FILE = sys.argv[1]
	OUTPUT_FILE = sys.argv[2]

code = {}
data = []
#Read the code from file
with open(INPUT_FILE, "rb") as f:
	code_s = f.readline().decode('utf-8')
	print(code_s)
	for key_val in code_s.split('|'): #split different key-value pairs
		#print(key_val)
		if len(key_val)>2:
			key, value = key_val.split(':') # split key value
			code[value] = key #build dicitonary
	data = f.read()
print("Kodne zamenjave so:")
print(code)

data_b = ""
for char in data: #build a string of 1s/0s from file data
	char_b = bin(char)[2:].zfill(8) #add 0s so that we always get whole byte
	data_b += char_b

text_out = ""
char_to_decode = "" #clear previous
#decode string of 1s/0s 
for ch in data_b: #for every 1/0
	char_to_decode +=ch #add it to previous
	if char_to_decode in code: #if that code exists add it to new text
		text_out +=str(chr(int(code[char_to_decode])))
		char_to_decode = "" #clear previous


with open(OUTPUT_FILE, "w", encoding="latin-1") as f: #write decoded data to file
	f.write(text_out)


print("Done")

