import fileinput
import sys
import csv
from locations import LocationGraph

#python build_airlinenet.py [quarter.csv] [quarter_net.csv] [nodes.out]

writer = csv.writer(open(sys.argv[2], 'wb'), delimiter=',')
out = open(sys.argv[3], 'wb')

epsilon = 1
airnet = LocationGraph()

for l in fileinput.input(sys.argv[1]):
    line = l.replace('"', '').split(',')
    airnet.add_edge(line[2], line[5], float(line[7]))

airnet.make_connected(epsilon)
T = airnet.transition_matrix()

for row in T:
    writer.writerow(row)

for n in airnet.nodes():
    out.write(n + '\n')

out.close()
