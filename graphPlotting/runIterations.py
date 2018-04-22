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
maxXCoord = 1000
maxYCoord = 1000
centreRadius = 40
nodeRadius = 20
ghostNodeRadius = 10
lineWidth = 5

# Values for centre node
centreNodeCoords = (maxXCoord/2,maxYCoord/2)

# Create a dictionary to list all the connections from each nodes
# each coordinate will link to a list of coordinates of nodes it's joined to


#############
# Functions #
#############

# Shamelessly poached from online
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def InitiateNodeDic():
    dic = {centreNodeCoords:[]}
    for node in nodeList:
        dic[node] = []
    return dic

# Function to create a random nodeList
def RandomNodeDic(maxNodes):
    randomList = [centreNodeCoords]
    while(len(randomList) < maxNodes):
        # random co-ordinate in square that's 2 node radii smaller than canvas
        randomCoord = (random.randint(2*nodeRadius,maxXCoord-2*nodeRadius),random.randint(2*nodeRadius,maxYCoord-2*nodeRadius))

        # not in centre box (centre + 2 node and centre radii)
        if(maxXCoord/2-2*nodeRadius-centreRadius<randomCoord[0]<maxXCoord/2+2*nodeRadius+centreRadius and maxYCoord/2-2*nodeRadius-centreRadius<randomCoord[1]<maxYCoord/2+2*nodeRadius+centreRadius):
            randomList.append(randomCoord)
    return randomList




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

# Returns length of wire using prims method, does no drawing
def Prims(nodeList):
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
    # Finally run prims with the finished list
    ghostingDic = Prims(unconnectedNodes)
    return ghostingDic


def GhostOptimumNode(nodeList):
    # combs is a list of all the combinations of all variation of nodes in the nodeList given
    combs = list(powerset(nodeList))
    # Set default value to None
    bestMidpoint = None
    # Value to beat is currentBest
    currentBest = NetworkLength(Prims(nodeList))
    # For each midpint, add to the unconnected list and check whether after using prims it creates a shorter network
    for comb in combs:
        unconnectedNodes = list(nodeList)
        ghostingDic = InitiateNodeDic()
        unconnectedNodes.append(Midpoint(comb))
        ghostingDic = Prims(unconnectedNodes)
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
    r = 7
    if len(s) < 7:
        r = len(s)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(2,r))


#########
# Logic #
#########

startValue = 10
endValue = 10
maxIterations = 1000

print("Starting Prims, Sun and Ghost Algorithm from " + str(startValue) + " to " + str(endValue) + " number of randomly placed nodes, for " + str(maxIterations) + " each...\n")

sunFile = open('sunDataFile.csv','w')
primFile = open('primsDataFile.csv','w')
ghostFile = open('ghostDataFile.csv','w')

for i in range(startValue,endValue+1):
    print(str(i) + " randomly placed nodes...")
    currentTally = [0,0,0]
    printProgressBar(0,maxIterations, prefix = 'Progress:', suffix = 'Complete')
    for j in range(maxIterations):
        nodeList = RandomNodeDic(i)
        sunIteration = NetworkLength(Sun(list(nodeList)))
        primIteration = NetworkLength(Prims(list(nodeList)))
        ghostIteration = NetworkLength(Ghost(list(nodeList)))
        sunFile.write(str(i)+","+str(sunIteration)+"\n")
        primFile.write(str(i)+","+str(primIteration)+"\n")
        ghostFile.write(str(i)+","+str(ghostIteration)+"\n")
        currentTally[0] += sunIteration
        currentTally[1] += primIteration
        currentTally[2] += ghostIteration
        printProgressBar(j+1,maxIterations, prefix = 'Progress:', suffix = 'Complete')
    #print("\n")
    print("- Averaged Sun network length was " + str(currentTally[0]/maxIterations))
    print("- Averaged Prim network length was " + str(currentTally[1]/maxIterations))
    print("- Averaged Ghost network length was " + str(currentTally[2]/maxIterations)+"\n")

print("Completed all iterations")


# Dan Gorringe April 2018
# In Progress
