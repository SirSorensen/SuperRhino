from pybricks.pupdevices import ColorSensor
import utils.calibrations as cal
from pybricks.tools import wait

class Vision:
    def __init__(self, left_eye_port, right_eye_port):
        # Initialize & calibrate the sensors.
        self.left_sensor: ColorSensor = ColorSensor(left_eye_port)
        self.right_sensor: ColorSensor = ColorSensor(right_eye_port)
        # Calibrate sensors
        self.left_sensor.lights.on()
        self.right_sensor.lights.on()
        wait(500)  # Wait 0.5 seconds

        self.calibrate()

    ########################## Calibrations: ##########################

    def calibrate(self):
        def min_max() -> tuple[float, float]:
            (min_left, max_left) = cal.min_max_measure(self.left_sensor.reflection)
            (min_right, max_right) = cal.min_max_measure(self.right_sensor.reflection)
            return (min(min_left, min_right), max(max_left, max_right))

        print("Please put my eyes over table, and press Enter.")
        input()
        self.table_range : tuple[float, float] = min_max()

        print("Please put my eyes over tape, and press Enter.")
        input()
        self.tape_range : tuple[float, float] = min_max()

        print("Please put my eyes over an edge, and press Enter.")
        input()
        self.edge_range : tuple[float, float] = min_max()

        if self.edge_range[1] >= self.tape_range[0]:
            print(f"ERROR! edge_range and tape_range overlap! edge_range:{self.edge_range} tape_range:{self.tape_range}")
        if self.tape_range[1] >= self.table_range[0]:
            print(f"ERROR! tape_range and table_range overlap! tape_range:{self.tape_range} table_range:{self.table_range}")
