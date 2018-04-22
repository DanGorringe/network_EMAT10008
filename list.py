import random

hublist = []
maxhubs = 20

# constants for drawing
maxXCoord = 1000
maxYCoord = 1000
centreRadius = 40
hubRadius = 20
lineWidth = 5

# Set number of hubs
maxHubs = 32

# Values for centre hub
centreHubCoords = [maxXCoord/2,maxYCoord/2]
centreHubSquareCoords = [maxXCoord/2-centreRadius,maxYCoord/2-centreRadius,maxXCoord/2+centreRadius,maxYCoord/2+centreRadius]

# make maxHub many entries
while(len(hublist) < maxHubs):
    # random co-ordinate in square that's 2 hub radii smaller than canvas
    hublist.append([random.randint(2*hubRadius,maxXCoord-2*hubRadius),random.randint(2*hubRadius,maxYCoord-2*hubRadius)])
    # not in centre box (centre + 2 hub and centre radii)
    if(maxXCoord/2-2*hubRadius-centreRadius<hublist[-1][0]<maxXCoord/2+2*hubRadius+centreRadius and maxYCoord/2-2*hubRadius-centreRadius<hublist[-1][1]<maxYCoord/2+2*hubRadius+centreRadius):
        hublist.pop()

for coordinate in hublist:
    print(str(coordinate[0])+","+str(coordinate[1]))
