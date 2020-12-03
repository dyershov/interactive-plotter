from .interactive_artist import InteractiveArtist

class QuadMesh(InteractiveArtist):
    def __init__(self, artist):
        super().__init__(artist)

    def plot(self, X=None, Y=None, C=None):
        if X is not None and Y is not None:
            import numpy as np
            self.artist.set_offsets(np.column_stack((X.ravel, Y.ravel)))
        if C is not None:
            self.artist.set_array(C)

del InteractiveArtist
