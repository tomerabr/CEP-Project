from Parser import Parser
from Pattern import Pattern, PTYPE
from Condition import Literal,Clause, Op
from NasdaqStock import Operand, NasdaqStock
from LeftDeepTree import LeftDeepTree

literal1 = Literal(Op.GREATER ,"AMZN",  Operand.VOLUME,"EBAY", Operand.VOLUME)
literal2 = Literal(Op.GREATER_OR_EQUAL,"CROX", Operand.VOLUME, "EBAY", Operand.VOLUME)
literal3 = Literal(Op.LESS, "EBAY", Operand.LOWEST_PRICE, 27.68)
literal4 = Literal(Op.LESS,"AMZN", Operand.CLOSE_PRICE, "AMZN", Operand.PEAK_PRICE)
literal5 = Literal(Op.GREATER,"AMZN", Operand.VOLUME, "BIDU", Operand.VOLUME)
literal6 = Literal(Op.GREATER,"CROX", Operand.VOLUME, "BIDU", Operand.VOLUME)
literal7 = Literal(Op.LESS,"CROX", Operand.VOLUME, "BIDU", Operand.VOLUME)
literal8 = Literal(Op.LESS,"BIDU", Operand.VOLUME,"CROX", Operand.VOLUME)

literal9 = Literal(Op.GREATER ,"AMZN",  Operand.VOLUME,"EBAY", Operand.VOLUME)
literal10 = Literal(Op.GREATER ,"EBAY",  Operand.VOLUME,"CROX", Operand.VOLUME)
literal11 = Literal(Op.GREATER ,"CROX",  Operand.VOLUME,"BIDU", Operand.VOLUME)
literal12 = Literal(Op.GREATER ,"EBAY",  Operand.VOLUME, 300)
litreal13 = Literal(Op.GREATER ,"CROX",  Operand.VOLUME, 400)
literal14 = Literal(Op.LESS ,"AMZN",  Operand.VOLUME, 300)
litreal15 = Literal(Op.LESS ,"CROX",  Operand.VOLUME, 400)

#Volume sequence
literal16 = Literal(Op.LESS ,"AMZN",  Operand.VOLUME,"EBAY", Operand.VOLUME)
literal17 = Literal(Op.LESS  ,"EBAY",  Operand.VOLUME,"CROX", Operand.VOLUME)
literal18 = Literal(Op.LESS  ,"CROX",  Operand.VOLUME,"BIDU", Operand.VOLUME)
literal19 = Literal(Op.GREATER ,"AMZN",  Operand.VOLUME, 100)
literal20 = Literal(Op.LESS_OR_EQUAL ,"BIDU",  Operand.VOLUME, 35000)

literal24 = Literal(Op.GREATER_OR_EQUAL ,"AMZN",  Operand.VOLUME, 1000)
literal25 = Literal(Op.LESS ,"AMZN",  Operand.VOLUME, 347)

#Opening price
literal21 = Literal(Op.GREATER_OR_EQUAL,"AMZN",  Operand.OPENING_PRICE, 78.66)
literal22 = Literal(Op.GREATER,"AMZN",  Operand.OPENING_PRICE, 78.68)
literal23 = Literal(Op.LESS,"EBAY",  Operand.OPENING_PRICE, 27.8)
literal26 = Literal(Op.EQUAL,"AMZN",  Operand.LOWEST_PRICE,"AMZN", Operand.PEAK_PRICE)

#Check new stock in the end
literal27 = Literal(Op.GREATER_OR_EQUAL,"AAPL", Operand.VOLUME, 25000)

#check triple
literal28 = Literal(Op.LESS,"EBAY", Operand.VOLUME, 1400)
literal29 = Literal(Op.LESS,"EBAY", Operand.VOLUME, 1400)
literal30 = Literal(Op.LESS,"EBAY", Operand.VOLUME, 1400)



clause1 = Clause({literal3})
clause2 = Clause({literal1})
clause3 = Clause({literal4})#check no double of events
clause4 = Clause({literal1,literal5})
clause5 = Clause({literal5})
clause6 = Clause({literal6})
clause7 = Clause({literal7})
clause8 = Clause({literal8})

