def generateWorkhours(start, end):
    # Preconditions
    if end <= start: raise Exception
    # Process
    hours = []
    for x in range(start, end):
        hours.append(x)
        print(x)
    return hours

professors = {
    'Nora': {
        'workshifts': {
            1: [7,8,9,10,11,12,13],
            2: [7,8,9,10,11,12,13],
            3: [7,8,9,10,11,12,13,14,15],
            4: [7,8,9,10,11,12,13,14,15,15],
            5: [10,11,12,13,14]
        }
    },
    'Lucy': {
        'workshifts': {
            1: [7,8,9,10,11,12,13],
            2: [7,8,9,10,11,12,13],
            3: [7,8,9,10,11,12,13,14,15],
            4: [7,8,9,10,11,12,13,14,15,15],
            5: [10,11,12,13,14]
        }
    },
    'Mauricio': {
        'workshifts': {
            1: [7,8,9,10,11,12,13],
            2: [7,8,9,10,11,12,13],
            3: [7,8,9,10,11,12,13,14,15],
            4: [7,8,9,10,11,12,13,14,15,15],
            5: [10,11,12,13,14]
        }
    },
    'Fatima': {
        'workshifts': {
            1: [7,8,9,10,11,12,13],
            2: [7,8,9,10,11,12,13],
            3: [7,8,9,10,11,12,13,14,15],
            4: [7,8,9,10,11,12,13,14,15,15],
            5: [10,11,12,13,14]
        }
    },
    'Maria': {
        'workshifts': {
            1: [7,8,9,10,11,12,13],
            2: [7,8,9,10,11,12,13],
            3: [7,8,9,10,11,12,13,14,15],
            4: [7,8,9,10,11,12,13,14,15,15],
            5: [10,11,12,13,14]
        }
    },
    'Glendy': {
        'workshifts': {
            1: [7,8,9,10,11,12,13],
            2: [7,8,9,10,11,12,13],
            3: [7,8,9,10,11,12,13,14,15],
            4: [7,8,9,10,11,12,13,14,15,15],
            5: [10,11,12,13,14]
        }
    },
    'Karime': {
        'workshifts': {
            1: [7,8,9,10,11,12,13],
            2: [7,8,9,10,11,12,13],
            3: [7,8,9,10,11,12,13,14,15],
            4: [7,8,9,10,11,12,13,14,15,15],
            5: [10,11,12,13,14]
        }
    }
}

courses = {
    'Programacion': {
        'semester': 1,
        'weekly_hours': 5,
        'professor':{
            '1SA': 'Nora',
            '1SB': 'Nora',
            '1SC': 'Aida'
        }
    },
    'Investigacion': {
        'semester': 1,
        'weekly_hours': 5,
        'professor':{
            '1SA': 'Mauricio',
            '1SB': 'Aida',
            '1SC': 'Mauricio'
        }
    },
    'Etica': {
        'semester': 1,
        'weekly_hours': 4,
        'professor':{
            '1SA': 'Fatima',
            '1SB': 'Fatima',
            '1SC': 'Fatima'
        }
    },
    'Calculo': {
        'semester': 1,
        'weekly_hours': 5,
        'professor':{
            '1SA': 'Maria',
            '1SB': 'Maria',
            '1SC': 'Glendy'
        }
    },
    'Administracion': {
        'semester': 1,
        'weekly_hours': 5,
        'professor':{
            '1SA': 'Fatima',
            '1SB': 'Fatima',
            '1SC': 'Fatima'
        }
    },
    'MatDiscretas': {
        'semester': 1,
        'weekly_hours': 5,
        'professor':{
            '1SA': 'Karime',
            '1SB': 'Karime',
            '1SC': 'Karime'
        }
    }
}

groups = {
    '1SA': {
        ''
    }
}
'''
groups: {
    '6SA': {
        'semester': 6,
        'sessions': {
            'ProgSessionID': 2
        },
        'rem_sessions': {

        },
        'schedule': {
            'Monday': [
                'ProgSessionID': [7, 8]
            ]
        }
        'configs': {
            'min_daily_class_hours': 4
            'current_day': 3
            'class_time_range': [7, 15]
        },
        'solved': False
    }
}
'''