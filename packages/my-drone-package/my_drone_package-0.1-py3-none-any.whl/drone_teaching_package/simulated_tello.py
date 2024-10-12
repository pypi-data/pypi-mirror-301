# simulated_tello.py
from DroneBlocksTelloSimulator import SimulatedDrone

class EasyTelloToSimulatedDrone:
    def __init__(self, simulator_key):
        self.drone = SimulatedDrone(simulator_key=simulator_key)

    def connect(self):
        print("Connecting to the simulated drone...")
        self.drone.connect()

    def takeoff(self):
        print("Taking off!")
        self.drone.takeoff()

    def land(self):
        print("Landing!")
        self.drone.land()

    def up(self, dist: int):
        print(f"Moving up {dist} cm")
        self.drone.fly_up(dist, "cm")

    def down(self, dist: int):
        print(f"Moving down {dist} cm")
        self.drone.fly_down(dist, "cm")

    def left(self, dist: int):
        print(f"Moving left {dist} cm")
        self.drone.fly_left(dist, "cm")

    def right(self, dist: int):
        print(f"Moving right {dist} cm")
        self.drone.fly_right(dist, "cm")

    def forward(self, dist: int):
        print(f"Moving forward {dist} cm")
        self.drone.fly_forward(dist, "cm")

    def back(self, dist: int):
        print(f"Moving backward {dist} cm")
        self.drone.fly_backward(dist, "cm")

    def cw(self, degrees: int):
        print(f"Rotating clockwise {degrees} degrees")
        self.drone.yaw_right(degrees)

    def ccw(self, degrees: int):
        print(f"Rotating counterclockwise {degrees} degrees")
        self.drone.yaw_left(degrees)

    def flip(self, direction: str):
        if direction == "l":
            print("Flipping left")
            self.drone.flip_left()
        elif direction == "r":
            print("Flipping right")
            self.drone.flip_right()
        elif direction == "f":
            print("Flipping forward")
            self.drone.flip_forward()
        elif direction == "b":
            print("Flipping backward")
            self.drone.flip_backward()

    def set_speed(self, speed: int):
        print(f"Setting speed to {speed} cm/s")
        self.drone.set_speed(speed)

    def get_battery(self):
        print("Getting battery level...")
        return "100%"  # Simulated battery level

    def go(self, x: int, y: int, z: int, speed: int):
        print(f"Flying to coordinates ({x}, {y}, {z}) with speed {speed}")
        self.drone.fly_to_xyz(x, y, z, "cm")

    def curve(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, speed: int):
        print(f"Flying in a curve from ({x1}, {y1}, {z1}) to ({x2}, {y2}, {z2}) at speed {speed} cm/s")
        self.drone.fly_curve(x1, y1, z1, x2, y2, z2, "cm")
