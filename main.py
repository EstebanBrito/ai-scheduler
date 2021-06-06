from generation import generate_ds
from backtracking import solve
from utils import see_ds_status
from data_requests import req_data

def gen_schedule(data):
    # Preprocess the data
    professors, courses, groups, config = generate_ds(data)
    see_ds_status(professors, courses, groups, config)
    # Initialize the closure function
    schedule_session = solve(professors, courses, groups, config)
    # Try to solve and return answer
    # solution = schedule_session(0, 0, groups[0]['hour_range'][0])
    # if solution: return format_solution(groups)
    # else: return None

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