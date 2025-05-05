"""
Controller module defining baseline and alternative controllers for wall-following behavior.
"""
from typing import Dict, Tuple, List, Any


class Controller:
    """
    Abstract base class for robot controllers.
    A controller maps sensor readings to left and right motor speeds.
    """
    def determine_speed(self, sensor_readings: Dict[str, Tuple[float, Any, Any]]) -> Tuple[float, float]:  # distance, color, intersect_point
        """
        Determine left and right motor speeds based on sensor readings.
        sensor_readings: dict with keys 'mid', 'left', 'right', each a tuple (distance, color, intersect_point)
        Returns: (left_speed, right_speed)
        """
        raise NotImplementedError

    @property
    def genome(self) -> List[float]:
        """
        Returns a list of parameters (floats) that can be evolved.
        """
        raise NotImplementedError

    def set_genome(self, genome: List[float]) -> None:
        """
        Set controller parameters from genome list.
        """
        raise NotImplementedError


class BaselineController(Controller):
    """
    Hand-coded proportional controller for wall-following at a fixed distance.
    Parameters:
      base_speed: nominal forward speed (rad/s)
      desired_distance: target distance to maintain from the wall (cm)
      k_p: proportional gain for distance error
      follow_side: 'left' or 'right' wall following
    """
    def __init__(self,
                 base_speed: float = 1.0,
                 desired_distance: float = 30.0,
                 k_p: float = 0.5,
                 follow_side: str = 'left'):
        self.base_speed = base_speed
        self.desired_distance = desired_distance
        self.k_p = k_p
        if follow_side not in ('left', 'right'):
            raise ValueError("follow_side must be 'left' or 'right'")
        self.follow_side = follow_side

    def determine_speed(self, sensor_readings: Dict[str, Tuple[float, Any, Any]]) -> Tuple[float, float]:
        # unpack distances
        d_mid, _, _ = sensor_readings.get('mid', (float('inf'), None, None))
        d_left, _, _ = sensor_readings.get('left', (float('inf'), None, None))
        d_right, _, _ = sensor_readings.get('right', (float('inf'), None, None))
        # corner or obstacle ahead: turn away from wall
        if d_mid < self.desired_distance:
            if self.follow_side == 'left':
                return (self.base_speed, -self.base_speed)
            else:
                return (-self.base_speed, self.base_speed)
        # compute lateral error and proportional correction
        if self.follow_side == 'left':
            error = d_left - self.desired_distance
            left_speed = self.base_speed - self.k_p * error
            right_speed = self.base_speed + self.k_p * error
        else:
            error = d_right - self.desired_distance
            left_speed = self.base_speed + self.k_p * error
            right_speed = self.base_speed - self.k_p * error
        return (left_speed, right_speed)

    @property
    def genome(self) -> List[float]:
        # [base_speed, desired_distance, k_p]
        return [self.base_speed, self.desired_distance, self.k_p]

    def set_genome(self, genome: List[float]) -> None:
        if len(genome) != 3:
            raise ValueError(f"Genome must be length 3, got {len(genome)}")
        self.base_speed, self.desired_distance, self.k_p = genome


class NeuralNetworkController(Controller):
    """
    Placeholder for an alternative controller (e.g., neural network based).
    """
    def __init__(self, model: Any = None):
        # model could be a loaded neural network
        self.model = model

    def determine_speed(self, sensor_readings: Dict[str, Tuple[float, Any, Any]]) -> Tuple[float, float]:
        # This is a stub; replace with actual NN inference
        # Example: inputs = [d_left, d_mid, d_right]; outputs = self.model.predict(inputs)
        raise NotImplementedError("NeuralNetworkController is not implemented yet")

    @property
    def genome(self) -> List[float]:
        # to be defined if model parameters are to be evolved
        return []

    def set_genome(self, genome: List[float]) -> None:
        # load parameters into model if appropriate
        pass