class InteractiveAxes:
    def __init__(self, axes):
        self.__axes = axes
        self.__foreground_artists = set()
        self.__background_artists = set()
        self.__background = None
        self.__zorder = 0

    @property
    def axes(self):
        return self.__axes

    @property
    def rendered(self):
        from itertools import chain
        return all([artist.rendered for artist in chain(self.__background_artists, self.__foreground_artists)])

    def render(self):
        from itertools import chain
        for artist in chain(self.__background_artists, self.__foreground_artists):
            artist.render()

    def move_to_background(self, artist):
        try:
            self.__foreground_artists.remove(artist)
            self.__background_artists.add(artist)
            artist.artist.set_animated(False)
        except KeyError:
            print("Artist ", artist, " is not in foreground")

    def move_to_foreground(self, artist):
        try:
            self.__background_artists.remove(artist)
            self.__foreground_artists.add(artist)
            artist.artist.set_animated(True)
        except KeyError:
            print("Artist ", artist, " is not in background")

    def save_background(self):
        self.__background = self.__axes.figure.canvas.copy_from_bbox(self.__axes.bbox)

    def restore_background(self):
        if self.__background is None:
            self.save_background()
            return False
        self.__axes.figure.canvas.restore_region(self.__background)
        return True

    def add_foreground_artist(self, interactive_artist):
        from matplotlib.collections import Collection
        from matplotlib.container import Container
        from matplotlib.collections import EllipseCollection
        from matplotlib.image import AxesImage
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch
        if isinstance(interactive_artist.artist, Collection):
            if isinstance(interactive_artist.artist, EllipseCollection):
                interactive_artist.artist._transOffset = self.__axes.transData
            self.__axes.add_collection(interactive_artist.artist)
        elif isinstance(interactive_artist.artist, Container):
            self.__axes.add_container(interactive_artist.artist)
        elif isinstance(interactive_artist.artist, AxesImage):
            self.__axes.add_image(interactive_artist.artist)
        elif isinstance(interactive_artist.artist, Line2D):
            self.__axes.add_line(interactive_artist.artist)
        elif isinstance(interactive_artist.artist, Patch):
            self.__axes.add_patch(interactive_artist.artist)
        else:
            print("Unsupported artist instance: ", type(interactive_artist.artist))
            return
        self.__add_foreground_artist(interactive_artist)

    def __add_foreground_artist(self, artist):
        self.__foreground_artists.add(artist)
        artist.artist.set_animated(True)
        artist.artist.set_zorder(self.__zorder)
        self.__zorder += 1

    def plot(self, *args, **kwargs):
        from interactive_plotter.interactive_artist import Line2D
        artist_list = self.axes.plot(*args, **kwargs)
        interactive_line2d_list = list()
        for artist in artist_list:
            interactive_line2d = Line2D(artist)
            interactive_line2d_list.append(interactive_line2d)
            self.__add_foreground_artist(interactive_line2d)
        return interactive_line2d_list

    def scatter(self, x, y, **kwargs):
        from interactive_plotter.interactive_artist import Scatter
        artist = self.axes.scatter(x, y, **kwargs)
        interactive_artist = Scatter(artist)
        self.__add_foreground_artist(interactive_artist)
        return interactive_artist

    def pcolormesh(self, *args, **kwargs):
        from interactive_plotter.interactive_artist import QuadMesh
        artist = self.axes.pcolormesh(*args, **kwargs)
        interactive_artist = QuadMesh(artist)
        self.__add_foreground_artist(interactive_artist)
        return interactive_artist

    def quiver(self, *args, **kwargs):
        from interactive_plotter.interactive_artist import Quiver
        artist = self.axes.quiver(*args, **kwargs)
        interactive_artist = Quiver(artist)
        self.__add_foreground_artist(interactive_artist)
        return interactive_artist

    def ellipse_collection(self, x, y, widths, heights, angles, cvalues=None, **kwargs):
        import numpy as np
        from interactive_plotter.interactive_artist import EllipseCollection
        from matplotlib.collections import EllipseCollection as __EllipseCollection
        artist = __EllipseCollection([0] * x.size, [0] * x.size, [0] * x.size, offsets=np.zeros((x.size, 2)), transOffset=self.__axes.transData, **kwargs)
        self.__axes.add_collection(artist)
        interactive_artist = EllipseCollection(artist)
        interactive_artist.plot(x, y, widths, heights, angles, cvalues)
        self.__add_foreground_artist(interactive_artist)
        return interactive_artist

    def scalar_field(self, *args, **kwargs):
        return self.pcolormesh(*args, **kwargs)

    def vector_field(self, *args, **kwargs):
        kwargs["angles"] = "xy"
        if "scale" not in kwargs:
            kwargs["scale"] = 1
        kwargs["scale_units"] = "xy"
        return self.quiver(*args, **kwargs)

    def tensor_field(self, x, y, tensors, cvalues=None, **kwargs):
        import numpy as np
        from interactive_plotter.interactive_artist import TensorField
        from matplotlib.collections import EllipseCollection as __EllipseCollection
        if "ec" not in kwargs and "edgecolor" not in kwargs:
            kwargs["edgecolor"] = "black"
        if "fc" not in kwargs and "facecolor" not in kwargs:
            kwargs["facecolor"] = "none"
        kwargs["units"]="xy"
        artist = __EllipseCollection([0] * x.size, [0] * x.size, [0] * x.size, offsets=np.zeros((x.size, 2)), transOffset=self.__axes.transData, **kwargs)
        self.__axes.add_collection(artist)
        interactive_artist = TensorField(artist)
        interactive_artist.plot(x, y, tensors, cvalues)
        self.__add_foreground_artist(interactive_artist)
        return interactive_artist

    def legend(self, *args, **kwargs):
        artist = self.axes.legend(*args, **kwargs)
        # TODO: make legend interactive
        return artist
