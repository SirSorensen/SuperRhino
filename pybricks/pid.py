
# Developed with inspiration from https://softinery.com/blog/implementation-of-pid-controller-in-python/

class PidController:
    def __init__(self, K_p = 0, K_i = 0, K_d = 0):
        self.K_p = K_p
        self.K_i = K_i
        self.K_d = K_d

        # For self.I()
        self.prev_i = -1 * 10**10

        # For self.D()
        self.prev_t = 0
        self.prev_e = 0

    # Error = Difference between process variable and setpoint
    def error(self):
        return self.process_variable - self.setpoint

    # Proportional
    def P(self):
        return self.K_p * self.error()

    # Integral
    def I(self, cur_t):
        cur_i = self.K_i * self.error() * (cur_t - self.prev_t)
        self.prev_i = self.prev_i + cur_i
        return self.prev_i

    # Derivative
    def D(self, cur_t):
        result = self.K_d * (self.error() - self.prev_e) / (cur_t)
        return result

    # Output = The result of the PID calculation to act. upon the system.
    def output(self, cur_t, process_variable, setpoint, offset):
        # Process Variable = Current level of in the vessel
        self.process_variable = process_variable
        # Setpoint = The level we want out vessel to be (Manuelly entered)
        self.setpoint = setpoint
        result = offset + self.P() + self.I(cur_t) + self.D(cur_t)

        self.prev_d = self.error()
        self.prev_t = cur_t
        return result


