class EllipseCollectionPlotter:
    def __init__(self, axes, origins, widths = None, heights = None, angles = None, values = None):
        import numpy as np
        xy = np.array(list(origins), dtype=np.float64)
        from operator import itemgetter
        self.__bounding_box = [[min(map(itemgetter(0), xy)), min(map(itemgetter(1), xy))],
                               [max(map(itemgetter(0), xy)), max(map(itemgetter(1), xy))]]
        self.__value_limits = (0.0, 1.0)

        w = np.zeros(len(xy)) if widths is None else widths
        h = np.zeros(len(xy)) if heights is None else heights
        a = np.zeros(len(xy)) if angles is None else angles

        from matplotlib.collections import EllipseCollection
        self.__artist = EllipseCollection(w, h, a, offsets=xy,
                                          transOffset=axes.transData,
                                          units='x')
        self.__set_values(values)
        
        axes.add_collection(self.__artist)

        self.__rendered = False

    @property
    def artist(self):
        return self.__artist

    @property
    def rendered(self):
        return self.__rendered

    @property
    def bounding_box(self):
        return self.__bounding_box

    def plot(self, widths, heights, angles, values = None):
        import numpy as np
        from matplotlib.collections import EllipseCollection
        new_artist = EllipseCollection(widths, heights, angles, offsets=self.__artist.get_offsets(),
                                       transOffset=self.__artist.axes.transData,
                                       units='x')
        self.__artist._widths = new_artist._widths
        self.__artist._heights = new_artist._heights
        self.__artist._angles = new_artist._angles
        self.__set_values(values)
        self.__rendered = False

    def tighten_clim(self):
        self.set_clim(self.__value_limits)

    def set_clim(self, clim):
        self.__artist.set_clim(clim)
        self.__rendered = False

    def render(self):
        self.__artist.axes.draw_artist(self.__artist)
        self.__rendered = True

    def __set_values(self, values):
        if values is None:
            return
        import numpy as np
        c = np.fromiter(values, dtype=np.float64)
        self.__artist.set_array(c)
        self.__value_limits = (min(c), max(c))


class SPDMatrixCollectionPlotter(EllipseCollectionPlotter):
    def __init__(self, axes, origins, spd_matrices = None, values = None, q = None):
        width, height, angle = (None, None, None) if spd_matrices is None else self.__spd_matrices_to_wha(spd_matrices, q)
        super().__init__(axes, origins, width, height, angle, values)
        self.artist.set_facecolor('none')
        self.artist.set_edgecolor('black')

    def plot(self, spd_matrices, values = None, q = None):
        from numpy import array, float64
        width, height, angle = self.__spd_matrices_to_wha(spd_matrices, q)
        super().plot(width, height, angle, values)

    def __spd_matrices_to_wha(self, spd_matrices, q):
        import numpy as np
        if q is None:
            scale = 1.0
        else:
            from scipy.stats import chi2
            scale = np.sqrt(chi2.ppf(q, 2))
        rad_to_deg = 180 / np.pi
        def spd_matrix_to_wha(spd_matrix):
            a11, a12, a22 = spd_matrix
            a_rad = 0.5 * np.arctan2(2 * a12, a11 + a22)
            cos_a = np.cos(a_rad)
            sin_a = np.sin(a_rad)
            cos_2_a = cos_a * cos_a
            cos_a_sin_a = cos_a * sin_a
            sin_2_a = sin_a * sin_a
            w = np.sqrt(cos_2_a * a11 + cos_a_sin_a * a12 + sin_2_a * a22)
            h = np.sqrt(sin_2_a * a11 - cos_a_sin_a * a12 + cos_2_a * a22)
            return [w * scale, h * scale, a_rad * rad_to_deg]
        wha = np.array(list(map(spd_matrix_to_wha, spd_matrices)), dtype=np.float64)
        return wha[:,0], wha[:,1], wha[:,2]
