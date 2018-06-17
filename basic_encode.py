#utf-8
# /**
# * Copyright (c) 2018 University of Ljubljana, Faculty of Electrical Engineering.
# * All rights reserved. Licensed under the Academic Free License version 3.0.
# * 
# * @author Tim Kambič 
# * @version 16/05/2018
# *
# * Demo koda, ki izracuna Huffmanov kod za podano porazdelitev znakov
# */

import sys

#Function that generates Huffmans code, based on input list with relative frequencies (python dictionary with byte as key and frequency as value)
#returns: python dicitonary with byte as key and huffman code for value)
def generateHuffmanCode(sorted_list): # see "encode.py" file for more detailed commentaries on this function
	code = {}
	for key_val in sorted_list:
		code[key_val[0]] = ""
	while(True):
		sorted_list = sorted(sorted_list, key=lambda x: x[1], reverse=True)

		char1 = sorted_list[-1][0]
		char2 = sorted_list[-2][0]

		for c in char1:
			code[c] = "1"+code[c]
		for c in char2:
			code[c] = "0"+code[c]

		combined_val = sorted_list[-1][1] + sorted_list[-2][1]
		combined_name = char1 + char2
		
		sorted_list.pop(-1)
		sorted_list.pop(-1)
		sorted_list.append((combined_name,combined_val))
		print(sorted_list)

		if len(sorted_list)<=1:
			break
	
	return code


print("enter probability for signs as comma separated values (e.g. 0.1,0.20,0.10,0.5,0.05,0.05) or press ENTER to test default data")
input_probability = []
read = input()
if read=="":
	input_probability = [0.25,0.20,0.15,0.10,0.08,0.07,0.06,0.05,0.04]
else:
	input_probability = [float(x) for x in read.split(',')]

print("\nInput probability is:")
print(input_probability)
print("\n")

input_symbols = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','z','x','y','w','q'];
input_list = []

for i in range(len(input_probability)):
	# code[input_symbols[i]] = ""
	input_list.append((input_symbols[i], input_probability[i]))
print(input_list)
print("\nFinal code for input is:")
print(generateHuffmanCode(input_list))




	

