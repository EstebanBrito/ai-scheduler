# THIS IS A EXAMPLE OF WHAT NEEDS TO BE INCLUDED INSIDE THE REQUEST BODY
# Just replace the variables professors, etc with their contents
# (an array, an object, etc.) according to what the example shows

request = {
    'body': {
        'professors': professors,
        'courses': courses,
        'groups': groups,
        'config': config
    }
}

professors = [
    {
        'id': 'KARIME-UUID',
        'workhours': [
            (7,14),
            (7,14),
            (7,16),
            (7,17),
            (10,15)
        ]
    }
]

courses = [
    {
        'id': 'PROGRAMACION-UUID',
        'semester': 1,
        'weekly_hours': 5,
        'classrooms': [
            { 'group': 'GROUP-ID1', 'professor': 'PROF-ID1' },
            { 'group': 'GROUP-ID2', 'professor': 'PROF-ID1' },
            { 'group': 'GROUP-ID3', 'professor': 'PROF-ID2' },
        ]
    }
]

groups = [
    {
        'id': '1SA-UUID',
        'semester': 1,
        'hour_range': [7,15]
    }
]

config = {
    'school_workhours': [7,20],
    'max_daily_idle_hours': 2
}