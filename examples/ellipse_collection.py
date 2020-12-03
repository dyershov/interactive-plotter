def main():
    import interactive_plotter as ip

    import itertools
    import numpy as np

    x = np.linspace(-10, 10, 8)
    y = np.linspace(-10, 10, 6)
    delta_x = x[1] - x[0]
    delta_y = y[1] - y[0]
    box_x = x[-1] - x[0]
    box_y = y[-1] - y[0]
    time_step = 1/60
    delta_angle = np.pi * time_step

    xy_flat = itertools.chain.from_iterable(itertools.starmap(lambda y, x: (x, y), itertools.product(y, x)))

    xy = np.fromiter(xy_flat, dtype=np.float64).reshape((x.size * y.size, 2))

    x = xy[:,0]
    y = xy[:,1]

    angle = 0.25 * np.pi
    w = np.ones(xy.shape[0]) * delta_x
    h = np.ones(xy.shape[0]) * delta_x * delta_x / delta_y
    c = (x / box_x)*3 + (y / box_y) + np.sin(angle)

    iFig = ip.InteractiveFigure()
    iAx = iFig.get_interactive_axes()
    iEc = iAx.ellipse_collection(x, y, w, h, np.ones(xy.shape[0]) * angle, c, units='x')
    iEc.artist.set_clim((-2., 2.))

    iAx.add_foreground_artist(iEc)

    iAx.axes.autoscale()
    iAx.axes.set_aspect('equal')

    iFig.render(pause=1)
    while True:
        angle += delta_angle
        if angle > 2.75 * np.pi:
            break
        c = (x / box_x)*3 + (y / box_y) + np.sin(angle)
        iEc.plot(widths=w, heights=h, angles=np.ones(xy.shape[0]) * angle, cvalues=c)
        iFig.render(pause=time_step)

if __name__ == '__main__':
    main()

