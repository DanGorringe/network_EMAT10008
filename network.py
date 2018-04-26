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
maxXCoord = 1000 #1280 # usually 1000
maxYCoord = 1000 #560
centreRadius = 40
nodeRadius = 20
ghostNodeRadius = 15
lineWidth = 5

# obstacles constants
obstacleSize = 20

# Values for centre node
centreNodeCoords = (int(maxXCoord/2),int(maxYCoord/2))

# Reading the csv file and filling a list with coordinates

nodeList = [centreNodeCoords]

with open('./csvFiles/list.csv','r') as csvfile1:
    csv = csv.reader(csvfile1,delimiter=',')
    for line in csv:
        nodeList.append((int(line[0])+10,int(line[1])+25))


import csv
obstacleList = []
'''
with open('obstacles.csv','r') as csvfile2:
    csv = csv.reader(csvfile2,delimiter=',')
    for line in csv:
        obstacleList.append((int(line[0]),int(line[1])))
'''

# Distance dic
# Don't think the global shit is required
global distanceDic
distanceDic = {(centreNodeCoords,centreNodeCoords):0}

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
        minX = centreNodeCoords[0] - nodeRadius*2
        maxX = centreNodeCoords[0] + nodeRadius*2
        minY = centreNodeCoords[1] - nodeRadius*2
        maxY = centreNodeCoords[1] + nodeRadius*2

        # not in centre box (centre + 2 node and centre radii)
        #if(maxXCoord/2-2*nodeRadius-centreRadius>randomCoord[0]>maxXCoord/2+2*nodeRadius+centreRadius and maxYCoord/2-2*nodeRadius-centreRadius<randomCoord[1]<maxYCoord/2+2*nodeRadius+centreRadius):

        #    randomList.append(randomCoord)
        if not (minX<randomCoord[0]<maxX) and not (minY<randomCoord[1]<maxY):
            randomList.append(randomCoord)

    print(randomList)
    return randomList




# Function to draw the central node
def DrawCentre(coordinates,draw):
    centreBox = [coordinates[0]-centreRadius,coordinates[1]-centreRadius,coordinates[0]+centreRadius,coordinates[1]+centreRadius]
    draw.ellipse(centreBox,red)

# Draw a node, where coordinates = [x,y]
def DrawNode(coordinates,draw):
    circleBox = [coordinates[0]-nodeRadius,coordinates[1]-nodeRadius,coordinates[0]+nodeRadius,coordinates[1]+nodeRadius]
    draw.ellipse(circleBox,blue)

# Draw an obstacle as a red square
def DrawObstacle(coordinates,draw):
    squareBox = [(coordinates[0]-obstacleSize,coordinates[1]+obstacleSize),(coordinates[0]+obstacleSize,coordinates[1]+obstacleSize),(coordinates[0]+obstacleSize,coordinates[1]-obstacleSize),(coordinates[0]-obstacleSize,coordinates[1]-obstacleSize)]
    draw.polygon(squareBox,red)

# Draw a tiny green square to represent a 'ghost' node, where coordinates = [x,y]
def DrawGhostNode(coordinates,draw):
    squareBox = [(coordinates[0]-ghostNodeRadius,coordinates[1]+ghostNodeRadius),(coordinates[0]+ghostNodeRadius,coordinates[1]+ghostNodeRadius),(coordinates[0]+ghostNodeRadius,coordinates[1]-ghostNodeRadius),(coordinates[0]-ghostNodeRadius,coordinates[1]-ghostNodeRadius)]
    draw.polygon(squareBox,green)

# Draw a line between a and b, where both are coordinates [x,y]
def DrawLine(a,b,draw):
    draw.line((a[0],a[1],b[0],b[1]),black,width=lineWidth)


