import matplotlib.pyplot as plt
with open("7_poisson_customers1000out.txt", "r") as f:
    line = f.readline()
    static_time_1 = eval(line.split(" ")[4])
    static_num_1 = list()
    dynamic_num_1 = list()
    static_times_1 = list()
    dynamic_times_1 = list()
    dynamic_data_1 = dict()
    for sim in range(10):
        line = f.readline()
        line = line.split(" ")
        static_num_1.append(eval(line[12]))
        dynamic_num_1.append(eval(line[-1]))
        line = f.readline()
        static_times_1.append(eval(line.split(" ")[9]))
        line = f.readline()
        dynamic_data_1[sim] = []
        for i in range(250):
            line = f.readline()
            line = line.split(" ")
            day = int(eval(line[6]))
            entering_customers = int(eval(line[10]))
            exiting_customers = int(eval(line[16]))
            remaining_from_static = int(eval(line[22]))
            remaining_from_dynamic = int(eval(line[-1]))
            if day == 1:
                customer_in_system = remaining_from_static + entering_customers - exiting_customers
            else:
                customer_in_system = dynamic_data_1[sim][day-2][5] + entering_customers - exiting_customers
            dynamic_data_1[sim].append((day, entering_customers, exiting_customers, remaining_from_static, remaining_from_dynamic, customer_in_system ))
Y1 = [0 for i in dynamic_data_1[0]]
for sim in range(10):
    X = [i[0] for i in dynamic_data_1[sim]]
    Y = [i[5] for i in dynamic_data_1[sim]]
    Y1 = [Y1[i] + dynamic_data_1[sim][i][5] for i in range(len(dynamic_data_1[sim]))]
    plt.plot(X, Y, label=f"{sim}")
X = [i[0] for i in dynamic_data_1[0]]
Y1 = [Y1[i]/10 for i in range(len(dynamic_data_1[sim]))]
plt.plot(X, Y1, label="MEAN", linewidth=4)
plt.xlabel("Gün")
plt.ylabel("Müşteri Sayısı")
plt.title("Havuzdaki Müşteri Sayısı")
plt.savefig("simul1.pdf")
plt.show()

with open("8customers1000out.txt", "r") as f:
    line = f.readline()
    static_time_2 = eval(line.split(" ")[4])
    static_num_2 = list()
    dynamic_num_2 = list()
    static_times_2 = list()
    dynamic_times_2 = list()
    dynamic_data_2 = dict()
    for sim in range(10):
        line = f.readline()
        line = line.split(" ")
        static_num_2.append(eval(line[12]))
        dynamic_num_2.append(eval(line[-1]))
        line = f.readline()
        static_times_2.append(eval(line.split(" ")[9]))
        line = f.readline()
        dynamic_data_2[sim] = []
        for i in range(250):
            line = f.readline()
            line = line.split(" ")
            day = int(eval(line[6]))
            entering_customers = int(eval(line[10]))
            exiting_customers = int(eval(line[16]))
            remaining_from_static = int(eval(line[22]))
            remaining_from_dynamic = int(eval(line[-1]))
            if day == 1:
                customer_in_system = remaining_from_static + entering_customers - exiting_customers
            else:
                customer_in_system = dynamic_data_2[sim][day-2][5] + entering_customers - exiting_customers
            dynamic_data_2[sim].append((day, entering_customers, exiting_customers, remaining_from_static, remaining_from_dynamic, customer_in_system ))
Y1 = [0 for i in dynamic_data_2[0]]
for sim in range(10):
    X = [i[0] for i in dynamic_data_2[sim]]
    Y = [i[5] for i in dynamic_data_2[sim]]
    Y1 = [Y1[i] + dynamic_data_2[sim][i][5] for i in range(len(dynamic_data_2[sim]))]
    plt.plot(X, Y, label=f"{sim}")
X = [i[0] for i in dynamic_data_2[0]]
Y1 = [Y1[i]/10 for i in range(len(dynamic_data_2[sim]))]
plt.plot(X, Y1, label="MEAN", linewidth=4)
plt.xlabel("Day")
plt.ylabel("Customer Num")
plt.title("Customers in system")
plt.savefig("simul2.pdf")
plt.show()

