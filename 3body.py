import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
import numpy as np
from numpy import random
from matplotlib.animation import FuncAnimation


t = 0
# gravitational constant and delta time
dt = 0.1
G = 6.67348 * 10**-11


class CelestialObject:
    def __init__(self, mass, p, velocity, radius):
        self.mass = mass
        self.p = p
        self.velocity = velocity
        self.radius = radius


class Vector:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.coords = [v1, v2, v3]

    def __add__(self, other):
        return Vector(self.v1 + other.v1, self.v2 + other.v2, self.v3 + other.v3)

    def addScalar(self, scalar):
        return Vector(self.v1 + scalar, self.v2 + scalar, self.v3 + scalar)

    def subScalar(self, scalar):
        return Vector(self.v1 - scalar, self.v2 - scalar, self.v3 - scalar)

    def __sub__(self, other):
        return Vector(self.v1 - other.v1, self.v2 - other.v2, self.v3 - other.v3)

    def __mul__(self, scalar):
        return Vector(self.v1 * scalar, self.v2 * scalar, self.v3 * scalar)

    def magnitude(self):
        return math.sqrt(self.v1**2 + self.v2**2 + self.v3**2)

    def __getitem__(self, index):
        return self.coords[index]

    def __repr__(self):
        return str(self.coords)


def distance(body1, body2):
    distance = body1.p - body2.p
    return distance


# finds the acceleration of a planet
def acceleration(body1, body2, body3):
    a = (
        distance(body1, body2)
        * (
            1
            / (
                (distance(body1, body2).magnitude())
                * (distance(body1, body2).magnitude() - (body1.radius + body2.radius))
                ** 2
            )
        )
        * G
        * body1.mass
        + distance(body1, body3)
        * (
            1
            / (
                (distance(body1, body3).magnitude())
                * (distance(body1, body3).magnitude() - (body1.radius + body3.radius))
                ** 2
            )
        )
        * G
        * body3.mass
    ) * -1
    return a


# initialises planets, can change mass,initial position, initial velocity
Sun = CelestialObject(10, Vector(0, 0, 0), Vector(0.04, 0, 0), 3)
Earth = CelestialObject(10, Vector(5, 0, 0), Vector(0, 0.02, 0), 1)
Moon = CelestialObject(10, Vector(10, 4, -1), Vector(0.03, 0, 0.02), 1)

print(distance(Sun, Earth))
# Sun = CelestialObject(
#     1.988420392 * (10**30), Vector(0, 0, 0), Vector(0, 0, 0), 696340 * (10**3)
# )
# Earth = CelestialObject(
#     5.972 * (10**30),
#     Vector(-0.012083728, -1.394770664, -0.604680716) * (10**11),
#     Vector(2.930141099, -0.032094528, -0.013869403) * (10**4),
#     6371 * (10**3),
# )
# Moon = CelestialObject(
#     7.345828157 * (10**22),
#     Vector(-0.015537064, -1.395982236, -0.605576290) * (10**11),
#     Vector(2.967343467, -0.121872473, -0.051163801) * (10**4),
#     1737 * (10**3),
# )


colours = ["yellow", "blue", "gray"]
x = np.array([Sun.p[0], Earth.p[0], Moon.p[0]])
y = np.array([Sun.p[1], Earth.p[1], Moon.p[1]])
z = np.array([Sun.p[2], Earth.p[2], Moon.p[2]])

x1 = []
y1 = []
z1 = []
x2 = []
y2 = []
z2 = []
x3 = []
y3 = []
z3 = []
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax = plt.axes(projection="3d")


def update():
    global t
    t += 1

    x = np.array([Sun.p[0], Earth.p[0], Moon.p[0]])
    y = np.array([Sun.p[1], Earth.p[1], Moon.p[1]])
    z = np.array([Sun.p[2], Earth.p[2], Moon.p[2]])
    ax.scatter3D(x, y, z, color=colours)
    x1.append(Sun.p[0])
    y1.append(Sun.p[1])
    z1.append(Sun.p[2])
    x2.append(Earth.p[0])
    y2.append(Earth.p[1])
    z2.append(Earth.p[2])
    x3.append(Moon.p[0])
    y3.append(Moon.p[1])
    z3.append(Moon.p[2])
    ax.plot3D(x1, y1, z1, color="red", linewidth=2)
    ax.plot3D(x2, y2, z2, color="blue", linewidth=2)
    ax.plot3D(x3, y3, z3, color="gray", linewidth=2)

    # Calculates the accelerations
    a1 = acceleration(Sun, Earth, Moon)
    a2 = acceleration(Earth, Sun, Moon)
    a3 = acceleration(Moon, Earth, Sun)

    # finds velocity using v = u + at
    Sun.velocity = Sun.velocity + a1 * dt
    Earth.velocity = Earth.velocity + a2 * dt
    Moon.velocity = Moon.velocity + a3 * dt

    # updates position using s = ut + 1/2*at**2
    # Sun.p = Sun.p + Sun.velocity * dt + a1 * 0.5 * dt**2
    Earth.p = Earth.p + Earth.velocity * dt + a2 * 0.5 * dt**2
    Moon.p = Moon.p + Moon.velocity * dt + a3 * 0.5 * dt**2


def animate(i):
    ax.clear()
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    update()


ani = FuncAnimation(fig, animate, frames=range(100), interval=20)
plt.show()
# ani.save("3bodyproblem.mp4", writer="ffmpeg")
# saves the animation as gif
# increase frames range to increase animation duration