def DrawNetwork(inputDic,draw):
    for obstacle in obstacleList:
        DrawObstacle(obstacle,draw)
    for node in inputDic:
        #print("Node is: " + str(node))
        for connection in inputDic[node]:
            #print("Connection is: " + str(connection))
            DrawLine(node,connection,draw)
            DrawGhostNode(connection,draw)
            DrawGhostNode(node,draw)
    for node in nodeList:
        DrawNode(node,draw)
    DrawCentre(centreNodeCoords,draw)

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

# Function to check whether line between a and b is obstructed
def CheckObstruction(a,b):
    for x in range(a[0],b[0]):
        y = (b[1]-a[1])/(b[0]-a[0])*x + a[1]
        #print(x,y)
        for obstacle in obstacleList:
            if x in range(obstacle[0]-obstacleSize,obstacle[0]+obstacleSize):
                if y in range(obstacle[1]-obstacleSize,obstacle[1]+obstacleSize):
                    return obstacle

def ObjectAvoidance(a,b,obstacle,dic):
    b = list(b)
    while CheckObstruction(a,b) != None:
        b[1] = b[1] + 1
    print(b[1])
    xPosition = obstacle[0] - obstacleSize

    yPoisition = ((b[1]-a[1])/(b[0]-a[0]))*float(xPosition) + a[1]
    obstaclePoint = (xPosition,yPoisition)
    print(obstaclePoint)
    Connect(a,obstaclePoint,dic)

# A function that returns the distance between two co-ordinates, in format [x,y]
def CalculateCoOrdDistance(a,b):
    global distanceDic
    # Now check whether already calculated distance
    if (a,b) in distanceDic:
        return distanceDic[(a,b)]
    else:
        deltaX = a[0] - b[0]
        deltaY = a[1] - b[1]
        distance = math.sqrt(deltaX**2 + deltaY**2)
        distanceDic[(a,b)] = distance
        distanceDic[(b,a)] = distance
        return distance


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
    i = 0
    while(len(unconnectedNodes) != 0):
        i = i + 1
        q = ShortestDistance(connectedNodes,unconnectedNodes)
        Connect(q[0][0],q[0][1],primmDic)
        #SaveNetworkImage(primmDic,"./primsGif/"+format(i,'02d')+".png")
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
    i = 0
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
    print("Checking all midpoints...")
    best = GhostOptimumNode(unconnectedNodes)
    # While there is a ghost node that shortens the network
    while(best != None):
        # Print something so you know the program isn't crashing
        print("Checking all midpoints...")
        # Append the list of nodes with the previous best
        unconnectedNodes.append(best)
        best = GhostOptimumNode(unconnectedNodes)
    print("Finished checking all midpoints")
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
    r = len(s)
    # Required so that the program can run in some reasonable time
    if r > 5:
        r = 5
    '''
    if len(s) < 3:
        r = len(s)
    '''
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(2,r+1))

def SaveNetworkImage(dic,fileString):
    # Open blank image
    image = Image.new("RGB", (maxXCoord, maxYCoord), white)
    # Alternativly, Instead open a png to draw over
    #image = Image.open("iow.png")
    draw = ImageDraw.Draw(image)
    DrawNetwork(dic,draw)
    # Save as the given fileString
    image.save(fileString)


#########
# Logic #
#########

# to iniate dictionary
dic = InitiateNodeDic()

# Run prims on dic
print("Running Prims...")
primDic = Prims(dic)

# Run our Quasi-Steiner algorithm on dic, can take quite a while
print("Running Quasi-Steiner...")
ghostDic = Ghost(dic)

print("Finished running algorithms.")

# Print lengths of networks
print("Length of Prim's network = " + str(NetworkLength(primDic)))
print("Length of Quasi-Steiner's network = " + str(NetworkLength(ghostDic)))

primFileName = "prim.png"
ghostFileName = "quasiSteiner.png"

print("Saving images to " + str(primFileName) + " and " + str(ghostFileName) + "...")

SaveNetworkImage(primDic,primFileName)
SaveNetworkImage(ghostDic,ghostFileName)

print("Finished saving.")

print("Finished program.")


# Dan Gorringe April 2018
# In Progress
