import typing
import collections.abc
import typing_extensions
import bpy.types

def attribute_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "Attribute",
    data_type: typing.Literal[
        "FLOAT", "INT", "FLOAT_VECTOR", "FLOAT_COLOR", "BYTE_COLOR", "STRING"
    ]
    | None = "FLOAT",
    domain: typing.Literal["VERTEX", "EDGE", "CORNER", "POLYGON", "POINT", "CURVE"]
    | None = "POINT",
):
    """Add attribute to geometry

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param name: Name, Name of new attribute
        :type name: str
        :param data_type: Data Type, Type of data stored in attribute

    FLOAT
    Float, Floating point value.

    INT
    Integer, 32 bit integer.

    FLOAT_VECTOR
    Vector, 3D vector with floating point values.

    FLOAT_COLOR
    Float Color, RGBA color with floating point precisions.

    BYTE_COLOR
    Byte Color, RGBA color with 8-bit precision.

    STRING
    String, Text string.
        :type data_type: typing.Literal['FLOAT','INT','FLOAT_VECTOR','FLOAT_COLOR','BYTE_COLOR','STRING'] | None
        :param domain: Domain, Type of element that attribute is stored on

    VERTEX
    Vertex, Attribute on mesh vertex.

    EDGE
    Edge, Attribute on mesh edge.

    CORNER
    Corner, Attribute on mesh polygon corner.

    POLYGON
    Polygon, Attribute on mesh polygons.

    POINT
    Point, Attribute on point.

    CURVE
    Curve, Attribute on hair curve.
        :type domain: typing.Literal['VERTEX','EDGE','CORNER','POLYGON','POINT','CURVE'] | None
    """

def attribute_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove attribute from geometry

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """
