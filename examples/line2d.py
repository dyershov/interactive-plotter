def main():
    import interactive_plotter as ip

    import numpy as np

    x = np.linspace(0, 2 * np.pi, 30)
    time_step = 1/30
    delta_angle = 2 * np.pi * time_step

    angle = 0.0
    y1 = np.sin(x + angle)
    y2 = np.cos(x + angle)

    iFig = ip.InteractiveFigure()
    iAx = iFig.get_interactive_axes()
    iLn1, iLn2 = iAx.plot(x + angle, y1, "xb-", x + angle, y2, "r--")
    iLn1.plot(label='sin(x)')
    iLn2.plot(label='cos(x)')
    iAx.legend(loc='upper right')

    iFig.render(pause=1)
    while True:
        angle += delta_angle
        if angle > 4 * np.pi:
            break
        y1 = np.sin(x + angle)
        y2 = np.cos(x + angle)
        iLn1.plot(x + angle, y1)
        iLn2.plot(x + angle, y2)
        iAx.axes.relim()
        iAx.axes.autoscale_view()
        iFig.render(pause=time_step)

if __name__ == '__main__':
    main()

