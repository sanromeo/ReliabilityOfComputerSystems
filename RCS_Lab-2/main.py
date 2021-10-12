from copy import copy, deepcopy

                   # 1, 2, 3, 4, 5, 6, 7, 8
adjacency_matrix = [[0, 0, 1, 0, 1, 0, 0, 0],  # 1
                    [0, 0, 0, 1, 0, 0, 1, 0],  # 2
                    [0, 0, 0, 0, 1, 0, 0, 0],  # 3
                    [0, 0, 0, 0, 0, 0, 1, 0],  # 4
                    [0, 0, 0, 0, 0, 1, 0, 0],  # 5
                    [0, 0, 0, 0, 0, 0, 0, 0],  # 6
                    [0, 0, 0, 0, 0, 0, 0, 1],  # 7
                    [0, 0, 0, 0, 0, 0, 0, 0]]  # 8

probabilities = [0.41, 0.3, 0.59, 0.44, 0.51, 0.63, 0.72, 0.48]
n = len(probabilities)
road = []
roads = []
probability = []


def road_search(apex, previous_apex):
    if previous_apex != n:
        if adjacency_matrix[apex][previous_apex:].count(1) > 0:
            index = adjacency_matrix[apex].index(1, previous_apex)
            road.append(index)
            road_search(index, 0)
        else:
            if adjacency_matrix[apex].count(0) == n:
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
    for element in array:
        result *= element
    return result


for i in probabilities:
    if i <= 0 or i > 1:
        print("Error! The probability can`t be less than zero or more than one!")
        exit(1)

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
        print("Error! No roads found")
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

print(f"Probability of trouble-free operation of the system within 10 hours = {probability}")
