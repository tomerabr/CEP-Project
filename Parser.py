
#Parsing the input file to the attributes of the given class.
class Parser:
    def __init__(self, pattern,filename,PythonClass):
        lines = open(filename, 'r').readlines()
        self.list_of_lists = []
        event_list = []
        for event_name in pattern.events:
            for line in lines:
                atributes = line.split(",")
                if atributes[0] != event_name:
                    continue
                else:
                    nasdaqStock = PythonClass()
                    nasdaqStock.setAttributes(atributes)
                    event_list.append(nasdaqStock)
                    lines.remove(line)
                
            self.list_of_lists.append(event_list.copy())
            event_list.clear()