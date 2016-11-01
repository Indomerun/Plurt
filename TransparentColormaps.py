import matplotlib as mpl
#import matplotlib.pyplot as plt
import numpy as np


# Return a copy of the cmap
def getCMapCopy(cmapName):
    cmapBase = mpl.cm.get_cmap(cmapName)
    color_list = cmapBase(np.linspace(0, 1, cmapBase.N))
    new_cmapName = None
    return cmapBase.from_list(new_cmapName, color_list)


def make_rgb_colormap(name, seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [mpl.colors.colorConverter.to_rgb(element) if isinstance(element, str) else element for element in seq]
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    cmap = mpl.colors.LinearSegmentedColormap('CustomMap', cdict)
    mpl.cm.register_cmap(name, cmap)


# Create custom transparency for a colormap.
# aFun is assumed to be defined on the interval [0,1]
def setAlpha(cmapName, aFun=None):
    if aFun is None:
        return
    cmapBase = mpl.cm.get_cmap(cmapName)
    x = np.linspace(0, 1, cmapBase.N)
    color_list = cmapBase(x)
    color_list[:, -1] = aFun(x)
    new_cmap = cmapBase.from_list(cmapName, color_list)
    mpl.cm.register_cmap(cmapName, new_cmap)


def alphaBlend(src_RGBA, dst_RGBA):
    src_A = src_RGBA[..., -1]
    src_R = src_RGBA[..., 0]
    src_G = src_RGBA[..., 1]
    src_B = src_RGBA[..., 2]
    dst_A = dst_RGBA[..., -1]
    dst_R = dst_RGBA[..., 0]
    dst_G = dst_RGBA[..., 1]
    dst_B = dst_RGBA[..., 2]

    """ # Allow transparent dst
    out_A = src_A + dst_A * (1 - src_A)
    out_R = (src_R * src_A + dst_R * dst_A * (1 - src_A)) / out_A
    out_G = (src_G * src_A + dst_G * dst_A * (1 - src_A)) / out_A
    out_B = (src_B * src_A + dst_B * dst_A * (1 - src_A)) / out_A
    """

    # Force opaque dst
    out_A = np.ones(dst_A.shape)
    out_R = dst_R + (src_R - dst_R) * src_A
    out_G = dst_G + (src_G - dst_G) * src_A
    out_B = dst_B + (src_B - dst_B) * src_A

    out_RGBA = np.zeros(src_RGBA.shape)
    out_RGBA[..., -1] = out_A
    out_RGBA[..., 0] = out_R
    out_RGBA[..., 1] = out_G
    out_RGBA[..., 2] = out_B

    return out_RGBA


def make_alphablended_cmap(cmapName, new_cmapName):
    cmapBase = mpl.cm.get_cmap(cmapName)
    src_RGBA = cmapBase(np.linspace(0, 1, cmapBase.N))
    dst_RGBA = np.ones(src_RGBA.shape)
    new_cmap = cmapBase.from_list(new_cmapName, alphaBlend(src_RGBA, dst_RGBA))
    mpl.cm.register_cmap(new_cmapName, new_cmap)
