from generation import generate_ds
from backtracking import solve
from utils import see_ds_status
from data_requests import req_data
import traceback

def gen_schedule(data):
    professors, courses, groups, config = None, None, None, None
    try:
        # Preprocess the data
        professors, courses, groups, config = generate_ds(data)
        # see_ds_status(professors, courses, groups, config)
        # Initialize the closure function
        schedule_session = solve(professors, courses, groups, config)
        # Try to solve and return answer
        solution = schedule_session(0, 0, groups[0]['hour_range'][0])
        if solution:
            see_ds_status(professors, courses, groups, config)
            return format_solution(groups)
        else: return None
    except Exception as err:
        print('Something has failed')
        print(err)
        traceback.print_exc()
        see_ds_status(professors, courses, groups, config)
        return None

def format_solution(groups):
    new_groups = []
    for group in groups:
        new_group = {
            'id': group['id'],
            'semester': group['semester'],
            'schedule': group['schedule']
        }
        new_groups.append(new_group)
    return new_groups

if __name__ == '__main__':
    data = req_data()
    res = gen_schedule(data)
    if res: print('Solved')
    else: print('Unsolved')