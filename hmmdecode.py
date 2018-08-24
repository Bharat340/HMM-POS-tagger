import sys, ast, time

start = time.time()
f = open("hmmmodel.txt", "r")
model_data = f.read()
content = model_data.split("\n")

transition_probabilities = ast.literal_eval(content[1])
emission_probabilities = ast.literal_eval(content[3])
state_frequency = ast.literal_eval(content[5])
preceding_state = ast.literal_eval(content[7])
emission_states = ast.literal_eval(content[9])
incoming_states = ast.literal_eval(content[11])
v = len(incoming_states)

testing_file_path = sys.argv[1]
# test_file = open("test.txt", "r")
# test_file = open("en_dev_raw.txt", "r")
test_file = open(testing_file_path, "r")
test_data = test_file.read().split("\n")

'''
TO DO:

'''


def handle_first_word(word, hmm_probabilities):
    index = 0
    if word not in emission_states:  # unknown word
        for state in incoming_states:
            if ("start", state) in transition_probabilities:
                hmm_probabilities[(word, state, index)] = (transition_probabilities[("start", state)], "start")
            else:
                prob = preceding_state["start"] if "start" in preceding_state else 0
                transition_probability = 1 / (prob + v)
                hmm_probabilities[(word, state, index)] = (transition_probability, "start")
        return

    states = emission_states[word]
    for state in states:
        if ("start", state) in transition_probabilities:
            probability = transition_probabilities[("start", state)] * emission_probabilities[(word, state)]
            hmm_probabilities[(word, state, index)] = (probability, "start")
        else:
            prob = preceding_state["start"] if "start" in preceding_state else 0
            transition_probability = 1 / (prob + v)
            probability = transition_probability * emission_probabilities[(word, state)]
            hmm_probabilities[(word, state, index)] = (probability, "start")


def handle_unseen_word(word, previous_word, hmm_probabilities, index):
    max_transition = float(-1)
    back_pointer = None
    for state in incoming_states:
        for s in incoming_states:
            if (previous_word, s, index - 1) in hmm_probabilities:
                if (s, state) in transition_probabilities:
                    p = hmm_probabilities[(previous_word, s, index - 1)][0] * transition_probabilities[(s, state)]
                    if max_transition < p:
                        max_transition = p
                        back_pointer = s
                else: #smoothing
                    prob = preceding_state[s] if s in preceding_state else 0
                    transition_probability = 1 / (prob + v)
                    p = hmm_probabilities[(previous_word, s, index - 1)][0] * transition_probability
                    if max_transition < p:
                        max_transition = p
                        back_pointer = s
        hmm_probabilities[(word, state, index)] = (max_transition, back_pointer)


def tag_word(word, previous_word, hmm_probabilities, index):
    if word not in emission_states:  # unknown word
        handle_unseen_word(word, previous_word, hmm_probabilities, index)
        return

    states = emission_states[word]
    max_transition = float(-1)
    back_pointer = None
    for state in states:
        for s in incoming_states:
            if (previous_word, s, index - 1) in hmm_probabilities:
                if (s, state) in transition_probabilities:
                    p = hmm_probabilities[(previous_word, s, index - 1)][0] * transition_probabilities[(s, state)]
                    if max_transition < p:
                        max_transition = p
                        back_pointer = s
                else: #smoothing
                    prob = preceding_state[s] if s in preceding_state else 0
                    transition_probability = 1 / (prob + v)
                    p = hmm_probabilities[(previous_word, s, index - 1)][0] * transition_probability
                    if max_transition < p:
                        max_transition = p
                        back_pointer = s
        probability = max_transition * emission_probabilities[(word, state)]
        hmm_probabilities[(word, state, index)] = (probability, back_pointer)


def build_tagged_line(words, hmm_probabilities):
    length = len(words)
    tags = []
    last_state = None
    max_prob = -1
    for state in incoming_states:
        if (words[length - 1], state, length - 1) in hmm_probabilities:
            if max_prob < hmm_probabilities[(words[length - 1], state, length - 1)][0]:
                max_prob = hmm_probabilities[(words[length - 1], state, length - 1)][0]
                last_state = state
    tags.append(last_state)
    i = length - 2
    while i >= 0:
        hmm_value = hmm_probabilities[(words[i + 1], last_state, i + 1)]
        last_state = hmm_value[1]
        tags.append(hmm_value[1])
        i -= 1
    tags = list(reversed(tags))
    if length != len(tags):
        print "Error in tags and words length"
        return ""
    tagged_line = ""
    i = 0
    while i < length:
        tagged_line += words[i] + "/" + tags[i]
        if i != length - 1:
            tagged_line += " "
        i += 1
    return tagged_line


def process_test_data():
    tagged_data = ""
    total_lines = len(test_data)
    i = 0
    while i < total_lines:
        hmm_probabilities = dict()
        words = test_data[i].split(" ")
        length = len(words)
        if length > 0:
            handle_first_word(words[0], hmm_probabilities)
            j = 1
            while j < length:
                tag_word(words[j], words[j - 1], hmm_probabilities, j)
                j += 1
        # print hmm_probabilities
        tagged_line = build_tagged_line(words, hmm_probabilities)
        tagged_data += tagged_line
        if i != total_lines:
            tagged_data += "\n"
        i += 1
    return tagged_data


f_out = open("hmmoutput.txt", "w")
f_out.write(process_test_data())
f_out.close()
test_file.close()
f.close()
print "Total time taken: ", (time.time() - start)

