def avg_measure(measurement_func, parameters=None, measure_num=100):
    measurements = []
    for _ in range(measure_num):
        if parameters is None:
            measurements.append(measurement_func())
        else:
            measurements.append(measurement_func(parameters))
    avg_measurement = sum(measurements) / len(measurements)
    return avg_measurement
