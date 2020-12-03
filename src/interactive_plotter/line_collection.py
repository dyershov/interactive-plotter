from .interactive_artist import InteractiveArtist

class LineCollection(InteractiveArtist):
    def __init__(self, segments, **kwargs):
        import numpy as np
        from matplotlib.collections import LineCollection as __LineCollection
        if "cvalues" in kwargs:
            cvalues = kwargs.pop("cvalues")
        else:
            cvalues = None
        artist = __LineCollection(segments, **kwargs)
        super().__init__(artist)
        if cvalues is not None:
            self.plot(cvalues=cvalues)

    def plot(self, segments=None, **kwargs):
        if segments is not None:
            self.artist.set_segments(segments)
        if "cvalues" in kwargs:
            self.artist.set_array(kwargs["cvalues"])
        super().plot()


class PiecewiseConstant(LineCollection):
    def __init__(self, x_bnd, y, **kwargs):
        if 'verticals' in kwargs:
            self.__verticals = kwargs.pop("verticals")
        else:
            self.__verticals=False
        self.__x_bnd = x_bnd
        super().__init__(self.__get_segments(x_bnd, y, self.__verticals), **kwargs)

    def plot(self, x_bnd=None, y=None, **kwargs):
        if "verticals" not in kwargs:
            verticals = self.__verticals
        else:
            verticals=kwargs.pop("verticals")
        x_bnd = self.__x_bnd if x_bnd is None else x_bnd
        super().plot(None if y is None else self.__get_segments(x_bnd, y, verticals), **kwargs)

    def __get_segments(self, x_bnd, y, verticals):
        import itertools
        x_l = itertools.islice(x_bnd, len(x_bnd) - 1)
        x_r = itertools.islice(x_bnd, 1, len(x_bnd))
        if verticals:
            x_2 = itertools.chain.from_iterable(itertools.zip_longest(x_l, x_r))
            y_2 = itertools.chain.from_iterable(itertools.zip_longest(y, y))
            segments = [list(itertools.starmap(lambda x, y: (x,y), itertools.zip_longest(x_2, y_2)))]
        else:
            segments = list(itertools.starmap(lambda x_l, x_r, y: [(x_l, y), (x_r, y)], itertools.zip_longest(x_l, x_r, y)))
        return segments

class ErrorBarPlotter(LineCollection):
    def __init__(self, x, y, e, **kwargs):
        self.__x = x
        self.__y = y
        super().__init__(self.__get_segments(x, y, e), **kwargs)

    def plot(self, x=None, y=None, e=None, **kwargs):
        x = self.__x if x in None else x
        y = self.__y if y in None else y
        super().plot(None if e is None else self.__get_segments(x, y, e), **kwargs)

    def __get_segments(self, x, y, e):
        return list(itertools.starmap(lambda x, y, e: [(x, y-e), (x, y+e)], itertools.zip_longest(x, y, e)))

del InteractiveArtist
