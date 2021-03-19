class InteractiveArtist:
    def __init__(self, artist):
        self.__artist = artist
        self.__rendered = False

    @property
    def artist(self):
        return self.__artist

    @property
    def rendered(self):
        return self.__rendered

    def render(self):
        self.__artist.axes.draw_artist(self.__artist)
        self.__rendered = True

    def plot(self, **kwargs):
        self.artist.set(**kwargs)
        self.__rendered = False

from .ellipse_collection import *
from .line2d import *
from .line_collection import *
from .poly_collection import *
from .quad_mesh import *
from .quiver import *
from .scatter import *
