class DrawScatter:
    def __init__(self, interactive_figure, interactive_axes, **kwargs):
        self.__interactive_figure = interactive_figure
        self.__interactive_axes = interactive_axes
        self.__kwargs = kwargs
        self.__interactive_scatter = None

        self.__callbacks = dict()
        self.__callback_id = 0

        self.__clean_scatter()
        self.connect()

    def __del__(self):
        self.disconnect()

    def __clean_scatter(self):
        if self.__interactive_scatter is not None:
            self.__interactive_axes.remove_artist(self.__interactive_scatter)
        self.__interactive_scatter = self.__interactive_axes.scatter([], [], **self.__kwargs)
        self.__xdata = []
        self.__ydata = []

    def register_callback(self, callback):
        self.__callback_id += 1
        self.__callbacks[self.__callback_id] = callback
        return self.__callback_id

    def unregister_callback(self, callback_id):
        self.__callbacks.pop(self.__callback_id)

    def call_all(self):
        for callback in self.__callbacks.values():
            callback(self.__interactive_scatter)

    def connect(self):
        self.__cidpress = self.__interactive_figure.figure.canvas.mpl_connect('button_press_event', self.on_press)

    def on_press(self, event):
        if event.inaxes != self.__interactive_axes.axes:
            return

        import matplotlib
        if event.button == matplotlib.backend_bases.MouseButton.LEFT:
            self.__xdata.append(event.xdata)
            self.__ydata.append(event.ydata)
            self.__interactive_scatter.plot(self.__xdata, self.__ydata)
        elif event.button == matplotlib.backend_bases.MouseButton.RIGHT:
            self.__clean_scatter()

        self.call_all()

    def disconnect(self):
        self.__interactive_figure.figure.canvas.mpl_disconnect(self.__cidpress)

class DrawLine2D:
    def __init__(self, interactive_figure, interactive_axes, *args, **kwargs):
        self.__interactive_figure = interactive_figure
        self.__interactive_axes = interactive_axes
        self.__args = args
        self.__kwargs = kwargs

        self.__callbacks = dict()
        self.__callback_id = 0

        self.__interactive_line_2d = None
        self.__xdata = []
        self.__ydata = []

        self.connect()

    def __del__(self):
        self.disconnect()

    def register_callback(self, callback):
        self.__callback_id += 1
        self.__callbacks[self.__callback_id] = callback
        return self.__callback_id

    def unregister_callback(self, callback_id):
        self.__callbacks.pop(self.__callback_id)

    def call_all(self):
        for callback in self.__callbacks.values():
            callback(self.__interactive_line_2d)

    def connect(self):
        self.__cidpress = self.__interactive_figure.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.__cidrelease = self.__interactive_figure.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.__cidmotion = self.__interactive_figure.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.__interactive_axes.axes:
            return

        self.__xdata.append(event.xdata)
        self.__ydata.append(event.ydata)

        self.__interactive_line_2d = self.__interactive_axes.plot(self.__xdata, self.__ydata, *self.__args, **self.__kwargs)[0]

    def on_motion(self, event):
        if self.__interactive_line_2d is None:
            return
        if event.inaxes != self.__interactive_axes.axes:
            return

        self.__xdata.append(event.xdata)
        self.__ydata.append(event.ydata)

        self.__interactive_line_2d.plot(self.__xdata, self.__ydata)

    def on_release(self, event):
        if self.__interactive_line_2d is None:
            return
        self.call_all()
        self.__interactive_axes.remove_artist(self.__interactive_line_2d)
        self.__interactive_line_2d = None
        self.__xdata = []
        self.__ydata = []

    def disconnect(self):
        self.__interactive_figure.figure.canvas.mpl_disconnect(self.__cidpress)
        self.__interactive_figure.figure.canvas.mpl_disconnect(self.__cidrelease)
        self.__interactive_figure.figure.canvas.mpl_disconnect(self.__cidmotion)
