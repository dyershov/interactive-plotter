class QuiverPlotter:
    def __init__(self, axes, origins, vectors=None, values=None):
        import numpy as np
        from operator import itemgetter
        x = np.fromiter(map(itemgetter(0), origins), dtype=np.float64)
        y = np.fromiter(map(itemgetter(1), origins), dtype=np.float64)
        try:
            z = np.fromiter(map(itemgetter(2), origins), dtype=np.float64)
        except IndexError:
            z = None
        zeros = np.zeros(x.size)
        if z is None or w is None:
            self.__artist = axes.quiver(x, y, zeros, zeros, scale=1.0, scale_units='x')
        else:
            self.__artist = axes.quiver(x, y, z, zeros, zeros, zeros, scale=1.0, scale_units='x')
        self.__bounding_box = [[min(x), min(y)], [max(x), max(y)]]
        self.__value_limits = (0.0, 1.0)
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

    def plot(self, vectors, values=None):
        import numpy as np
        from operator import itemgetter
        u = np.fromiter(map(itemgetter(0), vectors), dtype=np.float64)
        v = np.fromiter(map(itemgetter(1), vectors), dtype=np.float64)
        try:
            w = np.fromiter(map(itemgetter(2), vectors), dtype=np.float64)
        except IndexError:
            w = None
        c = None if values is None else np.fromiter(values, dtype=np.float64)

        if w is None:
            self.__artist.set_UVC(u, v, c)
        else:
            self.__artist.set_UVC(u, v, w, c)
        self.__rendered = False

    def tighten_clim(self):
        self.set_clim(self.__value_limits)

    def set_clim(self, clim):
        self.__artist.set_clim(clim)
        self.__rendered = False

    def render(self):
        # self.__artist.set_visible(True)
        self.__artist.axes.draw_artist(self.__artist)
        self.__rendered = True
        
