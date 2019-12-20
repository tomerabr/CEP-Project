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
        return ("ticker: " + self.ticker +"\ntimestamp: " + self.timestamp + "\nopening price: " + self.opening
                + "\npeak: " + self.peak
                + "\nlowest: " + self.lowest + "\nclose: " + self.close + "\nvolume: " + self.volume)