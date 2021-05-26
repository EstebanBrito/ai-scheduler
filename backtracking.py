# DATA STRUCTURES

from data import courses, professors, groups
from utils import gen_array_from_range

# FUNCTIONS

def is_change_permitted():
    pass
    # check min hours have been scheduled ()
    # check max number of changes is not reached (only two are permitted)


def get_next_available_time(group, day, hour):
    pass
    # If two hours remaining, 
    # 


def generate_heuristic():
    pass

def is_professor_avaliable(professors, professor, day, hour, hours):
    pass

def get_course_professor(courses, course, group):
    return courses[course]['professors'][group]

def is_course_session_scheduled(groups, group, day, course):
    for sess_name, sess in groups[group]['schedule'][day].items():
        scheduled_course = groups[group]['sessions'][sess_name]['course']
        if course == scheduled_course: return True
    return False

def generate_group_options(groups, group, day, hour):
    options = []
    # For every unassigned group session:
    for sess_name, sess in groups[group]['sessions'].items():
        if sess['scheduled']: continue
        # Check <asignatura> has not been scheduled that day [GroupSchedule]
        course = sess['course']
        if is_course_session_scheduled(groups, group, day, course): continue
        # Check professor is avaliable at that time [Professor]
        professor = get_course_professor(courses, course, group)
        session_length = sess['length']
        if not is_professor_avaliable(professors, professor, day, hour, session_length): continue
        # Generate heuristic metrics
        metric = generate_heuristic()
        options.add({'session': sess_name, 'metrics': metric})
    # Sort options
    return options


def get_next_group(groups):
    pass
    # For each group, compare most far behind:
        # If group.solved==True:
            # If curr_day > day:
                # If curr_hour > hour: we got new most far behind
            # Else, fuck off
        # Else continue
    # They can return null if no group is avaliable (all groups were solved)

def has_group_remaining_sessions(groups, group):
    return len(groups[group]['sessions'])>0

def mark_group_as_solved(groups, group):
    groups[group]['solved'] = True

def mark_group_as_unsolved(groups, group):
    groups[group]['solved'] = False

def mark(groups, group, day, hour, session):
    length = groups[group]['sessions'][session]['length']
    hours = gen_array_from_range(hour, hour+length)
    groups[group]['schedule'][day][session] = hours
    groups[group]['sessions'][session]['scheduled'] = True
    if not has_group_remaining_sessions(groups, group): mark_group_as_solved(groups, group)

def unmark(groups, group, day, hour, session):
    del groups[group]['schedule'][day][session]
    groups[group]['sessions'][session]['scheduled'] = False
    mark_group_as_unsolved(groups, group)

def schedule_session(group, day, hour):
    '''Tries recursively to schedule a session. Return True if a solution has been found.
    Return False to trigger backtracking'''

    options = generate_group_options(group, day, hour)
    # Change hours if sessions are not avaliable at that time
    while len(options)==0:
        if is_change_permitted(group):
            day, hour = get_next_available_time(group, day, hour)
            options = generate_group_options(group, day, hour)
        else: return False
    # Try to generate a solution by scheduling any of the sessions
    for session in options:
        mark(group, day, hour, session)
        next_group, next_day, next_hour = get_next_group()
        if group==None: return True # All groups have been schedules
        if schedule_session(next_group, next_day, next_hour): return True # Try scheduling next group
        unmark(group, day, hour, session)
    return False
            
# No options cuz only one hour rem, Deal with it
# What when daily hours have been completed?
