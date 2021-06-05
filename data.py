professor_ds = {}

'''Should be like...
professors = [
    {
        'id': 'KARIME-UUID',
        'workhours': [
            (7,14),
            (7,14),
            (7,16),
            (7,17),
            (10,15)
        ],
        'av_worhours': [
            [7,8,9,10,11,12,13],
            [7,8,9,10,11,12,13],
            [7,8,9,10,11,12,13,14,15],
            [7,8,9,10,11,12,13,14,15,16],
            [10,11,12,13,14]
        ]
    }
]
'''

courses_ds = {}

'''Should be like...
courses = [
    {
        'id': 'PROGRAMACION-UUID',
        'semester': 1,
        'weekly_hours': 5,
        'classrooms': [
            { 'group': '1SA', 'professor': 'NORA-ID' },
            { 'group': '1SB', 'professor': 'NORA-ID' },
            { 'group': '1SC', 'professor': 'NORA-ID' },
        ]
    }
]
'''

groups_ds = {}

'''Should be like...
groups = {
    '1SA': {
        'semester': 1,
        'sessions': [
            {
                'id': 'PROG-SES01',
                'course': 'Programacion',
                'length': 3,
                'scheduled': True
            }
        ],
        'schedule': [
            [ ['PROG-SES01', [7,10]] ],
            [],
            [],
            [],
            []
        ],
        'current_time': {
            'day': 1,
            'hour': 7
        },
        'hour_range': [7,15],
        'class_hours': [0,0,0,0,0],
        'weekly_class_hours': 31,
        'min_daily_class_hours': [7,6,6,6,6],
        'solved': False
    }
}
'''

config_ds = {}

'''Should be like...
config = {
    'school_workhours': [7,20],
    'max_daily_idle_hours': 2
}
'''