from Node import Node
from Node import Leaf

#The tree that algorithm is based on.
#The tree is based on a Pattern. 
#The tree contains leaves, which contains list of events from each type that in the pattern.
class LeftDeepTree:

    #Get the pattern that the tree is based on and list of lists that contain the events
    #that have been parsed from the input file
    def __init__(self,pattern,list_of_lists):
        self.root = None
        self.leftInnerNode = None
        self.innerNodes = []
        self.leaves = []
        self.pattern = pattern
        self.list_of_lists = list_of_lists

    # Creates the tree according the given pattern
    def createTreeAccordingPattern(self):
    
        pattern = self.pattern
        for name in pattern.events:
            leaf = Leaf(name)
            self.leaves.append(leaf)

        CNF = pattern.cond
        self.leftInnerNode = Node(CNF[0])  # the first clause
        leavesNames = CNF[0].eventsAppearInClause()  # It is the first node therefore the leaves in clause.eventsAppearInClause() didn't appear yet
        for leaf in leavesNames:
            for actual_leaf in self.leaves:
                if actual_leaf.name == leaf:
                    self.leftInnerNode.leavesList.append(actual_leaf)
                    break

        self.innerNodes.append(self.leftInnerNode)

        
        for clause in CNF[1:]:
            node = Node(clause)
            it = filter(lambda leaf: leaf not in leavesNames,
                                 clause.eventsAppearInClause())  # add only leaves which didn't appear yet
            for leaf in it:
                leavesNames.append(leaf)
                for actual_leaf in self.leaves:
                    if actual_leaf.name == leaf:
                        node.leavesList.append(actual_leaf)
                        break

            node.leftInnerNode = self.innerNodes[-1]  # the last innerNode we created
            self.innerNodes[-1].parent = node
            self.innerNodes.append(node)

        self.root = self.innerNodes[-1]

    def solveTree(self):
        self.createTreeAccordingPattern()
        self.fillLeaves()
        self.leftInnerNode.solveFirstNode(self.pattern.ptype,self.pattern.time_window,self.pattern.events)
        
    #Fills the leaves with events according to the list_of_lists
    def fillLeaves(self):
        for leaf in self.leaves:
            for stocks in self.list_of_lists:
                if stocks[0].ticker == leaf.name:
                    leaf.addStocksToLeaf(stocks)
                    break

    #Prints the leaves of the tree
    def printLeaves(self):
        for leaf in self.leaves:
            print(leaf.eventsList)

    #Prints the inner nodes of the tree
    def printInnerNodes(self):
        for node in self.innerNodes:
            node.printNode()

    #Prints the root of the tree
    def printRoot(self):
        self.root.printNode()

    #Prints the left inner node of the tree
    def printLeftInnerNode(self):
        self.leftInnerNode.printNode()

    #Prints the tree
    def printTree(self):
        print("Root:")
        self.printRoot()
        print("\nLeaves")
        self.printLeaves()
        print("\nleftInnerNode:")
        self.printLeftInnerNode()
        print("\nInnerNode:")
        self.printInnerNodes()

    #Gets a filename and prints to it the events that are in the root.
    #The events are printed according to the list of names that was given.
    def outputToFile(self, filename):
        f = open(filename,'w')
        for tupple in self.root.eventsLists:
            by_names = []
            for name in self.pattern.events:
                for ev in tupple:
                    if ev.ticker == name:
                        by_names.append(ev)
            print([a for a in by_names],file=f)
        f.close()


    

