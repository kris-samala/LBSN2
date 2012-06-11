import sys
import fileinput
import pickle
import math
import operator
import numpy as np

#python fix_locations.py [raw_checkin_data] census.p city_coordinates.p checkins_w_city.out

census = pickle.load(open(sys.argv[2], 'rb'))
city_coords = pickle.load(open(sys.argv[3], 'rb'))
found = {}
R = 3961
distances = []

def find_city(x, y):
    closest = []
    for c in city_coords:
        x2, y2 = city_coords[c]
        y2 = -y2
        d = distance(x, y, x2, y2)
        if d < 120.0:
            closest.append((c ,d))

    sorted_closest = sorted(closest, key=operator.itemgetter(1))

    for city, pop in sorted_closest:
        if city in census:
            distances.append(d)
            return city
    return None


def convert(x1, y1, x2, y2):
    x1 = math.radians(x1)
    y1 = math.radians(y1)
    x2 = math.radians(x2)
    y2 = math.radians(y2)

    return x1, y1, x2, y2


def distance(x1, y1, x2, y2):
    lat1, lon1, lat2, lon2 = convert(x1, y1, x2, y2)
    dlat = lat2-lat1
    dlon = lon2-lon1

    a = math.pow(math.sin(dlat/2.0),2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon/2.0),2)
    c = 2.0 * math.atan2( math.sqrt(a), math.sqrt(1.0-a) )
    d = R * c

    return d

out = open('out/' + sys.argv[4], 'wb')
err = open('out/not_found.out', 'wb')
found_loc = {}


if len(sys.argv) < 4:
    print "Filename required."
else:
    count = 0
    for l in fileinput.input(sys.argv[1]):
        line = l.split("\t")
        userID = line[0].rstrip()
        latitude = float(line[2])
        longitude = float(line[3])
        locID = line[4].rstrip()
        if locID in found_loc:
            new_loc = found_loc[locID]
        else:
            new_loc = find_city(latitude, longitude)

        if new_loc is None:
            err.write(str(latitude) + '\t' + str(longitude) + '\n')
        else:
            new_line = l.rstrip() + '\t' + new_loc + '\n'
            out.write(new_line)

out.close()
err.close()

avg = np.avg(distances)
print "Average distance = " + str(avg)
