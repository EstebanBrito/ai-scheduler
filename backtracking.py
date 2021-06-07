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

# General auxiliary functions

def get_professor_idx(professors, professor_id):
    '''Given his/her id, return index of professor within professors data structure'''
    for curr_idx, curr_prof in enumerate(professors):
        if curr_prof['id'] == professor_id: return curr_idx
    return None

def get_course_idx(courses, course_id):
    '''Given its id, return index of course within courses data structure'''
    for curr_idx, curr_course in enumerate(courses):
        if curr_course['id'] == course_id: return curr_idx
    return None

def get_group_idx(groups, group_id):
    '''Given its id, return index of group within groups data structure'''
    for curr_idx, curr_group in enumerate(groups):
        if curr_group['id'] == group_id: return curr_idx
    return None

def get_session_idx(groups, group_idx, session_id):
    '''Given its id, return index of session within group's sessions data structure'''
    for curr_idx, curr_sess in enumerate(groups[group_idx]['sessions']):
        if curr_sess['id'] == session_id: return curr_idx
    return None

def get_session_course(groups, group_idx, session_idx):
    '''Return session's course id, given group index and session index'''
    return groups[group_idx]['sessions'][session_idx]['course']

# get_next_avaliable_time() auxiliary functions

def calc_rem_min_daily_class_hours(groups, group_idx, day):
    '''Calc. rem. hours of class neede for that group that day'''
    min_hrs = groups[group_idx]['min_daily_class_hours'][day]
    class_hrs = groups[group_idx]['class_hours'][day]
    return min_hrs - class_hrs if min_hrs > class_hrs else 0

def calc_idle_hours(groups, group_idx, day, hour):
    '''Calc. idle hours in that group's schedule in the specified day'''
    idle_hours = 0
    prev_end_hour = None
    # Calc. idle hours already in schedule
    for curr_sess in groups[group_idx]['schedule'][day]:
        if prev_end_hour: idle_hours += curr_sess['hour_range'][0] - prev_end_hour
        prev_end_hour = curr_sess['hour_range'][1]
    # Calc idle hours that are created if a new session is scheduled at specified hour
    if prev_end_hour: idle_hours += hour - prev_end_hour
    return idle_hours

def get_next_available_time(config, groups, group_idx, day, hour):
    '''Get next time avaliable for a group to schedule a session, given that
    this group was trying to schedule a session at he specified day and hour'''
    # Calc. rem. hrs. of class for this group if we skip one hour
    top_hour = groups[group_idx]['hour_range'][day][1]
    rem_hours = top_hour - (hour + 1)
    # If rem. hrs are enough to schedule the min. hrs. of class needed that day for that group...
    if rem_hours < calc_rem_min_daily_class_hours(groups, group_idx, day): return None, None
    # ...and both rem. hrs. are enough to schedule a session (i.e. 2 hours)
    # and group's idle hours are acceptable (i.e. < max_daily_idle_hours)...
    idle_hours = calc_idle_hours(groups, group_idx, day)
    if rem_hours >= 2 and idle_hours <= config['max_daily_idle_hours']:
        # ...try to schedule session next hour
        return day, hour + 1
    # Else, if this day is not the last work day of the week (i.e. Friday)...
    elif day < FRIDAY: 
        # ...try to schedule session next day
        bottom_hour = groups[group_idx]['hour_range'][0]
        return day+1, bottom_hour
    # Otherwise, is impossible to move scheduling time. Backtracking is required.
    else:
        return None, None

# gen_group_options() auxiliary functions

def find_new_option_insert_index(options, metric):
    '''Given a new option, find where to insert it so options are in
    ASCENDING order according to their metrics'''
    # Case: no options exist yet
    if len(options) == 0: return 0
    # Case: new options belongs between existing options
    for curr_idx, curr_opt in enumerate(options):
        if metric < curr_opt['metric']:
            return curr_idx
    # Case: new options belong at the end of existing options
    return len(options)

def gen_heuristic(professors, groups, professor_idx, group_idx, day, hour):
    '''Calc. the time (in hours) a professor can impart classes to a group, 
    in a specific day and after the hour specified'''
    prof_top_hour = professors[professor_idx]['workhours'][day][1]
    group_top_hour = groups[group_idx]['hour_range'][1]
    # Calc. time between current hour and earlier (smaller) top hour
    earlier_top_hour = min([prof_top_hour, group_top_hour])
    metric = earlier_top_hour - hour
    return metric

def is_professor_avaliable(professors, professor_idx, day, hour, length):
    '''Returns if a professor is avalaible at that day and hour, and during that many time'''
    hours = gen_array_from_range(hour, hour+length)
    for hour in hours:
        if not hour in professors[professor_idx]['av_workhours'][day]: return False
    return True

def get_course_professor(courses, course_idx, group_id):
    '''Returns id of the professor teaching a course to a specific group'''
    # Find groups inside course's classrooms
    for curr_classroom in courses[course_idx]['classrooms']:
        if curr_classroom['group'] == group_id:
            # Return found professor
            return curr_classroom['professor']
        break
    return None # For consistency

