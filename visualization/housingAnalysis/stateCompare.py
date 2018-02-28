import matplotlib
# Must be before importing matplotlib.pyplot or pylab!
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np 
import json

with open('stateCompare.json') as data_file:    
    data = json.load(data_file)

west = [(data["results"][0]["data"][x][0]+data["results"][0]["data"][x][1])/2   for x in range(len(data["results"][0]["data"]))]

east = [(data["results"][0]["data"][x][2]+data["results"][0]["data"][x][3])/2   for x in range(len(data["results"][0]["data"]))]

west = np.asarray(west)
east = np.asarray(east)

fig = plt.figure()
plt.scatter(west, east)

xs = [a for a in range (0,100)]
ys = [b for b in range (0,100)]

plt.plot(xs,ys)

plt.ylim([0,100])
plt.xlim([0,100])

plt.xlabel("West Coast House Price Index")
plt.ylabel("East Coast House Price Index")

# Export the table to a PNG image
fig.savefig('temp.png')
