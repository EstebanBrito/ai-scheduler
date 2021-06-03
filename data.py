

professors = {
    'Karime': {
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
}

courses = {
    'Programacion': {
        'semester': 1,
        'weekly_hours': 5,
        'professors':{
            '1SA': 'Nora',
            '1SB': 'Nora',
            '1SC': 'Nora'
        }
    }
}

groups = {
    '1SA': {
        'semester': 1,
        'sessions': {
            'PROG-SES01': {
                'course': 'Programacion',
                'length': 3,
                'scheduled': True
            }
        },
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
        'weekly_class_hours': 25,
        'min_daily_class_hours': 0,
        'solved': False
    }
}

config: {
    'school_workhours': (7,20),
    'max_daily_idle_hours': 2
}