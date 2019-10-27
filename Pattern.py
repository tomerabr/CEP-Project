from enum import Enum


class Pattern:
    def __init__(self, ptype, events, cond, time_window):
        self.ptype = ptype  # type_enum
        self.events = events  # list of events, each is object(/name?)
        self.cond = cond  # list of functions
        self.time_window = time_window  # corresponding to time in python (msec, sec etc...)


class PTYPE(Enum):
    SEQ = 0
    AND = 1
    # continue
