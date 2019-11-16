from NasdaqStock import NasdaqStock

lines = open("Stocks ordered.txt", 'r').readlines()

for line in lines:
    name, timestamp, opening, peak, lowest, close, volume = line.split(",")
    nasdaqStock = NasdaqStock(name, timestamp, opening, peak, lowest, close, volume)



