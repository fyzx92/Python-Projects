#
# Authored by Bryce Burgess
#
# L system with two characters, a and b
#

from random import random as rand

def apply_axioms1(string_in, iter = 1):
    for i in range(iter):
        string_out = ""
        for c in string_in:
            if c == "a":
                string_out += "ab"
            elif c == "b":
                string_out += "a"
        string_in = string_out
    return string_out

def apply_axioms2(string_in, iter = 1, probA = 0.8, probB = 0.95):
    for i in range(iter):
        string_out = ""
        for c in string_in:
            if c == "a":
                if rand() < probA:
                    string_out += "ab"
            elif c == "b":
                if rand() < probB:
                    string_out += "a"
        string_in = string_out
    return string_out

def gen_start_str (method = "simple", input_str = None, str_length = 3, char_list = ["a","b"]):
    char_list = list(set(char_list))
    valid_input = [False]*len(input_str)
    for i in input_str:
        for j in char_list:
            if i == j:
                valid_input[i] = True

    if all(valid_input):
        start_str = input_str
    else:
        if method == "simple":
            start_str = "aaabbb"

        if method == "random":
            start_str = ""
            for i in range(str_length):
                next_char = "a"
                if rand() < 0.5:
                    next_char = "b"
                start_str += next_char

        if method == "manual":
            start_str = str(input("please enter a string of valid characters: " + str(char_list) + "\n"))

    return start_str


string = gen_start_str()
for i in range(20):
    print(string)
    string = apply_axioms1(string)
