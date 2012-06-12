import numpy as np
import random
import math
from datetime import datetime

class Util:

    @staticmethod
    def convert(x1, y1, x2, y2):
        x1 = math.radians(x1)
        y1 = math.radians(y1)
        x2 = math.radians(x2)
        y2 = math.radians(y2)

        return x1, y1, x2, y2

    @staticmethod
    def distance(x1, y1, x2, y2):
        R = 3961
        lat1, lon1, lat2, lon2 = Util.convert(x1, y1, x2, y2)
        dlat = lat2-lat1
        dlon = lon2-lon1

        a = math.pow(math.sin(dlat/2.0),2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon/2.0),2)
        c = 2.0 * math.atan2( math.sqrt(a), math.sqrt(1.0-a) )
        d = R * c

        return d

    @staticmethod
    def d(a, b):
        x1, y1 = a
        x2, y2 = b

        return Util.distance(x1, y1, x2, y2)

    @staticmethod
    def time_diff(a, b):
        timedelta = b - a
        days = timedelta.days
        fraction = timedelta.seconds / 86400.0
        return days+fraction
