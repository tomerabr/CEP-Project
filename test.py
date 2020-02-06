from Pattern import Pattern, PTYPE
from Condition import Literal,Clause, Op
from NasdaqStock import Operand, NasdaqStock
from LeftDeepTree import LeftDeepTree
from Parser import Parser

'''
Literals creation
'''
# Literals for basic tests
literal1 = Literal(Op.GREATER ,"AMZN",  Operand.VOLUME,"EBAY", Operand.VOLUME)
literal2 = Literal(Op.GREATER_OR_EQUAL,"CROX", Operand.VOLUME, "EBAY", Operand.VOLUME)
literal3 = Literal(Op.LESS, "EBAY", Operand.LOWEST_PRICE, 27.68)
literal4 = Literal(Op.LESS,"AMZN", Operand.CLOSE_PRICE, "AMZN", Operand.PEAK_PRICE)
literal5 = Literal(Op.GREATER,"AMZN", Operand.VOLUME, "BIDU", Operand.VOLUME)

# Cycle
literal6 = Literal(Op.GREATER,"CROX", Operand.VOLUME, "BIDU", Operand.VOLUME)
literal7 = Literal(Op.LESS,"CROX", Operand.VOLUME, "BIDU", Operand.VOLUME)
literal8 = Literal(Op.LESS,"BIDU", Operand.VOLUME,"CROX", Operand.VOLUME)

# Volume
literal9 = Literal(Op.GREATER ,"AMZN",  Operand.VOLUME,"EBAY", Operand.VOLUME)
literal10 = Literal(Op.GREATER ,"EBAY",  Operand.VOLUME,"CROX", Operand.VOLUME)
literal11 = Literal(Op.GREATER ,"CROX",  Operand.VOLUME,"BIDU", Operand.VOLUME)
literal12 = Literal(Op.GREATER ,"EBAY",  Operand.VOLUME, 300)
litreal13 = Literal(Op.GREATER ,"CROX",  Operand.VOLUME, 400)
literal14 = Literal(Op.LESS ,"AMZN",  Operand.VOLUME, 300)
litreal15 = Literal(Op.LESS ,"CROX",  Operand.VOLUME, 400)

# Volume sequence
literal16 = Literal(Op.LESS ,"AMZN",  Operand.VOLUME,"EBAY", Operand.VOLUME)
literal17 = Literal(Op.LESS  ,"EBAY",  Operand.VOLUME,"CROX", Operand.VOLUME)
literal18 = Literal(Op.LESS  ,"CROX",  Operand.VOLUME,"BIDU", Operand.VOLUME)
literal19 = Literal(Op.GREATER ,"AMZN",  Operand.VOLUME, 100)
literal20 = Literal(Op.LESS_OR_EQUAL ,"BIDU",  Operand.VOLUME, 35000)

# Opening price
literal21 = Literal(Op.GREATER_OR_EQUAL,"AMZN",  Operand.OPENING_PRICE, 78.66)
literal22 = Literal(Op.GREATER,"AMZN",  Operand.OPENING_PRICE, 78.68)
literal23 = Literal(Op.LESS,"EBAY",  Operand.OPENING_PRICE, 27.8)

# Volume with const
literal24 = Literal(Op.GREATER_OR_EQUAL ,"AMZN",  Operand.VOLUME, 1000)
literal25 = Literal(Op.LESS ,"AMZN",  Operand.VOLUME, 347)

# Lowest price
literal26 = Literal(Op.LESS,"AMZN",  Operand.LOWEST_PRICE,"AMZN", Operand.PEAK_PRICE)

# Check new stock in the end
literal27 = Literal(Op.GREATER_OR_EQUAL,"AAPL", Operand.VOLUME, 25000)

# check mutiple times the same condition
literal28 = Literal(Op.LESS,"EBAY", Operand.VOLUME, 1400)
literal29 = Literal(Op.LESS,"EBAY", Operand.VOLUME, 1400)
literal30 = Literal(Op.LESS,"EBAY", Operand.VOLUME, 1400)


'''''
Clause creation
'''
clause1 = Clause({literal1})
clause2 = Clause({literal2})
clause3 = Clause({literal3})
clause4 = Clause({literal4})
clause5_6 = Clause({literal5,literal6})
clause6 = Clause({literal6})
clause7 = Clause({literal7})
clause8 = Clause({literal8})
clause9 = Clause({literal9})
clause10 = Clause({literal10})
clause11 = Clause({literal11})
clause12_13 = Clause({literal12, litreal13})
clause14_15 = Clause({literal14, litreal15})
clause16 = Clause({literal16})
clause17 = Clause({literal17})
clause18 = Clause({literal18})
clause19 = Clause({literal19})
clause20 = Clause({literal20})
clause21 = Clause({literal21})
clause22_23 = Clause({literal22, literal23})
clause24_25 = Clause({literal24, literal25})
clause26 = Clause({literal26})
clause27 = Clause({literal27})
clause28_to_30 = Clause({literal28,literal29,literal30})


