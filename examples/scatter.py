def main():
    import interactive_plotter as ip

    import itertools
    import numpy as np

    time_step = 1/30
    delta_t = time_step

    n_points = 1000

    x = np.random.uniform(-1, 4, size=n_points)
    y = np.random.uniform(-1, 2, size=n_points)
    def f(x, y):
        return np.sin(x + 3 * y) * np.cos(2 * x - y)

    velocity_x = 1
    velocity_y = 0.3

    offset_x = 0.0
    offset_y = 0.0
    c = f(x, y)

    iFig = ip.InteractiveFigure()
    iAx = iFig.get_interactive_axes()
    iSc = iAx.scatter(x, y)
    iSc.plot(cvalues=c)
    iAx.axes.set_xlim([-1 + offset_x, 1 + offset_x])
    iAx.axes.set_ylim([-1 + offset_y, 1 + offset_y])

    iFig.render(pause=1)
    while offset_x < 3:
        offset_x += velocity_x * delta_t
        offset_y += velocity_y * delta_t
        iSc.plot(sizes=100*(np.random.uniform(size=n_points) + 0.1))
        iAx.axes.set_xlim([-1 + offset_x, 1 + offset_x])
        iAx.axes.set_ylim([-1 + offset_y, 1 + offset_y])
        iFig.render(pause=time_step)

if __name__ == '__main__':
    main()

