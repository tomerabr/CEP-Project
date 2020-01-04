from NasdaqParser import NasdaqParser
from Pattern import Pattern, PTYPE
from Condition import Literal,Clause, Op, Operand
from LeftDeepTree import LeftDeepTree

literal1 = Literal(Op.EQUAL ,"AMZN",  Operand.VOLUME,"EBAY", Operand.VOLUME)
literal2 = Literal(Op.GREATER_OR_EQUAL,"CROX", Operand.VOLUME, "EBAY", Operand.VOLUME)
literal3 = Literal(Op.GREATER_OR_EQUAL, "AMZN", Operand.LOWEST_PRICE, 74.75)
literal4 = Literal(Op.LESS,"AMZN", Operand.CLOSE_PRICE, "AMZN", Operand.PEAK_PRICE)
literal5 = Literal(Op.EQUAL,"AMZN", Operand.CLOSE_PRICE, "BIDU", Operand.CLOSE_PRICE)


clause1 = Clause({literal3})
clause2 = Clause({literal1})
clause3 = Clause({literal3,literal4})
clause4 = Clause({literal2})
clause5 = Clause({literal5})


pattern1 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX", "BIDU"], [clause3,clause4,clause5], 3)
pattern2 = Pattern(PTYPE.AND, ["AMZN", "EBAY"], [clause2], 1)
#test 2 clauses

np1 = NasdaqParser(pattern1)
np2 = NasdaqParser(pattern2)

#np1.printList()
'''
tree1 = LeftDeepTree()
tree1.createTreeAccordingPattern(pattern1)
tree1.fillLeaves(np1.list_of_lists)
tree1.solveTree()
tree1.printRoot()

'''
tree2 = LeftDeepTree(pattern2)#conceal
tree2.createTreeAccordingPattern()
tree2.fillLeaves(np2.list_of_lists)
tree2.solveTree()
tree2.printRoot()


