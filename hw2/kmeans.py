# Griffin Solimini (.1)
# CSE 5522
# HW 2 (K-Means)
# Usage: python kmeans.py <training file> <testing file>
# Example: python kmeans.py hw2_training.txt hw2_testing.txt

import random
import math
import sys

# Class describing a k-means vector and its methods
class Vector:
    def __init__(self, i):
        self.i = i
        self.x = random.random() * 100 - 50
        self.y = random.random() * 100 - 50
        self.children = []
    
    def distance(self, p):
        return math.sqrt((self.x - p.x)**2 + (self.y - p.y)**2)

    def adjust(self):
        converged = False

        if len(self.children) == 0:
            self.x = random.random() * 100 - 50
            self.y = random.random() * 100 - 50
            return converged

        avg_x = 0
        avg_y = 0
        for c in self.children:
            avg_x += c.x
            avg_y += c.y

        avg_x /= len(self.children)
        avg_y /= len(self.children)
        
        converged = abs(self.x - avg_x) == 0 and abs(self.y - avg_y) == 0

        self.x = avg_x
        self.y = avg_y

        return converged

# Class describing a k-means point
class Point:
    def __init__(self, c, x, y):
        self.c = c
        self.x = x
        self.y = y
        self.parent = None

# Function that reads training and test data into lists and builds
# a map of class probabilities
def setup(training_filename, testing_filename):
    training_points = []
    testing_points = []
    class_map = {}

    training_file = open(training_filename, 'r')

    for line in training_file:
        point = line.split()
        c = int(point[0])
        x = float(point[1])
        y = float(point[2])

        training_points.append(Point(c, x, y))

        if c in class_map:
            class_map[c] += 1
        else:
            class_map[c] = 0

    training_file.close()

    testing_file = open(testing_filename, 'r')

    for line in testing_file:
        point = line.split()
        c = int(point[0])
        x = float(point[1])
        y = float(point[2])

        testing_points.append(Point(c, x, y))

    testing_file.close()
    
    for i in class_map:
        class_map[i] /= float(len(training_points))

    return (class_map, training_points, testing_points) 

# Function that performs k-means clustering on training data then classifies
# testing data and outputs the error
def classify(k):
    vectors = []
    for i in range(k):
        vectors.append(Vector(i))

    converged = False
    while not converged:

        for v in vectors:
            v.children = []

        for p in training_points:        
            minimum_distance_vector = None
            minimum_distance = float("inf") 
            for v in vectors:
                distance = v.distance(p)
                if distance < minimum_distance:
                    minimum_distance = distance
                    minimum_distance_vector = v
            minimum_distance_vector.children.append(p)
            p.parent = minimum_distance_vector

        converged = True
        for v in vectors:
            if v.adjust() == False:
                converged = False

    table = []
    for i in range(len(class_map)):
        tmp = []
        for j in range(k):
            tmp.append(0)
        table.append(tmp)

    for p in training_points:
        table[p.c][p.parent.i] += 1

    for i in range(len(class_map)):
        for j in range(k):
            table[i][j] /= float(class_map[i])

    classifications = 0
    incorrect = 0
    
    for p in testing_points:
        minimum_distance_vector = None
        minimum_distance = float("inf")
        for v in vectors:
            distance = v.distance(p)
            if distance < minimum_distance:
                minimum_distance = distance
                minimum_distance_vector = v
        
        temp = []
        for i in range(len(class_map)):
            temp.append(class_map[i] * table[i][minimum_distance_vector.i])

        most_probable_class = temp.index(max(temp))
        
        if p.c != most_probable_class:
            incorrect += 1
        classifications += 1

    return float(incorrect) / classifications

# Entry point of python script
if len(sys.argv) != 3:
    print "usage: python kmeans.py <training file> <test file>"
    sys.exit()

class_map, training_points, testing_points = setup(sys.argv[1], sys.argv[2])

# Statistical functions
def mean(data):
    return sum(data) / len(data)

def stddev(data):
    avg = mean(data)
    return sum((x - avg) ** 2 for x in data)

# Error sampling and reporting
k_values = [10, 2, 5, 6, 8, 12, 15, 20, 50]

for k in k_values:
    n = 10
    runs = []
    for i in range(n):
        runs.append(classify(k))

    print "k = " + str(k)
    print "mean: " + str(mean(runs))
    print "std dev: " + str(stddev(runs))
    print

