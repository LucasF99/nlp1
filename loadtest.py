import random

a = []

r = 100

for i in range(r):
    a.append([])
    for j in range(r):
        a[i].append([])
        for k in range(r):
            a[i][j].append(random.uniform(-10,10))

t = 10000

for i in range(t):
    k = a[random.randint(0, len(a)-1)][random.randint(0, len(a[0])-1)][random.randint(0, len(a[0][0])-1)]
    a[random.randint(0, len(a)-1)][random.randint(0, len(a[0])-1)][random.randint(0, len(a[0][0])-1)] = k
    print('',i)
