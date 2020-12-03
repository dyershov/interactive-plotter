from .interactive_artist import InteractiveArtist

class Quiver(InteractiveArtist):
    def __init__(self, artist):
        super().__init__(artist)

    def plot(self, X=None, Y=None, U=None, V=None, C=None, **kwargs):
        import numpy as np
        if X is not None and Y is not None:
            self.artist.set_offsets(np.column_stack((X,Y)))
        if (U is not None and V is not None) or C is not None:
            self.artist.set_UVC(U, V, C)
        super().plot(**kwargs)

del InteractiveArtist
