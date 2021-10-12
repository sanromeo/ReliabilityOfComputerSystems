from copy import copy, deepcopy
from math import log, factorial
from functools import reduce

probabilities = [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.92, 0.94]

                    # 1, 2, 3, 4, 5, 6, 7, 8
adjacency_matrix = [[0, 1, 1, 0, 0, 0, 0, 0],  # 1
                    [0, 0, 0, 1, 1, 0, 0, 0],  # 2
                    [0, 0, 0, 1, 0, 1, 0, 1],  # 3
                    [0, 0, 0, 0, 1, 1, 0, 1],  # 4
                    [0, 0, 0, 0, 0, 1, 1, 0],  # 5
                    [0, 0, 0, 0, 0, 0, 1, 1],  # 6
                    [0, 0, 0, 0, 0, 0, 0, 0],  # 7
                    [0, 0, 0, 0, 0, 0, 0, 0]]  # 8

t = 1000
k1 = 1
k2 = 1
k3 = 1
k4 = 1


def lab2(probabilities, adjacency_matrix):
    road = []
    roads = []

    def road_search(apex, previous_apex):
        if previous_apex != n:
            if adjacency_matrix[apex][previous_apex:].count(True) > 0:
                index = adjacency_matrix[apex].index(True, previous_apex)
                road.append(index)
                road_search(index, 0)
            else:
                if adjacency_matrix[apex].count(False) == n:
                    roads.append(copy(road))
                road.remove(apex)
                if road:
                    road_search(road[-1], apex + 1)
        else:
            road.remove(apex)
            if road:
                road_search(road[-1], apex + 1)

    def break_or_not(x, y):
        if x == 0:
            return 1 - y
        if x == 1:
            return y

    def product_of_elements(array):
        result = 1
        for elem in array:
            result *= elem
        return result

    for i in probabilities:
        if i < 0 or i > 1:
            print("Error! The probability can`t be less than zero or more than one!")
            exit(1)

    n = len(probabilities)

    if n < 1:
        print("Error! There are no elements in the scheme!")
        exit(1)

    if len(adjacency_matrix) != n:
        print("Error! Incorrect adjacency matrix!")
        exit(1)
    else:
        for i in adjacency_matrix:
            if i.count(1) + i.count(0) != n:
                print("Error! Incorrect adjacency matrix!")
                exit(1)

    transposed_matrix = list(zip(*adjacency_matrix))
    beginning_of_apexes = []
    end_of_apexes = []
    for i in range(len(transposed_matrix)):
        if transposed_matrix[i].count(0) == n:
            beginning_of_apexes.append(i)
    for i in range(len(adjacency_matrix)):
        if adjacency_matrix[i].count(0) == n:
            end_of_apexes.append(i)

    if not beginning_of_apexes or not end_of_apexes:
        print("Error! There is no beginning or end of the apex!")
        exit(1)

    if n == 1:

        probability = probabilities[0]
    else:
        for i in beginning_of_apexes:
            road.append(i)
            road_search(i, 0)
        if not roads:
            print("No roads found")
            exit(1)
        else:
            serviceable_roads = []
            for i in roads:
                serviceable_condition = [[]]
                for j in range(n):
                    if j in i:
                        for k in range(len(serviceable_condition)):
                            serviceable_condition[k].append(1)
                    else:
                        serviceable_condition.extend(deepcopy(serviceable_condition))
                        for k in range(int(len(serviceable_condition) / 2)):
                            serviceable_condition[k].append(0)
                            serviceable_condition[-k - 1].append(1)
                for k in serviceable_condition:
                    if k not in serviceable_roads:
                        serviceable_roads.append(k)
            probability = 0
            for i in serviceable_roads:
                probability += product_of_elements(list(map(break_or_not, i, probabilities)))
    return probability


probability = lab2(probabilities, adjacency_matrix)
Q = 1 - probability
t_average = -t / log(probability)
print(f"Basic probability of failure-free = {probability}\n"
      f"Basic probability of failure = {Q}\n"
      f"Basic average MTBF = {t_average}\n")


# Система з загальним ненавантаженим резервуванням
def system_with_general_unloaded_reservation(t, k, Q, possibility, t_aver):
    q_for_gen_unloaded_reservation = 1 / factorial(k + 1) * Q
    p_for_gen_unloaded_reservation = 1 - q_for_gen_unloaded_reservation
    t_aver_gen_unloaded_reservation = -t / log(p_for_gen_unloaded_reservation)
    g_q_for_gen_unloaded_reservation = q_for_gen_unloaded_reservation / Q
    g_p_for_gen_unloaded_reservation = p_for_gen_unloaded_reservation / possibility
    g_t_for_gen_unloaded_reservation = t_aver_gen_unloaded_reservation / t_aver
    print(f"Failure-free probability of the system with UNLOADED GENERAL reservation = {p_for_gen_unloaded_reservation}\n"
          f"Probability of failure of a system with UNLOADED GENERAL reservation = {q_for_gen_unloaded_reservation}\n"
          f"Average system operating time with UNLOADED GENERAL reservation = {t_aver_gen_unloaded_reservation}")

    print(f"Winning of system with UNLOADED GENERAL reservation on the probability of failure-free = {g_p_for_gen_unloaded_reservation}\n"
          f"Winning of system with UNLOADED GENERAL reservation on the probability of failure = {g_q_for_gen_unloaded_reservation}\n"
          f"Winning of system with UNLOADED GENERAL reservation for the average operating time = {g_t_for_gen_unloaded_reservation}\n")


