import sys
import fileinput
import pickle
import operator
import numpy as np
from util import Util

#python match_airports.py [raw_checkin_data-brightkite] [airports.p] checkins_w_airport.out

airports = pickle.load(open(sys.argv[2], 'rb'))
found_loc = {}
out = open(sys.argv[3], 'wb')
err = open('out/not_found.out', 'wb')
distances = []

def find_city(x, y):
    closest = []
    for a in airports:
        x2, y2 = airports[a]
        d = Util.distance(x, y, x2, y2)
        if d < 60.0:
            closest.append((a,d))

    sorted_closest = sorted(closest, key=operator.itemgetter(1))

    for airport, dist in sorted_closest:
        distances.append(dist)
        return airport

    return None

count = 0
for l in fileinput.input(sys.argv[1]):
    count +=1
    line = l.split("\t")
    if len(line) < 5:
        break
    userID = line[0].rstrip()
    latitude = float(line[2])
    longitude = float(line[3])
    locID = line[4].rstrip()
    if locID in found_loc:
        new_loc = found_loc[locID]
    else:
        new_loc = find_city(latitude, longitude)

    if new_loc is None:
        err.write(l)
    else:
        new_line = l.rstrip() + '\t' + new_loc + '\n'
        out.write(new_line)

    print count

out.close()
err.close()

avg = np.average(distances)
print "Average distance = " + str(avg)
