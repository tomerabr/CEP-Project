from Node import Node
from Node import Leaf


first_clause = 0
second_clause = 1
last_clause = -1
name = 0

'''
The tree that the algorithm is based on.
The tree is based on a Pattern. 
The tree contains leaves, which contains list of events from each type that in the pattern.
Every inner node relates to a clause and contains tuples of events that provided the clause of the node.
'''
class LeftDeepTree:

    '''
    Params:
    -pattern: the pattern the tree is based on.
    -list_of_lists: a list that contains lists for every event type. Each list contains the events
                    that been parsed from the input file.
    '''
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
        #for each event type's name, make a Leaf object and append it to the list of leaves
        for name in pattern.events:
            leaf = Leaf(name)
            self.leaves.append(leaf)

        CNF = pattern.cond
        self.leftInnerNode = Node(CNF[first_clause])  # the first clause
        leavesNames = CNF[first_clause].eventsAppearInClause()  # It is the first node therefore the leaves in clause.eventsAppearInClause() didn't appear yet
        for leaf in leavesNames:
            for actual_leaf in self.leaves:
                if actual_leaf.name == leaf:
                    self.leftInnerNode.leavesList.append(actual_leaf) #appending the leaf to the first inner node that uses it in the condition
                    break

        self.innerNodes.append(self.leftInnerNode)

        #for all other clauses
        for clause in CNF[second_clause:]:
            node = Node(clause)
            it = filter(lambda leaf: leaf not in leavesNames,
                                 clause.eventsAppearInClause())  # add only leaves which didn't appear yet
            for leaf in it:
                leavesNames.append(leaf)
                for actual_leaf in self.leaves:
                    if actual_leaf.name == leaf:
                        node.leavesList.append(actual_leaf)#appending the leaf to the first inner node that uses it in the condition
                        break

            node.leftInnerNode = self.innerNodes[last_clause]  # the last innerNode we created
            self.innerNodes[last_clause].parent = node
            self.innerNodes.append(node)

        self.root = self.innerNodes[last_clause] #the root is the last innerNode that was created

        #for every other leaf that hasn't been attached to an innerNode, attach to the root, as 
        #it only needs to be part of the list but doesn't have a clause that uses it
        for leaf in self.leaves:
            if leaf.name not in leavesNames:
                self.root.leavesList.append(leaf)

    '''
    First, creates the tree according to the pattern that been given.
    Next, fills the leaves according to list that been given.
    After that, calls the first innerNode's solve method a start running the algorithm.
    In the end, the root contains the tuples of events that meet all the conditions.
    '''
    def solveTree(self):
        self.createTreeAccordingPattern()
        self.fillLeaves()
        self.leftInnerNode.solveFirstNode(self.pattern.ptype,self.pattern.time_window,self.pattern.events)
        
    #Fills the leaves with events according to the list_of_lists
    def fillLeaves(self):
        for leaf in self.leaves:
            for events in self.list_of_lists:
                if events[name].ticker == leaf.name:
                    leaf.addEventsToLeaf(events)
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

    #Gets a filename and prints to it the tuples of events that are in the root.
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


    

