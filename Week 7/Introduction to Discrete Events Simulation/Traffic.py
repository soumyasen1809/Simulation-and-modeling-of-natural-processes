# Coursera - Simulation and modeling of natural processes - Discrete Event Simulation

# Importing Libraries
import heapq

# Defining parameters
Tp = 10 # Time taken by 1 car to pass the traffic light
Tc = 30 # Latency to change traffic light

# Defining the State of traffic


class State:
    def __init__(self):
        self.cars = 0
        self.green = False

    def already_green(self):                        # Check if signal is already green
        return self.green

    def turn_green(self):                           # Turn to green signal
        self.green = True

    def turn_red(self):                             # Turn to red signal
        self.green = False

    def insert_car(self):                           # Add one car
        self.cars = self.cars + 1

    def remove_car(self):                           # Remove all cars
        self.cars = 0

    def waiting_cars(self):                         # Number of cars waiting in the queue
        return self.cars

    def __str__(self):
        return "Green light status is: " + str(self.green) + "Number of cars are: " + str(self.cars)

# Defining an event


class Event:
    def time(self):
        return self.time

    def __str__(self):
        return self.name + "(" + str(self.time) + ")"

    def __lt__(self, other):
        return self.time < other.time


class Car(Event):
    def __init__(self, time):
        self.time = time
        self.name = "Car"

    def action(self, queue, state):
        if not state.already_green():
            state.insert_car()
            if state.waiting_cars() == 1:
                queue.push(Red2Green(self.time + Tc))


class Red2Green(Event):                                 # Traffic signal turning from red to green
    def __init__(self, time):
        self.time = time
        self.name = "Red2Green"

    def action(self, queue, state):
        queue.push(Green2Red(self.time + Tp * state.waiting_cars()))
        state.turn_green()                              # turn signal to green
        state.remove_car()                              # clear all cars


class Green2Red(Event):                                 # Traffic signal turning from green to red
    def __init__(self, time):
        self.time = time
        self.name = "Green2Red"

    def action(self, queue, state):
        state.turn_red()                                # turn signal to red


# Defining the queue


class Queue:
    def __init__(self):
        self.q = []

    def push(self, event):
        heapq.heappush(self.q, event)                   # pushing in a heap data structure

    def pop(self):
        return heapq.heappop(self.q)                    # popping out from a heap data structure

    def notempty(self):
        return len(self.q)


# Adding cars to simulate
Q = Queue()                                             # Defining a heap for First In First Out
Q.push(Car(10))
Q.push(Car(25))
Q.push(Car(35))
Q.push(Car(60))
Q.push(Car(75))

S = State()

# Processing events until the queue is empty
while Q.notempty() > 0:
    e = Q.pop()
    print(e)
    e.action(Q,S)
