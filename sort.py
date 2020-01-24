#A script for sorting the input file by timestamp.

lines = open("stocks.txt", 'r').readlines()
output_file = open("Stocks ordered.txt", 'w')

for line in sorted(lines, key=lambda line: line.split(",")[1]):
	output_file.write(line)
	
output_file.close()