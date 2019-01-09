import matplotlib.animation as animation
import matplotlib.pyplot as plt

import numpy as np


plt.style.use('dark_background')

fig = plt.figure()
fig.set_dpi(100)
ax1 = fig.add_subplot(1, 1, 1)
# x axis
x0 = np.linspace(-3 * np.pi, 3 * np.pi, 10000)

#  Initial time
t0 = 0

#  Increment
dt = 0.1
v = 3


def u(x, t):
    return 0.5 * (np.cos(x + v * t) + np.cos(x - v * t))


a = []
si = []
co = []

for i in range(500):
    value = u(x0, t0)
    s = 0.5 * np.cos(x0 + v * t0)
    c = 0.5 * np.cos(x0 - v * t0)
    t0 = t0 + dt
    a.append(value)
    si.append(s)
    co.append(c)

k = 0


def animate(i):
    global k
    x = a[k]
    k += 1
    ax1.clear()
    plt.plot(x0, x, color='cyan')
    plt.plot(x0, si[k], color='red')
    plt.plot(x0, co[k], color='green')
    plt.grid(True)
    plt.ylim([-2, 2])


anim = animation.FuncAnimation(fig, animate, frames=360, interval=1)
plt.show()
