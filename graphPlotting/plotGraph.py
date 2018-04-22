# Python program for MDat Project 4
# To investigate the shortest length of cable to connect nodes in a network

# Import the libaries we need
import csv
import matplotlib.pyplot as plt

sunFile = open('sunDataFile.csv','r')
primFile = open('primsDataFile.csv','r')
ghostFile = open('ghostDataFile.csv','r')

sunData = []
primData = []
ghostData = []
xValues = []

red = [255,0,0]
blue = [0,0,255]

reader = csv.reader(sunFile)
for row in reader:
    data = [int(row[0]),float(row[1])]
    sunData.append(data[1])
    xValues.append(data[0])

reader = csv.reader(primFile)
for row in reader:
    data = [int(row[0]),float(row[1])]
    primData.append(data[1])

reader = csv.reader(ghostFile)
for row in reader:
    data = [int(row[0]),float(row[1])]
    ghostData.append(data[1])

def AverageData(X,Y):
    previous = X[0]
    returningY = []
    iterations = 0
    runningTotal = 0
    i = 0
    for x in X:
        if x!=previous:
            returningY.append(runningTotal/iterations)
            iterations = 0
            runningTotal = 0
        runningTotal += Y[i]
        iterations += 1
        i += 1
        previous = x
    returningY.append(runningTotal/iterations)
    return returningY

print("Averaging data...")
XAverage = AverageData(xValues,xValues)
sunAverage = AverageData(xValues,sunData)
print(" - Finished averaging Sun data")
primAverage = AverageData(xValues,primData)
print(" - Finished averaging Prims data")
ghostAverage = AverageData(xValues,ghostData)
print(" - Finished averaging Ghost data")

'''
print("Plotting Sun data...")
plt.scatter(xValues,sunData,c='red')
plt.plot(XAverage,sunAverage,c='red')
'''

for i in range(len(primAverage)):
    print(ghostAverage[i]/primAverage[i])


print("Plotting Prim data...")
plt.scatter(xValues,primData,s=0.5,c='red')
plt.plot(XAverage,primAverage,c='red',label="Prims")
print("Plotting Ghost data...")
plt.scatter(xValues,ghostData,s=0.5,c='blue')
plt.plot(XAverage,ghostAverage,c='blue',label="Quasi-Steiner")

plt.xlabel('Randomly placed nodes')
plt.ylabel('Length of network')
plt.legend()

print("\nFinished plotting, now opening graph...")

plt.show(block=False)
input("Hit Enter To Close")
plt.close()


# Dan Gorringe April 2018
# In Progress
