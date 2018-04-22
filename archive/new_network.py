import random
import math
from tkinter import *
from tkinter import ttk

import csv
hublist = []
with open('list.csv') as csvfile:
    csv = csv.reader(csvfile,delimiter=',')
    for line in csv:
        hublist.append([int(line[0]),int(line[1])])

from PIL import ImageFont, ImageDraw, Image

# Iniating colour tuples
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

# constants for drawing
maxXCoord = 1000
maxYCoord = 1000
centreRadius = 40
hubRadius = 20
lineWidth = 5

# Values for centre hub
centreHubCoords = [maxXCoord/2,maxYCoord/2]
centreHubSquareCoords = [maxXCoord/2-centreRadius,maxYCoord/2-centreRadius,maxXCoord/2+centreRadius,maxYCoord/2+centreRadius]


# A function that joins any two points
# a and b are co-ordinates, [x,y]
def Join(a,b):
    # Draw a line connecting two points
    draw.line((a[0],a[1],b[0],b[1]),black,width=lineWidth)
    # Check whether you're connecting to the centre point
    # If so redraw the centre hub
    if(a[0] == maxXCoord/2 and a[1] == maxYCoord/2):
        draw.ellipse(centreHubSquareCoords,red)
    else:
    # Otherwise draw a normal hub
        circleBox = [a[0]-hubRadius,a[1]-hubRadius,a[0]+hubRadius,a[1]+hubRadius]
        draw.ellipse(circleBox,blue)
    if(b[0] == maxXCoord/2 and b[1] == maxYCoord/2):
        draw.ellipse(centreHubSquareCoords,red)
    else:
        circleBox = [b[0]-hubRadius,b[1]-hubRadius,b[0]+hubRadius,b[1]+hubRadius]
        draw.ellipse(circleBox,blue)

# A function that returns the distance between two co-ordinates, in format [x,y]
def CalculateCoOrdDistance(a,b):
    deltaX = a[0] - b[0]
    deltaY = a[1] - b[1]
    distance = deltaX**2 + deltaY**2
    return math.sqrt(distance)

# Used for finding shortest connections for Prim's Algorithm
def ShortestDistance(connectedHubs,unconnectedHubs):
    # Current best is a list of two co-ordinates
    currentBest = [[],[]]
    # Value of the shortest distance between these points, initally set to a V. high value
    currentBestValue = maxYCoord*maxXCoord
    # Search though every hub finding the shortest unconnected hub to connected hubs
    for hub in connectedHubs:
        for joinee in unconnectedHubs:
            #print("Distance from " + str(hub) + " to " + str(joinee) + " is " + str(CalculateCoOrdDistance(hub,joinee)))
            if(int(CalculateCoOrdDistance(hub,joinee)) < int(currentBestValue)):
                currentBestValue = int(CalculateCoOrdDistance(hub,joinee))
                currentBest = [hub,joinee]
    return [currentBest,currentBestValue]

# Returns length of wire using primms method, does no drawing
def Primms(inputList):
    connectedHubs = [centreHubCoords]
    unconnectedHubs = []
    # only way to 'duplicate' a list is with list()
    unconnectedHubs = list(inputList)
    total = 0
    while(len(unconnectedHubs) != 0):
        q = ShortestDistance(connectedHubs,unconnectedHubs)
        total += q[1]
        connectedHubs.append(q[0][1])
        unconnectedHubs.remove(q[0][1])
    return total

# Returns length of wire using sun method, does no drawing
def Sun(inputList):
    connectedHubs = [centreHubCoords]
    unconnectedHubs = []
    # only way to 'duplicate' a list is with list()
    unconnectedHubs = list(inputList)
    total = 0
    while(len(unconnectedHubs) != 0):
        total += math.sqrt(((centreHubCoords[0]-unconnectedHubs[-1][0])**2)+((centreHubCoords[1]-unconnectedHubs[-1][1])**2))
        connectedHubs.append(unconnectedHubs[-1])
        unconnectedHubs.remove(unconnectedHubs[-1])
    return total



# Loop through

maxIterations = 10
maxHubs = 100

sunData = []
primmsData = []


for hubs in range(1,maxHubs):
    print(hubs)
    for iteration in range(maxIterations):
        hublist = []
        while(len(hublist) < hubs):
            hublist.append([random.randint(2*hubRadius,maxXCoord-2*hubRadius),random.randint(2*hubRadius,maxYCoord-2*hubRadius)])
            # not in centre box (centre + 2 hub and centre radii)
            if(maxXCoord/2-2*hubRadius-centreRadius<hublist[-1][0]<maxXCoord/2+2*hubRadius+centreRadius and maxYCoord/2-2*hubRadius-centreRadius<hublist[-1][1]<maxYCoord/2+2*hubRadius+centreRadius):
                hublist.pop()
        sunData.append([hubs,int(Sun(hublist))])
        primmsData.append([hubs,int(Primms(hublist))])


sun = open('sunDataFile.csv','w')
for row in sunData:
    sun.write(str(row[0])+","+str(row[1])+"\n")

primms = open('primmsDataFile.csv','w')
for row in primmsData:
    primms.write(str(row[0])+","+str(row[1])+"\n")

# Dan Gorringe March 2018
# In Progress
