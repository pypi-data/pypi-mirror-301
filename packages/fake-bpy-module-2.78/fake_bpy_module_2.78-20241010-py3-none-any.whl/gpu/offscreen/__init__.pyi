"""
This module provides access to offscreen rendering functions.

```../examples/gpu.offscreen.1.py```

"""

import typing
import collections.abc
import typing_extensions

class GPUOffscreen:
    """bind(save=True)draw_view3d(scene, view3d, region, modelview_matrix, projection_matrix)free()unbind(restore=True)"""

    color_texture: int
    """ Color texture.

    :type: int
    """

    height: int
    """ Texture height.

    :type: int
    """

    width: int
    """ Texture width.

    :type: int
    """

def new(width, height, samples: int = 0):
    """Return a GPUOffScreen.

    :param width: Horizontal dimension of the buffer.
    :param height: Vertical dimension of the buffer.
    :param samples: OpenGL samples to use for MSAA or zero to disable.
    :type samples: int
    :return: Newly created off-screen buffer.
    """
