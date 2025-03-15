# Hardware of Vehicle 4:
#     Adding nonlinear speed dependencies to Vehicle 3

class Vehicle_4:
    def __init__(
                 self,
                 motor_left,  sensor_left,  dependency_function_left,
                 motor_right, sensor_right, dependency_function_right
                ):
        self.motor_left = motor_left
        self.sensor_left = sensor_left
        self.dependency_function_left = dependency_function_left
        self.motor_right = motor_right
        self.sensor_right = sensor_right
        self.dependency_function_right = dependency_function_right

    def run_lover(self):
        while True:
            self.motor_left(100-self.dependency_function_left(self.sensor_left()))
            self.motor_right(100-self.dependency_function_right(self.sensor_right()))

    def run_explorer(self):
        while True:
            self.motor_left(100-self.dependency_function_left(self.sensor_right()))
            self.motor_right(100-self.dependency_function_right(self.sensor_left()))