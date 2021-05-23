# DATA STRUCTURES

from data import courses, professors, groups
from utils import genArrayFromRange

# FUNCTIONS

def isChangePermitted():
    pass
    # check min hours have been scheduled ()
    # check max number of changes is not reached (only two are permitted)


def getNextAvailableTime(group, day, hour):
    pass
    # If two hours remaining, 
    # 


def generateHeuristic():
    pass

def isProfessorAvaliable(professors, professor, day, hour, hours):
    pass

def getCourseProfessor(courses, course, group):
    return courses[course]['professors'][group]

def isCourseSessionScheduled(groups, group, day, course):
    for sess_name, sess in groups[group]['schedule'][day].items():
        scheduled_course = groups[group]['sessions'][sess_name]['course']
        if course == scheduled_course: return True
    return False

def generateGroupOptions(groups, group, day, hour):
    options = []
    # For every unassigned group session:
    for sess_name, sess in groups[group]['sessions'].items():
        if sess['scheduled']: continue
        # Check <asignatura> has not been scheduled that day [GroupSchedule]
        course = sess['course']
        if isCourseSessionScheduled(groups, group, day, course): continue
        # Check professor is avaliable at that time [Professor]
        professor = getCourseProfessor(courses, course, group)
        session_length = sess['length']
        if not isProfessorAvaliable(professors, professor, day, hour, session_length): continue
        # Generate heuristic metrics
        metric = generateHeuristic()
        options.add({'session': sess_name, 'metrics': metric})
    # Sort options
    return options


def getNextGroup(groups):
    pass
    # For each group, compare most far behind:
        # If group.solved==True:
            # If curr_day > day:
                # If curr_hour > hour: we got new most far behind
            # Else, fuck off
        # Else continue
    # They can return null if no group is avaliable (all groups were solved)

def hasGroupRemainingSessions(groups, group):
    return len(groups[group]['sessions'])>0

def markGroupAsSolved(groups, group):
    groups[group]['solved'] = True

def markGroupAsUnsolved(groups, group):
    groups[group]['solved'] = False

def mark(groups, group, day, hour, session):
    length = groups[group]['sessions'][session]['length']
    hours = genArrayFromRange(hour, hour+length)
    groups[group]['schedule'][day][session] = hours
    groups[group]['sessions'][session]['scheduled'] = True
    if not hasGroupRemainingSessions(groups, group): markGroupAsSolved(groups, group)

def unmark(groups, group, day, hour, session):
    del groups[group]['schedule'][day][session]
    groups[group]['sessions'][session]['scheduled'] = False
    markGroupAsUnsolved(groups, group)

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
