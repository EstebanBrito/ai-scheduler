from utils import gen_array_from_range

def generate_ds(data):
    # Separate data
    professors = data['professors']
    courses = data['courses']
    groups = data['courses']
    config = data['config']
    # Generate aditional data
    config_professors(professors)
    config_groups(courses, groups)
    # Return
    return professors, courses, groups, config

def config_professors(professors):
    # For each professor...
    for professor in professors:
        professor['av_workhours'] = []
         # Configure avaliable workhours for every day worked
        for day in professor['workhours']:
            start_hour, end_hour = professor['workhours'][day]
            hours = gen_array_from_range(start_hour, end_hour)
            professors['av_workhours'][day].push(hours)

def find_group_courses(courses, group):
    group_courses = []
    for course in courses:
        if course['semester'] == group['semester']: group_courses.append(course)
    return group_courses

def gen_group_weekly_hours(group, group_courses):
    sum_hours = 0
    for course in group_courses: sum_hours += course['weekly_hours']
    group['weekly_class_hours'] = sum_hours

def gen_group_sessions(group, group_courses):
    group['sessions'] = []
    curr_session_id = 1
    for course in group_courses:
        # Hardcoded rules for no. of sessions and their length
        session_lengths = []
        if course['weekly_class_hours'] == 4: session_lengths = [2,2]
        elif course['weekly_class_hours'] == 5: session_lengths = [2,3]
        elif course['weekly_class_hours'] == 6: session_lengths = [2,2,2]
        for length in session_lengths:
            # TODO: test uuid generation
            session_info = {
                'id': curr_session_id,
                'course': course['id'],
                'length': course['length'],
                'scheduled': False
            }
            group['sessions'].append(session_info.copy())
            curr_session_id += 1

def gen_group_current_time(group):
    group['current_time'] = {
        'day': 0,
        'hour': group['hour_range'][0]
    }

def gen_group_min_daily_class_hours(group):
    min_daily_class_hours = group['weekly_class_hours'] // 5
    extra_min_daily_class_hours = group['weekly_class_hours'] % 5
    for hour in group['min_daily_class_hours']:
        hour = min_daily_class_hours
    group['min_daily_class_hours'][0] += extra_min_daily_class_hours

def config_groups(courses, groups):
    # For each group...
    for group in groups:
        # Find their courses...
        group_courses = find_group_courses(courses, groups, group)
        # generate their sessions and weekly hours...
        gen_group_weekly_hours(groups, group_courses)
        gen_group_sessions(group, group_courses)
        # their current time...
        gen_group_current_time(group)
        # their minimal no. of hours of class every day
        gen_group_min_daily_class_hours(group)
        # ...and other attributes
        group['schedule'] = [[], [], [], [], []]
        group['class_hours'] = [0, 0, 0, 0, 0]
        group['solved'] = False

