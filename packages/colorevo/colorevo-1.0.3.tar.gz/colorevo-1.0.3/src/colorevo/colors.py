#  Copyright 2019 Carlos Pascual-Izarra <cpascual@users.sourceforge.net>
#
#  This file is part of colorevo.
#
#  colorevo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  colorevo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np
import itertools


def bgr2h(arr):
    """Obtain hue from BGR image.
    Code adapted from matplotlib.colors.rgb_to_hsv

    See: https://en.wikipedia.org/wiki/HSL_and_HSV#Hue_and_chroma
    """
    arr = arr.astype(np.promote_types(arr.dtype, np.float32))
    b, g, r = 0, 1, 2
    out = np.zeros_like(arr[..., b])
    arr_max = arr.max(-1)
    ipos = arr_max > 0
    delta = arr.ptp(-1)
    # Saturation (s) is not needed. Commented out for efficiency
    # s = np.zeros_like(delta)
    # s[ipos] = delta[ipos] / arr_max[ipos]
    ipos = delta > 0
    # red is max
    idx = (arr[..., r] == arr_max) & ipos
    out[idx] = (arr[idx, g] - arr[idx, b]) / delta[idx]
    # green is max
    idx = (arr[..., g] == arr_max) & ipos
    out[idx] = 2.0 + (arr[idx, b] - arr[idx, r]) / delta[idx]
    # blue is max
    idx = (arr[..., b] == arr_max) & ipos
    out[idx] = 4.0 + (arr[idx, r] - arr[idx, g]) / delta[idx]

    out = (out / 6.0) % 1.0

    return out


def bgr2hsv(arr):
    """
    Convert an array of float BGR values (in the range [0, 1]) to HSV values.

    Code adapted from matplotlib.colors.rgb_to_hsv

    See: https://en.wikipedia.org/wiki/HSL_and_HSV#Hue_and_chroma

    Parameters
    ----------
    arr : (..., 3) array-like
       All values must be in the range [0, 1]

    Returns
    -------
    (..., 3) `~numpy.ndarray`
       Colors converted to HSV values in range [0, 1]
    """
    arr = np.asarray(arr)
    b, g, r = 0, 1, 2

    # check length of the last dimension, should be _some_ sort of rgb
    if arr.shape[-1] != 3:
        raise ValueError(
            "Last dimension of input array must be 3; " f"shape {arr.shape} was found."
        )

    in_shape = arr.shape
    arr = np.array(
        arr,
        dtype=np.promote_types(arr.dtype, np.float32),  # Don't work on ints.
        ndmin=2,  # In case input was 1D.
    )
    out = np.zeros_like(arr)
    arr_max = arr.max(-1)
    ipos = arr_max > 0
    delta = np.ptp(arr, -1)
    s = np.zeros_like(delta)
    s[ipos] = delta[ipos] / arr_max[ipos]
    ipos = delta > 0
    # red is max
    idx = (arr[..., r] == arr_max) & ipos
    out[idx, 0] = (arr[idx, g] - arr[idx, b]) / delta[idx]
    # green is max
    idx = (arr[..., g] == arr_max) & ipos
    out[idx, 0] = 2.0 + (arr[idx, b] - arr[idx, r]) / delta[idx]
    # blue is max
    idx = (arr[..., b] == arr_max) & ipos
    out[idx, 0] = 4.0 + (arr[idx, r] - arr[idx, g]) / delta[idx]

    out[..., 0] = (out[..., 0] / 6.0) % 1.0
    out[..., 1] = s
    out[..., 2] = arr_max

    return out.reshape(in_shape)


def bgr2rgb(arr):
    return arr[..., ::-1]


def hsv_generator(h0=0, hn=15, s=(0.99, 0.5), v=0.99):
    """
    Generator that returns evenly-spaced non-repeated hsv colors.
    It varies the H using the golden ratio, and cycles the saturation
    according to the given values.
    Inspired in:
     https://martin.ankerl.com/2009/12/09/how-to-create-random-colors-programmatically/
    """
    gr = 0.618033988749895  # golden_ratio_conjugate
    h = h0
    s_cycle = itertools.cycle(s)
    while True:
        s = next(s_cycle)
        for _ in range(hn):
            yield h, s, v
            h = (h + gr) % 1


if __name__ == "__main__":
    # from matplotlib.colors import rgb_to_hsv
    #
    # a = np.random.rand(100, 200, 3)
    # print(np.allclose(bgr2h(a), rgb_to_hsv(a[..., ::-1])[...,0]))
    #
    # a = np.arange(100*200*3).reshape(100, 200, 3)
    # print(np.allclose(bgr2h(a), rgb_to_hsv(a[..., ::-1])[...,0]))

    colors = hsv_generator()
    for i in range(60):
        print(i, next(colors))
