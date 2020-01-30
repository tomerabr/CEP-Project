from enum import Enum

#The pattern that the tree is based on.
#Contains the type, names of events, conditions and time window.
class Pattern:
    def __init__(self, ptype, events, cond, time_window):
        self.ptype = ptype  # the pattern type. Enum of type PTYPE.
        self.events = events  # list of events names that would be pat of the pattern
        self.cond = cond  # list of clauses, that all of them assemble the condtion for the tree
        self.time_window = time_window  # the max time between the first event and the last event.


class PTYPE(Enum):
    SEQ = 0
    AND = 1
    # continue
