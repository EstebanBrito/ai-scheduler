# DATA STRUCTURES

# from data import courses, professors, groups
from utils import gen_array_from_range

# Constants
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4

# FUNCTIONS

def calc_idle_hours(groups, group, day):
    idle_hours = 0
    prev_end_hour = None
    for session_name, session_hours in groups[group]['schedule'][day]:
        if (prev_end_hour):
            idle_hours += session_hours[0] - prev_end_hour
            prev_end_hour = session_hours[1]
    return idle_hours

def get_next_available_time(config, groups, group, day, hour):
    # Calc. remaining hours of class for this group if we skip one hour of class
    top_hour = groups[group]['hour_range'][day][1]
    rem_hours = top_hour - (hour + 1)
    # If rem. hours are enough to schedule a session (i.e 2 hours), try to skip one hour...
    if rem_hours >= 2:
        # ...unless you have already skipped many hours (> max_idle_hours)
        idle_hours = calc_idle_hours(groups, group, day)
        if idle_hours >= config['max_daily_idle_hours']: return None, None
        # If conditions are met, skip one hour today and return the next hour
        return day, hour + 1
    else:
        if day < 5: # If this day is not the last work day of the week (i.e. Friday), try to jump to next day...
            # ...unless you have not meet the required daily hours of class
            if groups[group]['class_hours'][day] < groups[group]['min_daily_class_hours']: return None, None
            # If conditions are met, return first avaliable hour of the next day
            bottom_hour = groups[group]['hour_range'][day+1][0]
            return day+1, bottom_hour
        else:
            return None, None


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
    for sess_name, sess_hours in groups[group]['schedule'][day]:
        scheduled_course = groups[group]['sessions'][sess_name]['course']
        if course == scheduled_course: return True
    return False

def get_session_course(groups, group, session):
    return groups[group]['sessions'][session]['course']

def generate_group_options(professors, courses, groups, group, day, hour):
    options = []
    # For every unassigned group session:
    for sess_name, sess in groups[group]['sessions'].items():
        if sess['scheduled']: continue
        # Check course session has not been scheduled that day
        course = sess['course']
        if is_course_session_scheduled(groups, group, day, course): continue
        # Check professor is avaliable to give a class
        professor = get_course_professor(courses, course, group)
        session_length = sess['length']
        if not is_professor_avaliable(professors, professor, day, hour, session_length): continue
        # If all is OK, generate heuristic metrics
        metric = gen_heuristic(professors, groups, professor, group, day, hour)
        options.add({'session': sess_name, 'metrics': metric})
    # Sort options
    return options


def gen_hour_of_week(day, hour):
    return day*24 + hour

def get_next_group(groups):
    '''Given a collection of groups, find the most delayed one
    which still has sessions to schedule. Returns that group's
    name and the day and hour its next session should be scheduled'''
    next_group = None
    next_group_day = 7
    next_group_hour = 0
    next_group_hour_of_week = gen_hour_of_week(7, 0)
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
    for sess_name, sess in groups[group]['sessions'].items():
        if sess['scheduled']: return True
    return False

def mark_group_as_solved(groups, group):
    groups[group]['solved'] = True

def mark_group_as_unsolved(groups, group):
    groups[group]['solved'] = False

def remove_professor_available_hours(professors, professor, day, hour, length):
    hours = gen_array_from_range(hour, hour+length)
    for hour in hours:
        if hour in professor[professor]['av_workhours'][day]:
            professor[professor]['av_workhours'][day].remove(hour)

def restitute_professor_available_hours(professors, professor, day, hour, length):
    hours = gen_array_from_range(hour, hour+length)
    # Find index where to restitute avaliable hours
    hour_idx = 0
    for av_hour, idx in enumerate(professor[professor]['av_workhours'][day]):
        if av_hour > hours[0]:
            hour_idx = idx
            break
    # Restitute hours to the av. hours array
    for hour in hours[::-1]:
        if not hour in professor[professor]['av_workhours'][day]:
            professor[professor]['av_workhours'][day].insert(hour_idx, hour)

