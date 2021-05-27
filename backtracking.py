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


def gen_heuristic(professors, groups, professor, group, day, hour):
    prof_top_hour = professors[professor]['workhours'][day][1]
    group_top_hour = group[group]['hour_range'][day][1]
    # Calc. time between current hour and early top hour
    metric = group_top_hour-hour if group_top_hour < prof_top_hour else prof_top_hour-hour
    return metric

def is_professor_avaliable(professors, professor, day, hour, length):
    hours = gen_array_from_range(hour, hour+length)
    for hour in hours:
        if not hour in professors[professor]['av_workhours'][day]:
            return False
    return True

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
        metric = gen_heuristic(professors, groups, professor, group, day, hour)
        options.add({'session': sess_name, 'metrics': metric})
    # Sort options
    return options


def gen_hour_of_week(day, hour):
    return (day-1)*24 + hour

def get_next_group(groups):
    '''Given a collections of groups, find the most delayed
    which still has session to schedule. Returns that group's
    name and the day and hour its next session should be scheduled'''
    next_group = None
    next_group_day = 8
    next_group_hour = 0
    next_group_hour_of_week = gen_hour_of_week(8, 0)
    # For each group...
    for group_name, group in groups.items():
        if group['solved']: continue # Ignore solved groups
        # Calc time and compare with current most delayed group
        day, hour = group['current_time']['day'], group['current_time']['hour']
        hour_of_week = gen_hour_of_week(day, hour)
        if hour_of_week < next_group_hour_of_week:
            next_group = group_name
            next_group_day = day
            next_group_hour = hour
            next_group_hour_of_week = hour_of_week
    return next_group, next_group_day, next_group_hour


def has_group_remaining_sessions(groups, group):
    return len(groups[group]['sessions'])>0

def mark_group_as_solved(groups, group):
    groups[group]['solved'] = True

def mark_group_as_unsolved(groups, group):
    groups[group]['solved'] = False

def mark(groups, group, day, hour, session):
    length = groups[group]['sessions'][session]['length']
    hours = gen_array_from_range(hour, hour+length)
    # Schedule session
    groups[group]['schedule'][day][session] = hours
    groups[group]['sessions'][session]['scheduled'] = True
    # Change group's current time TODO
    groups[group]['current_hour'] = [day, hour+length]
    # Verify if groups scheduling is complete
    if not has_group_remaining_sessions(groups, group): mark_group_as_solved(groups, group)

def unmark(groups, group, day, hour, session):
    # Delete session scheduled
    del groups[group]['schedule'][day][session]
    groups[group]['sessions'][session]['scheduled'] = False
    # Change the group's current time TODO
    groups[group]['current_hour'] = [day, hour]
    # Scheduling for the group is not complete
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
    for opt in options:
        session = opt.session
        mark(group, day, hour, session)
        next_group, next_day, next_hour = get_next_group()
        if group==None: return True # All groups have been schedules
        if schedule_session(next_group, next_day, next_hour): return True # Try scheduling next group
        unmark(group, day, hour, session)
    return False
            
# No options cuz only one hour rem, Deal with it
# What when daily hours have been completed?