def is_course_session_scheduled(groups, group_idx, day, course_id):
    '''Return whether a course session has been scheduled for a group in a specific day'''
    for sess in groups[group_idx]['schedule'][day]:
        if sess['course'] == course_id: return True
    return False

def generate_group_options(professors, courses, groups, group_idx, day, hour):
    '''Generates the sessions a group can take that day at that hour, taking in
    account that professors teaching those sessions are avaliable at that time
    and only one session of a course can be scheduled for a group that day'''
    options = []
    # For every unassigned group session:
    for curr_sess in groups[group_idx]['sessions']:
        if curr_sess['scheduled']: continue
        # Check if a session of that course has not been scheduled this day
        course_id = curr_sess['course']
        if is_course_session_scheduled(groups, group_idx, day, course_id): continue
        # Find professor of current course
        course_idx = get_course_idx(courses, course_id)
        group_id = groups[group_idx]['id']
        professor_id = get_course_professor(courses, course_idx, group_id)
        # Check if professor is avaliable
        professor_idx = get_professor_idx(professors, professor_id)
        session_length = curr_sess['length']
        if not is_professor_avaliable(professors, professor_idx, day, hour, session_length): continue
        # If all is OK, generate heuristic metric...
        metric = gen_heuristic(professors, groups, professor_idx, group_idx, day, hour)
        # ...and then insert new option so options are in ASCENDING order according to heuristic metric
        option_idx = find_new_option_insert_index(options, metric)
        options.insert(option_idx, {'session': curr_sess['id'], 'metric': metric})
    # Return options
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
        day, hour = group['current_time'][0], group['current_time'][1]
        hour_of_week = gen_hour_of_week(day, hour)
        if hour_of_week < next_group_hour_of_week:
            next_group = group_name
            next_group_day = day
            next_group_hour = hour
            next_group_hour_of_week = hour_of_week
    return next_group, next_group_day, next_group_hour

# mark() and unmark() auxiliary functions

def has_group_remaining_sessions(groups, group_idx):
    '''Return whether the group has scheduled all its class sessions or not'''
    for curr_sess in groups[group_idx]['sessions']:
        if curr_sess['scheduled']: return True
    return False

def remove_professor_available_hours(professors, professor_idx, day, hour, length):
    '''Remove hours from professor's avaliable time'''
    professor = professors[professor_idx]
    class_hours = range(hour, hour + length)
    for class_hour in class_hours:
        if class_hour in professor['av_workhours'][day]:
            professor['av_workhours'][day].remove(class_hour)

def restitute_professor_available_hours(professors, professor_idx, day, hour, length):
    '''Restitutes hours to professor's avaliable time'''
    professor = professors[professor_idx]
    # Find index where to restitute avaliable hours
    hour_idx = 0 # Default: at the beginning
    for curr_idx, curr_av_hour in enumerate(professor['av_workhours'][day]):
        if hour < curr_av_hour:
            hour_idx = curr_idx
            break
    # Restitute hours to the av. hours array (starting by the last hour)
    class_hours = range(hour, hour + length)
    for class_hour in class_hours[::-1]:
        if not class_hour in professor['av_workhours'][day]:
            professor['av_workhours'][day].insert(hour_idx, class_hour)

def recalc_min_daily_class_hours(groups, group_idx, day):
    '''Changes min. daily class hours required for that group in the rest of the week'''
    if day >= FRIDAY: return # No need to recalc. if today is the last day of the week (Friday)
    # Calc. worked hours (take req. hours if group have not met req. hours in a day)
    worked_hours_week = 0
    prev_days = range(0, day + 1)
    for curr_day in prev_days:
        worked_hours_day = groups[group_idx]['class_hours'][curr_day]
        req_hours_day = groups[group_idx]['min_daily_class_hours'][curr_day]
        worked_hours_week += max([worked_hours_day, req_hours_day])
    # Calc. req. daily class hours for the remaining days of the week
    rem_days = range(day+1, FRIDAY+1)
    no_rem_days = len(rem_days)
    no_rem_work_hours = groups[groups]['weekly_class_hours'] - worked_hours_week
    min_daily_hours = no_rem_work_hours // no_rem_days
    rem_min_daily_hours = no_rem_work_hours % no_rem_days
    # Set req. daily class hours for each remaining day of the week
    for curr_day in rem_days:
        groups[group_idx]['min_daily_class_hours'][curr_day] = min_daily_hours
    # Can't have point something hours, so add remainder to tomorrow
    groups[group_idx]['min_daily_class_hours'][day + 1] += rem_min_daily_hours

def remove_min_daily_class_hours(groups, group_idx, day):
    '''Removes required class hours for the remaining days of the week'''
    # Recalc. min. daily class hrs. for next days if today's min. daily class hrs. have been exceeded
    if groups[group_idx]['class_hours'][day] > groups[group_idx]['min_daily_class_hours'][day]:
        recalc_min_daily_class_hours(groups, group_idx, day)

