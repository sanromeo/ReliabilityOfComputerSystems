"""Incoming data"""
inp_sample = [1325, 977, 243, 3, 145, 997, 27, 67, 30, 934,
              1039, 240, 371, 86, 164, 96, 156, 145, 280,
              444, 887, 726, 41, 503, 174, 1809, 349, 532,
              1541, 148, 489, 198, 4, 761, 389, 37, 317,
              1128, 514, 426, 23, 184, 365, 153, 624, 31,
              49, 1216, 61, 189, 286, 1269, 365, 1085,
              279, 228, 95, 391, 683, 39, 7, 486, 715, 204,
              1553, 736, 1622, 1892, 448, 23, 135, 555,
              252, 569, 8, 491, 724, 331, 1243, 567, 788,
              729, 62, 636, 227, 227, 245, 153, 151, 217,
              1009, 143, 301, 342, 48, 493, 117, 78, 113, 67]
gamma = 0.74
infallible_time = 1586
time_on_failure_intensity = 1798

"""LabWork"""
# 1 task
Avg_operating_time_on_failure = sum(inp_sample) / len(inp_sample)

# 2 task
inp_sample.sort()
dimension_of_sample = inp_sample[-1] / 10
density_fi = [0]
Probability_P = [1]
index = 0
new_count = 0
i = 0

for k in range(1, 11):
    count = 0
    while i < len(inp_sample) and inp_sample[i] <= k * dimension_of_sample + inp_sample[0]:
        count += 1
        new_count += 1
        i += 1
    density_fi.append(count / (dimension_of_sample * len(inp_sample)))
    Q = new_count / len(inp_sample)
    Probability_P.append(1 - Q)
   # Probability_P.append(count / len(inp_sample))  # P = density_fi * range_sample = (count * range_sample) / ((range_sample * len(inp_sample))
    if Probability_P[k - 1] > gamma > Probability_P[k]:
        iter_i = k
d = (Probability_P[iter_i - 1] - gamma) / (Probability_P[iter_i - 1] - Probability_P[iter_i])
T = density_fi[iter_i - 1] + dimension_of_sample * d

# 3 task
probability_infallible_time = 1
k = 1
while k * dimension_of_sample <= infallible_time:
    probability_infallible_time -= density_fi[k] * dimension_of_sample
    k += 1
probability_infallible_time -= density_fi[k] * (infallible_time - (k - 1) * dimension_of_sample)

# 4 task
probability_infallible_time_from_f = 1
k = 1
while k * dimension_of_sample <= time_on_failure_intensity:
    probability_infallible_time_from_f -= density_fi[k] * dimension_of_sample
    k += 1
probability_infallible_time_from_f -= density_fi[k] * (time_on_failure_intensity - (k - 1) * dimension_of_sample)
failure_rate_lambda = density_fi[k] / probability_infallible_time_from_f

"""Output results in console"""
print("Average operating time to failure (Tcp) =", Avg_operating_time_on_failure)
print(f"γ-percent work on refusal Tγ at γ = {gamma}, T = {T}")
print(f"Probable uptime on time {infallible_time}, P({infallible_time}) = {probability_infallible_time}")
print(f"Failure intensity on time {time_on_failure_intensity}, λ = {failure_rate_lambda}")
