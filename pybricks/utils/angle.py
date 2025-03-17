import umath as math

class Angle:
    def __init__(self, degree):
        self.value = degree % 360
        if self.value > 180:
            self.value -= 360

    def to_angle(degree) -> float:
        angle = Angle(degree)
        return angle.value

    def to_angle_from_radians(radians) -> float:
        degrees = math.degrees(radians)
        return Angle.to_angle(degrees)

    def in_diff_domains(degree_1 : float, degree_2 : float):
        angle_1 = Angle.to_angle(degree_1)
        angle_2 = Angle.to_angle(degree_2)
        return (angle_1 >= 0 > angle_2) or (angle_2 >= 0 > angle_1)

    def calc_error(current_degree : float, measured_degree : float):
        current_angle = Angle.to_angle(current_degree)
        measured_angle = Angle.to_angle(measured_degree)
        # If i.e. current_angle = 179 and measure_angle = -179
        if Angle.in_diff_domains(current_angle, measured_angle) and (abs(current_angle) > 100 and abs(measured_angle) > 100):
            print(f"({current_angle} >= 0 > {measured_angle} or {measured_angle} >= 0 > {current_angle}) = True" )
            if current_angle >= 0 > measured_angle:
                return current_angle - (measured_angle + 360)
            else:
                return current_angle - (measured_angle - 360)
        else:
            return current_angle - measured_angle
