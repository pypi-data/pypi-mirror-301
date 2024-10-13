"""
This module provides access to GPUShader internal functions.

Built-in shaders

All built-in shaders have the mat4 ModelViewProjectionMatrix

 uniform.

Its value must be modified using the gpu.matrix module.

2D_UNIFORM_COLOR


    Attributes: vec3 pos
    Uniforms: vec4 color



2D_FLAT_COLOR


    Attributes: vec3 pos, vec4 color
    Uniforms: none



2D_SMOOTH_COLOR


    Attributes: vec3 pos, vec4 color
    Uniforms: none



2D_IMAGE


    Attributes: vec3 pos, vec2 texCoord
    Uniforms: sampler2D image



3D_UNIFORM_COLOR


    Attributes: vec3 pos
    Uniforms: vec4 color



3D_FLAT_COLOR


    Attributes: vec3 pos, vec4 color
    Uniforms: none



3D_SMOOTH_COLOR


    Attributes: vec3 pos, vec4 color
    Uniforms: none



"""

import typing
import collections.abc
import typing_extensions

def code_from_builtin(pygpu_shader_name: str) -> dict:
    """Exposes the internal shader code for consultation.

        :param pygpu_shader_name: One of these builtin shader names:

    2D_FLAT_COLOR

    2D_IMAGE

    2D_SMOOTH_COLOR

    2D_UNIFORM_COLOR

    3D_FLAT_COLOR

    3D_SMOOTH_COLOR

    3D_UNIFORM_COLOR

    3D_POLYLINE_FLAT_COLOR

    3D_POLYLINE_SMOOTH_COLOR

    3D_POLYLINE_UNIFORM_COLOR
        :type pygpu_shader_name: str
        :return: Vertex, fragment and geometry shader codes.
        :rtype: dict
    """

def from_builtin(shader_name: str, config: str = "DEFAULT"):
    """Shaders that are embedded in the blender internal code.
    They all read the uniform mat4 ModelViewProjectionMatrix,
    which can be edited by the `gpu.matrix` module.You can also choose a shader configuration that uses clip_planes by setting the CLIPPED value to the config parameter. Note that in this case you also need to manually set the value of mat4 ModelMatrix.For more details, you can check the shader code with the
    `gpu.shader.code_from_builtin` function.

        :param shader_name: One of these builtin shader names:

    2D_FLAT_COLOR

    2D_IMAGE

    2D_SMOOTH_COLOR

    2D_UNIFORM_COLOR

    3D_FLAT_COLOR

    3D_SMOOTH_COLOR

    3D_UNIFORM_COLOR

    3D_POLYLINE_FLAT_COLOR

    3D_POLYLINE_SMOOTH_COLOR

    3D_POLYLINE_UNIFORM_COLOR
        :type shader_name: str
        :param config: One of these types of shader configuration:

    DEFAULT

    CLIPPED
        :type config: str
        :return: Shader object corresponding to the given name.
    """

def unbind():
    """Unbind the bound shader object."""
