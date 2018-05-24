import random
import math
import time

wa = {} # word attributes

file = open("port-wiki.txt", "r")
test_string = file.read()
file.close()

print(test_string[0])

avg_delta_val = 0.60

word_memory = 10

choice_pool = 120

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

CONST_LIST_0_1 = const_list(val = 0.1)
CONST_LIST_1 = const_list(val = 1)
CONST_LIST_0_05 = const_list(val = 0.05)
CONST_LIST_NEG1 = const_list(val = -1)

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
    d = math.sqrt(d)
    return d

def inverse_list(a):
    r = []
    for i in a:
        r.append(1/i)

    return r

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def avg_delta():
    d = 0
    l = len(list(wa.items()))
    for i in range(l):
        i1 = random.choice(list(wa.items()))
        i2 = random.choice(list(wa.items()))
        d += compare_lists(i1[1], i2[1])

    d = d/l
    return d

change_list_1 = random_change_list()

def read_string(s):
    current_word = ''
    last_words = []

    last_delta = avg_delta_val

    n = 0

    while n < len(s):

        if s[n] == ' ':

            meta_change_list = random_change_list()
            change_list = change_list_1
            change_list = apply_change(meta_change_list, change_list)

            if current_word in wa:

                if len(last_words) >= 1:
                    wa[current_word] = apply_change(sum_lists(apply_change(CONST_LIST_0_1, apply_change(change_list, wa[last_words[-1]])), CONST_LIST_1), wa[current_word])
                if len(last_words) >= 2:
                    wa[current_word] = apply_change(sum_lists(apply_change(CONST_LIST_0_05, apply_change(change_list, wa[last_words[-2]])), CONST_LIST_1), wa[current_word])

                #wa[current_word] = apply_change(random_change_list(), wa[current_word])
            else:
                wa[current_word] = random_list()

                if len(last_words) >= 1:
                    wa[current_word] = apply_change(sum_lists(apply_change(CONST_LIST_0_1, apply_change(change_list, wa[last_words[-1]])), CONST_LIST_1), wa[current_word])
                if len(last_words) >= 2:
                    wa[current_word] = apply_change(sum_lists(apply_change(CONST_LIST_0_05, apply_change(change_list, wa[last_words[-2]])), CONST_LIST_1), wa[current_word])

            last_words.append(current_word)

            current_word = ''

            # learning

            if len(last_words) >= 2:
                curr_delta = compare_lists(wa[last_words[-1]], wa[last_words[-2]])
                if curr_delta > last_delta:
                    meta_change_list = inverse_list(meta_change_list)
                    change_list = apply_change(meta_change_list, change_list)
                    change_list = apply_change(meta_change_list, change_list)

                last_delta = curr_delta

        elif ord(s[n]) in ord_ignore:
            pass
        else:
            current_word += s[n]

        if len(last_words) >= word_memory:
            del(last_words[0])



        n+=1

read_string(test_string)

def generate_sentence(l = 10, pool = choice_pool):
    time_i = time.clock()

    s = ''

    prev_words = []
    prev_words.append(random.choice(list(wa.items())))
    s += (prev_words[0][0] + ' ')

    total_delta = 0

    for i in range(l):
        min_delta = math.inf
        min_word = ('',[0])

        for j in range(pool):
            next_word = random.choice(list(wa.items()))

            delta_iter = []
            delta_sum = 0

            for k in range(len(prev_words)):
                delta_iter.append(compare_lists(prev_words[k][1], next_word[1]))
            for k in range(len(delta_iter)):
                delta_sum += delta_iter[k]

            delta_mean = delta_sum/(len(delta_iter))

            if delta_mean < min_delta:
                min_word = next_word
                min_delta = delta_mean

        total_delta += min_delta

        if len(prev_words) >= word_memory:
            prev_words.pop(0)
        prev_words.append(min_word)

        s += (min_word[0] + ' ')

    total_delta = total_delta/l

    print('delta time: ', time.clock()-time_i)
    print('total delta: ', total_delta)

    return s

print(generate_sentence(l = 15))

#print(str(wa))
