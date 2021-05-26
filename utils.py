def gen_array_from_range(start, end):
    # Preconditions
    if end <= start: raise Exception
    # Process
    res = []
    for x in range(start, end):
        res.append(x)
    return res