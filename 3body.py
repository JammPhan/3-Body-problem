
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

t = 0
dt = 0.2
G = 0.01
class CelestialObject:
    def __init__(self,mass,p,velocity):
        self.mass = mass
        self.p = p
        self.velocity = velocity
        
class Vector:
    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2
        self.coords = [v1,v2]
        
    def __add__(self,other):
        return Vector(self.v1 + other.v1,self.v2+other.v2)
    
    def __sub__(self,other):
        return Vector(self.v1 - other.v1,self.v2-other.v2)
    
    def __mul__(self,scalar):
        return Vector(self.v1*scalar,self.v2*scalar)
    
    def magnitude(self):
        return math.sqrt(self.v1**2+self.v2**2)
    
    def __getitem__(self,index):
        return self.coords[index]
    
    def __repr__(self):
        return str(self.coords)
    
def distance(p1,p2):
    distance = p1-p2
    return distance.magnitude()  


#finds the acceleration of a planet
def acceleration(m1,m2,p0= Vector,p1 = Vector,p2 = Vector):
    a = ((p0-p1)*(1/(distance(p0,p1)**3))*G*m1 + (p0-p2)*(1/(distance(p0,p2)**3))*G*m2)*-1
    return a

#initialises planets, can change mass,initial position, initial velocity
r1 = CelestialObject(10,Vector(0,-3),Vector(-0.1,0.1))
r2 = CelestialObject(10,Vector(5,0),Vector(0,0))
r3 = CelestialObject(10,Vector(3,10),Vector(0,-0.05))


colours = ['red','blue','yellow']
x = np.array([r1.p[0],r2.p[0],r3.p[0]])
y = np.array([r1.p[1],r2.p[1],r3.p[1]])
x1 = []
y1 = []
x2 = []
y2 = []
x3 = []
y3 = []
fig,ax = plt.subplots()

def update(): 
    x = np.array([r1.p[0],r2.p[0],r3.p[0]])
    y = np.array([r1.p[1],r2.p[1],r3.p[1]])
    ax.scatter(x,y,color = colours)
    x1.append(r1.p[0])
    y1.append(r1.p[1])
    x2.append(r2.p[0])
    y2.append(r2.p[1])
    x3.append(r3.p[0])
    y3.append(r3.p[1])
    ax.plot(x1,y1,color = 'red',linewidth = 2)
    ax.plot(x2,y2,color = 'blue',linewidth =2)
    ax.plot(x3,y3,color = 'yellow', linewidth = 2)
    
    #Calculates the accelerations
    a1 = acceleration(r2.mass,r3.mass,r1.p,r2.p,r3.p)
    a2 = acceleration(r1.mass,r3.mass,r2.p,r1.p,r3.p)
    a3 = acceleration(r1.mass,r2.mass,r3.p,r1.p,r2.p)
    
    #finds velocity using v = u + at
    r1.velocity = r1.velocity+a1*dt
    r2.velocity = r2.velocity+a2*dt
    r3.velocity = r3.velocity+a3*dt
    
    #updates position using s = ut + 1/2*at**2
    r1.p = r1.p + r1.velocity*dt + a1*0.5*dt**2
    r2.p = r2.p + r2.velocity*dt + a2*0.5*dt**2
    r3.p = r3.p + r3.velocity*dt + a3*0.5*dt**2
    
    
def animate(i):
    ax.clear()
    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)
    update()
    
    

ani = FuncAnimation(fig,animate,frames = 1000, interval = 25)
plt.show()
ani.save('3bodyproblem.gif',writer=PillowWriter(fps = 40))



    
