import sys
import fileinput
import operator
import pickle
from datetime import datetime
from util import Util

#python user_history.py [checkins] out/user_checkins.out

users = {}
fmt = "%Y-%m-%dT%H:%M:%SZ"
frequent = {}
diffs = []

for l in fileinput.input(sys.argv[1]):
    line = l.split('\t')
    userID = line[0]
    geoloc = (float(line[2]), float(line[3]))
    locID = line[4]
    date = datetime.strptime(line[1].rstrip(), fmt)
    checkins = []
    if userID in users:
        checkins = users[userID]

    checkins.append((locID,geoloc,date))
    users[userID] = checkins

checkin_list = open(sys.argv[2], 'w')

for user in users:
    checkins = users[user]
    sorted_checkins = sorted(checkins, key=operator.itemgetter(2))
    users[user] = sorted_checkins
    out = user
    first = None
    prevloc = None
    prevdate = None
    for loc,geoloc,date in sorted_checkins:
        out += "|" + loc + ">" + date.strftime(fmt)
        if prevloc is not None and prevdate is not None:
            d = Util.d(prevloc, geoloc)
            time_d = Util.time_diff(prevdate, date)
            diffs.append(time_d)
            if time_d < .04 and d > 600:
                if user not in frequent:
                    frequent[user] = []
                times = frequent[user]
                times.append(prevdate)
                times.append(date)
                frequent[user] = times
        prevloc = geoloc
        prevdate = date

    checkin_list.write(out + "\n")

checkin_list.close()

freq = open('out/freq.out', 'wb')
for user in frequent:
    out = user
    for t in frequent[user]:
        out += ' ' + str(t)
    freq.write(out + '\n')
freq.close()

pickle.dump(diffs, open('out/diffs.p', 'wb'))
