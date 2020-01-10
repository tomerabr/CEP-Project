from NasdaqParser import NasdaqParser
from Pattern import Pattern, PTYPE
from Condition import Literal,Clause, Op, Operand
from LeftDeepTree import LeftDeepTree

literal1 = Literal(Op.GREATER ,"AMZN",  Operand.VOLUME,"EBAY", Operand.VOLUME)
literal2 = Literal(Op.GREATER_OR_EQUAL,"CROX", Operand.VOLUME, "EBAY", Operand.VOLUME)
literal3 = Literal(Op.GREATER_OR_EQUAL, "AMZN", Operand.LOWEST_PRICE, 74.75)
literal4 = Literal(Op.LESS,"AMZN", Operand.CLOSE_PRICE, "AMZN", Operand.PEAK_PRICE)
literal5 = Literal(Op.GREATER,"AMZN", Operand.VOLUME, "BIDU", Operand.VOLUME)
literal6 = Literal(Op.GREATER,"CROX", Operand.VOLUME, "BIDU", Operand.VOLUME)


clause1 = Clause({literal3})
clause2 = Clause({literal1})
clause3 = Clause({literal3,literal4})#check no double of events
clause4 = Clause({literal2})
clause5 = Clause({literal5})
clause6 = Clause({literal6})

pattern1 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX", "BIDU"], [clause2,clause1,clause5,clause4], 2)
pattern2 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX"], [clause2,clause4], 2)
pattern3 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX","BIDU"], [clause2,clause6,clause5], 2)
#test 2 clauses

np1 = NasdaqParser(pattern1)
np2 = NasdaqParser(pattern2)
np3 = NasdaqParser(pattern3)

#np1.printList()
'''
tree3 = LeftDeepTree(pattern3)#conceal
tree3.createTreeAccordingPattern()
tree3.fillLeaves(np3.list_of_lists)
tree3.solveTree()
tree3.printRoot()


tree1 = LeftDeepTree(pattern1)
tree1.createTreeAccordingPattern()
tree1.fillLeaves(np1.list_of_lists)
tree1.solveTree()
tree1.printRoot()
'''

tree2 = LeftDeepTree(pattern2)#conceal
tree2.createTreeAccordingPattern()
tree2.fillLeaves(np2.list_of_lists)
tree2.solveTree()
tree2.printRoot()