def recalc_min_daily_class_hours(groups, group, day):
    if day >= FRIDAY: return # No need to recalc. if today is the last day of the week (Friday)
    # Calc. worked hours (take req. hours if group have not met req. hours in a day)
    hours = 0
    prev_days = range(0, day+1)
    for curr_day in prev_days:
        worked_hours = groups[group]['class_hours'][curr_day]
        req_hours = groups[group]['min_daily_class_hours'][curr_day]
        hours += max([worked_hours, req_hours])
    # Calc. req. daily class hours for the rest of the days of the week
    rem_days = range(day+1, FRIDAY+1)
    no_rem_days = len(rem_days)
    min_daily_hours = (groups[groups]['weekly_class_hours'] - worked_hours) // no_rem_days
    rem_min_daily_hours = (groups[groups]['weekly_class_hours'] - worked_hours) % no_rem_days
    for curr_day in rem_days:
        groups[group]['min_daily_class_hours'][day] = min_daily_hours
    # Addendum: Can't have point something hours, so add module to tomorrow
    groups[group]['min_daily_class_hours'][day+1] += rem_min_daily_hours

def remove_min_daily_class_hours(groups, group, day, length):
    # Substract session length from daily hours of class needed by that group that day
    if groups[group]['class_hours'][day] > groups[group]['min_daily_class_hours'][day]:
        recalc_min_daily_class_hours(groups, group, day)

def restitute_min_daily_class_hours(groups, group, day, hour, length):
    if groups[group]['class_hours'][day] + length > groups[group]['min_daily_class_hours'][day]:
        recalc_min_daily_class_hours(groups, group, day)

def mark(professors, courses, groups, group, day, hour, session):
    length = groups[group]['sessions'][session]['length']
    hours = gen_array_from_range(hour, hour+length)
    # Schedule session
    groups[group]['schedule'][day][session] = hours
    groups[group]['sessions'][session]['scheduled'] = True
    # Change group's current time
    groups[group]['current_hour'] = [day, hour+length]
    # Change group's class hours
    groups[group]['class_hours'][day] += length
    # Change group's min. daily class hours (IMPORTANT TO GO AFTER CHANGING GROUP'S CLASS HOURS)
    remove_min_daily_class_hours(groups, group, day, length)
    # Change professor's avaliable hours
    course = get_session_course(groups, group, session)
    professor = get_course_professor(courses, course, group)
    remove_professor_available_hours(professors, professor, day, hour, length)
    # Verify if group's scheduling is complete
    if not has_group_remaining_sessions(groups, group): mark_group_as_solved(groups, group)

def unmark(professors, courses, groups, group, day, hour, session):
    length = groups[group]['sessions'][session]['length']
    # Delete session scheduled
    del groups[group]['schedule'][day][session]
    groups[group]['sessions'][session]['scheduled'] = False
    # Change the group's current time
    groups[group]['current_hour'] = [day, hour]
    # Change group's class hours
    groups[group]['class_hours'][day] -= length
    # Change groups's min. daily class hours (IMPORTANT TO GO AFTER CHANGING GROUP'S CLASS HOURS)
    restitute_min_daily_class_hours(groups, group, day, hour, length)
    # Change professor's avaliable hours
    course = get_session_course(groups, group, session)
    professor = get_course_professor(courses, course, group)
    restitute_professor_available_hours(professors, professor, day, hour, length)
    # Scheduling for the group is not complete
    mark_group_as_unsolved(groups, group)

def solve(professors, courses, groups, config):
    def schedule_session(group, day, hour):
        '''Tries recursively to schedule a session. Return True if a solution has been found.
        Return False to trigger backtracking'''

        options = generate_group_options(group, day, hour)
        # Change hours if sessions are not avaliable at that time
        while len(options)==0:
            day, hour = get_next_available_time(group, day, hour)
            # If next time available is None, you cannot change hours and got to trigger backtracking
            if day==None or hour==None: return False
            options = generate_group_options(group, day, hour)
        # Try to generate a solution by scheduling any of the sessions
        for opt in options:
            session = opt.session
            mark(professors, courses, groups, group, day, hour, session)
            next_group, next_day, next_hour = get_next_group()
            if next_group==None: return True # All groups have been scheduled
            if schedule_session(next_group, next_day, next_hour): return True # Try scheduling next group
            unmark(professors, courses, groups, group, day, hour, session)
        return False
    return schedule_session

