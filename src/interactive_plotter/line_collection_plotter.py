class LineCollectionPlotter:
    def __init__(self, axes, segments, values = None):
        import numpy as np
        segs = np.array(list(segments), dtype=np.float64)
        from operator import itemgetter
        from itertools import chain
        self.__bounding_box = [[min(map(itemgetter(0), chain(*segs))), min(map(itemgetter(1), chain(*segs)))],
                               [max(map(itemgetter(0), chain(*segs))), max(map(itemgetter(1), chain(*segs)))]]
        self.__value_limits = (0.0, 1.0)

        from matplotlib.collections import LineCollection
        self.__artist = LineCollection(segs)

        self.__set_values(values)
        
        axes.add_collection(self.__artist)

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

    def plot(self, segments=None, values = None):
        import numpy as np
        if segments is not None:
            segs = np.array(list(segments), dtype=np.float64)
            self.__artist.set_segments(segs)
        self.__set_values(values)
        self.__rendered = False

    def tighten_clim(self):
        self.set_clim(self.__value_limits)

    def set_clim(self, clim):
        self.__artist.set_clim(clim)
        self.__rendered = False

    def render(self):
        self.__artist.axes.draw_artist(self.__artist)
        self.__rendered = True

    def __set_values(self, values):
        if values is None:
            return
        import numpy as np
        self.__artist.set_array(values)
        self.__value_limits = (min(values), max(values))
