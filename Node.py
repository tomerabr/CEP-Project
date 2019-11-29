from Condition import Clause
from Pattern import Pattern


class Node:
    def __init__(self, clause, pattern):

        self.eventsLists = []
        self.clause = clause
        self.leftInnerNode = null
        self.leavesList = []

    # def checkClause(self, stock1, stock2):
    #  if self.clause.checkClause(stock1, stock2):

    def checkNoLeaves(self):
        for events in self.leftInnerNode.eventsLists:
            flag = False

            for first in events:
                for second in events:
                    if self.clause.checkClasuse(first, sceon
                    flag = True
                    break
                if flag == true
                    break

            self.eventsLists.append(events)
            flag = false

    def addLeaf(self, leaf):
        self.leavesList.append(leaf)

    def addLeftInnerNode(self, node):
        self.leftInnerNode = node


# each leaf will contain list of specific event
# each leaf will be connected to only one inner node
class Leaf:
    def __init__(self, name):
        self.eventList = []
        self.name = name
        self.parent = null

    def addStockToLeaf(self, stock):
        self.eventList.add(stock)

    def addParent(self, node):
        self.node = node