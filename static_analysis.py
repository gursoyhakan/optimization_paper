# this program simulates the pattern of incoming and exiting customers for any predefined number
# of times. The result of each run is saved and will be used for evaluation of our studies
import copy
import random
import time
import gurobipy as gp
import numpy as np
from linear_programming import FileOperations, Optimization
input_file = "customers1000.txt"
output_file = 'static_analysis_1000out.txt'
# Here we get the data by using FileOperations class
reading = FileOperations()
num_day, num_actions, num_people, num_paths, paths, debts, CLV, action_costs, base_action_constraints, reading_time = \
    reading.read_from_file(input_file)
debts = list()
CLV = list()
for customer in range(1000):
    debts.append(random.randint(1000, 15000000))
    CLV.append(random.randint(1000, 15000000))
for action_rate in [0.1]:
    output = open(f"{output_file}", "w")
    action_constraints = dict()
    for day, action in base_action_constraints:
        if action >= 8:
            action_constraints[day, action] = int(action_rate*base_action_constraints[day, action])
        else:
            action_constraints[day, action] = base_action_constraints[day, action]

    # ##### STATIC OPTIMIZATION #######
    static_time = time.time()
    first_static_optimization = Optimization()
    first_static_optimization.paths = copy.deepcopy(paths)
    first_static_optimization.num_people = num_people
    first_static_optimization.num_paths = copy.deepcopy(num_paths)
    first_static_optimization.num_day = num_day
    first_static_optimization.num_actions = num_actions
    first_static_optimization.action_constraints = {}
    for i in range(1, num_day + 1):
        for j in range(1, num_actions + 1):
            first_static_optimization.action_constraints[i, j] = action_constraints[i, j]
    first_static_optimization.action_costs = action_costs
    first_static_optimization.CLV = copy.deepcopy(CLV)
    first_static_optimization.debts = copy.deepcopy(debts)
    first_static_optimization.reading_time = time.time()
    first_static_optimization.log_to_console = 1
    status, objVal, cust_path_bin, optimization_time = first_static_optimization.optimize()
    for key in cust_path_bin:
        if cust_path_bin[key] == 1:
            output.writelines(f"{key}, {debts[key[0]]}, {CLV[key[0]]}\n")
    print(f"Static optimization finished in {(time.time()-static_time):.2f}")
    output.writelines(f"Static optimization finished in {(time.time()-static_time):.2f}\n")
    output.close()




