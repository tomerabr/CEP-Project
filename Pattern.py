from enum import Enum

#The pattern that the tree is based on.
#Contains the type, names of events, condtions and time windows.
class Pattern:
    def __init__(self, ptype, events, cond, time_window):
        self.ptype = ptype  # type_enum
        self.events = events  # list of events, each is object(/name?)
        self.cond = cond  # object
        self.time_window = time_window  # corresponding to time in python (msec, sec etc...)


class PTYPE(Enum):
    SEQ = 0
    AND = 1
    # continue
