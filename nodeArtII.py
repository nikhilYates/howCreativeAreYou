import cv2
import numpy as np
import math
import random
import subprocess
import time
from scipy.spatial import KDTree

numberOfNodes = 5000
fileName = "brainScan.jpg"
map = cv2.imread(fileName)

RED = (70,78,166)


class point:
    def __init__(self, x, y,next = None, prev = None,radius = 1):
        self.x = x
        self.y = y
        self.next = next
        self.prev = prev
        self.radius = radius
        self.color = (127,127,0)

#=======================================================================================================================================

# USE THIS METHOD TO DETERMINE IF A GENERATED POINT IS ON AN OBSTACLE
def point_obst_overlap(map, p):
    def is_not_free(x, y):
        overlap = False
        if all(map[y, x] != [0, 0, 0]):
            overlap = True
        return overlap

    mapx, mapy = p.x, p.y

    if is_not_free(mapx, mapy):
        return True    
    return False

# USE THIS METHOD TO DETIRMINE IF A LINE BETWEEN TWO VALID POINTS CROSSES OVER AN OBSTACLE
def line_color_intersection(map, v1, v2):
    # we are going to check if the pixel at the specified coordinates is white
    def is_not_white(x, y):
        lineOverlap = False
        if all(map[y, x] != [0, 0, 0]):
            lineOverlap = True
            print('LINE COLOR INTERSECTION HAS OCCURED')
        return lineOverlap 
    # first, we are going to assign the point coordinates to new variables
    x1, y1, x2, y2 = v1.x, v1.y, v2.x, v2.y
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    # now, the x and y coordinates will be that of the first point
    x, y = x1, y1
    print('X COORD TO BE CHECKED = ',x)
    print('Y VALUE TO BE CHECKED = ', y)
    # here, we do some shifting by steps. If x1 > x2. For example, if x1 is greater than x2 then we 
    # will take a negative step in the x axis with sx. Similar for the y axis with sy
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    # err represents the direction we will move in along the line to get from one point to the next
    err = dx - dy
    while True:
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
        if is_not_white(x, y):
            return True
    print('NO LINE COLOR INTERSECTION')
    return False

#=======================================================================================================================================


#=======================================================================================================================================

# GET THE DISTANCE BETWEEN TWO POINTS
def findDistace (p1, p2):
    distance = math.sqrt((p1.x - p2.x)**2 + (p2.y - p1.y)**2)
    return distance

# DRAW LINE BETWEEN POINTS
def drawLine(v1,v2,color =RED, thickness=2):
    cv2.line(map, (v1.x,v1.y), (v2.x,v2.y), color, thickness)


def bigBrainAlgo(exploredVertexList,listOfVertix):
    newConnection = 0 # This will be two different vertexes we will be returning
    smallestDistance = float('inf')
    for exploredV in exploredVertexList:
        for unexploredVertix in listOfVertix:
            calculateDistance = findDistace(exploredV,unexploredVertix)
            if calculateDistance < smallestDistance and line_color_intersection(map, exploredV, unexploredVertix) == False:
                smallestDistance = calculateDistance
                newConnection = (exploredV,unexploredVertix)

    return newConnection

# FIND THE CLOSEST NODE TO A GRAPH
def findClosestNodeToGraph(exploredVertexList, listOfVertix):
    # Convert vertex points to a list of tuples
    unexploredPoints = [(v.x, v.y) for v in listOfVertix]

    # Create a KD-tree with unexplored vertices
    tree = KDTree(unexploredPoints)

    smallestDistance = float('inf')
    newConnection = None

    for exploredV in exploredVertexList:
        # Find the nearest neighbor to exploredV in the KD-tree
        distance, index = tree.query((exploredV.x, exploredV.y))

        #if line_color_intersection(map, exploredV, listOfVertix[index]):
        if distance < smallestDistance and line_color_intersection(map, exploredV, listOfVertix[index]) == False:

            smallestDistance = distance
            newConnection = (exploredV, listOfVertix[index])
            print('NEW CONNECTION MADE')
        
    
        # Early exit if the distance is zero
        if distance == 0:
            break
    if newConnection == None:
        newConnection = bigBrainAlgo(exploredVertexList,listOfVertix)
    return newConnection

# HERE WE WILL GENERATE RANDOM POINTS AND ADD THEM TO A LIST OF POINTS
def buildMap():
    # first need to define the list of generated points
    randomPoints = [(np.random.randint(120, map.shape[1]-120), np.random.randint(10, map.shape[0]-10)) for _ in range(numberOfNodes)]
    listOfVertix = []
    # now, populate the map
    for i in range(0,numberOfNodes):
        v = point(x = randomPoints[i][0], y = randomPoints[i][1])
        # if a point is generated on an obstacle, change its colour and do NOT add it to new list
        if point_obst_overlap(map,v):
            v.color = RED
        else: 
            listOfVertix.append(v)
        # print(v.x)
        cv2.circle(map, (v.x,v.y), v.radius, v.color, thickness=-1)

    cv2.imwrite('nodeBrain.jpg', map)
    return listOfVertix

buildMap()
#=======================================================================================================================================
# def mainRead():
    
#     #get the list of points
#     listOfVertix = buildMap()
#     exploredVertexList = []

#     exploredVertexList.append(listOfVertix[0])
#     listOfVertix.pop(0)

#     # iterate through the list of points (vertices) until we reach the goal vertex
#     while(len(listOfVertix) > 2):

#         graphNode, newNode = findClosestNodeToGraph(exploredVertexList, listOfVertix)

#         graphNode.next = newNode
#         newNode.prev = graphNode
#         # if line_color_intersection(map, graphNode, newNode) == False:
#         drawLine(graphNode, newNode) 
#         exploredVertexList.append(newNode)
#         listOfVertix.remove(newNode)
#         # random.shuffle(listOfVertix)

#     cv2.imwrite("nodeBrain.jpg", map)

