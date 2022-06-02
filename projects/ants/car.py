# Note that this simulation does not currently support multiple cars on a single course.
from time import sleep
import sys

class Color():
    GREEN, YELLOW, RED = "Green", "Yellow", "Red"
    GO, STOP = GREEN, RED
    NONE = "White"
    CAR = BLUE = "Blue"
    codes = {GREEN: "\033[92m", YELLOW: "\033[93m", RED: "\033[91m", NONE: "\033[0m", CAR: "\033[38;5;6m"}

class TrafficLight():

    lights = (Color.GREEN, Color.YELLOW, Color.RED)

    def __init__(self, signal=Color.GREEN):
        assert signal in self.lights, "Invalid TrafficLight color"
        self.index = self.lights.index(signal)
        self.signal = signal

    def cycle(self):
        self.index = (self.index + 1) % len(self.lights)
        self.signal = self.lights[self.index]

    def __str__(self):
        return f"{Color.codes[self.signal]}{self.signal[0]}{Color.codes[Color.NONE]}"

class StopSign(TrafficLight):

    lights = (Color.RED,)

    def __init__(self):
        TrafficLight.__init__(self, Color.RED)

    def __str__(self):
        return f"{Color.codes[self.signal]}S{Color.codes[Color.NONE]}"

class Road(TrafficLight):

    lights = (Color.GREEN,)

    def __init__(self):
        TrafficLight.__init__(self, Color.GREEN)

    def __str__(self):
        return "-"

class Course():

    def __init__(self, *args):
        self.course = list(args)

    def __str__(self):
        result = ""
        for obj in self.course:
            if isinstance(obj, Car):
                result += f"{Color.codes[Color.CAR]}*{Color.codes[Color.NONE]}"
            else:
                result += str(obj)
        return "[" + result + "]"

    def __len__(self):
        return len(self.course) - len([obj for obj in self.course if isinstance(obj, Car)])

    def remove(self, el):
        self.course.remove(el)

    def insert(self, index, el):
        self.course.insert(index, el)

    def get(self):
        return self.course

def simulate(course, car):
    while True:
        print(course)
        try:
            car.drive()
        except AssertionError:
            print("Simulation complete!")
            break
        for obj in course.course:
            if not (obj is car):
                obj.cycle()
        sleep(0.5)

class Car():
    """A Car is a vehicle that can move through a course."""

    def __init__(self, course, owner=None, manufacturer=None, year=None, gas=100):
        self.owner = owner
        self.manufacturer = manufacturer
        self.year = year
        self.course = course
        self.gas = gas
        self.pos = 0
        self.course.insert(self.pos, self)

    def _move(self):
        self.pos += 1
        self.gas -= 5
        self.course.remove(self)
        self.course.insert(self.pos, self)

    def refuel(self):
        self.gas = 100

    def infront(self):
        front = self.course.get()[min(self.pos + 1, len(self.course) - 1)]
        if isinstance(front, TrafficLight):
            return front
        return Road()

    def __str__(self):
        return f"{self.owner}'s {self.manufacturer}"

    def drive(self):
        """Advance this Car one space forward."""
        assert self.pos < len(self.course), "Finished the course"
        assert self.gas > 0, "Out of gas"
        self._move()

def speed_up(car, drive):
    """Returns a new drive method that allows car to drive twice as fast."""
    "*** YOUR CODE HERE ***"
    def speed_drive():
        drive()
        drive()
    return speed_drive

def alt_speed(car, drive):
    """Returns a new drive method that allows car to alternate between fast
       driving and slow driving."""
    "*** YOUR CODE HERE ***"
    fast_drive = speed_up(car, drive)
    count = 0
    def alt_drive():
        nonlocal count
        if count % 2 == 0:
            fast_drive()
        else:
            drive()
        count += 1
    return alt_drive

def follow_laws(car, drive):
    """Returns a new drive method that makes car abide by driving laws.
    This was not included in the video."""
    waiting = False
    def legal_drive():
        nonlocal waiting
        if not waiting:
            signal = car.infront().signal
            if signal == Color.STOP:
                waiting = True
            else:
                drive()
        else:
            waiting = False
            drive()
    return legal_drive

def main():
    course = Course(Road(), Road(), Road(), Road(), Road(), Road(), Road(), Road())
    """ 
    # Uncomment to try a course with StopSigns and TrafficLights.
    course = Course(Road(), Road(), StopSign(), Road(), TrafficLight(), Road(), Road(), Road())
    """
    my_car = Car(course)
    my_car.drive = alt_speed(my_car, my_car.drive)
    """
    # Uncomment this to make the car abide by driving laws.
    my_car.drive = follow_laws(my_car, my_car.drive)
    """
    simulate(course, my_car)

main()
