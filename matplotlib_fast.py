import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
def init():
    line.set_data([], [])
    return line,
def update(frame):
    x = np.linspace(0, 10, 100)
    y = np.sin(x + 2 * np.pi * frame / 100)
    line.set_data(x, y)
    return line,
fig, ax = plt.subplots()
line, = ax.plot([], [])
ani = FuncAnimation(fig, update, frames=range(100), init_func=init, blit=True)
plt.show()