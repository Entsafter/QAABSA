from QAABSA.utils import cutOff

def linearScaleDict(inputDict, wanted_max, wanted_min):
    """Returns a scaled list. Min value will be wanted_min, max value wanted_mad
       values inbetween are scaled linearly."""
    values = inputDict.values()
    min_ = min(values)
    max_ = max(values)
    return {key: round((((v - min_)/(max_ - min_))*(wanted_max - wanted_min))+wanted_min) for (key, v) in inputDict.items()}

def cufOffScaleDict(inputDict, wanted_max, wanted_min):
    """Cutting off values in a dict that are larger or smaller than wanted."""
    return {key: cutOff(v, wanted_max, wanted_min) for (key, v) in inputDict.items()}

def cufOffRoundScaleDict(inputDict, wanted_max, wanted_min):
    """Cutting off values in a dict that are larger or smaller than wanted and rounding them."""
    return {key: cutOff(round(v), wanted_max, wanted_min) for (key, v) in inputDict.items()}
