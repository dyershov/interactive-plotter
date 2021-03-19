from .interactive_artist import InteractiveArtist

class PolyCollection(InteractiveArtist):
    def __init__(self, verts=None, closed=True, **kwargs):
        import numpy as np
        from matplotlib.collections import PolyCollection as __PolyCollection
        if "cvalues" in kwargs:
            cvalues = kwargs.pop("cvalues")
        else:
            cvalues = None
        self.__closed = closed
        if verts is None:
            verts = [[(0.0, 0.0)]]
        artist = __PolyCollection(verts, closed=closed, **kwargs)
        super().__init__(artist)
        if cvalues is not None:
            self.plot(cvalues=cvalues)

    def plot(self, verts=None, closed=None, **kwargs):
        if verts is not None:
            if closed is None:
                closed = self.__closed
            self.artist.set_paths(verts, closed)
        if "cvalues" in kwargs:
            self.artist.set_array(kwargs["cvalues"])
        super().plot()

class BarCollection(PolyCollection):
    def __init__(self, x_bar=None, y_bar=None, **kwargs):
        super().__init__(None if x_bar is None or y_bar is None else self.__get_verts(x_bar, y_bar), closed=True, **kwargs)

    def plot(self, x_bar, y_bar, **kwargs):
        super().plot(self.__get_verts(x_bar, y_bar), **kwargs)

    def __get_verts(self, x_bar, y_bar):
        return [[(x[0], y[0]), (x[0], y[1]), (x[1], y[1]), (x[1], y[0])] for x, y in zip(x_bar, y_bar)]

del InteractiveArtist
