import random
import math
from tkinter import *
from tkinter import ttk

from PIL import ImageFont, ImageDraw, Image

# Iniating colour tuples
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

# constants for drawing
maxCoord = 1000
centreRadius = 10
hubRadius = 2
centreCoords = [maxCoord/2-centreRadius,maxCoord/2-centreRadius,maxCoord/2+centreRadius,maxCoord/2+centreRadius]

# A list for our hubs
hublist = []
# make 3 entries
while(len(hublist) < 500):
    # random co-ordinate in square that's 2 hub radii smaller than canvas
    hublist.append([random.randint(2*hubRadius,maxCoord-2*hubRadius),random.randint(2*hubRadius,maxCoord-2*hubRadius)])
    # not in centre box (centre + 2 hub and centre radii)
    if(maxCoord/2-2*hubRadius-centreRadius<hublist[-1][0]<maxCoord/2+2*hubRadius+centreRadius and maxCoord/2-2*hubRadius-centreRadius<hublist[-1][1]<maxCoord/2+2*hubRadius+centreRadius):
        print("Destroying entry")
        hublist.pop()



# A function that joins any two points
# a and b are co-ordinates, [x,y]
def Join(a,b):
    draw.line((a[0],a[1],b[0],b[1]),black,width=2)
    # Check whether you're connecting to the centre point
    if(a[0] and a[1] == maxCoord/2):
        draw.ellipse(centreCoords,red)
    else:
        circleBox = [a[0]-hubRadius,a[1]-hubRadius,a[0]+hubRadius,a[1]+hubRadius]
        draw.ellipse(circleBox,blue)
    if(b[0] and b[1] == maxCoord/2):
        draw.ellipse(centreCoords,red)
    else:
        circleBox = [b[0]-hubRadius,b[1]-hubRadius,b[0]+hubRadius,b[1]+hubRadius]
        draw.ellipse(circleBox,blue)

def CalculateCoOrdDistance(a,b):
    deltaX = a[0] - b[0]
    deltaY = a[1] - b[1]
    distance = deltaX**2 + deltaY**2
    return math.sqrt(distance)

def ShortestDistance(connectedHubs,unconnectedHubs):
    # Current best is a list of two co-ordinates
    currentBest = [[],[]]
    currentBestValue = maxCoord
    for hub in connectedHubs:
        for joinee in unconnectedHubs:
            #print("Distance from " + str(hub) + " to " + str(joinee) + " is " + str(CalculateCoOrdDistance(hub,joinee)))
            if(int(CalculateCoOrdDistance(hub,joinee)) < int(currentBestValue)):
                currentBestValue = int(CalculateCoOrdDistance(hub,joinee))
                currentBest = [hub,joinee]
                #print("Altering estimation")
    #print("Suggested connection: " + str(currentBest))
    return currentBest

unconnectedHubs = hublist
connectedHubs = [[maxCoord/2,maxCoord/2]]

image = Image.new("RGB", (maxCoord, maxCoord), white)
draw = ImageDraw.Draw(image)
# draws centre 'hub', around centre point
while(len(unconnectedHubs) != 0):
    q = ShortestDistance(connectedHubs,unconnectedHubs)
    connectedHubs.append(q[1])
    unconnectedHubs.remove(q[1])
    Join(q[0],q[1])

image.save("foo.png")



# Dan Gorringe January 2018
