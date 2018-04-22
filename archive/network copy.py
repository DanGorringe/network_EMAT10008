# Python program for MDat Project 4
# To investigate the shortest length of cable to connect nodes in a network

# Import the libaries we need
import random
import math
from PIL import ImageFont, ImageDraw, Image
import csv
#from itertools import combinations
import itertools

# Iniating colour tuples
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)

# constants for drawing
maxXCoord = 2000
maxYCoord = 2000
centreRadius = 40
nodeRadius = 20
ghostNodeRadius = 10
lineWidth = 5

# Values for centre node
centreNodeCoords = (maxXCoord/2,maxYCoord/2)


# Reading the csv file and filling a list with coordinates
nodeList = [centreNodeCoords]
with open('list.csv') as csvfile:
    csv = csv.reader(csvfile,delimiter=',')
    for line in csv:
        nodeList.append((int(line[0]),int(line[1])))

# Create a dictionary to list all the connections from each nodes
# each coordinate will link to a list of coordinates of nodes it's joined to


#############
# Functions #
#############

def InitiateNodeDic():
    dic = {centreNodeCoords:[]}
    for node in nodeList:
        dic[node] = []
    return dic

# Function to draw the central node
def DrawCentre(coordinates):
    centreBox = [coordinates[0]-centreRadius,coordinates[1]-centreRadius,coordinates[0]+centreRadius,coordinates[1]+centreRadius]
    draw.ellipse(centreBox,red)

# Draw a node, where coordinates = [x,y]
def DrawNode(coordinates):
    circleBox = [coordinates[0]-nodeRadius,coordinates[1]-nodeRadius,coordinates[0]+nodeRadius,coordinates[1]+nodeRadius]
    draw.ellipse(circleBox,blue)

def DrawGhostNode(coordinates):
    squareBox = [(coordinates[0]-ghostNodeRadius,coordinates[1]+ghostNodeRadius),(coordinates[0]+ghostNodeRadius,coordinates[1]+ghostNodeRadius),(coordinates[0]+ghostNodeRadius,coordinates[1]-ghostNodeRadius),(coordinates[0]-ghostNodeRadius,coordinates[1]-ghostNodeRadius)]
    draw.polygon(squareBox,green)

# Draw a line between a and b, where both are coordinates [x,y]
def DrawLine(a,b):
    draw.line((a[0],a[1],b[0],b[1]),black,width=lineWidth)

# Add connecitions in the dictionary
def Connect(a,b,dic):
    if a in dic:
        dic[a].append(b)
    if a not in dic:
        dic[a] = [b]
    if b in dic:
        dic[b].append(a)
    if b not in dic:
        dic[b] = [a]

def DrawNetwork(inputDic):
    for node in inputDic:
        #print("Node is: " + str(node))
        for connection in inputDic[node]:
            #print("Connection is: " + str(connection))
            DrawLine(node,connection)
            DrawGhostNode(connection)
            DrawGhostNode(node)
    for node in nodeList:
        DrawNode(node)
    DrawCentre(centreNodeCoords)

# A function that returns the distance between two co-ordinates, in format [x,y]
def CalculateCoOrdDistance(a,b):
    deltaX = a[0] - b[0]
    deltaY = a[1] - b[1]
    distance = deltaX**2 + deltaY**2
    return math.sqrt(distance)

# Used for finding shortest connections for Prim's Algorithm
def ShortestDistance(connectedNodes,unconnectedNodes):
    # Current best is a list of two co-ordinates
    currentBest = [[],[]]
    # Value of the shortest distance between these points, initally set to a V. high value
    currentBestValue = maxYCoord*maxXCoord
    # Search though every node finding the shortest unconnected node to connected nodes
    for node in connectedNodes:
        for joinee in unconnectedNodes:
            #print("Distance from " + str(node) + " to " + str(joinee) + " is " + str(CalculateCoOrdDistance(node,joinee)))
            if(CalculateCoOrdDistance(node,joinee) < currentBestValue):
                currentBestValue = CalculateCoOrdDistance(node,joinee)
                currentBest = [node,joinee]
    return [currentBest,currentBestValue]

