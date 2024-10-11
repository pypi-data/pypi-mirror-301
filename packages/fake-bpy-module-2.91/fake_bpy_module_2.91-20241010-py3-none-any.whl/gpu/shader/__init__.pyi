"""
This module provides access to GPUShader internal functions.

Built-in shaders

All built-in shaders have the mat4 ModelViewProjectionMatrix

 uniform.
The value of it can only be modified using the gpu.matrix module.

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

def code_from_builtin(shader_name: str) -> dict:
    """Exposes the internal shader code for query.

        :param shader_name: One of these builtin shader names:

    2D_UNIFORM_COLOR

    2D_FLAT_COLOR

    2D_SMOOTH_COLOR

    2D_IMAGE

    3D_UNIFORM_COLOR

    3D_FLAT_COLOR

    3D_SMOOTH_COLOR
        :type shader_name: str
        :return: Vertex, fragment and geometry shader codes.
        :rtype: dict
    """

def from_builtin(shader_name: str):
    """Shaders that are embedded in the blender internal code.
    They all read the uniform mat4 ModelViewProjectionMatrix,
    which can be edited by the `gpu.matrix` module.
    For more details, you can check the shader code with the
    `gpu.shader.code_from_builtin` function.

        :param shader_name: One of these builtin shader names:

    2D_UNIFORM_COLOR

    2D_FLAT_COLOR

    2D_SMOOTH_COLOR

    2D_IMAGE

    3D_UNIFORM_COLOR

    3D_FLAT_COLOR

    3D_SMOOTH_COLOR
        :type shader_name: str
        :return: Shader object corresponding to the given name.
    """

def unbind():
    """Unbind the bound shader object."""
