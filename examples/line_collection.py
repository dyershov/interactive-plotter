def main():
    import interactive_plotter as ip

    import numpy as np
    import time

    xf = np.linspace(0, 12 * np.pi, 10000)
    x = np.linspace(0, 2 * np.pi, 11)
    time_step = 1/30
    delta_angle = 1 * np.pi * time_step

    angle = 0.5 * np.pi
    xc = x[:-1] + 0.5 * np.diff(x)
    y = np.sin(xc + angle)

    iFig = ip.InteractiveFigure()
    iAx = iFig.get_interactive_axes()
    iAx.plot(xf, np.sin(xf), ':', color='r', label="sin(x)")
    iLc = ip.PiecewiseConstant(x + angle, y, color='k', label="sin step", verticals=True)
    iAx.add_foreground_artist(iLc)
    iAx.axes.autoscale()
    iAx.axes.set_xlim([np.min(x+angle), np.max(x+angle)])
    iAx.legend(loc='upper right')

    iFig.render(pause=1)
    while True:
        angle += delta_angle
        if angle > 4 * np.pi:
            break
        xc = x[:-1] + 0.5 * np.diff(x)
        y = np.sin(xc + angle)
        iLc.plot(x + angle, y)
        iAx.axes.set_xlim([np.min(x+angle), np.max(x+angle)])
        iFig.render(pause=time_step)

if __name__ == '__main__':
    main()

