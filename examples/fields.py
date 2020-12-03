def main():
    import interactive_plotter as ip

    import itertools
    import numpy as np

    x = np.linspace(-1, 1, 31)
    y = np.linspace(-1, 1, 29)
    xc = x[:-1] + 0.5 * np.diff(x)
    yc = y[:-1] + 0.5 * np.diff(y)
    time_step = 0.03
    delta_t = time_step

    X, Y = np.meshgrid(x, y)
    Xc, Yc = np.meshgrid(xc, yc)

    def f(x, y):
        return np.sin(x + 3 * y) * np.cos(2 * x - y)

    def df_dx(x, y):
        return np.cos(x + 3 * y) * np.cos(2 * x - y) - 2 * np.sin(x + 3 * y) * np.sin(2 * x - y)

    def df_dy(x, y):
        return 3 * np.cos(x + 3 * y) * np.cos(2 * x - y) + np.sin(x + 3 * y) * np.sin(2 * x - y)

    velocity_x = 1
    velocity_y = 1
    offset_x = 0
    offset_y = 0

    C=f(Xc + offset_x, Yc + offset_y)
    U=df_dx(Xc + offset_x, Yc + offset_y)
    V=df_dy(Xc + offset_x, Yc + offset_y)

    iFig = ip.InteractiveFigure(figsize=(4,4))
    iAx = iFig.get_interactive_axes()
    iAx.axes.axis("off")
    iQr = iAx.vector_field(Xc, Yc, U, V, color='black', scale=10)
    iQm = iAx.scalar_field(X, Y, C)


    iAx.axes.autoscale()
    iAx.axes.set_aspect('equal')

    iFig.render(pause=1)
    index = 0
    while True:
        if offset_y > 2 * np.pi:
            break
        offset_x += velocity_x * delta_t
        offset_y += velocity_y * delta_t
        C=f(Xc + offset_x, Yc + offset_y)
        U=df_dx(Xc + offset_x, Yc + offset_y)
        V=df_dy(Xc + offset_x, Yc + offset_y)
        iQm.plot(C=C)
        iQr.plot(U=U, V=V)
        iFig.render(pause=time_step)
        iFig.savefig('fields.png', index=index, bbox_inches='tight', pad_inches = 0)
        index +=1

if __name__ == '__main__':
    main()

