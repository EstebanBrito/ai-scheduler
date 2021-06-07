def gen_array_from_range(start, end):
    '''Given two inputs, generates an array including every
    element form start (included) to end (not included)'''
    # Preconditions
    if end <= start: raise Exception
    # Process
    res = []
    for x in range(start, end):
        res.append(x)
    return res

def see_ds_status(professors, courses, groups, config):
    print('PROFESSORS')
    print(professors)
    print('COURSES')
    print(courses)
    print('GROUPS')
    print(groups)
    print('CONFIG')
    print(config)
    print()