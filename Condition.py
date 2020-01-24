from enum import Enum
from Pattern import PTYPE
from NasdaqStock import Operand

#Enum for the operators between 2 event's operands.
#Use: Op.Greater, Op.LESS, etc.
class Op(Enum):
    GREATER = 1
    LESS = 2
    GREATER_OR_EQUAL = 3
    LESS_OR_EQUAL = 4
    EQUAL = 5
    NOT_EQUAL = 6


'''
A class that represents a condition between 2 opernads of 2 events (for example: A.volume < B.volume, A.close_price >= A.peak_price)
Can also represent a condition between event's operand and a const number(for example: A.close_price == 56.77)
Each Literal is a condition between maximum 2 attributes.
'''
class Literal:
    '''
    Initiate an object of Literal.
    Params:
    -operator: an enum of type Op, represent the comparison operator between the two operands
    -event_name_A: the name of the first event's type (for example: "AMZN", "EBAY")
    -opernad_A: an enum of type Operand, represents the attribute of the first event that we want 
                to compare
    -event_name_B: the name of the second event's type. In case of unary literal, contains a const number.
    -operand_B: an enum of type Operand, represents the attribute of the second event that we want 
                to compare. In case of unary literal, not given as argument to the constructor and
                is None as default.
    '''
    def __init__(self, operator, event_name_A, operand_A, event_name_B, operand_B=None):
        self.event_name_A = event_name_A  # first event name, string
        self.event_name_B = event_name_B  # second event name, string
        self.operand_A = operand_A  # first event operand, enum
        self.operand_B = operand_B  # second event operand, enum
        self.operator = operator

    
    '''
    Checks the comparison operator and return true if the values provide the condition.
    Params:
    -
    '''
    def checkOperator(self, value1, value2):
        if self.operator == Op.GREATER:
            return value1 > value2
        elif self.operator == Op.LESS:
            return (value1 < value2)
        elif self.operator == Op.GREATER_OR_EQUAL:
            return (value1 >= value2)
        elif self.operator == Op.LESS_OR_EQUAL:
            return (value1 <= value2)
        elif self.operator == Op.EQUAL:
            return (value1 == value2)
        elif self.operator == Op.NOT_EQUAL:
            return (value1 != value2)
        else:
            return False
    
    #Gets 2 events and returns true if the desired attributes' values maintain the condition
    #stock2 == None means the literal is unary and relating only to stock1
    def checkLiteral(self, stock1, stock2=None):
        if stock1.ticker != self.event_name_A or (stock2 is not None and stock2.ticker != self.event_name_B):
            return False
        valueA = stock1.parseToValue(self.operand_A)
        if stock2 is not None:
            valueB = stock2.parseToValue(self.operand_B) 
        else:
            valueB = self.event_name_B #in this case event_name_B contains a const number
        return self.checkOperator(valueA,valueB)
        
    #Prints the literal
    def printLiteral(self):
        print("(", end='')
        print(self.event_name_A, end='')
        print(".", end='')
        print(self.operand_A, end='')
        print(" ", end='')
        print(self.operator, end='')
        print(" ", end='')
        print(self.event_name_B, end='')
        if self.operand_B is not None:
            print(".", end='')
            print(self.operand_B, end='')
        print(")", end='')

    #returns the literal as string
    def returnLiteral(self):
        str = self.printLiteral

        return str

    #return true if the literal is unary - the condition is only on operand_A,
    #means that operand_A is compared to a const number
    def isUnary(self):
        return self.operand_B is None

    #Returns a list of the names of the events that exist in the literal
    def eventsAppearInLiteral(self):
        if self.event_name_B is not None and self.event_name_A != self.event_name_B and not isinstance(self.event_name_B,float):
          return [self.event_name_A,self.event_name_B]
        else:
          return [self.event_name_A]


#Contains of literals, that have logical or between them in the clause.
class Clause:
    def __init__(self, clause):
        self.clause = clause

    #Returns a list of the event's names that exist in the clause
    def eventsAppearInClause(self):
        events = []

        for literal in self.clause:
            if literal.event_name_A not in events:
                events.append(literal.event_name_A)
            if not literal.isUnary():
                if literal.event_name_B not in events:
                    events.append(literal.event_name_B)

        return events

    #Prints the clause
    def printClause(self):
        print("(", end='')
        count = 0
        length = len(self.clause)
        for literal in self.clause:
            literal.printLiteral()
            if count != length-1:
                print(" OR ", end='')
            count += 1
        print(")", end='')