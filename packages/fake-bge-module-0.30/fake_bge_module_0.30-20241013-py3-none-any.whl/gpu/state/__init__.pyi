"""
This module provides access to the gpu state.

"""

import typing
import collections.abc
import typing_extensions

def blend_depth_test_get():
    """Current depth_test equation."""

def blend_get():
    """Current blending equation."""

def blend_set(mode: str):
    """Defines the fixed pipeline blending equation.

        :param mode: The type of blend mode.
    * NONE No blending.
    * ALPHA The original color channels are interpolated according to the alpha value.
    * ALPHA_PREMULT The original color channels are interpolated according to the alpha value with the new colors pre-multiplied by this value.
    * ADDITIVE The original color channels are added by the corresponding ones.
    * ADDITIVE_PREMULT The original color channels are added by the corresponding ones that are pre-multiplied by the alpha value.
    * MULTIPLY The original color channels are multiplied by the corresponding ones.
    * SUBTRACT The original color channels are subtracted by the corresponding ones.
    * INVERT The original color channels are replaced by its complementary color.
        :type mode: str
    """

def clip_distances_set(distances_enabled: int):
    """Sets the number of gl_ClipDistance planes used for clip geometry.

    :param distances_enabled: Number of clip distances enabled.
    :type distances_enabled: int
    """

def color_mask_set(r: bool, g, b, a):
    """Enable or disable writing of frame buffer color components.

    :param r: components red, green, blue, and alpha.
    :type r: bool
    """

def depth_mask_set(value):
    """Write to depth component.

    :param value: True for writing to the depth component.
    """

def depth_mask_set_get():
    """Writing status in the depth component."""

def depth_test_set(mode: str):
    """Defines the depth_test equation.

        :param mode: The depth test equation name.
    Possible values are NONE, ALWAYS, LESS, LESS_EQUAL, EQUAL, GREATER and GREATER_EQUAL.
        :type mode: str
    """

def face_culling_set(culling):
    """Specify whether none, front-facing or back-facing facets can be culled."""

def framebuffer_active_get(enable):
    """Return the active framefuffer in context."""

def front_facing_set(invert):
    """Specifies the orientation of front-facing polygons.

    :param invert: True for clockwise polygons as front-facing.
    """

def line_width_get():
    """Current width of rasterized lines."""

def line_width_set(width):
    """Specify the width of rasterized lines."""

def point_size_set(size):
    """Specify the diameter of rasterized points.

    :param size: New diameter.
    """

def use_program_point_size(enable: bool):
    """If enabled, the derived point size is taken from the (potentially clipped) shader builtin gl_PointSize.

    :param enable: True for shader builtin gl_PointSize.
    :type enable: bool
    """

def viewport_get():
    """Viewport of the active framebuffer."""

def viewport_set(x: int, y, xsize, ysize):
    """Specifies the viewport of the active framebuffer.
    Note: The viewport state is not saved upon framebuffer rebind.

        :param x: lower left corner of the viewport_set rectangle, in pixels.
        :type x: int
    """
