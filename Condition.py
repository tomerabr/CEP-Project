from enum import Enum


# from NasdaqStock import NasdaqStock


class Op(Enum):
    GREATER = 1
    LESS = 2
    GREATER_OR_EQUAL = 3
    LESS_OR_EQUAL = 4
    EQUAL = 5
    NOT_EQUAL = 6


class Operand(Enum):
    OPENING_PRICE = 1
    PEAK_PRICE = 2
    LOWEST_PRICE = 3
    CLOSE_PRICE = 4
    VOLUME = 5


class Literal:
    def __init__(self, operator, event_name_A, operand_A, event_name_B, operand_B=None):
        self.event_name_A = event_name_A  # first event name, string
        self.event_name_B = event_name_B  # second event name, string
        self.operand_A = operand_A  # first event operand, string
        self.operand_B = operand_B  # second event operand, string
        self.operator = operator

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

    def OperandOfStockB(self, stock=None):
        if stock is None:
            return self.event_name_B
        if self.operand_B == Operand.OPENING_PRICE:
            return stock.opening
        elif self.operand_B == Operand.PEAK_PRICE:
            return stock.peak
        elif self.operand_B == Operand.LOWEST_PRICE:
            return stock.lowest
        elif self.operand_B == Operand.CLOSE_PRICE:
            return stock.close
        elif self.operand_B == Operand.VOLUME:
            return stock.volume

    # if stock2 = None it will return the const value


    def checkLiteral(self, stock1, stock2=None):
        if stock1.ticker != self.event_name_A or (stock2 is not None and stock2.ticker != self.event_name_B):
            return False
        if self.operand_A == Operand.OPENING_PRICE:
            return self.checkOperator(stock1.opening, self.OperandOfStockB(stock2))
        elif self.operand_A == Operand.PEAK_PRICE:
            return self.checkOperator(stock1.peak, self.OperandOfStockB(stock2))
        elif self.operand_A == Operand.LOWEST_PRICE:
            return self.checkOperator(stock1.lowest, self.OperandOfStockB(stock2))
        elif self.operand_A == Operand.CLOSE_PRICE:
            return self.checkOperator(stock1.close, self.OperandOfStockB(stock2))
        elif self.operand_A == Operand.VOLUME:
            return self.checkOperator(stock1.volume, self.OperandOfStockB(stock2))
        else:
            return False

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


    def returnLiteral(self):
        str = self.printLiteral

        return str


def isUnary(self):
    return self.operand_B is None


# clause is a disjunction of literals, where each literal is a PrimitiveCondition
# every inner node in the tree is a clause
class Clause:
    def __init__(self, clause):
        self.clause = clause

    def checkClause(self, stock1, stock2=None):
        for literal in self.clause:
            if stock2 == None and literal.isUnary():  # we want to check only Unary
                if literal.checkLiteral(stock1):
                    return True
            elif stock2 is not None and literal.isUnary() == False:
                if literal.checkLiteral(stock1, stock2):
                    return True
        return False

    def eventsAppearInClause(self):
        events = []

        for literal in self.clause:
            if literal.event_name_A not in events:
                events.append(literal.event_name_A)
            if not literal.isUnary():
                if literal.event_name_B not in events:
                    events.append(literal.event_name_B)

        return events

    def printClause(self):
        print("(", end='')
        flag = 0
        for literal in self.clause:
            literal.printLiteral()
            if (flag == 1):
                print(" OR ", end='')
            flag = 1
        print(")", end='')



