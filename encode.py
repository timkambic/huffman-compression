# /**
# * Copyright (c) 2018 University of Ljubljana, Faculty of Electrical Engineering.
# * All rights reserved. Licensed under the Academic Free License version 3.0.
# * 
# * @author Tim Kambič 
# * @version 16/05/2018
# *
# * Koda, ki kodira vhodno datoteko s Hufmanovim kodom in jo shrani v izhodno datoteko
# * UPORABA: python3 encode.py inputfile outputfile
# */

from bitstring import BitArray
import sys

#Function that analyses the relative frequencies of bytes in file - same as was used in Lab 1 of 'Informacija in kodi' when calculating entropy
def analyiseFile(filename): 
	acum = {}
	total_chars = 0

	with open(filename, "rb") as f:
		while True:
			chunk = f.read(100000)
			if not chunk:
				break
			for i in range(len(chunk)):
				sequence_str=str(chunk[i])
				if sequence_str not in acum:
					acum[sequence_str] = 0
				acum[sequence_str] += 1
				total_chars+=1

	list_out = []
	for key, value in acum.items():
		acum[key] = value/total_chars
		list_out.append((key,value/total_chars))

	return list_out

#Function that generates Huffmans code, based on input list with relative frequencies (python dictionary with byte as key and frequency as value)
#returns: python dicitonary with byte as key and huffman code for value)
def generateHuffmanCode(r_freq_list):
	code = {} 
	for key_val in r_freq_list: # initialize dictionary to empty strings as value
		code[key_val[0]] = ""
	while(True):
		r_freq_list = sorted(r_freq_list, key=lambda x: x[1], reverse=True) # sort the dictionary by values, greater first
		char1 = r_freq_list[-1][0] # take two chars with the smallest value
		char2 = r_freq_list[-2][0]

		for c in char1.split("-"): #separate on '-' to get individual chars (saved in dictionary as e.g. 96-116-70)
			code[c] = "1"+code[c] # add '1' to all chars that were together smallest as per huffmans algorithm
		for c in char2.split("-"):
			code[c] = "0"+code[c] # add '0' to second smallest as per huffmans algorithm

		combined_val = r_freq_list[-1][1] + r_freq_list[-2][1] # combine the smallest two value
		combined_name = char1 +"-"+ char2 # combine the smallest two names
		
		r_freq_list.pop(-1) # remove smallest two from dictionary 
		r_freq_list.pop(-1)
		r_freq_list.append((combined_name,combined_val)) # add new combined entry to dicitionary
		
		if len(r_freq_list)<=1: # repeat untill all chars are combined
			break
	return code


#-------------------------------------------------------------------------

if len(sys.argv) is not 3:
	print("Usage is encode.py inputfile outputfile ")
	sys.exit()
else:
	INPUT_FILE = sys.argv[1]
	OUTPUT_FILE = sys.argv[2]

input_list = analyiseFile(INPUT_FILE)
code = generateHuffmanCode(input_list)

print("Kodne zamenjave so:")
print(code)

dataout_s = ""
with open(INPUT_FILE, "rb") as f: # open input file
	filedata = f.read() 
	for char in filedata: 
		replacement_code = code[str(char)] #for every char in file find replacement code
		dataout_s += replacement_code # add this to string of 1s/0s 

while len(dataout_s)%8 is not 0: # add padding at the end so that we get whole bytes to write to file
	dataout_s +="0"

with open(OUTPUT_FILE, "w") as f: # write code to file in following format: key1:value1|key2:value2|...
	for key, value in code.items():
		f.write(str(key)+":"+str(value)+"|")
	f.write('\n')

with open(OUTPUT_FILE, "ab") as f: # write data to file
	out_bytes = bytearray(int(dataout_s[8*k:8*k+8], 2) for k in range(int(len(dataout_s)/8))) # convert string of bytes to bytearray 
	f.write(out_bytes)

print("Done")