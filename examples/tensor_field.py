def main():
    import interactive_plotter as ip

    import itertools
    import numpy as np

    x = np.linspace(-10, 10, 9)
    y = np.linspace(-10, 10, 7)
    delta_x = x[1] - x[0]
    delta_y = y[1] - y[0]
    box_x = x[-1] - x[0]
    box_y = y[-1] - y[0]
    time_step = 1/30
    delta_angle = 0.5 * np.pi * time_step

    xy_flat = itertools.chain.from_iterable(itertools.starmap(lambda y, x: (x, y), itertools.product(y, x)))

    xy = np.fromiter(xy_flat, dtype=np.float64).reshape((x.size * y.size, 2))

    x = xy[:,0]
    y = xy[:,1]

    w = delta_x * 1.2
    h = delta_y * 0.6

    angle = 0.75 * np.pi
    R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    SPD = np.dot(R, np.dot(np.array([[w * w, 0], [0, h * h]]), R.T))
    scale = 0.8 * (np.abs(np.sin(angle)) + 1)
    tensors = np.ones(shape=(x.size, 3), dtype=np.float64)
    tensors[:,0] *= SPD[0,0] * scale
    tensors[:,1] *= SPD[0,1] * scale
    tensors[:,2] *= SPD[1,1] * scale

    iFig = ip.InteractiveFigure()
    iAx = iFig.get_interactive_axes()
    iSPD = iAx.tensor_field(x, y, tensors)

    iAx.add_foreground_artist(iSPD)
    iAx.axes.autoscale()

    iFig.render(pause=1)
    while True:
        angle += delta_angle
        if angle > 3.25 * np.pi:
            break
        R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        SPD = np.dot(R, np.dot(np.array([[w * w, 0], [0, h * h]]), R.T))
        scale = 0.8*(np.abs(np.sin(angle)) + 1)
        tensors = np.ones(shape=(x.size, 3), dtype=np.float64)
        tensors[:,0] *= SPD[0,0] * scale
        tensors[:,1] *= SPD[0,1] * scale
        tensors[:,2] *= SPD[1,1] * scale
        iSPD.plot(tensors=tensors)
        iFig.render(pause=time_step)

if __name__ == '__main__':
    main()