# Система з загальним навантаженим резервуванням
def system_with_general_loaded_reservation(t, k, Q, prob, possibility, t_aver):
    new_possibility = reduce(lambda x, y: x * y, possibility)
    p_for_gen_loaded_reservation = 1 - (1 - new_possibility) ** (k + 1)
    q_for_gen_loaded_reservation = 1 - p_for_gen_loaded_reservation
    t_aver_for_gen_loaded_reservation = -t / log(p_for_gen_loaded_reservation)
    g_q_for_gen_loaded_reservation = q_for_gen_loaded_reservation / Q
    g_p_for_gen_loaded_reservation = p_for_gen_loaded_reservation / prob
    g_t_for_gen_loaded_reservation = t_aver_for_gen_loaded_reservation / t_aver

    print(f"Failure-free probability of the system with LOADED GENERAL reservation = {p_for_gen_loaded_reservation}\n"
          f"Probability of failure of a system with LOADED GENERAL reservation = {q_for_gen_loaded_reservation}\n"
          f"Average system operating time with LOADED GENERAL reservation = {t_aver_for_gen_loaded_reservation}")

    print(f"Winning of system with LOADED GENERAL reservation on the probability of failure-free = {g_p_for_gen_loaded_reservation}\n"
          f"Winning of system with LOADED GENERAL reservation on the probability of failure = {g_q_for_gen_loaded_reservation}\n"
          f"Winning of system with LOADED GENERAL reservation for the average operating time = {g_t_for_gen_loaded_reservation}\n")


# Система з розподіленим ненавантаженим резервуванням
def system_with_distributed_unloaded_reservation(t, k, Q, possibility, t_aver, adj_mat):
    new_possibilities = []
    for p in probabilities:
        new_possibilities.append(1 - (1 / factorial(k + 1) * Q))
    p_for_distr_unloaded_reservation = lab2(new_possibilities, adj_mat)
    q_for_distr_unloaded_reservation = 1 - p_for_distr_unloaded_reservation
    t_aver_for_distr_unloaded_reservation = -t / log(p_for_distr_unloaded_reservation)
    g_q_for_distr_unloaded_reservation = q_for_distr_unloaded_reservation / Q
    g_p_for_distr_unloaded_reservation = p_for_distr_unloaded_reservation / possibility
    g_t_for_distr_unloaded_reservation = t_aver_for_distr_unloaded_reservation / t_aver

    print(f"Failure-free probability of the system with UNLOADED DISTRIBUTED reservation = {p_for_distr_unloaded_reservation}\n"
          f"Probability of failure of a system with UNLOADED DISTRIBUTED reservation = {q_for_distr_unloaded_reservation}\n"
          f"Average system operating time with UNLOADED DISTRIBUTED reservation = {t_aver_for_distr_unloaded_reservation}")

    print(f"Winning of system with UNLOADED DISTRIBUTED reservation on the probability of failure-free = {g_p_for_distr_unloaded_reservation}\n"
          f"Winning of system with UNLOADED DISTRIBUTED reservation on the probability of failure = {g_q_for_distr_unloaded_reservation}\n"
          f"Winning of system with UNLOADED DISTRIBUTED reservation for the average operating time = {g_t_for_distr_unloaded_reservation}\n")


# Система з розподіленим навантаженим резервуванням
def system_with_distributed_loaded_reservation(t, k, Q, prob, possibility, t_aver, adj_mat):
    new_possibilities = list(map(lambda x: 1 - (1 - x) ** (k + 1), possibility))
    p_for_distr_loaded_reservation = lab2(new_possibilities, adj_mat)
    q_for_distr_loaded_reservation = 1 - p_for_distr_loaded_reservation
    t_aver_for_distr_loaded_reservation = -t / log(p_for_distr_loaded_reservation)
    g_q_for_distr_loaded_reservation = q_for_distr_loaded_reservation / Q
    g_p_for_distr_loaded_reservation = p_for_distr_loaded_reservation / prob
    g_t_for_distr_loaded_reservation = t_aver_for_distr_loaded_reservation / t_aver

    print(f"Failure-free probability of the system with LOADED DISTRIBUTED reservation = {p_for_distr_loaded_reservation}\n"
          f"Probability of failure of a system with LOADED DISTRIBUTED reservation = {q_for_distr_loaded_reservation}\n"
          f"Average system operating time with LOADED DISTRIBUTED reservation = {t_aver_for_distr_loaded_reservation}")

    print(f"Winning of system with LOADED DISTRIBUTED reservation on the probability of failure-free = {g_p_for_distr_loaded_reservation}\n"
          f"Winning of system with LOADED DISTRIBUTED reservation on the probability of failure = {g_q_for_distr_loaded_reservation}\n"
          f"Winning of system with LOADED DISTRIBUTED reservation for the average operating time = {g_t_for_distr_loaded_reservation}\n")


# Система з загальним ненавантаженим резервуванням
system_with_general_unloaded_reservation(t, k1, Q, probability, t_average)
# Система з загальним навантаженим резервуванням
system_with_general_loaded_reservation(t, k2, Q, probability, probabilities, t_average)
# Система з розподіленим ненавантаженим резервуванням
system_with_distributed_unloaded_reservation(t, k3, Q, probability, t_average, adjacency_matrix)
# Система з розподіленим навантаженим резервуванням
system_with_distributed_loaded_reservation(t, k4, Q, probability, probabilities, t_average, adjacency_matrix)

