import sys
import fileinput

#python count_stats.py [checkins_with_city] [out_file]

users = set()
cities = set()
spots = set()
checkins = 0

for line in fileinput.input(sys.argv[1]):
    line = line.split()
    checkins += 1
    u = line[0]
    s = line[4]
#    c = line[5]
    users.add(u)
    spots.add(s)
#    cities.add(c)

out = open(sys.argv[2], 'wb')

out.write('Users = ' + str(len(users)))
out.write('\nSpots = ' + str(len(spots)))
out.write('\nCities = ' + str(len(cities)))
out.write('\nCheckins = ' + str(checkins))
