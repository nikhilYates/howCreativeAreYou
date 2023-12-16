import cv2
import math
import random
import numpy as np


NODE_COUNT = 1000
HEIGHT = 800
WIDTH = 700
map = np.zeros((HEIGHT, WIDTH, 3), np.uint8)


RED = (55,24,227)

class circles:
    def __init__(self, x, y, next = None, prev = None, color = RED):
        self.x = x
        self.y = y
        self.radius = np.random.randint(1, 3)
        self.color = color
        self.next = next
        self.prev = prev


# USE THIS METHOD TO DETERMINE IF A GENERATED POINT IS ON AN OBSTACLE
def point_obst_overlap(map, p):
    def is_not_free(x, y):
        overlap = False
        if all(map[y, x] == [0, 0, 0]):
            overlap = True
        return overlap

    mapx, mapy = p.x, p.y

    if is_not_free(mapx, mapy):
        return True    
    return False


def drawLine(p1, p2):
    cv2.line(map, (p1.x, p1.y), (p2.x, p2.y), RED, 1)

def buildMap():

    points_list = [(np.random.randint(10, WIDTH - 10), np.random.randint(10, HEIGHT-10)) for _ in range(NODE_COUNT)]
    list_of_points = []
    for i in range(0, NODE_COUNT):
        v = circles(x = points_list[i][0], y = points_list[i][1])
        cv2.circle(map, (v.x, v.y), v.radius, v.color, thickness=-1)
        list_of_points.append(v)
    
    

    while len(list_of_points) > 2:

        node = list_of_points[np.random.randint(0, len(list_of_points)/2)]
        node_two = list_of_points[np.random.randint(len(list_of_points)/2, len(list_of_points))]
        drawLine(node, node_two)
        list_of_points.remove(node)



buildMap()
cv2.imwrite("neuralNet_red.jpg", map)

