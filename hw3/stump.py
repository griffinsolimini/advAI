import math

class Node:
    def __init__(self):
        self.entries = []
    
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
            info_gain -= float(len(child.entries)) / len(self.entries) * child.entropy()

        return info_gain

    def bestSplit(self):
        maximum_gain = 0
        category = None
        for key in attribute_map:
            if key != 'game':
                gain = self.gain(key)
                if gain > maximum_gain:
                    maximum_gain = gain
                    category = key

        return (category, self.split(category))
    
    def prob_apples(self):
        num_apples = 0
        for entry in self.entries:
            if entry.attr["game"] == "ApplesToApples":
                num_apples += 1
        return float(num_apples) / len(self.entries)

    def prob_setters(self):
        num_setters = 0
        for entry in self.entries:
            if entry.attr["game"] == "SettersOfCatan":
                num_setters += 1
        return float(num_setters) / len(self.entries)

class Entry:
    def __init__(self, dayOfWeek, timeOfDay, 
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

attribute_file = open('game_attributes.txt', 'r')

attribute_map = {}
for line in attribute_file:
    attribute = line.split(':')
    
    tmp = []
    for token in attribute[1].split(','):
        tmp.append(token.strip())
    attribute_map[attribute[0]] = tmp

attribute_file.close()

training_file = open('game_attrdata_train.dat', 'r')

node = Node()

for line in training_file:
    tmp = line.strip().split(',')
    entry = Entry(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8])
    node.entries.append(entry)

training_file.close()

classifier = node.bestSplit()

testing_file = open('game_attrdata_test.dat', 'r')

correct = 0
total = 0
for line in testing_file: 
    tmp = line.strip().split(',')
    entry = Entry(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8])
    
    attribute = entry.attr[classifier[0]]
    classifying_node = classifier[1][attribute]
    
    if classifying_node.prob_apples() > classifying_node.prob_setters():
        if entry.attr["game"] == "ApplesToApples":
            correct += 1
    else:
        if entry.attr["game"] == "SettersOfCatan":
            correct += 1
    
    total += 1

print 100.0 * correct / total

