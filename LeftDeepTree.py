from Node import Node
from Node import Leaf


class LeftDeepTree:
    def __init__(self,pattern):
        self.root = None
        self.leftInnerNode = None
        self.innerNodes = []
        self.leaves = []
        self.pattern = pattern

    # CNF is a list of Clauses
    def createTreeAccordingPattern(self):
        # leaves
        # self.leaves = self.getLeaves(CNF)
        # self.createLeaves(pattern.cond)

        pattern = self.pattern
        for name in pattern.events:
            leaf = Leaf(name)
            self.leaves.append(leaf)

        CNF = pattern.cond
        # leftInnerNode
        # events = pattern.events.copy
        self.leftInnerNode = Node(CNF[0])  # the first clause
        # self.leftInnerNode.leavesList = CNF[0].eventsAppearInClause()
        leavesNames = CNF[0].eventsAppearInClause()  # Is is the first node therefor the leaves in clause.eventsAppearInClause() didnt appear yet
        for leaf in leavesNames:
            for actual_leaf in self.leaves:
                if actual_leaf.name == leaf:
                    self.leftInnerNode.leavesList.append(actual_leaf)
                    break

        self.innerNodes.append(self.leftInnerNode)

        #tmp_leaves = []
        #for leaf in self.leftInnerNode.leavesList:
            #tmp_leaves.extend(leaf.name)
        for clause in CNF[1:]:
            node = Node(clause)
            it = filter(lambda leaf: leaf not in leavesNames,
                                 clause.eventsAppearInClause())  # add only leaves which didnt appear yet
            # node.leavesList(filter(lambda leaf: leaf not in tmp_leaves,
            #                      clause.eventsAppearInClause()))
            for leaf in it:
                leavesNames.extend(leaf)
                for actual_leaf in self.leaves:
                    if actual_leaf.name == leaf:
                        node.leavesList.append(actual_leaf)
                        break

            node.leftInnerNode = self.innerNodes[-1]  # the last innerNode we were created
            self.innerNodes[-1].parent = node
            self.innerNodes.append(node)

        self.root = self.innerNodes[-1]

    def solveTree(self):
        self.leftInnerNode.solveInnerNode()
        #check timewindow for each tupple in root's eventsList
        self.root.checkTimeWindow(self.pattern.ptype,self.pattern.time_window,self.pattern.events)

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

    def printLeaves(self):
        for leaf in self.leaves:
            print(leaf.eventsList)

    def printInnerNodes(self):
        for node in self.innerNodes:
            node.printNode()

    def printRoot(self):
        self.root.printNode()

    def printLeftInnerNode(self):
        self.leftInnerNode.printNode()

    def printTree(self):
        print("Root:")
        self.printRoot()
        print("\nLeaves")
        self.printLeaves()
        print("\nleftInnerNode:")
        self.printLeftInnerNode()
        print("\nInnerNode:")
        self.printInnerNodes()