with open("2customers1000out.txt", "r") as f:
    line = f.readline()
    static_time_3 = eval(line.split(" ")[4])
    static_num_3 = list()
    dynamic_num_3 = list()
    static_times_3 = list()
    dynamic_times_3 = list()
    dynamic_data_3 = dict()
    for sim in range(10):
        line = f.readline()
        line = line.split(" ")
        static_num_3.append(eval(line[12]))
        dynamic_num_3.append(eval(line[-1]))
        line = f.readline()
        static_times_3.append(eval(line.split(" ")[9]))
        line = f.readline()
        dynamic_data_3[sim] = []
        for i in range(250):
            line = f.readline()
            line = line.split(" ")
            day = int(eval(line[6]))
            entering_customers = int(eval(line[10]))
            exiting_customers = int(eval(line[16]))
            remaining_from_static = int(eval(line[22]))
            remaining_from_dynamic = int(eval(line[-1]))
            if day == 1:
                customer_in_system = remaining_from_static + entering_customers - exiting_customers
            else:
                customer_in_system = dynamic_data_3[sim][day-2][5] + entering_customers - exiting_customers
            dynamic_data_3[sim].append((day, entering_customers, exiting_customers, remaining_from_static, remaining_from_dynamic, customer_in_system ))
Y1 = [0 for i in dynamic_data_3[0]]
for sim in range(10):
    X = [i[0] for i in dynamic_data_3[sim]]
    Y = [i[5] for i in dynamic_data_3[sim]]
    Y1 = [Y1[i] + dynamic_data_3[sim][i][5] for i in range(len(dynamic_data_3[sim]))]
    plt.plot(X, Y, label=f"{sim}")
X = [i[0] for i in dynamic_data_3[0]]
Y1 = [Y1[i]/10 for i in range(len(dynamic_data_3[sim]))]
plt.plot(X, Y1, label="MEAN", linewidth=4)
plt.xlabel("Day")
plt.ylabel("Customer Num")
plt.title("Customers in system")
plt.savefig("simul3.pdf")
plt.show()

with open("1customers1000out.txt", "r") as f:
    line = f.readline()
    static_time_4 = eval(line.split(" ")[4])
    static_num_4 = list()
    dynamic_num_4 = list()
    static_times_4 = list()
    dynamic_times_4 = list()
    dynamic_data_4 = dict()
    for sim in range(10):
        line = f.readline()
        line = line.split(" ")
        static_num_4.append(eval(line[12]))
        dynamic_num_4.append(eval(line[-1]))
        line = f.readline()
        static_times_4.append(eval(line.split(" ")[9]))
        line = f.readline()
        dynamic_data_4[sim] = []
        for i in range(250):
            line = f.readline()
            line = line.split(" ")
            day = int(eval(line[6]))
            entering_customers = int(eval(line[10]))
            exiting_customers = int(eval(line[16]))
            remaining_from_static = int(eval(line[22]))
            remaining_from_dynamic = int(eval(line[-1]))
            if day == 1:
                customer_in_system = remaining_from_static + entering_customers - exiting_customers
            else:
                customer_in_system = dynamic_data_4[sim][day-2][5] + entering_customers - exiting_customers
            dynamic_data_4[sim].append((day, entering_customers, exiting_customers, remaining_from_static, remaining_from_dynamic, customer_in_system ))
Y1 = [0 for i in dynamic_data_4[0]]
for sim in range(10):
    X = [i[0] for i in dynamic_data_4[sim]]
    Y = [i[5] for i in dynamic_data_4[sim]]
    Y1 = [Y1[i] + dynamic_data_4[sim][i][5] for i in range(len(dynamic_data_4[sim]))]
    plt.plot(X, Y, label=f"{sim}")
X = [i[0] for i in dynamic_data_4[0]]
Y1 = [Y1[i]/10 for i in range(len(dynamic_data_4[sim]))]
plt.plot(X, Y1, label="MEAN", linewidth=4)
plt.xlabel("Day")
plt.ylabel("Customer Num")
plt.title("Customers in system")
plt.savefig("simul4.pdf")
plt.show()
