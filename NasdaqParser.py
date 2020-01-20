from NasdaqStock import NasdaqStock


# from Pattern import Pattern


class NasdaqParser:
    def __init__(self, pattern,filename):
        lines = open(filename, 'r').readlines()
        self.list_of_lists = []
        event_list = []
        for event_name in pattern.events:
            for line in lines:
                name, timestamp, opening, peak, lowest, close, volume = line.split(",")
                if name != event_name:
                    continue
                else:
                    nasdaqStock = NasdaqStock(name, float(timestamp), float(opening), float(peak), float(lowest),
                                              float(close), float(volume))
                    event_list.append(nasdaqStock)
            self.list_of_lists.append(event_list.copy())
            event_list.clear()

    def printList(self):
        for i in self.list_of_lists[0]:
            print(i.ticker + ", " + i.timestamp)
        for i in self.list_of_lists[1]:
            print(i.ticker + ", " + i.timestamp)