'''
Pattern creation
'''
pattern1 = Pattern(PTYPE.AND, ["AMZN", "EBAY"], [clause1], 2)
pattern2 = Pattern(PTYPE.AND, ["CROX", "EBAY"], [clause2], 2)
pattern3 = Pattern(PTYPE.AND, ["AMZN", "EBAY"], [clause3], 2)
pattern4 = Pattern(PTYPE.AND, ["AMZN"], [clause4], 2)
pattern5_6 = Pattern(PTYPE.AND, ["AMZN", "BIDU", "CROX"], [clause5_6], 4)
pattern6_7 = Pattern(PTYPE.AND, ["CROX","BIDU"], [clause6, clause7], 1)
pattern7_8 = Pattern(PTYPE.AND, ["CROX","BIDU"], [clause7, clause8], 1)
pattern9_to_13 = Pattern(PTYPE.SEQ, ["AMZN", "EBAY", "CROX", "BIDU"], [clause9,clause10,clause11,clause12_13], 3)
pattern9_to_15 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX", "BIDU"], [clause9,clause10,clause11,clause14_15], 3)
pattern16_to_20_with_aapl = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX", "BIDU","AAPL"],
                                    [clause16,clause17,clause18,clause19,clause20], 5)
pattern16_to_20 = Pattern(PTYPE.AND, ["AMZN", "EBAY", "CROX", "BIDU"], [clause16,clause17,clause18,clause19,clause20],3)
pattern21_to_23 = Pattern(PTYPE.AND, ["AMZN", "EBAY"], [clause21,clause22_23], 3)
pattern24_25 = Pattern(PTYPE.AND, ["AMZN", "EBAY"], [clause24_25], 3)
pattern26_27 = Pattern(PTYPE.AND, ["AMZN", "BIDU", "AAPL"], [clause26,clause27], 3)
pattern28_to_30 = Pattern(PTYPE.AND, ["AMZN", "EBAY"], [clause28_to_30], 3)


'''
Parser creation
'''
Parser1 = Parser(pattern1,"Stocks_6000.txt", NasdaqStock)
Parser2 = Parser(pattern2,"Stocks_6000.txt", NasdaqStock)
Parser3 = Parser(pattern3,"Stocks_6000.txt", NasdaqStock)
Parser4 = Parser(pattern4,"Stocks_6000.txt", NasdaqStock)
Parser5_6 = Parser(pattern5_6,"Stocks_6000.txt", NasdaqStock)
Parser6_7 = Parser(pattern5_6,"Stocks_6000.txt", NasdaqStock)
Parser7_8 = Parser(pattern7_8,"Stocks_6000.txt", NasdaqStock)
Parser9_to_13 = Parser(pattern9_to_13,"Stocks_6000.txt", NasdaqStock)
Parser9_to_15 = Parser(pattern9_to_15,"Stocks_6000.txt", NasdaqStock)
Parser16_to_20 = Parser(pattern16_to_20,"Stocks_6000.txt", NasdaqStock)
Parser16_to_20_with_aapl = Parser(pattern16_to_20_with_aapl,"Stocks_6000.txt", NasdaqStock)
Parser21_to_23 = Parser(pattern21_to_23,"Stocks_6000.txt", NasdaqStock)
Parser24_25 = Parser(pattern24_25,"Stocks_6000.txt", NasdaqStock)
Parser26_27 = Parser(pattern26_27,"Stocks_6000.txt", NasdaqStock)
Parser28_to_30 = Parser(pattern28_to_30,"Stocks_6000.txt", NasdaqStock)


'''
Tree creation.
Each tree is basically a test
'''
# Basic tests
tree1 = LeftDeepTree(pattern1, Parser1.list_of_lists)
tree2 = LeftDeepTree(pattern2, Parser2.list_of_lists)
tree3 = LeftDeepTree(pattern3, Parser3.list_of_lists)
tree4 = LeftDeepTree(pattern4, Parser4.list_of_lists)
tree5_6 = LeftDeepTree(pattern5_6, Parser5_6.list_of_lists)

# Should get an empty file, zero matches
tree6_7 = LeftDeepTree(pattern6_7, Parser6_7.list_of_lists)
tree7_8 = LeftDeepTree(pattern7_8, Parser7_8.list_of_lists)

# Volume tests
tree9_to_13 = LeftDeepTree(pattern9_to_13, Parser9_to_13.list_of_lists) #check SEQ
tree9_to_15 = LeftDeepTree(pattern9_to_15, Parser9_to_15.list_of_lists)
tree16_to_20 = LeftDeepTree(pattern16_to_20, Parser16_to_20.list_of_lists)

# Check new events in the end, which do not appear in the clause
tree16_to_20_with_aapl = LeftDeepTree(pattern16_to_20_with_aapl, Parser16_to_20_with_aapl.list_of_lists)

# Opening price test with const and OR
tree21_to_23 = LeftDeepTree(pattern21_to_23, Parser21_to_23.list_of_lists)

# Volume with const
tree24_25 = LeftDeepTree(pattern24_25, Parser24_25.list_of_lists)

# check stock in the last node AND check when Pattern include events with aren't appear in the clause
tree26_27 = LeftDeepTree(pattern26_27, Parser26_27.list_of_lists)

# Check multiple time the same condition
tree28_to_30 = LeftDeepTree(pattern28_to_30, Parser28_to_30.list_of_lists)

'''
Using the test:
in order to run a test, i.e solve a tree, change the name of the tree below to the desirable tree
'''

tree1.solveTree()
tree1.outputToFile("output.txt")