# DATA STRUCTURES

from data import courses, professors, groups

# FUNCTIONS

def isChangePermitted():
    pass
    # check min hours have been scheduled ()
    # check max number of changes is not reached (only two are permitted)


def getNextAvailableTime(group, day, hour):
    pass
    # If two hours remaining, 
    # 


def generateGroupOptions(group, day, hour):
    pass
    # For every unassigned group session:
        # Check professor is avaliable at that time [Professor]
        # AND
        # Check <asignatura> has not been scheduled that day [GroupSchedule]
            # Generate heuristic metrics
            # Add to options
    # Sort options
    # Return options


def getNextGroup():
    pass
    # For each group, compare most far behind:
        # If group.solved==True:
            # If curr_day > day:
                # If curr_hour > hour: we got new most far behind
            # Else, fuck off
        # Else continue
    # They can return null if no group is avaliable (all groups were solved)


def mark(group, day, hour, session):
    pass
    # In groups, find group
    # In group's schedule, find day
    # In day, schedule session with no of hour = session.length
    # Find professor and mark those hours as occupied
    # If no sessions remain, make group.solved = True

def unmark(groups, day, hour, session):
    pass
    # In groups, find group
    # In group's schedule, find day
    # In day, remove session entry
    # Find professor and mark those hours as free

def schedule_session(group, day, hour):
    '''Tries recursively to schedule a session. Return True if a solutions has been found.
    Return False to trigger backtracking'''

    options = generateGroupOptions(group, day, hour)
    # Change hours if sessions are not avaliable at that time
    while len(options)==0:
        if isChangePermitted(group):
            day, hour = getNextAvailableTime(group, day, hour)
            options = generateGroupOptions(group, day, hour)
        else: return False
    # Try to generate a solution by scheduling any of the sessions
    for session in options:
        mark(group, day, hour, session)
        next_group, next_day, next_hour = getNextGroup()
        if group==None: return True
        if schedule_session(next_group, next_day, next_hour): return True
        unmark(group, day, hour, session)
    return False
            
# No options cuz only one hour rem, Deal with it
# What when daily hours have been completed?
