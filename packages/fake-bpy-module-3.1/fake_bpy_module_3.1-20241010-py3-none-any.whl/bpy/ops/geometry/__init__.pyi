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
    domain: typing.Literal["POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE"]
    | None = "POINT",
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

    INSTANCE
    Instance -- Attribute on instance.
        :type domain: typing.Literal['POINT','EDGE','FACE','CORNER','CURVE','INSTANCE'] | None
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

def attribute_convert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["GENERIC", "UV_MAP", "VERTEX_GROUP", "VERTEX_COLOR"]
    | None = "GENERIC",
    domain: typing.Literal["POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE"]
    | None = "POINT",
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
    """Change how the attribute is stored

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode
        :type mode: typing.Literal['GENERIC','UV_MAP','VERTEX_GROUP','VERTEX_COLOR'] | None
        :param domain: Domain, Which geometry element to move the attribute to

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

    INSTANCE
    Instance -- Attribute on instance.
        :type domain: typing.Literal['POINT','EDGE','FACE','CORNER','CURVE','INSTANCE'] | None
        :param data_type: Data Type

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
