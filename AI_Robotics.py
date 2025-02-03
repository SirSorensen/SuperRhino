from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

left_wheel = Port(hub.)



while True:
    # Turn the light on at 100% brightness.
    hub.light.on(Color(h=0, s=100, v=100))
    hub.speaker.beep(10)
    wait(500)

    # Turn the light off.
    hub.light.off()
    wait(500)

