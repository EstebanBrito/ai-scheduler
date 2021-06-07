from generation import generate_ds
from backtracking import solve, get_course_idx, get_classroom_id
from utils import see_ds_status
from data_requests import req_data
import traceback

def gen_schedule(data):
    try:
        # Preprocess the data
        professors, courses, groups, config = generate_ds(data)
        # Initialize the closure function
        schedule_session = solve(professors, courses, groups, config)
        # Try to solve and return answer
        solution = schedule_session(0, 0, groups[0]['hour_range'][0])
    except Exception as err:
        print('Something has failed inside the scheduling algorithm')
        # print(err)
        # traceback.print_exc()
        return None
    try:
        if solution: return format_solution(courses, groups)
        else: return None
    except Exception as err:
        print('Solution found, but reformatting failed')
        return None
    
def format_solution(courses, groups):
    new_schedule = [[],[],[],[],[]]
    days = range(0, 5)
    for curr_day in days:
        for curr_group in groups:
            for curr_sess in curr_group['schedule'][curr_day]:
                # Find necessary info to find classroom
                group_id = curr_group['id']
                course_id = curr_sess['course']
                course_idx = get_course_idx(courses, course_id)
                # Find classroom for that combination of group and course
                clsrm_id = get_classroom_id(courses, course_idx, group_id)
                # Build new session format to send to client
                new_session = {
                    'classroom': clsrm_id,
                    'hour_range': curr_sess['hour_range']
                }
                new_schedule[curr_day].append(new_session.copy())
    return new_schedule

if __name__ == '__main__':
    # data is body of request, containing fields like professors, courses and groups
    data = req_data()
    # res should be attached to response body and sent to client
    res = gen_schedule(data)
    if res:
        print('Solved')
        print(res)
    else:
        print('Unsolved')
        print(res)
