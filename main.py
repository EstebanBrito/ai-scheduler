from generation import generate_ds
from backtracking import schedule_session
from utils import see_ds_status
from data_requests import req_data

def solve(data):
    professors, courses, groups, config = generate_ds(data)
    see_ds_status(professors, courses, groups, config)

if __name__ == '__main__':
    data = req_data()
    solve(data)