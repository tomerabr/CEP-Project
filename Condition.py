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
    def __init__(self, event_name_A, event_name_B, operand_A, operand_B, operator):
        self.event_name_A = event_name_A  # first event name, string
        self.event_name_B = event_name_B  # second event name, string
        self.operand_A = operand_A  # first event operand, string
        self.operand_B = operand_B  # second event operand, string
        self.operator = operator

    def checkOperator(self, value1, value2):
        if self.operator == Op.GREATER:
            return (value1 > value2)
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

    def OperandOfStockB(self, stock):
        if self.operand_B == Operand.OPENING_PRICE:
            return stock.opening

        elif self.operand_B == Operand.PEAK_PRICE:
            return stock.peak

        elif self.operand_ == Operand.LOWEST_PRICE:
            return stock.lowest
        elif self.operand_B == Operand.CLOSE_PRICE:
            return stock.close
        elif self.operand_B == Operand.VOLUME:
            return stock.volume


def checkLiteral(self, stock1, stock2):
    if stock1.ticker != self.event_name_A or stock2.ticker != self.event_name_B:
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


# clause is a disjunction of literals, where each literal is a PrimitiveCondition
# every inner node in the tree is a clause
class Clause:
    def __init__(self, clause):
        self.clause = clause

    def checkClause(self, stock1, stock2):
        for literal in self.clause:
            if literal.checkLiteral(stock1, stock2):
                return True
        return False


    # class CNF:
    #   def __init__(self, cnf):
    #    self.cnf = cnf
