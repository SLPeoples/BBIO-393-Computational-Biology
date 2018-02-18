#Import functions 

from random import random,choice

#Open a file for writing
output_filename = "results.txt"

#We've gotten biologial results here

result_lines = []

input_data = [23,17,2400,2304,43,3]
for tumor_load in input_data:
    result = tumor_load**2
    print(result)
    result_lines.append(str(result)+"\n")
    print(result_lines)

f = open(output_filename,"w")
for line in result_lines:
    f.write(line)
