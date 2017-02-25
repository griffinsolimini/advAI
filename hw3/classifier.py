import math
import pdb
import sys

class Node:
    def __init__(self):
        self.entries = []

    def total_weight(self):
        weight = 0
        for entry in self.entries:
            weight += entry.attr["weight"]
        
        return weight
    
    def entropy(self):
        ratio_a = self.prob_apples()
        ratio_s = self.prob_setters()
        return -ratio_a * math.log(ratio_a, 2) - ratio_s * math.log(ratio_s, 2)
    
    def split(self, question):
        children = {}
        for attribute in attribute_map[question]:
            child = Node()
            for entry in self.entries:
                if entry.attr[question] == attribute:
                    child.entries.append(entry)
            children[attribute] = child

        return children

    def gain(self, question):
        info_gain = self.entropy()
        split_dict = self.split(question)
        for split in split_dict:
            child = split_dict[split]

            info_gain -= child.total_weight() / self.total_weight() * child.entropy()
        
        return info_gain
    
    def best_classifier(self):
        maximum_gain = 0
        category = None
        for key in attribute_map:
            if key != 'game':
                gain = self.gain(key)
                if gain > maximum_gain:
                    maximum_gain = gain
                    category = key
        
        return Classifier(category, self.split(category))
   
    def prob_apples(self): 
        num_apples = 0
        for entry in self.entries:
            if entry.attr["game"] == "ApplesToApples":
                num_apples += entry.attr["weight"]
        return num_apples / self.total_weight() 

    def prob_setters(self):
        num_setters = 0
        for entry in self.entries:
            if entry.attr["game"] == "SettersOfCatan":
                num_setters += entry.attr["weight"]
        return num_setters / self.total_weight()
    
    def normalize(self): 
        total = 0
        for x in self.entries:
            total += x.attr["weight"]
        for i in range(len(self.entries)):
            self.entries[i].attr["weight"] /= total

class Classifier:
    def __init__(self, category, splits):
        self.category = category
        self.splits = splits

    def classify(self, entry):
        classifying_node = self.classifyingNode(entry) 
        if classifying_node.prob_apples() >= classifying_node.prob_setters():
            return "ApplesToApples"
        else:
            return "SettersOfCatan"

    def classifyingNode(self, entry):
        attribute = entry.attr[self.category]
        return self.splits[attribute]

class Entry:
    def __init__(self, weight, dayOfWeek, timeOfDay, 
            timeToPlay, mood, friendsVisiting, 
            kidsPlaying, atHome, snacks, game):
        
        self.attr = {}
        self.attr["weight"] = weight
        self.attr["dayOfWeek"] = dayOfWeek
        self.attr["timeOfDay"] = timeOfDay
        self.attr["timeToPlay"] = timeToPlay
        self.attr["mood"] = mood
        self.attr["friendsVisiting"] = friendsVisiting
        self.attr["kidsPlaying"] = kidsPlaying
        self.attr["atHome"] = atHome
        self.attr["snacks"] = snacks
        self.attr["game"] = game

def adaboost(K):
    N = len(node.entries)
    for entry in node.entries:
        entry.attr["weight"] = 1.0 / N

    h = []
    z = []
    for k in range(K):
        classifier = node.best_classifier()
        
        for split in classifier.splits:
            print split + " " + str(classifier.splits[split].prob_setters())

        error = 0.0
        for entry in node.entries:
            if classifier.classify(entry) != entry.attr["game"]:
                error += entry.attr["weight"]

        for entry in node.entries:
            if classifier.classify(entry) == entry.attr["game"]:
                entry.attr["weight"] = entry.attr["weight"] * (error / (1 - error))
        
        node.normalize()
        
        h.append(classifier) 
        z.append(math.log((1-error) / error))

    for hyp in h:
        print hyp.category
    print z

    correct = 0
    total = 0
    for entry in test_data:
        class_score = 0
        for k in range(K):
            k_class = h[k].classify(entry)
            class_score += z[k] if k_class == "ApplesToApples" else -z[k]

        if class_score >= 0:
            if entry.attr["game"] == "ApplesToApples":
                correct += 1
        else:
            if entry.attr["game"] == "SettersOfCatan":
                correct += 1

        total += 1

    print("adaboost accuracy for K=" + str(K) + ": " + str(100.0 * correct / total))

if len(sys.argv) != 4:
    print "usage: classifier.py <attribute file> <training file> <testing file>"
    sys.exit()

attribute_file = open(sys.argv[1], 'r')

attribute_map = {}
for line in attribute_file:
    attribute = line.split(':')
    
    tmp = []
    for token in attribute[1].split(','):
        tmp.append(token.strip())
    attribute_map[attribute[0]] = tmp

attribute_file.close()

training_file = open(sys.argv[2], 'r')
node = Node()
for line in training_file:
    tmp = line.strip().split(',')
    entry = Entry(1.0,tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8])
    node.entries.append(entry)

N = len(node.entries)
for entry in node.entries:
    entry.attr["weight"] = 1.0 / N

training_file.close()

testing_file = open(sys.argv[3], 'r')
test_data = []
for line in testing_file:
    tmp = line.strip().split(',')
    entry = Entry(0.0,tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8])
    test_data.append(entry)

testing_file.close()

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

#  K = [2, 3, 4, 5]
K = [2]
for k in K:
    adaboost(k)
    
