from .interactive_artist import InteractiveArtist

class Scatter(InteractiveArtist):
    def __init__(self, artist):
        super().__init__(artist)

    def plot(self, x=None, y=None, **kwargs):
        import numpy as np
        if x is not None and y is not None:
            if len(x) is 0 or len(y) is 0:
                self.artist.set_offsets(np.array([[1.e+300,1.e+300]]))
            else:
                self.artist.set_offsets(np.array([[_x,_y] for _x, _y in zip(x,y)]))
        if "cvalues" in kwargs:
            self.artist.set_array(kwargs["cvalues"])
        if "sizes" in kwargs:
            self.artist.set_sizes(kwargs["sizes"])
        super().plot()

del InteractiveArtist
