# Griffin Solimini(.1)
# CSE 5522
# Stump Classifier and AdaBoost
#
#  Usage: 
#  python classifier.py <attribute file> <training file> <testing file>
#  
#  Example: 
#  python classifier.py game_attributes.txt game_attrdata_train.dat game_attrdata_test.dat

import math
import pdb
import sys
import copy

# represents a node of the decision tree
class Node:
    def __init__(self):
        self.entries = []
        self.weights = []
    
    # calculates total weight 
    def total_weight(self):
        weight = 0
        for i in range(len(self.weights)):
            weight += self.weights[i]

        return weight
    
    # calculate entropy of a node
    def entropy(self):
        ratio_a = self.prob_apples()
        ratio_s = self.prob_setters()
        return -ratio_a * math.log(ratio_a, 2) - ratio_s * math.log(ratio_s, 2)
   
    # split parent node into children given a category
    def split(self, question):
        children = {}
        for attribute in attribute_map[question]:
            child = Node()
            for i in range(len(self.entries)):
                entry = self.entries[i]
                if entry.attr[question] == attribute:
                    child.entries.append(entry)
                    child.weights.append(self.weights[i])
            children[attribute] = child

        return children
    
    # calculate the gain of a split
    def gain(self, question):
        info_gain = self.entropy()
        split_dict = self.split(question)
        for split in split_dict:
            child = split_dict[split]

            info_gain -= child.total_weight() / self.total_weight() * child.entropy()
        
        return info_gain
    
    # determine the best split and make a stump classifier
    def best_classifier(self):
        maximum_gain = 0
        category = None
        for key in attribute_map:
            if key != 'game':
                gain = self.gain(key)
                #  print key + " " + str(gain)
                if gain > maximum_gain:
                    maximum_gain = gain
                    category = key
        
        return Classifier(category, self.split(category))
    
    # normalize the weights
    def normalize(self):
        total = sum(self.weights)
        for i in range(len(self.weights)):
            self.weights[i] /= total
    
    # probability distribution of apples
    def prob_apples(self):
        num_apples = 0.0
        for i in range(len(self.entries)):
            if self.entries[i].attr["game"] == "ApplesToApples":
                num_apples += 1.0 * self.weights[i]

        return num_apples / self.total_weight()
    
    # probability distribution of setters
    def prob_setters(self):
        num_setters = 0.0
        for i in range(len(self.entries)):
            if self.entries[i].attr["game"] == "SettersOfCatan":
                num_setters += 1.0 * self.weights[i]

        return num_setters / self.total_weight() 

# class that describes a stump classifier
class Classifier:
    def __init__(self, category, splits):
        self.category = category
        self.splits = splits
    
    # classify an entry
    def classify(self, entry):
        classifying_node = self.classifyingNode(entry)

        if classifying_node.prob_apples() >= classifying_node.prob_setters():
            return "ApplesToApples"
        else:
            return "SettersOfCatan"
    
    # return the classifying node of an entry
    def classifyingNode(self, entry):
        attribute = entry.attr[self.category]
        return self.splits[attribute]

# class describing a singular test/train entry
class Entry:
    def __init__(self, weight, dayOfWeek, timeOfDay, 
            timeToPlay, mood, friendsVisiting, 
            kidsPlaying, atHome, snacks, game):
        
        self.attr = {}
        self.attr["dayOfWeek"] = dayOfWeek
        self.attr["timeOfDay"] = timeOfDay
        self.attr["timeToPlay"] = timeToPlay
        self.attr["mood"] = mood
        self.attr["friendsVisiting"] = friendsVisiting
        self.attr["kidsPlaying"] = kidsPlaying
        self.attr["atHome"] = atHome
        self.attr["snacks"] = snacks
        self.attr["game"] = game

# function that runs the adaboost algorithm with K iterations
def adaboost(K):
    N = len(node.entries)
    for i in range(len(node.entries)):
        node.weights[i] = 1.0 / N

    h = []
    z = []
    for k in range(K):
        classifier = node.best_classifier()
       
        # determine error
        error = 0.0
        for i in range(len(node.entries)):
            entry = node.entries[i]
            if classifier.classify(entry) != entry.attr["game"]:
                error += node.weights[i] 
        
        # update weights
        for i in range(len(node.entries)):
            entry = node.entries[i]
            if classifier.classify(entry) == entry.attr["game"]:
                node.weights[i] *= (error / (1 - error))
        
        node.normalize()
        
        h.append(classifier) 
        z.append(math.log((1-error) / error))
    
    # classify test data
    correct = 0.0
    total = 0.0
    for entry in test_data:
        # "vote" with weighted hypothesis
        class_score = 0
        for k in range(K):
            k_class = h[k].classify(entry)
            class_score += z[k] if k_class == "ApplesToApples" else -z[k]
       
        # classify
        if class_score >= 0:
            if entry.attr["game"] == "ApplesToApples":
                correct += 1
        else:
            if entry.attr["game"] == "SettersOfCatan":
                correct += 1

        total += 1

    print("adaboost accuracy for K=" + str(K) + ": " + str(correct / total))

if len(sys.argv) != 4:
    print "usage: classifier.py <attribute file> <training file> <testing file>"
    sys.exit()

# build attribute map
attribute_file = open(sys.argv[1], 'r')

attribute_map = {}
for line in attribute_file:
    attribute = line.split(':')
    
    tmp = []
    for token in attribute[1].split(','):
        tmp.append(token.strip())
    attribute_map[attribute[0]] = tmp

attribute_file.close()

# input training data
training_file = open(sys.argv[2], 'r')
node = Node()
for line in training_file:
    tmp = line.strip().split(',')
    entry = Entry(1.0,tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8])
    node.entries.append(entry)
    node.weights.append(1.0)

N = len(node.weights)
for i in range(len(node.weights)):
    node.weights[i] = 1.0 / N

training_file.close()

# input testing data
testing_file = open(sys.argv[3], 'r')
test_data = []
for line in testing_file:
    tmp = line.strip().split(',')
    entry = Entry(0.0,tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8])
    test_data.append(entry)

testing_file.close()

# test stump classifier
correct = 0
classifier = node.best_classifier()
avg_prob = 0
for entry in test_data:
    if entry.attr["game"] == "ApplesToApples":
        avg_prob += classifier.classifyingNode(entry).prob_apples()
    else:
        avg_prob += classifier.classifyingNode(entry).prob_setters()


    if classifier.classify(entry) == entry.attr["game"]:
        correct += 1

print "decision stump accuracy: " + str(correct / float(len(test_data)))
print "decision stump average probability: " + str(avg_prob / float(len(test_data)))
print

# test adaboost
K = [2, 3, 4, 5]
for k in K:
    adaboost(k)
    
