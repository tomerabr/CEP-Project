from Node import Node
from Node import Leaf

class LeftDeepTree:
    def __init__(self):
        self.root = None
        self.leftInnerNode = None
        self.innderNodes = []
        self.leaves = []

    # CNF is a list of Clauses
    def createTreeAccordingPattern(self, pattern):
        # leaves
        # self.leaves = self.getLeaves(CNF)
        # self.createLeaves(pattern.cond)

        for name in pattern.events:
            leaf = Leaf(name)
            self.leaves.append(leaf)

        CNF = pattern.cond
        # leftInnerNode
        # events = pattern.events.copy
        self.leftInnerNode = Node(CNF[0])  # the first clause
        self.leftInnerNode.leavesList = CNF[
            0].eventsAppearInClause()  # Is is the first node therefor the leaves in clause.eventsAppearInClause() didnt appear yet
        self.innderNodes.append(self.leftInnerNode)

        # tmp_leaves = []
        tmp_leaves = self.leftInnerNode.leavesList
        for clause in CNF[1:]:
            node = Node(clause)
            node.leavesList(filter(lambda leaf: leaf not in tmp_leaves,
                                   clause.eventsAppearInClause()))  # add only leaves which didnt appear yet
            node.leftInnerNode = self.innerNodes[-1]  # the last innerNode we were created
            self.innerNodes[-1].parent = node
            self.innerNodes.append(node)

        self.root = self.innerNodes[-1]


def solveTree(self):
    self.leftInnerNode.solveInnerNode()


'''
    def createLeaves(self, leavesNames):
      for name in leavesNames:
     		leaf = Leaf(name)
        self.leaves.append(leaf)


    def dumbCreateLeaves(self, CNF):
        leaves = []
        for clause in CNF:
          new_leaves = filter(lambda leaf: leaf not in leaves, clause.eventsAppearInClause())
          leaves.extend(new_leaves)
          for new_leaf in new_leaves:
            leaf = Leaf(new_leaf.name)
            self.leaves.append(new_leaf)
'''


def getNewLeaves(self, clause, leaveslist):
    new_leaves = filter(lambda leaf: leaf not in leaveslist, clause.eventsAppearInClause())
    return new_leaves


def fillLeaves(self, stocksList):
    for leaf in self.leaves:
        for stocks in stocksList:
            if stocks[0].ticker == leaf.name:
                leaf.addStocksToLeaf(stocks)
                break
