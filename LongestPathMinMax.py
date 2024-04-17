import copy
import random
import time
import math
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:05:46 2021

@author: hakan
"""
FILENAME = "bigmapLongestPath.txt"
OUTFILE = 'firstLPMM.txt'
BIGNUM = 1000000000
BIGOUTFILE = 'customers1000.txt'
CUSTOMER_NUM = 1000
original_nodeweights = dict()
original_edges = dict()


def convert(print_path):
    converted_path = [1 for i in range(60)]
    for i in range(1, len(print_path)-1):
        j_day = (print_path[i]-2)//12
        j_action = print_path[i-1] % 12
        if j_action == 0:
            j_action = 12
        converted_path[j_day] = j_action
    return converted_path


def longest_path(max_w2):  # here we try to find the longest path, without passing the minmax limit
    weights = {}
    for j in range(1, nodenum+1):
        weights[j] = -1*BIGNUM
    weights[end] = 0
    new_max_w2 = -1
    parents = [-1 for i in range(nodenum+1)]
    for j in range(nodenum, 0, -1):
        if nodeweights[j] < max_w2:
            if nodeweights[j] > new_max_w2:
                new_max_w2 = nodeweights[j]
            for k in revadj[j]:
                if nodeweights[k] < max_w2:
                    if nodeweights[k] > new_max_w2:
                        new_max_w2 = nodeweights[k]
                    if weights[k] < weights[j]+edges[k, j]:
                        weights[k] = weights[j]+edges[k, j]
                        parents[k] = j
    return new_max_w2, parents, weights[start]

    
def first_pass(nodeweights):  # here we do the first pass traversal on the graph, to find the MINMAX value
    priority_q = []
    weights = {}
    for j in range(1, nodenum+1):
        weights[j] = BIGNUM
    weights[end] = 0
    priority_q.append(end)
    pivot = end
    visited = [1 for i in range(nodenum+1)]
    visited[pivot] = 0
    visited[0] = 0
    is_it_done = 1
    while priority_q and is_it_done:
        pivot = 0
        for j in range(len(priority_q)):  # selects the minimum of the priority queue as pivot
            if weights[priority_q[j]] < weights[priority_q[pivot]]:
                pivot = j
        pivot = priority_q.pop(pivot)
        visited[pivot] = 0
        for j in revadj[pivot]:
            # passing through reverse adjacency list of the pivot, doing relaxation and pushing to priority queue
            if max(nodeweights[j], weights[pivot]) < weights[j]:
                weights[j] = max(nodeweights[j], weights[pivot])
                priority_q.append(j)
        if priority_q:
            k = 0
            for j in range(len(priority_q)):
                if weights[priority_q[k]] > weights[priority_q[j]]:
                    k = j
            priority_q[0], priority_q[k] = priority_q[k], priority_q[0]
        is_it_done = 0
        for t in range(nodenum+1):
            if visited[t]:
                is_it_done = 1
    return weights[start]


def reading():  # here we read the map from the file
    f = open(FILENAME)
    str1 = f.readline()
    str2 = str1.split(",")
    adjacency = {}
    revadj = {}
    nodenum = eval(str2[0])
    edgenum = eval(str2[1])
    start = eval(str2[2])
    end = eval(str2[3])
    edges = {}
    labelnums = {}
    nodeweights = {}
    for i in range(nodenum):
        adjacency[i+1] = []
        revadj[i+1] = []
        labelnums[i+1] = 0
        str1 = f.readline()
        str2 = str1.split(",")
        a = eval(str2[0])
        b = eval(str2[1])
        nodeweights[a] = b
    for i in range(edgenum):
        str1 = f.readline()
        str2 = str1.split(",")
        a = eval(str2[0])
        b = eval(str2[1])
        c = eval(str2[2])
        edges[a, b] = -c
        adjacency[a].append(b)
        revadj[b].append(a)
    f.close()
    for i in nodeweights.keys():
        original_nodeweights[i] = nodeweights[i]
    for i in edges.keys():
        original_edges[i] = edges[i]
    return nodenum, edgenum,  edges, start, end, adjacency, labelnums, revadj, nodeweights


def new_weights(nodeweight, edges):
    newnodeweights = dict()
    for i in nodeweight.keys():
        randseed = random.randint(10, 20)
        newnodeweights[i] = nodeweight[i]*random.randrange(100-randseed, 100+randseed)/1000
    newedges = {}
    for i, j in edges.keys():
        randseed = random.randint(10, 20)
        newedges[i, j] = edges[i, j]*random.randrange(100-randseed, 100+randseed)/1000
    return newnodeweights, newedges


# reading from the file
t1 = time.time()
nodenum, edgenum,  edges, start, end, adjacency, labelnums, revadj, nodeweights= reading()
# above are the global variables

# below is the first pass to find MINMAX
minW2 = first_pass(nodeweights)

paths = list()
max_w2 = BIGNUM
while max_w2 >= minW2:
    max_w2, path, lp = longest_path(max_w2)
    if abs(lp) >= BIGNUM/10:
        continue
    #print(lp, math.exp(-1*lp))
    paths.append([math.exp(-1*lp), max_w2, path])
if paths[-1][1] == 0:
    del(paths[-1])
isunique = [1 for i in range(len(paths))]
for i in range(len(paths)-1):
    if paths[i][0] == paths[i+1][0]:
        isunique[i] = 0

t2 = time.time()
print(t1)
print(t2)
t2 -= t1
#f = open(OUTFILE, "w")
strr = "Completion time: "
strr += str(t2-t1)
#f.writelines(f"Completion time : {t2:.2f} seconds" )
#f.writelines("\n")
t = -1
printing_paths = {}
printing_paths[0] = []
for i in paths:
    t += 1
    if isunique[t]:
        print_path = []
        strr = "[ Total length of the path (First Criteria) : "
        strr += str(i[0])
        strr += "- MinMax of path (Second criteria) : "
        strr += str(i[1])
        strr += " *** Nodes in the path=> "
        k = i[2][start]
        strr += str(start)
        print_path.append(start)
        while k != -1:
            strr += "->"+str(k)
            print_path.append(k)
            k = i[2][k]
        strr += "]"
#        f.writelines(strr)
#        f.writelines("\n")
        printing_paths[0].append((i[0], i[1], convert(print_path)))
# f.close()

for customer in range(CUSTOMER_NUM-1):
    print(f"{customer+1} bitti")
    printing_paths[customer + 1] = []
    nodeweights, edges = new_weights(original_nodeweights, original_edges)
    minW2 = first_pass(nodeweights)
    paths = list()
    max_w2 = BIGNUM
    while max_w2 >= minW2:
        max_w2, path, lp = longest_path(max_w2)
        if abs(lp) >= BIGNUM/10:
            continue
        paths.append([math.exp(-1*lp), max_w2, path])
    if paths[-1][1] == 0:
        del (paths[-1])
    isunique = [1 for i in range(len(paths))]
    t = -1
    for i in range(len(paths) - 1):
        if paths[i][0] == paths[i + 1][0]:
            isunique[i] = 0
    for i in paths:
        t += 1
        if isunique[t]:
            print_path = []
            k = i[2][start]
            print_path.append(start)
            while k != -1:
                print_path.append(k)
                k = i[2][k]
            printing_paths[customer+1].append((i[0], i[1], convert(print_path)))
t2 = time.time()
print(f"{CUSTOMER_NUM} musteri icin toplam {(t2-t1):.2f} sn")
with (open(BIGOUTFILE, "w")) as f:
    f.writelines(f"{CUSTOMER_NUM},60,12 \n")
    strr =""
    for i in range(9):
        strr += "," + str(CUSTOMER_NUM)
    strr += "," + str(int(CUSTOMER_NUM*0.95))
    strr += "," + str(int(CUSTOMER_NUM*0.90))
    strr += "," + str(int(CUSTOMER_NUM*0.85))
    strr = strr[1:] + "\n"
    f.writelines(strr)
    strr = ""
    for i in range(12):
        strr += f",{max(5,i*i-5*i)}"
    strr = strr[1:]+"\n"
    for i in range(CUSTOMER_NUM):
        strr += f"{len(printing_paths[i])},"
    strr = strr[:-1]+"\n"
    for i in range(CUSTOMER_NUM):
        strr += f"{random.random()*1000000},"
    strr += "\n"
    for i in range(CUSTOMER_NUM):
        strr += f"{random.random()*1000000},"
    strr = strr[:-1] + "\n"
    f.writelines(strr)
    for i in range(CUSTOMER_NUM):
        for k in range(len(printing_paths[i])):
            path = copy.deepcopy(printing_paths[i][k])
            strr = f"[{start},"
            for act in path[2]:
                strr += f"{act},"
            strr += f"{path[0]},{path[1]}]\n"
            f.writelines(strr)
print(f"{CUSTOMER_NUM} musteri icin toplam yazma zamani {(time.time()-t2):.2f} sn")
