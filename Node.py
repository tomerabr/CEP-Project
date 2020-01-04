from Condition import Clause
from Pattern import Pattern, PTYPE
import copy


class Node:
    def __init__(self, clause):
        self.eventsLists = []
        self.clause = clause
        self.leftInnerNode = None
        self.leavesList = []
        self.parent = None
        #self.ptype = ptype
        #self.timeWindow = timeWindow

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
                        self.eventsLists.append(copy.copy(events))
                flag = True
                break
            if flag:
                break

        self.leftInnerNode.eventsLists.clear()  # dunno if efficient

    # Can only happen in the first leftInnerNode in the left deep tree. Iterate over the first two leaves and save
    # all the partial result. Than, iterate each leaf(except the first two which we had already taken care of),
    # and Filter the the eventsList accordingly.
    def checkWhenOnlyLeaves(self):

        # TODO: check num of leaves, empty pattern
        # double c in one clause

        # if(len(self.leavesList) == 1):
        # for stock in self.leavesList[0].eventList:
        #  if self.

        if len(self.leavesList) == 0:  # empty tree
            return

        if len(self.leavesList) == 1:  # a < a or a < const
            # for stock in self.leavesList[0].eventsList:
            # if self.clause.checkClause(stock) or self.clause.checkClause(stock,stock):
            # self.eventsLists.append([stock.copy()])
            self.solveSoloLeaf(self.leavesList[0])
            self.leavesList[0].eventsList.clear()
            return
            # for stock1 in self.leavesList[0].eventsList:
            # for stock2 in self.leavesList[0].eventsList:
            # if stock1 != stock2:
            # if self.clause.checkClause(stock1,stock2):
            # self.eventsLists.appen([stock1.copy(),stock2.copy()])

            # there are more than 2 leaves at the beginning
            # add function build
        first_leaf_list = self.leavesList[0].eventsList
        second_leaf_list = self.leavesList[1].eventsList

        # handle Unary
        self.solveSoloLeaf(self.leavesList[0])
        self.solveSoloLeaf(self.leavesList[1])

        for stock1 in first_leaf_list:
            for stock2 in second_leaf_list:
                if self.clause.checkClause(stock1, stock2):
                    self.eventsLists.append([copy.copy(stock1), copy.copy(stock2)])

        self.leavesList[0].eventsList.clear()
        self.leavesList[1].eventsList.clear()

        # iterate over the other leaves
        if len(self.leavesList) > 2:
            self.filterAccordingLeaves(2)

    def solveSoloLeaf(self, leavesList):
        for stock in leavesList.eventsList:
            if self.clause.checkClause(stock) or self.clause.checkClause(stock, stock):
                self.eventsLists.append([copy.copy(stock)])
        # We need the create the left deep tree and than operate this function on the first inner leaf

    def solveInnerNode(self):
        # We are in the root

        if self.parent is None and self.leftInnerNode is None:  # we have only one node
            self.checkWhenOnlyLeaves()
            return
        elif self.parent is None and self.leftInnerNode is not None:  # we are in the root (we have more then 1 inner node)
            if self.leavesList is None:
                self.checkWhenNoLeaves()
            else:
                self.checkWhenBoth()
            return

        # first node
        if self.leftInnerNode is None:
            self.checkWhenOnlyLeaves()
        elif self.leavesList is None:
            self.checkWhenNoLeaves()
        else:
            self.checkWhenBoth()

        self.parent.solveInnerNode()

    def checkWhenBoth(self):
        self.eventsLists = copy.copy(self.leftInnerNode.eventsLists)
        self.filterAccordingLeaves(0)

    def filterAccordingLeaves(self, index):
        num = len(self.eventsLists[0])  # cannot be empty
        for leaf in self.leavesList[index:]:
            for stock in leaf.eventsList:
                for events_list in self.eventsLists:

                    for event in events_list:
                        if self.clause.checkClause(stock, event) and len(events_list) == num:
                            events_list.append(stock)
                            # flag = True
                            break
            num += 1

        self.eventsLists = filter(lambda eventsList: len(eventsList) == (num + 1), self.eventsLists)

    def printNode(self):
        self.clause.printClause()
        print("\nLeaves:")
        for leaf in self.leavesList:
            print(leaf.name)
        # print(self.leavesList)
        # if self.eventsLists is not None:
        for eventList in self.eventsLists:
            print(eventList)

    def checkTimeWindow(self, ptype, time_window,eventsNames):
        tmpList = [tupple for tupple in self.eventsLists if self.checkTime(tupple,time_window,ptype,eventsNames)]
        self.eventsLists = tmpList
        
    
    def checkTime(self, tupple, time_window,ptype,eventsNames):
        if ptype == PTYPE.AND:
            max_t = max(event.timestamp for event in tupple)
            min_t = min(event.timestamp for event in tupple)
            return (max_t - min_t <= time_window)
        elif ptype == PTYPE.SEQ:
            sortedTupple = sorted(tupple, key=lambda x: x.timestamp)
            max_t = max(event.timestamp for event in sortedTupple)
            min_t = min(event.timestamp for event in sortedTupple)
            if (max_t - min_t > time_window):
                return False
            for idx in range(len(sortedTupple)):
                if(sortedTupple[idx].ticker != eventsNames[idx]):
                    return False
            return True        


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