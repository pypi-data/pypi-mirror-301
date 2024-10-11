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
    domain: typing.Literal["POINT", "EDGE", "FACE", "CORNER", "CURVE"] | None = "POINT",
    data_type: typing.Literal[
        "FLOAT",
        "INT",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
        "BYTE_COLOR",
        "STRING",
        "BOOLEAN",
        "FLOAT2",
    ]
    | None = "FLOAT",
):
    """Add attribute to geometry

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param name: Name, Name of new attribute
        :type name: str
        :param domain: Domain, Type of element that attribute is stored on

    POINT
    Point -- Attribute on point.

    EDGE
    Edge -- Attribute on mesh edge.

    FACE
    Face -- Attribute on mesh faces.

    CORNER
    Face Corner -- Attribute on mesh face corner.

    CURVE
    Spline -- Attribute on spline.
        :type domain: typing.Literal['POINT','EDGE','FACE','CORNER','CURVE'] | None
        :param data_type: Data Type, Type of data stored in attribute

    FLOAT
    Float -- Floating-point value.

    INT
    Integer -- 32-bit integer.

    FLOAT_VECTOR
    Vector -- 3D vector with floating-point values.

    FLOAT_COLOR
    Color -- RGBA color with floating-point values.

    BYTE_COLOR
    Byte Color -- RGBA color with 8-bit values.

    STRING
    String -- Text string.

    BOOLEAN
    Boolean -- True or false.

    FLOAT2
    2D Vector -- 2D vector with floating-point values.
        :type data_type: typing.Literal['FLOAT','INT','FLOAT_VECTOR','FLOAT_COLOR','BYTE_COLOR','STRING','BOOLEAN','FLOAT2'] | None
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
