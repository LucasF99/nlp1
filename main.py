import random
import math
import time

wa = {} # word attributes

file = open("port-wiki.txt", "r")
test_string = file.read()
file.close()

print(test_string[0])

word_memory = 10

choice_pool = 300

num_par = 50

min_random = -1
max_random = 1

min_change = 0.85
max_change = 1.15

ord_ignore = [10, ord(','), ord('.')]

def random_list(size = num_par, min = min_random, max = max_random, int_only = False):
    r = []

    for i in range(size):
        if int_only:
            r.append(random.randint(min, max))
        else:
            r.append(random.uniform(min, max))

    return r

def random_change_list(size = num_par, min = min_change, max = max_change, int_only = False):
    r = random_list(size, min, max, int_only)

    for i in range(len(r)):
        if random.uniform(-1,1) <= 0:
            r[i] = -r[i]

    return r

def const_list(size = num_par, val = 0):
    r = [val]*size
    return r

def apply_change(chg, lst):
    r = []
    for i in range(len(chg)):
        r.append(sigmoid(lst[i]*chg[i]))

    return r

def sum_lists(a, b):
    r = []
    for i in range(len(a)):
        r.append(a[i]+b[i])

    return r

def compare_lists(a, b):
    d = 0
    for i in range(len(a)):
        d += (a[i]-b[i])**2

    return d

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def read_string(s):
    current_word = ''
    last_words = []

    i = 0

    while i < len(s):
        
        if s[i] == ' ':

            if current_word in wa:

                if len(last_words) >= 1:
                    wa[current_word] = apply_change(sum_lists(apply_change(const_list(val = 0.1), wa[last_words[-1]]), wa[current_word]), wa[current_word])

                wa[current_word] = apply_change(random_change_list(), wa[current_word])
            else:
                wa[current_word] = random_list()
            current_word = ''

        elif ord(s[i]) in ord_ignore:
            pass
        else:
            current_word += s[i]

        if len(last_words) >= word_memory:
            del(last_words[0])

        last_words.append(current_word)
        i+=1

read_string(test_string)

def generate_sentence(l = 10, pool = choice_pool):
    time_i = time.clock()

    s = ''

    prev_word = random.choice(list(wa.items()))
    s += (prev_word[0] + ' ')

    for i in range(l):
        min_delta = math.inf
        min_word = ('',[0])

        for j in range(pool):
            next_word = random.choice(list(wa.items()))
            delta_iter = compare_lists(prev_word[1], next_word[1])

            if delta_iter < min_delta:
                min_word = next_word
                min_delta = delta_iter

        s += (min_word[0] + ' ')

    print('delta time: ', time.clock()-time_i)

    return s

print(generate_sentence())

#print(str(wa))
