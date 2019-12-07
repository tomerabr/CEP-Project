from Condition import Clause
from Pattern import Pattern


class Node:
    def __init__(self, clause):
        self.eventsLists = []
        self.clause = clause
        self.leftInnerNode = None
        self.leavesList = []
        self.parent = None

    '''
    def addLeaves(self, leavesList):
        self.leavesList = leavesList
    '''

    # def checkClause(self, stock1, stock2):
    #  if self.clause.checkClause(stock1, stock2):

    # Filter the eventsLists according to the clause of the current Node
    def checkWhenNoLeaves(self):
        for events in self.leftInnerNode.eventsLists:
            flag = False

            for first in events:
                for second in events:
                    if self.clause.checkClause(first, second):
                        flag = True
                    break
                if flag == True:
                    break

            self.eventsLists.append(events)

    # Can only happen in the first leftInnerNode in the left deep tree.
    # Iterate over the first two leaves and save all the partial result.
    # Than, iterate each leaf(except the first two which we had already taken care of), and Filter the the eventsList accordingly.
    def checkWhenOnlyLeaves(self):
        # assuming there are more than 2 leaves at the beginning,
        # TODO: check num of leaves
        first_leaf_list = self.leavesList[0].eventsList
        second_leaf_list = self.leavesList[1].eventsList

        for stock1 in first_leaf_list:
            for stock2 in second_leaf_list:
                if self.clause.checkClause(stock1, stock2):
                    self.eventsLists.append([stock1, stock2])

        # iterate over the other leaves
        self.filterAccordingLeaves(2)

    def checkWhenBoth(self):
        self.filterAccordingLeaves(0)

    def filterAccordingLeaves(self, index):
        for leaf in self.leavesList[index:]:
            for stock in leaf.eventList:
                for events_list in self.eventsLists:  # Filter this
                    flag = False
                    for event in events_list:
                        if self.clause.checkClause(stock, event):
                            events_list.append(stock.copy())
                            flag = True
                            break
                    if not flag:
                        self.eventsLists.remove(events_list)
                        # remove is not efficient

        # We need the create the left deep tree and than operate this function on the first inner leaf

    def solveInnerNode(self):
        # We are in the root
        if self.parent is None and self.leftInnerNode is None:  # we have only one node
            self.checkWhenOnlyLeaves()
            return
        elif self.parent is None and self.leftInnerNode is not None:  # we are in the root (we have more then 1 inner node)
            if self.leavesList is None:
                self.checkWhenNoLeaves()
            elif self.checkWhenBoth:
                self.checkWhenBoth()
        return

        if self.leftInnerNode is None:
            self.checkWhenOnlyLeaves()
        elif self.leavesList is None:
            self.checkWhenNoLeaves()
        elif self.checkWhenBoth:
            self.checkWhenBoth()

        self.solveInnerNode(self.parent)

    def printNode(self):
        self.clause.printClause()
        print("\nLeaves:")
        for leaf in self.leavesList:
            print(leaf.name)
        # print(self.leavesList)
        # if self.eventsLists is not None:
        for eventList in self.eventsLists:
            print(eventList)


# Create functions for organizing the code i.e כפילויות קוד
# Memory mangement - delete each stock from the leaf when we finish with it
# Tests

'''
    def addLeaf(self, leaf):
        self.leavesList.append(leaf)


    def addLeftInnerNode(self, node):
        self.leftInnerNode = node
'''


# each leaf will contain list of specific event
# each leaf will be connected to only one inner node
class Leaf:
    def __init__(self, name):
        self.eventsList = []
        self.name = name
        # self.parent = None

    def addStocksToLeaf(self, stocks):
        self.eventsList.extend(stocks)


'''
    def addParent(self, node):
        self.node = node
'''
