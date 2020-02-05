from Condition import Clause
from Pattern import Pattern, PTYPE
import copy

'''
The node that the leftDeepTree is using.
each node represents a Clause in the CNF.

eventsLists - list of events which are suitable to the clause
clause - the clause which the node represents
leftInnerNode - the left node of the current node.
                each node has a left node (which may be empty).
parent - the parent of the current node.
        the current node is the leftInnerNode of the node which the parent field represents
leavesList - each node can have multiple leaves (and may have none).
            each leaf represent a new event type which didnt in the CNF yet(i.e up to this point in the tree).
'''
class Node:
    def __init__(self, clause):
        self.eventsLists = []
        self.clause = clause
        self.leftInnerNode = None
        self.leavesList = []
        self.parent = None

    def do_all_in(self, litSet, names, names_in_tupple, event1, event2=None):
        all_in = []
        self.forOtherLeaves(all_in, names_in_tupple, len(names) + 1, event1, event2)
        if len(names_in_tupple) == len(names):
            if event2 is None:
                all_in = [[event1]]
            else:
                all_in = [[event1, event2]]
        for array in all_in:
            litSet.add(frozenset(array))

    '''
    This function solves the first inner node in the tree(pre-ordered).
    this tree has at least 1 leaf(because there has to be at least one type in each clause, 
    and this node represents the first clause in the CNF, therefore each type in the clause will be
    represented as a leaf in the first node.
    solving the first node is basically filter all the combinations of the leafs according to the current clause.
    '''
    def solveFirstNode(self, ptype, time_window, eventsNames):
        setsList = []
        for literal in self.clause.clause:
            litSet = set()
            names = literal.eventsAppearInLiteral()  # [x for x in a if isinstance(x, int)]
            for leaf1 in [leaf for leaf in self.leavesList if leaf.name in names]:
                if len(names) == 1:  # a<const or a<a
                    for event in leaf1.eventsList:
                        if (literal.isUnary() and literal.checkLiteral(event)) or literal.checkLiteral(event, event):
                            self.do_all_in(litSet, names[event.ticker], event)
                else:
                    for leaf2 in self.leavesList:
                        if leaf2.name != leaf1.name and leaf2.name in names:
                            for event1 in leaf1.eventsList:
                                for event2 in leaf2.eventsList:
                                    if literal.checkLiteral(event1, event2) or literal.checkLiteral(event2, event1):
                                        self.do_all_in(litSet, names, [event1.ticker, event2.ticker], event1, event2)
            setsList.append(litSet)
        # now each literal has his set
        self.eventsLists = set.union(*setsList)
        # check time window
        self.checkTimeWindow(ptype, time_window, eventsNames)

        if self.parent is not None:
            self.parent.solveInnerNode(ptype, time_window, eventsNames)

    '''
    This function solves an inner node which is not the first node in the tree(pre-ordered).
    every node can have zero or more leaves.
    solving an innerNode is basically filter all the combinations of the events from the leaves with the events from
    the leftInnerNode, according to the current clause.
    '''
    def solveInnerNode(self, ptype, time_window, eventsNames):
        setsList = []
        for literal in self.clause.clause:
            litSet = set()
            names = literal.eventsAppearInLiteral()
            for tupple in self.leftInnerNode.eventsLists:
                for event1 in tupple:
                    if event1.ticker in names:
                        if (literal.isUnary() and literal.checkLiteral(event1)) or literal.checkLiteral(event1, event1):
                            self.innerNodeOnlyTupple(litSet, tupple)
                            break
                        else:
                            check_leaves = True
                            for event2 in tupple:
                                if self.indexInTuple(tupple, event2) > self.indexInTuple(tupple,
                                                                                         event1) and event2.ticker in names:
                                    if literal.checkLiteral(event1, event2) or literal.checkLiteral(event2, event1):
                                        self.innerNodeOnlyTupple(litSet, tupple)
                                        check_leaves = False
                                        break

                            if check_leaves:
                                for leaf in self.leavesList:
                                    if leaf.name in names:
                                        for event2 in leaf.eventsList:
                                            if literal.checkLiteral(event1, event2) or literal.checkLiteral(event2,
                                                                                                            event1):
                                                self.innerNodeBoth(litSet, tupple, event2, leaf.name)

            for leaf1 in self.leavesList:
                if leaf1.name in names:
                    if len(names) == 1:  # a<const or a<a
                        for event in leaf1.eventsList:
                            if (literal.isUnary() and literal.checkLiteral(event)) or literal.checkLiteral(event,
                                                                                                           event):
                                self.innerNodeOnlyLeaves(litSet, [event.ticker], event)
                    else:
                        for leaf2 in self.leavesList:
                            if leaf2.name != leaf1.name and leaf2.name in names:
                                for event1 in leaf1.eventsList:
                                    for event2 in leaf2.eventsList:
                                        if literal.checkLiteral(event1, event2) or literal.checkLiteral(event2, event1):
                                            self.innerNodeOnlyLeaves(litSet, [event1.ticker, event2.ticker], event1,
                                                                     event2)

            setsList.append(litSet)

        # now each literal has his set
        self.eventsLists = set.union(*setsList)
        # check time window
        self.checkTimeWindow(ptype, time_window, eventsNames)

        if self.parent is not None:
            self.parent.solveInnerNode(ptype, time_window, eventsNames)
    '''
    This function is used in the "solveInnerNode" function, when the inner node which we are trying to solve
    has both leaves and events from the left node.
    '''
    def innerNodeBoth(self, litSet, tupple, event2, name):
        nofrozen = [a for a in tupple]
        nofrozen.append(event2)
        all_in = []
        first = True
        for other_leaf in self.leavesList:
            if other_leaf.name != name:
                if first:
                    for ev in other_leaf.eventsList:
                        c = copy.copy(nofrozen)
                        c.append(ev)
                        all_in.append(c)
                    first = True
                else:
                    self.appendOtherLeaf(all_in, other_leaf)
        if len(all_in) == 0:
            all_in.append(nofrozen)
        for arr in all_in:
            litSet.add(frozenset(arr))

    '''
    This function is used in the "solveInnerNode" function, when the inner node which we are trying to solve
    has only leaves(i.e the first inner node in the tree).
    '''
    def innerNodeOnlyLeaves(self, litSet, names_in_tupple, event1, event2=None):
        all_in = []
        for tupple in self.leftInnerNode.eventsLists:
            nofrozen = [a for a in tupple]
            nofrozen.append(event1)
            if event2 is not None:
                nofrozen.append(event2)
            all_in.append(nofrozen)
        for other_leaf in filter(lambda leaf: leaf.name not in names_in_tupple, self.leavesList):
            self.appendOtherLeaf(all_in, other_leaf, names_in_tupple)
        for array in all_in:
            litSet.add(frozenset(array))
    '''
    This function is used in the "solveInnerNode" function, when the inner node which we are trying to solve
    has no leaves, and we will filter only the events from the left node.
    '''
    def innerNodeOnlyTupple(self, litSet, tupple):
        all_in = []
        nofrozen = [a for a in tupple]
        first = True
        for leaf in self.leavesList:
            if first:
                for ev in leaf.eventsList:
                    c = copy.copy(nofrozen)
                    c.append(ev)
                    all_in.append(c)
                first = False
            else:
                self.appendOtherLeaf(all_in, leaf)
        if len(all_in) == 0:  # no other leaves
            all_in.append(nofrozen)
        for arr in all_in:
            litSet.add(frozenset(arr))
    '''
    This function is used in order to iterate on all the leaves in node.
    '''
    def forOtherLeaves(self, all_in, names_in_tupple, len_when_first, event1, event2=None):
        for other_leaf in filter(lambda leaf: leaf.name not in names_in_tupple, self.leavesList):
            names_in_tupple.append(other_leaf.name)
            if len(names_in_tupple) == len_when_first:
                for ev in other_leaf.eventsList:
                    if event2 is not None:
                        all_in.append([event1, event2, ev])
                    else:
                        all_in.append([event1, ev])
            else:
                self.appendOtherLeaf(all_in, other_leaf)
    '''
    The field eventsList in the node contain list of list of events.
    This function is used in order to expand each list of events with all the events in a specific leaf,
    i.e append all the combinations each list with each events in the leaf. 
    '''
    def appendOtherLeaf(self, all_in, other_leaf, names_in_tupple=None):
        if names_in_tupple is not None:
            names_in_tupple.append(other_leaf.name)
        size = len(all_in)
        count = 0
        for tupple in all_in:
            if (count == size):
                break
            for ev in other_leaf.eventsList:
                c = copy.copy(tupple)
                c.append(ev)
                all_in.append(c)
            all_in.pop(0)
            count += 1
    '''
    This function return the index of the data in the list.
    '''
    def indexInTuple(self, setList, data2):  # ok
        i = -1
        for data in setList:
            i = i + 1
            if data == data2:
                return i
        return -1
    '''
    This function iterate over the eventsList of the node, and prints each list of events.
    '''
    def printNode(self):
        for eventList in self.eventsLists:
            print(eventList)
    '''
    This function gets a list of events and check whether the events are getting along with the time window.
    '''
    def checkTimeWindow(self, ptype, time_window, eventsNames):
        tmpList = [tupple for tupple in self.eventsLists if self.checkTime(tupple, time_window, ptype, eventsNames)]
        self.eventsLists = tmpList
    '''
    This function check the perfection of the time window by using the function checkTimeWindow for each list of events.
    '''
    def checkTime(self, tupple, time_window, ptype, eventsNames):
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

            tmp = []
            for name in eventsNames:
                for event in tupple:
                    if event.ticker == name:
                        tmp.append(event)
            for i in range(len(tmp) - 1):
                if tmp[i].timestamp > tmp[i + 1].timestamp:
                    return False
            return True

'''
each leaf will contain list of specific event(i.e events from the same type).
each leaf will be connected to only one inner node.
'''
class Leaf:
    def __init__(self, name):
        self.eventsList = []
        self.name = name

    def addEventsToLeaf(self, stocks):
        self.eventsList.extend(stocks)