import sys, time

training_file_path = sys.argv[1]
# training_file_path = "en_train_tagged.txt"
# training_file_path = "zh_train_tagged.txt"
training_file = open(training_file_path, "r")
training_data = training_file.read()

state_frequency = dict()
preceding_state = dict()
transition_probabilities = dict()
emission_probabilities = dict()
emission_states = dict()
states = set()


def each_line_processing(line):
    elements = line.split(" ")
    i, length = 0, len(elements)
    if 0 == length:
        return

    start_part = elements[0].rsplit("/", 1)
    if len(start_part) < 2:
        return
    tag0 = start_part[1]
    preceding_state["start"] += 1
    # handling transition frequency for first state
    if ("start", tag0) in transition_probabilities:
        transition_probabilities[("start", tag0)] += 1
    else:
        transition_probabilities[("start", tag0)] = 1

    states_index = len(states)
    while i < length:
        first_parts = elements[i].rsplit("/", 1)
        tag1 = first_parts[1]
        # state frequency
        if tag1 in state_frequency:
            state_frequency[tag1] += 1
        else:
            state_frequency[tag1] = 1

        # unique states
        if tag1 not in states:
            states.add(tag1)

        # next element
        if i == (length - 1):
            tag2 = "end"
        else:
            second_parts = elements[i+1].rsplit("/", 1)
            tag2 = second_parts[1]
            if tag1 in preceding_state:
                preceding_state[tag1] += 1
            else:
                preceding_state[tag1] = 1
        # transition probability
        if (tag1, tag2) in transition_probabilities:
            transition_probabilities[(tag1, tag2)] += 1
        else:
            transition_probabilities[(tag1, tag2)] = 1

        #emission probability
        if (first_parts[0], tag1) in emission_probabilities:
            emission_probabilities[(first_parts[0], tag1)] += 1
        else:
            emission_probabilities[(first_parts[0], tag1)] = 1

        #emission states
        if first_parts[0] in emission_states:
            emission_states[first_parts[0]].add(tag1)
        else:
            emission_states[first_parts[0]] = set()
            emission_states[first_parts[0]].add(tag1)

        i += 1


def process_training_data():
    state_frequency["end"] = 1
    preceding_state["start"] = 0
    for line in training_data.split("\n"):
        line = line.rstrip()
        each_line_processing(line)


def evaluate_probabilities():
    v = len(states)
    for key, value in transition_probabilities.iteritems():
        if "end" == key[1]:
            continue
        denominator = preceding_state[key[0]] + v
        transition_probabilities[key] = (transition_probabilities[key] + 1) / float(denominator)
    for key, value in emission_probabilities.iteritems():
        denominator = state_frequency[key[1]]
        emission_probabilities[key] /= float(denominator)
    for key, value in emission_states.iteritems():
        emission_states[key] = list(emission_states[key])


start = time.time()
process_training_data()
evaluate_probabilities()
states = list(states)

f = open("hmmmodel.txt", "w")
f.write("Transition_probabilities\n")
f.write(repr(transition_probabilities) + "\n")
f.write("Emission_probabilities\n")
f.write(repr(emission_probabilities) + "\n")
f.write("State_frequency\n")
f.write(repr(state_frequency) + "\n")
f.write("Preceding_state\n")
f.write(repr(preceding_state) + "\n")
f.write("Emission states\n")
f.write(repr(emission_states) + "\n")
f.write("Unique states\n")
f.write(repr(states) + "\n")
f.close()


# print len(transition_probabilities), len(emission_probabilities), len(state_frequency), len(preceding_state)
# print "Total time taken", (time.time() - start)

training_file.close()

