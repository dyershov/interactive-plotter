class InteractiveFigure:
    def __init__(self, nrows=1, ncols=1, **kwargs):
        import matplotlib.pyplot as plt
        from .interactive_axes import InteractiveAxes
        self.__fig, axs = plt.subplots(nrows=nrows, ncols=ncols, squeeze=False, **kwargs)

        self.__interactive_axes_collection = [[InteractiveAxes(ax) for ax in row_axs] for row_axs in axs]

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

    def savefig(self, fname, *, index=None, index_length=4, **kwargs):
        index_format = "_%%0%dd" % index_length
        index_str = '' if index is None else index_format % index
        last_dot_index = fname.rfind('.')
        fname = fname + index_str if last_dot_index == -1 else fname[:last_dot_index] + index_str + fname[last_dot_index:]
        return self.__fig.savefig(fname, **kwargs)

