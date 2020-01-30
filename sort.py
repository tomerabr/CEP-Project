#a script for sorting the input file by timestamp.

by_timestamp = 1

lines = open("stocks.txt", 'r').readlines()
output_file = open("Stocks ordered.txt", 'w')

for line in sorted(lines, key=lambda line: line.split(",")[by_timestamp]):
	output_file.write(line)
	
output_file.close()