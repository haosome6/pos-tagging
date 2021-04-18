import os
import sys

all_pos = []  # all pos ever seen in training process


def increment_table_count(key, table, increment_by=1):
    if key in table:
        table[key] += increment_by
    else:
        table[key] = increment_by


def update_conditional_table(table, sum_over_idx):
    """Calculate conditional probability by the count in <table>.
    <sum_over_idx> indicates which variable in the condition(table's key)
    should be summed over.
    """
    count = {}
    for condition, times in table.items():
        increment_table_count(condition[sum_over_idx], count, times)
    for condition in table:
        table[condition] = table[condition] / count[condition[sum_over_idx]]


def normalize_state_table(state_table):
    """This is a helper function for test_sentence(). It normalize the given
    state probability table to avoid the probability goes zero after serval
    computations.
    """
    total = 0
    for p in state_table.values():
        total += p[0]
    for state in state_table:
        state_table[state][0] = state_table[state][0] / total


def test_sentence(sentence, init_table, transit_table, emit_table):
    """Given a sentence as a list, where each element is a word. Using three
    tables to test the POS of the sentence. Return a list of POSs.
    """
    weight = 0.0000001  # Replace for missing probability
    curr_p = {}
    for i in range(len(sentence)):
        word = sentence[i].lower()
        if i == 0:
            for pos in all_pos:
                if pos in init_table and (word, pos) in emit_table:
                    curr_p[pos] = \
                        [init_table[pos] * emit_table[(word, pos)], [pos]]
                elif pos in init_table:
                    curr_p[pos] = [init_table[pos] * weight, [pos]]
                elif (word, pos) in emit_table:
                    curr_p[pos] = [emit_table[(word, pos)] * weight, [pos]]
        else:
            prev_p = curr_p
            curr_p = {}
            for pos in all_pos:
                max_prob = 0
                max_path = []
                for last_pos, p in prev_p.items():
                    if (last_pos, pos) in transit_table \
                            and (word, pos) in emit_table:
                        prob = p[0] * transit_table[(last_pos, pos)] * \
                               emit_table[(word, pos)]
                    elif (last_pos, pos) in transit_table:
                        prob = p[0] * transit_table[(last_pos, pos)] * weight
                    elif (word, pos) in emit_table:
                        prob = p[0] * emit_table[(word, pos)] * weight
                    if prob > max_prob:
                        max_prob = prob
                        max_path = p[1].copy()
                if max_prob != 0:
                    max_path.append(pos)
                    curr_p[pos] = [max_prob, max_path]
        normalize_state_table(curr_p)

    max_prob = 0
    result_path = []
    for p in curr_p.values():
        if p[0] > max_prob:
            max_prob = p[0]
            result_path = p[1]
    return result_path


def tag(training_list, test_file, output_file):
    print("Tagging the file.")

    end_puncs = [".", "!", "?"]
    init_table = {}
    transit_table = {}
    emit_table = {}

    # Training process
    for file_name in training_list:
        cur_word = "."
        cur_pos = None

        f = open(file_name)
        lines = f.readlines()

        for line in lines:
            # remove '\n'
            line = line[:-1]

            last_word, last_pos = cur_word, cur_pos
            cur_word, cur_pos = line.split(" : ")
            cur_word = cur_word.lower()
            if cur_pos not in all_pos:
                all_pos.append(cur_pos)

            if last_word in end_puncs and cur_word not in end_puncs:
                increment_table_count(cur_pos, init_table)
            increment_table_count((last_pos, cur_pos), transit_table)
            increment_table_count((cur_word, cur_pos), emit_table)

        f.close()

    init_count = sum(init_table.values())
    for pos in init_table:
        init_table[pos] = init_table[pos] / init_count
    update_conditional_table(transit_table, 0)
    update_conditional_table(emit_table, 1)

    # Testing process, and write to output file
    f = open(test_file)
    output_f = open(output_file, "w")
    lines = f.readlines()
    sentence = []
    for line in lines:
        line = line[:-1]
        sentence.append(line)
        if line in end_puncs:
            result = test_sentence(sentence, init_table, transit_table,
                                   emit_table)
            for i in range(len(sentence)):
                output_f.writelines([sentence[i], " : ", result[i], "\n"])
            sentence = []
    f.close()
    output_f.close()


if __name__ == '__main__':
    print("Starting the tagging process.")

    parameters = sys.argv
    training_list = parameters[
                    parameters.index("-d") + 1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t") + 1]
    output_file = parameters[parameters.index("-o") + 1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    tag(training_list, test_file, output_file)
