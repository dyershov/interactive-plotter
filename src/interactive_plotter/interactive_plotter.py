class InteractiveAxes:
    def __init__(self, axes):
        self.__axes = axes
        self.__background_plotters = set()
        self.__plotters = set()
        self.__background = None

    @property
    def axes(self):
        return self.__axes

    @property
    def rendered(self):
        from itertools import chain
        return all([plotter.rendered for plotter in chain(self.__background_plotters, self.__plotters)])

    def render(self):
        from itertools import chain
        for plotter in chain(self.__background_plotters, self.__plotters):
            plotter.render()

    def tighten_view_box(self, aspect='auto'):
        view_box = None
        from itertools import chain
        for plotter in chain(self.__background_plotters, self.__plotters):
            if view_box is None:
                view_box = plotter.bounding_box
                continue
            bounding_box = plotter.bounding_box
            view_box[0][0] = min(view_box[0][0], bounding_box[0][0])
            view_box[0][1] = min(view_box[0][1], bounding_box[0][1])
            view_box[1][0] = max(view_box[1][0], bounding_box[1][0])
            view_box[1][1] = max(view_box[1][1], bounding_box[1][1])
        if view_box is not None:
            self.set_view_box(view_box, aspect)

    def set_view_box(self, view_box, aspect='auto'):
        self.__axes.set_xbound(view_box[0][0], view_box[1][0])
        self.__axes.set_ybound(view_box[0][1], view_box[1][1])
        self.__axes.set_aspect(aspect)

    def get_view_box(self):
        x_bnd = self.__axes.get_xbound()
        y_bnd = self.__axes.get_ybound()
        return [[x_bnd[0], y_bnd[0]], [x_bnd[1], y_bnd[1]]], self.__axes.get_aspect()
        
    def move_to_background(self, plotter):
        try:
            self.__plotters.remove(plotter)
            self.__background_plotters.add(plotter)
            plotter.artist.set_animated(False)
        except KeyError:
            print("Plotter ", plotter, " is not in foreground")

    def move_to_foreground(self, plotter):
        try:
            self.__background_plotters.remove(plotter)
            self.__plotters.add(plotter)
            plotter.artist.set_animated(True)
        except KeyError:
            print("Plotter ", plotter, " is not in background")

    def save_background(self):
        self.__background = self.__axes.figure.canvas.copy_from_bbox(self.__axes.bbox)
        print(self.__axes, self.__axes.bbox, self.__background)

    def restore_background(self):
        if self.__background is None:
            self.save_background()
            return False
        print(self.__axes, self.__background)
        self.__axes.figure.canvas.restore_region(self.__background)
        return True
        
    # def add_function_plotter(self, function_space):
    #     from .function_plotter import FunctionPlotter
    #     plotter = FunctionPlotter(self.__axes, function_space)
    #     self.__plotters.add(plotter)
    #     return plotter

    # def add_scatter_scalar_plotter(self, points):
    #     from .scalar_plotter import ScatterPlotter
    #     plotter = ScatterPlotter(self.__axes, points)
    #     self.__plotters.add(plotter)
    #     return plotter

    # def add_mesh_scalar_plotter(self, mesh):
    #     from .scalar_plotter import MeshPlotter
    #     plotter = MeshPlotter(self.__axes, mesh)
    #     self.__plotters.add(plotter)
    #     return plotter
    
    # def add_vector_plotter(self, dimension_number, points):
    #     from .vector_plotter import VectorPlotter
    #     plotter = VectorPlotter(self.__axes, dimension_number, points)
    #     self.__plotters.add(plotter)
    #     return plotter

    def add_plotter(self, PlotterBuilder, *args):
        plotter = PlotterBuilder(self.__axes, *args)
        self.__plotters.add(plotter)
        plotter.artist.set_animated(True)
        return plotter
    
class InteractiveFigure:
    def __init__(self, nrows=1, ncols=1):
        import matplotlib.pyplot as plt
        self.__fig, axs = plt.subplots(nrows=nrows, ncols=ncols)
        
        if nrows==1 and ncols==1:
            self.__interactive_axes_collection = [[InteractiveAxes(axs)]]
        elif nrows==1:
            self.__interactive_axes_collection = [[InteractiveAxes(ax) for ax in axs]]
        elif ncols==1:
            self.__interactive_axes_collection = [[InteractiveAxes(ax)] for ax in axs]
        else:
            self.__interactive_axes_collection = [[InteractiveAxes(ax) for ax in row_axs] for row_axs in axs]
        self.__interactive_axes_collection = tuple([tuple(iaxs) for iaxs in self.__interactive_axes_collection])

        self.__fig.canvas.mpl_connect('draw_event', self.__draw)
        plt.show(block=False)
        plt.pause(0.1)

        self.__background = None
        
    def __del__(self):
        import matplotlib.pyplot as plt
        plt.close(self.__fig)

    def __draw(self, event=None):
        if event is not None and event.canvas != self.__fig.canvas:
                raise RuntimeError
        
        self.save_background()

        from itertools import chain
        for interactive_axes in chain(*self.__interactive_axes_collection):
            # interactive_axes.save_background()
            interactive_axes.render()

    def save_background(self):
        self.__background = self.__fig.canvas.copy_from_bbox(self.__fig.bbox)

    def restore_background(self):
        if self.__background is None:
            self.save_background()
            return False
        self.__fig.canvas.restore_region(self.__background)
        return True
    
    def render(self, pause=0.0333):
        import matplotlib.pyplot as plt
        if not plt.fignum_exists(self.__fig.number):
            raise RuntimeError

        restored = self.restore_background()

        # restored = False
        from itertools import chain
        for interactive_axes in chain(*self.__interactive_axes_collection):
            # restored = restored or interactive_axes.restore_background()
            interactive_axes.render()

        if restored:
            self.__fig.canvas.blit(self.__fig.bbox)
        self.__fig.canvas.draw_idle()
#        plt.show(block=False)
        self.__fig.canvas.start_event_loop(pause)
#        plt.pause(pause)

    def get_interactive_axes(self, row=0, col=0):
        return self.__interactive_axes_collection[row][col]

    def savefig(self, fname, *, transparent=None, **kwargs):
        return self.__fig.savefig(fname, transparent=transparent, **kwargs)
    