def restitute_min_daily_class_hours(groups, group_idx, day, hour, length):
    '''Restitutes required class hours for the remaining days of the week'''
    # Recalc. min. daily class hrs. for next days if today's min. daily class hrs. were exceeded
    if groups[group_idx]['class_hours'][day] + length > groups[group_idx]['min_daily_class_hours'][day]:
        recalc_min_daily_class_hours(groups, group_idx, day)

def delete_scheduled_session(groups, group_idx, day, session_id):
    '''Deletes a session from group's schedule'''
    idx = None
    # Find session idx, then delete that element from scheduled sessions
    for curr_idx, curr_sess in enumerate(groups[group_idx]['schedule'][day]):
        if curr_sess['id'] == session_id: idx = curr_idx
    groups[group_idx]['schedule'][day].pop(idx)

def mark(professors, courses, groups, group_idx, day, hour, session_idx):
    '''Schedules a session for that groups  with those parameters, and changes 
    group's info so the algorithm can keep working'''
    # Get session info
    sess = groups[group_idx]['sessions'][session_idx]
    # Schedule session
    sess_id, sess_length, sess_course_id = sess['id'], sess['length'], sess['course']
    new_sess = {'session': sess_id, 'hour_range': [hour, hour + sess_length], 'course': sess_course_id}
    groups[group_idx]['schedule'][day].append(new_sess)
    groups[group_idx]['sessions'][session_idx]['scheduled'] = True
    # Change group's current time
    groups[group_idx]['current_time'] = [day, hour + sess_length]
    # Change group's class hours
    groups[group_idx]['class_hours'][day] += sess_length
    # Change group's min. daily class hours (IMPORTANT TO GO AFTER CHANGING GROUP'S CLASS HOURS)
    remove_min_daily_class_hours(groups, group_idx, day)
    # Change professor's avaliable hours
    course_idx = get_course_idx(courses, sess_course_id)
    group_id = groups[group_idx]['id']
    professor_id = get_course_professor(courses, course_idx, group_id)
    professor_idx = get_professor_idx(professors, professor_id)
    remove_professor_available_hours(professors, professor_idx, day, hour, sess_length)
    # Verify if group's scheduling is complete
    if not has_group_remaining_sessions(groups, group_idx): groups[group_idx]['solved'] = True

def unmark(professors, courses, groups, group_idx, day, hour, session_idx, last_day, last_hour):
    '''Unschedules a session (with the provided parameters) for that groups, and changes 
    group's info so the algorithm can keep working'''
    # Get session info
    sess = groups[group_idx]['sessions'][session_idx]
    # Delete session scheduled
    delete_scheduled_session(groups, group_idx, day, sess['id'])
    groups[group_idx]['sessions'][session_idx]['scheduled'] = False
    # Change the group's current time
    groups[group_idx]['current_time'] = [last_day, last_hour]
    # Change group's class hours
    groups[group_idx]['class_hours'][day] -= sess['length']
    # Change groups's min. daily class hours (IMPORTANT TO GO AFTER CHANGING GROUP'S CLASS HOURS)
    restitute_min_daily_class_hours(groups, group_idx, day, hour, sess['length'])
    # Change professor's avaliable hours
    course_idx = get_course_idx(courses, sess['id'])
    group_id = groups[group_idx]['id']
    professor_id = get_course_professor(courses, course_idx, group_id)
    professor_idx = get_professor_idx(professors, professor_id)
    restitute_professor_available_hours(professors, professor_idx, day, hour, sess['length'])
    # Scheduling for the group is not complete
    groups[group_idx]['solved'] = False

# Main functions

def solve(professors, courses, groups, config):
    def schedule_session(group_idx, day, hour):
        '''Tries recursively to schedule a session. Return True if a solution has been found.
        Return False to trigger backtracking'''
        options = generate_group_options(professors, courses, groups, group_idx, day, hour)
        # Change hours if sessions are not avaliable at that time
        while len(options)==0:
            day, hour = get_next_available_time(config, groups, group_idx, day, hour)
            # If next time available is None, you cannot change hours and got to trigger backtracking
            if day==None or hour==None: return False
            options = generate_group_options(professors, courses, groups, group_idx, day, hour)
        # Save prev. info
        last_day, last_hour = groups[group_idx]['current_time']
        # Try to generate a solution by scheduling any of the sessions
        for opt in options:
            session_id = opt['session']
            session_idx = get_session_idx(groups, group_idx, session_idx)
            mark(professors, courses, groups, group_idx, day, hour, session_idx)
            next_group_idx, next_day, next_hour = get_next_group(groups)
            if next_group_idx==None: return True # All groups have been scheduled, a solution has been found
            if schedule_session(next_group_idx, next_day, next_hour): return True # Try scheduling next group
            unmark(professors, courses, groups, group_idx, day, hour, session_idx, last_day, last_hour)
        # If options did not provide solution, trigger backtracking
        return False
    return schedule_session

