from math import floor, ceil

def ceilFloor(x):
    """Returns the floor for positive numbers, the ceil for negative numbers."""
    if x > 0:
        return floor(x)
    else:
        return ceil(x)

def cutOff(x, max_, min_):
    """Cuts off values larger than the maximum or smaller than the minimum and
        returns the maximum/minimum."""
    if x > max_:
        return max_
    elif x < min_:
        return min_
    else:
        return x
