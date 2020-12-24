class DrawHistory:
    def __init__(self, interactive_axes, buffer_depth):
        self.__interactive_axes = interactive_axes
        self.__buffer_depth = buffer_depth

        self.__artist_buffer = list()

    def callback(self, line_2d_artist):
        self.__artist_buffer.append(self.__interactive_axes.plot(line_2d_artist.artist.get_xdata(), line_2d_artist.artist.get_ydata())[0])
        while len(self.__artist_buffer) > self.__buffer_depth:
            interactive_artist = self.__artist_buffer.pop(0)
            self.__interactive_axes.remove_artist(interactive_artist)

def main():
    import interactive_plotter as ip

    import numpy as np

    iFig = ip.InteractiveFigure()
    iAx = iFig.get_interactive_axes()
    iAx.axes.set_xlim([0,1])
    iAx.axes.set_ylim([0,1])
    iAx.axes.set_aspect('equal')
    line_draw = ip.DrawLine2D(iFig, iAx, '-k.')
    hystory = DrawHistory(iAx, 10)
    line_draw.register_callback(hystory.callback)

    iFig.render(pause=0.01)
    while True:
        iFig.render(pause=0.01)

if __name__ == '__main__':
    main()
