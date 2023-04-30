class QuadMeshPlotter:
    def __init__(self, axes, vertex_coordinates, shape, colors=None):
        import numpy as np
        from operator import itemgetter
        x = np.fromiter(map(itemgetter(0), vertex_coordinates), dtype=np.float64)
        y = np.fromiter(map(itemgetter(1), vertex_coordinates), dtype=np.float64)
        self.__bounding_box = [[min(x), min(y)], [max(x), max(y)]]
        shape = np.array(shape)[::-1]
        x = x.reshape(shape + 1)
        y = y.reshape(shape + 1)
        self.__artist = axes.pcolormesh(x, y, np.zeros(shape))
        self.__value_limits = (0.0, 1.0)
        if colors is not None:
            self.plot(colors)
        self.__rendered = False

    @property
    def artist(self):
        return self.__artist

    @property
    def rendered(self):
        return self.__rendered

    @property
    def bounding_box(self):
        return self.__bounding_box

    def plot(self, values):
        import numpy as np
        values = np.fromiter(values, dtype=np.float64)
        self.__value_limits = (min(values), max(values))
        self.__artist.set_array(values)
        self.__rendered = False

    def tighten_clim(self):
        self.set_clim(self.__value_limits)

    def set_clim(self, clim):
        self.__artist.set_clim(clim)
        self.__rendered = False

    def render(self):
        self.__artist.axes.figure.draw_artist(self.__artist)
        self.__rendered = True
        