clause9 = Clause({literal9})
clause10 = Clause({literal10 })
clause11 = Clause({literal11})
clause12 = Clause({literal12, litreal13})
clause13 = Clause({literal14, litreal15})
clause14 = Clause({literal16})
clause15 = Clause({literal17})
clause16 = Clause({literal18})
clause17 = Clause({literal19})
clause20 = Clause({literal20})
clause21 = Clause({literal21})
clause22 = Clause({literal22, literal23})
clause24 = Clause({literal24, literal25})
clause26 = Clause({literal26})
clause27 = Clause({literal27})
clause28 = Clause({literal28,literal29,literal30})


pattern1 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX", "BIDU"], [clause2,clause1,clause5,clause4], 2)
pattern2 = Pattern(PTYPE.SEQ, ["AMZN","EBAY", "CROX", "BIDU"], [clause4,clause1,clause3], 1)
pattern3 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX","BIDU"], [clause2,clause6,clause5], 1)
pattern4 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "BIDU"], [clause4,clause1], 1)
pattern7 = Pattern(PTYPE.AND, ["CROX","BIDU"], [clause7, clause6], 1)
pattern8 = Pattern(PTYPE.AND, ["CROX","BIDU"], [clause7, clause8], 1)
pattern9 = Pattern(PTYPE.SEQ, ["CROX","BIDU"], [clause7, clause8], 1)

pattern10 = Pattern(PTYPE.SEQ, ["AMZN", "EBAY", "CROX", "BIDU"], [clause9,clause10,clause11,clause12], 3)
pattern11 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX", "BIDU"], [clause9,clause10,clause11,clause12], 3)
pattern12 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX", "BIDU"], [clause9,clause10,clause11,clause13], 3)
pattern13 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX", "BIDU", "AAPL"],
                    [clause14,clause15,clause16,clause17,clause20,clause21,clause22,clause24,clause26,clause28,clause27], 5)
#test 2 clauses
'''
np1 = NasdaqParser(pattern1,"Stocks o.txt")
np2 = NasdaqParser(pattern2,"Stocks o.txt")
np3 = NasdaqParser(pattern3,"Stocks o.txt")
np4 = NasdaqParser(pattern4,"Stocks o.txt")
np7 = NasdaqParser(pattern7,"Stocks o.txt")
np8 = NasdaqParser(pattern8,"Stocks o.txt")

n10 = NasdaqParser(pattern10,"Stocks o.txt")
n11 = NasdaqParser(pattern10,"Stocks o.txt")
n12 = NasdaqParser(pattern12,"Stocks o.txt")'''
n13 = Parser(pattern13,"Stocks o.txt",NasdaqStock)


tree13 = LeftDeepTree(pattern13, n13.list_of_lists)#conceal
tree13.solveTree()
tree13.outputToFile("output2.txt")

'''
tree12 = LeftDeepTree(pattern12,n12.list_of_lists)#conceal
tree12.solveTree()
tree12.outputToFile("output.txt")

tree11 = LeftDeepTree(pattern11,n11.list_of_lists)#conceal
tree11.solveTree()
tree11.outputToFile("output.txt")


tree10 = LeftDeepTree(pattern10,n10.list_of_lists)#conceal
tree10.solveTree()
tree10.outputToFile("output.txt")



tree4 = LeftDeepTree(pattern4,np4.list_of_lists)#conceal
tree4.solveTree()
tree4.printRoot()
tree4.outputToFile("output.txt")


tree3 = LeftDeepTree(pattern3,np3.list_of_lists)#conceal
tree3.solveTree()
tree3.printRoot()


tree1 = LeftDeepTree(pattern1,np1.list_of_lists)
tree1.solveTree()
#tree1.printRoot()
tree1.outputToFile("output.txt")''''''


tree2 = LeftDeepTree(pattern2,np2.list_of_lists)#conceal
tree2.solveTree()
#tree2.printRoot()
tree2.outputToFile("output.txt") '''

#test for no output - working
'''
tree7 = LeftDeepTree(pattern7,np7.list_of_lists)
tree7.solveTree()
tree7.outputToFile("output.txt")

tree8 = LeftDeepTree(pattern8,np8.list_of_lists)
tree8.solveTree()
tree8.outputToFile("output.txt")

tree9 = LeftDeepTree(pattern8,np8.list_of_lists)
tree9.solveTree()
tree9.outputToFile("output.txt")'''







