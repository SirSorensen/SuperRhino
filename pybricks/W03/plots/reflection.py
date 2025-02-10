import matplotlib.pyplot as plt

distances = [
    1.5,
    3,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    20,
    30
]
reflections = [
    34,
    13,
    7,
    4,
    3,
    2,
    2,
    1,
    1,
    1,
    1,
    0,
    0,
    0,
    0
]

plt.plot(distances, reflections)
plt.title("sensor value vs. distance")
plt.xlabel('distances (cm)')
plt.ylabel('sensor value')
plt.show()
