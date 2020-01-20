from enum import Enum

class Operand(Enum):
    OPENING_PRICE = 1
    PEAK_PRICE = 2
    LOWEST_PRICE = 3
    CLOSE_PRICE = 4
    VOLUME = 5

class NasdaqStock:
    def __init__(self, name, timestamp, opening_price, peak_price, lowest_price, close_price, volume):
        self.ticker = name
        self.timestamp = timestamp
        self.opening = opening_price
        self.peak = peak_price
        self.lowest = lowest_price
        self.close = close_price
        self.volume = volume

    def __repr__(self):
        return ("ticker: " + str(self.ticker) +"\ntimestamp: " + str(self.timestamp) + "\nopening price: " + str(self.opening)
                + "\npeak: " + str(self.peak)
                + "\nlowest: " + str(self.lowest) + "\nclose: " + str(self.close) + "\nvolume: " + str(self.volume) + "\n")

    def __eq__(self,other):
        return self.ticker == other.ticker and self.timestamp == other.timestamp

    def __hash__(self):
        return hash((self.timestamp, self.ticker))

    def parseToValue(self,operand):
        if operand == Operand.OPENING_PRICE:
            return self.opening
        elif operand == Operand.PEAK_PRICE:
            return self.peak
        elif operand == Operand.LOWEST_PRICE:
            return self.lowest
        elif operand == Operand.CLOSE_PRICE:
            return self.close
        else:
            return self.volume