# Find th midpoint between a list of coordinates [(x_1,y_1),(x_2,y_2),..,(x_n,y_n)]
def Midpoint(coordinateList):
    x = 0
    y = 0
    for coordinate in coordinateList:
        x += coordinate[0]
        y += coordinate[1]
    x = x/len(coordinateList)
    y = y/len(coordinateList)
    return((x,y))

# Returns length of wire using primms method, does no drawing
def Primms(nodeList):
    connectedNodes = [centreNodeCoords]
    # only way to 'duplicate' a list is with list()
    unconnectedNodes = list(nodeList)
    # Create a dictionary
    primmDic = InitiateNodeDic()
    #unconnectedNodes.append((600,600))
    while(len(unconnectedNodes) != 0):
        q = ShortestDistance(connectedNodes,unconnectedNodes)
        Connect(q[0][0],q[0][1],primmDic)
        connectedNodes.append(q[0][1])
        unconnectedNodes.remove(q[0][1])
    return primmDic

# Returns length of wire using sun method, does no drawing
def Sun(nodeList):
    connectedNodes = [centreNodeCoords]
    # only way to 'duplicate' a list is with list()
    unconnectedNodes = list(nodeList)
    total = 0
    # Initiate a dictionary
    sunDic = InitiateNodeDic()
    while(len(unconnectedNodes) != 0):
        Connect(centreNodeCoords,unconnectedNodes[-1],sunDic)
        connectedNodes.append(unconnectedNodes[-1])
        unconnectedNodes.remove(unconnectedNodes[-1])
    return sunDic

# Dan's ghost node method: placing 'ghost nodes' at midpoints to shorten overall length of wire used
def Ghost(nodeList):
    connectedNodes = [centreNodeCoords]
    unconnectedNodes = list(nodeList)
    ghostingDic = InitiateNodeDic()
    # Create a 'value' of wire to 'beat'
    # best is the midpoint ghost node which shortens the network the most
    best = GhostOptimumNode(unconnectedNodes)
    # While there is a ghost node that shortens the network
    while(best != None):
        # Append the list of nodes with the previous best
        unconnectedNodes.append(best)
        best = GhostOptimumNode(unconnectedNodes)
    # Finally run primms with the finished list
    ghostingDic = Primms(unconnectedNodes)
    return ghostingDic


def GhostOptimumNode(nodeList):
    # combs is a list of all the combinations of all variation of nodes in the nodeList given
    combs = list(powerset(nodeList))
    # Set default value to None
    bestMidpoint = None
    # Value to beat is currentBest
    currentBest = NetworkLength(Primms(nodeList))
    # For each midpint, add to the unconnected list and check whether after using primms it creates a shorter network
    for comb in combs:
        unconnectedNodes = list(nodeList)
        ghostingDic = InitiateNodeDic()
        unconnectedNodes.append(Midpoint(comb))
        ghostingDic = Primms(unconnectedNodes)
        # Check whether the difference is bigger than a certain tolerance
        if (currentBest - NetworkLength(ghostingDic) > 1):
            optimumGhostingDic = ghostingDic
            currentBest = NetworkLength(ghostingDic)
            bestMidpoint = Midpoint(comb)
    return bestMidpoint



# Function to calculate distance of 'wire' used to connect the network
def NetworkLength(dic):
    localDic = dict(dic)
    total = 0
    for node in localDic:
        for connection in localDic[node]:
            # We record the connection from both ends, therefore we only add half the displacement
            total += CalculateCoOrdDistance(node,connection)/2
    return total

# Return a list of all the different combinations of the list given
def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(2,len(s)+1))


#########
# Logic #
#########

# Opening an image
image = Image.new("RGB", (maxXCoord, maxYCoord), white)
draw = ImageDraw.Draw(image)

# Create a network's dictionary
# can use Sun(),Primms(),and Ghost()
print("Running ghost Algorithm...")
ghostDic = Ghost(nodeList)
print("Finished running Algorithm\n")

# Draw out the network
DrawNetwork(ghostDic)

# Print to terminal the length of wire used to connect the network
print("Working out network lengths...")
currentBest = NetworkLength(Primms(nodeList))
print("Primms gets: " + str(currentBest))
print("Ghosting method gets: "  + str(NetworkLength(ghostDic)) + "\n")

# Save the image
fileString = "test.png"
print("Saving Image to " + str(fileString) + "...")
image.save(fileString)
print("Image saved\n")

# Dan Gorringe March 2018
# In Progress
