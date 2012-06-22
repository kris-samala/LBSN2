import fileinput
import pickle
import sys

#python load_airports.py airports.csv primary_airports.txt [out/airports.p]

airports = {}

primary = []

for l in fileinput.input(sys.argv[2]):
    primary.append(l.strip())

for l in fileinput.input(sys.argv[1]):
    line = l.strip().replace('"', '').split(',')
    if line[2] == "US" and line[1] in primary:
        airports[line[1]] = (float(line[3]), float(line[4]))

pickle.dump(airports, open(sys.argv[3], 'wb'))
