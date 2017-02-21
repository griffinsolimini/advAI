import sys

if len(sys.argv) != 3:
    print "usage: python bayesclassifier.py <training file> <test file>"
    sys.exit()

training_file = open(sys.argv[1], 'r')

poisonous = [dict() for x in range(22)]
edible = [dict() for x in range(22)]

for line in training_file:
    
    pos = -1
    poisonous_flag = True

    line = line.strip().split(',')
    for token in line:
        if pos == -1:
            if token == 'p':
                poisonous_flag = True
            elif token == 'e':
                poisonous_flag = False
        else:
            if poisonous_flag:
                if token in poisonous[pos].keys():
                    poisonous[pos][token] += 1
                else:
                    poisonous[pos][token] = 1
            elif not poisonous_flag:
                if token in edible[pos].keys():
                    edible[pos][token] += 1
                else:
                    edible[pos][token] = 1
        pos += 1

num_poisonous = 0
for key in poisonous[0].keys():
    num_poisonous += poisonous[0][key]

num_edible = 0
for key in edible[0].keys():
    num_edible += edible[0][key]

prob_poisonous = float(num_poisonous) / float(num_poisonous + num_edible)
prob_edible = float(num_edible) / float(num_poisonous + num_edible)

training_file.close()

testing_file = open(sys.argv[2], 'r')

correct = 0
guesses = 0

for line in testing_file:
    pos = -1
    poisonous_flag = True
    
    prob_poisonous_est = prob_poisonous
    prob_edible_est = prob_edible

    line = line.strip().split(',')
    for token in line:
        
        if pos == -1:
            if token == 'p':
                poisonous_flag = True
            elif token == 'e':
                poisonous_flag = False
        else:
            if token in poisonous[pos].keys():
                prob_poisonous_est *= float(poisonous[pos][token]) / num_poisonous
            else:
                prob_poisonous_est *= 0

            if token in edible[pos].keys():
                prob_edible_est *= float(edible[pos][token]) / num_edible
            else:
                prob_edible_est *= 0
            
        pos += 1
   
    norm_poisonous = prob_poisonous_est / (prob_poisonous_est + prob_edible_est)
    norm_edible = prob_edible_est / (prob_poisonous_est + prob_edible_est)

    print str(guesses) + ": P: " + str(round(norm_poisonous, 5)) + " E: " + str(round(norm_edible, 5))

    guesses += 1 
    if (prob_poisonous_est >= prob_edible_est and poisonous_flag) or (prob_poisonous_est < prob_edible_est and not poisonous_flag):
        correct += 1

testing_file.close()

print
print "the classifier was " + str(100.0 * correct / guesses) + "% correct"

