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

    def do_all_in(self, litSet, names, names_in_tupple, event1, event2=None): #checked
        all_in = []
        self.forOtherLeaves(all_in, names_in_tupple, len(names) + 1, event1, event2)
        if len(names_in_tupple) == len(names):
            if event2 is None:
                all_in = [[event1]]
            else:
                all_in = [[event1, event2]]
        for array in all_in:
            litSet.add(frozenset(array))

    def solveFirstNode(self, ptype, time_window, eventsNames): #checked
        setsList = []
        for literal in self.clause.clause:
            litSet = set()
            names = literal.eventsAppearInLiteral() #[x for x in a if isinstance(x, int)]
#            for leaf1 in self.leavesList:
#                if leaf1.name in names:
            for leaf1 in [leaf for leaf in self.leavesList if leaf.name in names]:
                if len(names) == 1: # a<const or a<a
                    for event in leaf1.eventsList:
                        if (literal.isUnary() and literal.checkLiteral(event)) or literal.checkLiteral(event,event):
                            self.do_all_in(litSet,names [event.ticker], event)
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
#                                if self.indexInTuple(tupple, event2) <= self.indexInTuple(tupple, event1):
#                                    continue
                                if self.indexInTuple(tupple, event2) > self.indexInTuple(tupple, event1) and event2.ticker in names:
                                    if literal.checkLiteral(event1, event2) or literal.checkLiteral(event2, event1):
                                        self.innerNodeOnlyTupple(litSet, tupple)
                                        check_leaves = False
                                        break
#                            if not check_leaves:
#                                break
#                            else:
                            if check_leaves:
                                for leaf in self.leavesList:
                                    if leaf.name in names:
                                        for event2 in leaf.eventsList:
                                            if literal.checkLiteral(event1, event2) or literal.checkLiteral(event2, event1):
                                                self.innerNodeBoth(litSet, tupple, event2, leaf.name)

            for leaf1 in self.leavesList:
                if leaf1.name in names:
 #                   if len(names) == 1 or isinstance(names[1], float):  # a<const or a<a
                    if len(names) == 1:  # a<const or a<a
                        for event in leaf1.eventsList:
                            if (literal.isUnary() and literal.checkLiteral(event)) or literal.checkLiteral(event, event):
#                                names_in_tupple = [event.ticker]
                                self.innerNodeOnlyLeaves(litSet, [event.ticker], event1)
                    else:
                        for leaf2 in self.leavesList:
                            if leaf2.name != leaf1.name and leaf2.name in names:
                                for event1 in leaf1.eventsList:
                                    for event2 in leaf2.eventsList:
                                        if literal.checkLiteral(event1, event2) or literal.checkLiteral(event2, event1):
#                                            names_in_tupple = [event1.ticker, event2.ticker]
                                            self.innerNodeOnlyLeaves(litSet, [event1.ticker, event2.ticker], event1, event2)

            setsList.append(litSet)

        # now each literal has his set
        self.eventsLists = set.union(*setsList)
        # check time window
        self.checkTimeWindow(ptype, time_window, eventsNames)

        if self.parent is not None:
            self.parent.solveInnerNode(ptype, time_window, eventsNames)

    def innerNodeBoth(self,litSet,tupple,event2,name): #ok
        nofrozen = [a for a in tupple]
        nofrozen.append(event2)
        all_in = []
        first = True
        for other_leaf in self.leavesList:
            if other_leaf.name != name:
                if first:
                    for ev in other_leaf.eventsList:
                        c = copy.copy(nofrozen)
                        all_in.append(c.append(ev))
                    first = True
                else:
                    self.appendOtherLeaf(all_in,other_leaf)
        if len(all_in) == 0:
            all_in.append(nofrozen)
        for arr in all_in:
            litSet.add(frozenset(arr))

    def innerNodeOnlyLeaves(self,litSet,names_in_tupple, event1,event2=None): #ok
        all_in = []
        for tupple in self.leftInnerNode.eventsLists:
            nofrozen = [a for a in tupple]
            nofrozen.append(event1)
            if event2 is not None:
                nofrozen.append(event2)
            all_in.append(nofrozen)
        for other_leaf in filter(lambda leaf: leaf.name not in names_in_tupple, self.leavesList):
#            if other_leaf.name in names_in_tupple:
#                continue
#            else:
             self.appendOtherLeaf(all_in,other_leaf,names_in_tupple)
        for array in all_in:
            litSet.add(frozenset(array))

    def innerNodeOnlyTupple(self, litSet, tupple): #ok
        all_in = []
        nofrozen = [a for a in tupple]
        first = True
        for leaf in self.leavesList:
            if first:
                for ev in leaf.eventsList:
                    c = copy.copy(nofrozen)
                    all_in.append(c.append(ev))
                first = False
            else:
                self.appendOtherLeaf(all_in,leaf)
        if len(all_in) == 0: #no other leaves
            all_in.append(nofrozen)
        for arr in all_in:
            litSet.add(frozenset(arr))

    def forOtherLeaves(self,all_in, names_in_tupple, len_when_first, event1, event2=None): #checked
        for other_leaf in filter(lambda leaf: leaf.name not in names_in_tupple, self.leavesList):
#            if other_leaf.name in names_in_tupple:
#                continue
#            else:
            names_in_tupple.append(other_leaf.name)
            if len(names_in_tupple) == len_when_first:
                for ev in other_leaf.eventsList:
                    if event2 is not None:
                        all_in.append([event1,event2,ev])
                    else:
                        all_in.append([event1,ev])
            else:
                self.appendOtherLeaf(all_in,other_leaf)

    def appendOtherLeaf(self,all_in,other_leaf,names_in_tupple=None): #ok
        if names_in_tupple is not None:
            names_in_tupple.append(other_leaf.name)
        size = len(all_in)
        count = 0
        for tupple in all_in:
            if(count == size):
                break
            for ev in other_leaf.eventsList:
                c = copy.copy(tupple)
                c.append(ev)
                all_in.append(c)
            all_in.pop(0)
            count += 1                                       
                                                        
    def indexInTuple(self,setList, data2): #ok
        i=-1
        for data in setList:
            i=i+1
            if data==data2:
                return i
        return -1 

    def printNode(self):
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
            
            tmp = []
            for name in eventsNames:
                for event in tupple:
                    if event.ticker == name:
                        tmp.append(event)
            for i in range(len(tmp)-1):
                if tmp[i].timestamp > tmp[i+1].timestamp:
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