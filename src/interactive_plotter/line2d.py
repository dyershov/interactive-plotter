from .interactive_artist import InteractiveArtist

class Line2D(InteractiveArtist):
    def __init__(self, artist):
        super().__init__(artist)

    def plot(self, x=None, y=None, **kwargs):
        if y is not None:
            if x is None:
                x, _ = self.artist.get_data(x)
            self.artist.set_data(x, y)
        super().plot(**kwargs)
