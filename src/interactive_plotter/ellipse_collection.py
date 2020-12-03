from .interactive_artist import InteractiveArtist

class EllipseCollection(InteractiveArtist):
    def __init__(self, artist):
        super().__init__(artist)

    def plot(self, x=None, y=None, widths=None, heights=None, angles=None, cvalues=None, **kwargs):
        import numpy as np
        if x is not None and y is not None:
            self.artist.set_offsets(np.column_stack((x, y)))
        if widths is not None:
            self.artist._widths = 0.5 * np.array(widths)
        if heights is not None:
            self.artist._heights = 0.5 * np.array(heights)
        if angles is not None:
            self.artist._angles = np.array(angles)
        if cvalues is not None:
            self.artist.set_array(cvalues)
        super().plot(**kwargs)


class TensorField(EllipseCollection):
    def __init__(self, artist):
        super().__init__(artist)

    def plot(self, x=None, y=None, tensors=None, cvalues=None, **kwargs):
        if tensors is not None:
            widths, heights, angles = self.__tensors_to_wha(tensors)
        else:
            widths, heights, angles = None, None, None
        super().plot(x, y, widths, heights, angles, cvalues, **kwargs)

    def __tensors_to_wha(self, tensors):
        import numpy as np
        def tensor_to_wha(tensor):
            a11, a12, a22 = tensor
            d1 = 0.5 * (a22 - a11)
            d2 = np.sqrt(d1 * d1 + a12 * a12)
            d3 = 0.5 * (a22 + a11)
            angle = np.arctan2(d1 + d2, a12)
            w = np.sqrt(d3 + d2)
            h = np.sqrt(d3 - d2)
            return [w, h, angle]
        wha = np.array(list(map(tensor_to_wha, tensors)), dtype=np.float64)
        return wha[:,0], wha[:,1], wha[:,2]

del InteractiveArtist
