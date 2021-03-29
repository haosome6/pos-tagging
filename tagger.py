# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys


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


def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE
    #
    end_puncs = [".", "!", "?"]
    init_table = {}
    transit_table = {}
    emit_table = {}

    # Training process
    for file_name in training_list:
        last_word = "."  # init as period makes the first word as start
        cur_word = ""
        last_pos = cur_pos = None

        f = open(file_name)
        lines = f.readlines()

        for line in lines:

            last_word, last_pos = cur_word, cur_pos
            cur_word, cur_pos = line.split(" : ")

            if last_word in end_puncs and cur_word not in end_puncs:
                increment_table_count(cur_pos, init_table)
            increment_table_count((last_pos, cur_pos), transit_table)
            increment_table_count((cur_word, cur_pos), emit_table)

    init_count = sum(init_table.values())
    for pos in init_table:
        init_table[pos] = init_table[pos] / init_count
    update_conditional_table(transit_table, 0)
    update_conditional_table(emit_table, 1)


if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[
                    parameters.index("-d") + 1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t") + 1]
    output_file = parameters[parameters.index("-o") + 1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag(training_list, test_file, output_file)
