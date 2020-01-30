from enum import Enum

#Enum for every attribute that can be compared in the class
class Operand(Enum):
    OPENING_PRICE = 1
    PEAK_PRICE = 2
    LOWEST_PRICE = 3
    CLOSE_PRICE = 4
    VOLUME = 5

#a class for the type of events we want to get the algorithm work on
class NasdaqStock:
    
    #Gets a list of values (in order that are exist in input file),
    #creates the attributes of the class and put the values in them
    def setAttributes(self, atributes):
        self.ticker = atributes[0]
        self.timestamp = float(atributes[1])
        self.opening = float(atributes[2])
        self.peak = float(atributes[3])
        self.lowest = float(atributes[4])
        self.close = float(atributes[5])
        self.volume = float(atributes[6])

    #Return the string that will be printed when we print the class (print(NasdaqStock))
    def __repr__(self):
        return ("ticker: " + str(self.ticker) +"\ntimestamp: " + str(self.timestamp) + "\nopening price: " + str(self.opening)
                + "\npeak: " + str(self.peak)
                + "\nlowest: " + str(self.lowest) + "\nclose: " + str(self.close) + "\nvolume: " + str(self.volume) + "\n")

    #A compare method between 2 objects
    def __eq__(self,other):
        return self.ticker == other.ticker and self.timestamp == other.timestamp

    #Hash function for each object of the class
    def __hash__(self):
        return hash((self.timestamp, self.ticker))

    #Gets an Operand and return the value of it
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