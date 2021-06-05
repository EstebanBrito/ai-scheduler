import requests

def req_data():
    data = {}
    data['professors'] = req_prof()
    data['courses'] = req_courses()
    data['groups'] = req_groups()
    return data

def req_prof():
    req = requests.get('https://digital-window-dev.herokuapp.com/api/v1/schedule/professors/?format=json')
    return req.json()['results']

def req_courses():
    req = requests.get('https://digital-window-dev.herokuapp.com/api/v1/schedule/courses/?format=json')
    return req.json()['results']

def req_groups():
    req = requests.get('https://digital-window-dev.herokuapp.com/api/v1/schedule/groups/?format=json')
    return req.json()['results']
