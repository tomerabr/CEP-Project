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
        
    def solveWhenOnlyLeaves(self, ptype, time_window,eventsNames):
        setsList = []
        for literal in self.clause.clause:
            litSet = set()
            names = literal.eventsAppearInLiteral()
            for leaf1 in self.leavesList:
                if leaf1.name in names:
                    if len(names) == 1 or isinstance(names[1],float): #a<const or a<a
                        for event in leaf1.eventsList:
                            if (literal.isUnary() and literal.checkLiteral(event)) or literal.checkLiteral(event,event):
                                all_in = []
                                a = [event.ticker]
                                for other_leaf in self.leavesList:
                                    if other_leaf.name in a:
                                        continue
                                    else:
                                        a.append(other_leaf.name)
                                        if len(a) == 2:
                                            for ev in other_leaf.eventsList:
                                                all_in.append([event,ev])
                                        else:
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
                                if len(a) == 1:
                                    all_in = [[event]]
                                for array in all_in:
                                    litSet.add(frozenset(array))
                    else:
                        for leaf2 in self.leavesList:
                            if leaf2.name != leaf1.name and leaf2.name in names:
                                for event1 in leaf1.eventsList:
                                    for event2 in leaf2.eventsList:
                                        if literal.checkLiteral(event1,event2) or literal.checkLiteral(event2,event1):
                                            all_in = []
                                            a = [event1.ticker,event2.ticker]
                                            for other_leaf in self.leavesList:
                                                if other_leaf.name in a:
                                                    continue
                                                else:
                                                    a.append(other_leaf.name)
                                                    if len(a) == 3:
                                                        for ev in other_leaf.eventsList:
                                                            all_in.append([event1,event2,ev])
                                                    else:
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
                                            if len(a) == 2:
                                                all_in = [[event1,event2]]
                                            for array in all_in:
                                                litSet.add(frozenset(array))
            setsList.append(litSet)
        
        #now each literal has his set
        self.eventsLists = set.union(*setsList)
        #check time window
        self.checkTimeWindow(ptype, time_window, eventsNames)

        if self.parent is not None:
            self.parent.solveInnerNode(ptype, time_window, eventsNames)

    def solveInnerNode(self, ptype, time_window,eventsNames):
        setsList = []
        for literal in self.clause.clause:
            litSet = set()
            names = literal.eventsAppearInLiteral()
            for tupple in self.leftInnerNode.eventsLists:
                for event1 in tupple:
                    if event1.ticker in names:
                        if (literal.isUnary() and literal.checkLiteral(event1)) or literal.checkLiteral(event1,event1):
                            all_in = []
                            nofrozen = [a for a in tupple]###################tuple with no frozenset
                            first = True
                            for leaf in self.leavesList:
                                if first:
                                    for ev in leaf.eventsList:
                                        c = copy.copy(nofrozen)
                                        all_in.append(c.append(ev))
                                    first = False
                                else:
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
                            if len(all_in) == 0: #no other leaves
                                all_in.append(nofrozen)
                            for arr in all_in:
                                litSet.add(frozenset(arr))
                            break
                        else:
                            dont = False
                            for event2 in tupple:
                                if self.indexInTuple(tupple,event2) <= self.indexInTuple(tupple,event1):
                                    continue
                                if event2.ticker in names:
                                    if literal.checkLiteral(event1,event2) or literal.checkLiteral(event2,event1):
                                        all_in = []
                                        nofrozen = [a for a in tupple]###################tuple with no frozenset
                                        first = True
                                        for leaf in self.leavesList:
                                            if first:
                                                for ev in leaf.eventsList:
                                                    c = copy.copy(nofrozen)
                                                    d = c.append(ev)
                                                    all_in.append(d)
                                                first = False
                                            else:
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
                                        if len(all_in) == 0: #no other leaves
                                            all_in.append(nofrozen)
                                        for arr in all_in:
                                            litSet.add(frozenset(arr))
                                            dont = True
                                        break
                            if not dont:
                                for leaf in self.leavesList:
                                    if leaf.name in names:
                                        for event2 in leaf.eventsList:
                                            if literal.checkLiteral(event1,event2) or literal.checkLiteral(event2,event1):
                                                nofrozen = [a for a in tupple]###################tuple with no frozenset
                                                nofrozen.append(event2)
                                                all_in = []
                                                first = True
                                                for other_leaf in self.leavesList:
                                                    if other_leaf.name != leaf.name:
                                                        if first:
                                                            for ev in other_leaf.eventsList:
                                                                c = copy.copy(nofrozen)
                                                                all_in.append(c.append(ev))
                                                            first = True
                                                        else:
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
                                                if len(all_in) == 0:
                                                    all_in.append(nofrozen)
                                                for arr in all_in:
                                                    litSet.add(frozenset(arr))
            for leaf1 in self.leavesList:
                if leaf1.name in names:
                    if len(names) == 1 or isinstance(names[1],float): #a<const or a<a
                        for event in leaf1.eventsList:
                            if (literal.isUnary() and literal.checkLiteral(event)) or literal.checkLiteral(event,event):
                                all_in = []
                                a = [event.ticker]
                                for tupple in self.leftInnerNode.eventsLists:
                                    nofrozen = [a for a in tupple]
                                    nofrozen.append(event)
                                    all_in.append(nofrozen)
                                for other_leaf in self.leavesList:
                                    if other_leaf.name in a:
                                        continue
                                    else:
                                        a.append(other_leaf.name)
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
                                for array in all_in:
                                    litSet.add(frozenset(array))
                    else:
                        for leaf2 in self.leavesList:
                            if leaf2.name != leaf1.name and leaf2.name in names:
                                for event1 in leaf1.eventsList:
                                    for event2 in leaf2.eventsList:
                                        if literal.checkLiteral(event1,event2) or literal.checkLiteral(event2,event1):
                                            all_in = []
                                            a = [event1.ticker,event2.ticker]
                                            for tupple in self.leftInnerNode.eventsLists:
                                                nofrozen = [a for a in tupple]
                                                nofrozen.append(event1)
                                                nofrozen.append(event2)
                                                all_in.append(nofrozen)
                                            for other_leaf in self.leavesList:
                                                if other_leaf.name in a:
                                                    continue
                                                else:
                                                    a.append(other_leaf.name)
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
                                            for array in all_in:
                                                litSet.add(frozenset(array))
                                                
        setsList.append(litSet)
        
        #now each literal has his set
        self.eventsLists = set.union(*setsList)
        #check time window
        self.checkTimeWindow(ptype, time_window, eventsNames)

        if self.parent is not None:
            self.parent.solveInnerNode(ptype, time_window, eventsNames)                                                             
                                                        
    def indexInTuple(self,setList, data2):
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
            if(self.parent == None):
                for idx in range(len(sortedTupple)):
                    if(sortedTupple[idx].ticker != eventsNames[idx]):
                        return False
            else:
                for i in range(len(sortedTupple)):
                    for j in range(i+1,len(sortedTupple)):
                        if(eventsNames.index(sortedTupple[i].ticker) > eventsNames.index(sortedTupple[j].ticker)):
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