from NasdaqStock import NasdaqStock

lines = open("Stocks ordered.txt", 'r').readlines()
count = 0

for line in lines:
    name, timestamp, opening, peak, lowest, close, volume = line.split(",")
    nasdaqStock = NasdaqStock(name,timestamp,opening,peak, lowest, close, volume)
    count += 1
    print(nasdaqStock)
    if count == 10:
        break

