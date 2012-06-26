import fileinput
import sys
import csv
import pickle
from locations import LocationGraph

#python build_airlinenet.py [quarter.csv] [airports.p] [quarter_net.csv] [nodes.out]

airports = pickle.load(open(sys.argv[2], 'rb'))
writer = csv.writer(open(sys.argv[3], 'wb'), delimiter=',')
out = open(sys.argv[4], 'wb')

epsilon = 1
airnet = LocationGraph()

for l in fileinput.input(sys.argv[1]):
    line = l.replace('"', '').split(',')
    if line[2] in airports and line[5] in airports:
        airnet.add_edge(line[2], line[5], float(line[7]))

for a in airports:
    if a not in airnet.nodes():
        airnet.add_node(a)

airnet.make_connected(epsilon)
T = airnet.transition_matrix(airports)

for row in T:
    writer.writerow(row)

for n in airnet.nodes():
    out.write(n + '\n')

out.close()
