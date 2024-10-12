# real_tello.py
from easytello import Tello

class EasyTelloRealDrone:
    def __init__(self):
        self.drone = Tello()

    def connect(self):
        print("Connecting to the real Tello drone...")

    def takeoff(self):
        print("Taking off!")
        self.drone.takeoff()

    def land(self):
        print("Landing!")
        self.drone.land()

    def up(self, dist: int):
        print(f"Moving up {dist} cm")
        self.drone.up(dist)

    def down(self, dist: int):
        print(f"Moving down {dist} cm")
        self.drone.down(dist)

    def left(self, dist: int):
        print(f"Moving left {dist} cm")
        self.drone.left(dist)

    def right(self, dist: int):
        print(f"Moving right {dist} cm")
        self.drone.right(dist)

    def forward(self, dist: int):
        print(f"Moving forward {dist} cm")
        self.drone.forward(dist)

    def back(self, dist: int):
        print(f"Moving backward {dist} cm")
        self.drone.back(dist)

    def cw(self, degrees: int):
        print(f"Rotating clockwise {degrees} degrees")
        self.drone.cw(degrees)

    def ccw(self, degrees: int):
        print(f"Rotating counterclockwise {degrees} degrees")
        self.drone.ccw(degrees)

    def flip(self, direction: str):
        print(f"Flipping {direction}")
        self.drone.flip(direction)

    def set_speed(self, speed: int):
        print(f"Setting speed to {speed} cm/s")
        self.drone.set_speed(speed)

    def get_battery(self):
        print("Getting battery level...")
        return self.drone.get_battery()

    def go(self, x: int, y: int, z: int, speed: int):
        print(f"Flying to coordinates ({x}, {y}, {z}) with speed {speed}")
        self.drone.go(x, y, z, speed)

    def curve(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, speed: int):
        print(f"Flying in a curve from ({x1}, {y1}, {z1}) to ({x2}, {y2}, {z2}) at speed {speed}")
        self.drone.curve(x1, y1, z1, x2, y2, z2, speed)
