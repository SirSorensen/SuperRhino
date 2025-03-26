from pybricks.pupdevices import ColorSensor
from utils.calibrations import min_max_measure
from utils.state import VisionObject
from pybricks.tools import wait

class Vision:
    def __init__(self, left_eye_port, right_eye_port):
        # Initialize & calibrate the sensors.
        self.left_sensor: ColorSensor = ColorSensor(left_eye_port)
        self.right_sensor: ColorSensor = ColorSensor(right_eye_port)
        # Calibrate sensors
        self.left_sensor.lights.on()
        self.right_sensor.lights.on()
        wait(500)  # Wait 0.5 seconds for lights to turn on

        self.table_range : tuple[float, float] = (13, 31)
        self.tape_range : tuple[float, float] = (2, 12)
        #self.table_tape_mid : float = (self.tape_range[1] + self.table_range[0]) / 2
        self.edge_range : tuple[float, float] = (0, 1)
        #self.tape_edge_mid : float = (self.table_range[1] + self.edge_range[0]) / 2

    def measure(self):
        return (self.left_sensor.reflection(), self.right_sensor.reflection())

    def _determine_object(self, reflection) -> VisionObject:
        if self.table_range[0] <= reflection and reflection <= self.table_range[1]:
            return VisionObject.TABLE
        elif self.tape_range[0] <= reflection and reflection <= self.tape_range[1]:
            return VisionObject.TAPE
        elif self.edge_range[0] <= reflection and reflection <= self.edge_range[1]:
            return VisionObject.EDGE
        else:
            return VisionObject.UNKNOWN

    def what_is_seen(self):
        left, right = self.measure()
        left_result = self._determine_object(left)
        right_result = self._determine_object(right)
        return (left_result, right_result)
