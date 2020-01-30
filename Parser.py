
name = 0

#Parsing the input file to the attributes of the given class.
class Parser:
    def __init__(self, pattern,filename,PythonClass):
        lines = open(filename, 'r').readlines()
        self.list_of_lists = []
        event_list = []
        for event_name in pattern.events:
            for line in lines:
                atributes = line.split(",") #parse the attributes from the line
                if atributes[name] != event_name: #check if the event's name (that been parsed) equals to the name of the type
                    continue
                else:
                    nasdaqStock = PythonClass() #make new object
                    nasdaqStock.setAttributes(atributes) #fill the new object
                    event_list.append(nasdaqStock) #add the object to the list
                    lines.remove(line) #remove the line as we won't need it anymore, so reduces running time
                
            self.list_of_lists.append(event_list.copy()) #add the list to the list of lists 
            event_list.clear() 