from pylab import *
from mpl_toolkits.mplot3d import Axes3D

s = 10.0
r = 30.0
b = 3.0
Dt = 0.01

x = 1.001
y = 1.0
z = 1.0
t = 0.0

xlist = [x]
ylist = [y]
zlist = [z]
tlist = [t]

while t < 30.0:
    dx = s * (y - x)
    dy = r * x - y - x * z
    dz = x * y - b * z

    x += dx * Dt
    y += dy * Dt
    z += dz * Dt
    t += Dt

    xlist.append(x)
    ylist.append(y)
    zlist.append(z)
    tlist.append(t)

subplot(3, 1, 1)
plot(tlist, xlist, 'r--')
xlabel('t')
ylabel('x')
title('X vs Time')
grid(True)

subplot(3, 1, 2)
plot(tlist, ylist, 'g-.')
xlabel('t')
ylabel('y')
title('Y vs Time')
grid(True)

subplot(3, 1, 3)
plot(tlist, zlist, 'b-')
xlabel('t')
ylabel('z')
title('Z vs Time')
grid(True)

fig = figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(xlist, ylist, zlist, color='purple')
ax.set_title('Атрактор Лоренца')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

show()
