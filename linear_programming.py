import gurobipy as gp
import time


class FileOperations:

    cust_path_bin = {}
    paths = []
    start_time = 0
    reading_time = 0
    writing_time = 0
    num_people = 0
    num_paths = []

    def read_from_file(self, input_file):
        self.start_time = time.time()
        f = open(input_file, "r")
        strr = f.readline()
        line = strr.split(",")
        num_people = eval(line[0])
        num_day = eval(line[1])
        num_actions = eval(line[2])
        strr = f.readline()
        line = strr.split(",")
        action_constraints = {}
        for i in range(num_actions):
            k = eval(line[i])
            for j in range(num_day):
                action_constraints[j+1, i+1] = k
        strr = f.readline()
        line = strr.split(",")
        action_costs = []
        for i in range(num_actions):
            action_costs.append(eval(line[i]))
        strr = f.readline()
        line = strr.split(",")
        num_paths = []
        for i in range(num_people):
            num_paths.append(eval(line[i]))
        strr = f.readline()
        line = strr.split(",")
        CLV = []
        for i in range(num_people):
            CLV.append(eval(line[i]))
        strr = f.readline()
        line = strr.split(",")
        debts = []
        for i in range(num_people):
            debts.append(eval(line[i]))
        paths = []
        for i in range(num_people):
            person_paths = []
            for j in range(num_paths[i]):
                path = []
                strr = f.readline()
                line = strr[1:-2].split(",")
                for k in line:
                    path.append(eval(k))
                person_paths.append(path)
            paths.append(person_paths)
        f.close()
        self.reading_time = time.time()
        print(f'Reading OK in {(self.reading_time-self.start_time):.2f} seconds')
        return num_day, num_actions, num_people, num_paths, paths, debts, CLV, action_costs, action_constraints, self.reading_time

    def write_to_file(self, output_file):
        # Printing Results
        f = open(output_file, "w")
        for i in range(self.num_people):
            for j in range(self.num_paths[i]):
                if self.cust_path_bin[i, j].x == 1:
                    f.writelines(f" For customer {i + 1} we have to choose path {j} \n")
                    strr = "Path start ->"
                    for k in self.paths[i][j]:
                        strr += str(k) + "->"
                    strr += "\n"
                    f.writelines(strr)
        self.writing_time = time.time()
        print(f"Finished optimization in {self.writing_time - self.reading_time}")
        f.close()

    def write_infeasible(self, output_file):
        f = open(output_file, "w")
        f.writelines("Infeasible \n")
        f.close()


class Optimization:

    m = gp.Model()
    input_file = "deneme2_input.txt"
    output_file = "output.txt"
    num_day = 0
    num_actions = 0
    num_people = 0
    num_paths = 0
    paths = []
    debts = []
    CLV = []
    action_costs = []
    action_constraints = {}
    reading_time = 0
    status = gp.GRB.INFEASIBLE
    log_to_console = 1
    def read_data(self):
        reading = FileOperations()
        self.num_day, self.num_actions, self.num_people, self.num_paths, self.paths, self.debts, self.CLV, \
            self.action_costs, self.action_constraints, self.reading_time = reading.read_from_file(self.input_file)

    def reset(self):
        self.m.reset(0)

    def optimize(self):
        # variable definitions
        cust_path_bin = {}
        self.m.Params.LogToConsole = self.log_to_console
        non_payment_cost = self.m.addVar(vtype='C')
        churn_cost = self.m.addVar(vtype='C')
        action_cost = self.m.addVar(vtype='C')
        for i in range(self.num_people):
            for j in range(self.num_paths[i]):
                cust_path_bin[i, j] = self.m.addVar(vtype='B')
        '''constraints'''
        self.m.addConstr(non_payment_cost ==
                    gp.quicksum(self.debts[i] * gp.quicksum(cust_path_bin[i, j] * self.paths[i][j][-2]
                                                            for j in range(self.num_paths[i]))
                                for i in range(self.num_people))
        )
        self.m.addConstr(churn_cost ==
                    gp.quicksum(self.CLV[i] * gp.quicksum(cust_path_bin[i, j] * self.paths[i][j][-1]
                                                          for j in range(self.num_paths[i]))
                                for i in range(self.num_people))
        )
        self.m.addConstr(action_cost ==
                         gp.quicksum(self.action_costs[i] *
                                     gp.quicksum(gp.quicksum(cust_path_bin[j, k] *
                                                             gp.quicksum(1 for t in range(self.num_day)
                                                                         if self.paths[j][k][t] == i+1)
                                                             for k in range(self.num_paths[j]))
                                                 for j in range(self.num_people))
                                     for i in range(self.num_actions))
        )
        for i in range(self.num_people):
            self.m.addConstr(gp.quicksum(cust_path_bin[i, j] for j in range(self.num_paths[i])) == 1)

        for i in range(1, self.num_day+1):
            for j in range(1, self.num_actions+1):
                self.m.addConstr(
                    gp.quicksum(gp.quicksum(cust_path_bin[k, t] *
                                            1 for t in range(self.num_paths[k]) if self.paths[k][t][i] == j)
                                for k in range(self.num_people))
                    <= self.action_constraints[i, j])
        # objective function
        self.m.setObjective(non_payment_cost+churn_cost+action_cost, gp.GRB.MINIMIZE)

        # Optimizations
        self.m.optimize()
        optimization_time = time.time() - self.reading_time
        if self.m.STATUS == gp.GRB.OPTIMAL:
            self.status = gp.GRB.OPTIMAL
            cust_path_bin_new = {}
            for customer, path in cust_path_bin.keys():
                cust_path_bin_new[customer, path] = cust_path_bin[customer, path].x
            return self.status, self.m.ObjVal, cust_path_bin_new, optimization_time
        else:
            self.status = self.m.STATUS
            return self.status, None, None, optimization_time

    def write_result_to_file(self, cust_path_bin):
        # writing to file
        reading = FileOperations()
        reading.paths = self.paths
        reading.output_file = self.output_file
        reading.reading_time = self.reading_time
        if self.status == gp.GRB.OPTIMAL:
            reading.cust_path_bin = cust_path_bin
            reading.write_to_file(self.output_file)
        else:
            reading.write_infeasible(self.output_file)

    def action_number_render(self, cust_path_bin):
        used_actions = {}
        for day in range(1,self.num_day + 2):
            for action in range(1, self.num_actions + 1):
                used_actions[day, action] = 0
        for customer, path in cust_path_bin.keys():
            if cust_path_bin[customer, path] == 1:
                selected_path = self.paths[customer][path]
                for i in range(len(selected_path)-2):
                    used_actions[i + 1, selected_path[i]] += 1
        return used_actions
