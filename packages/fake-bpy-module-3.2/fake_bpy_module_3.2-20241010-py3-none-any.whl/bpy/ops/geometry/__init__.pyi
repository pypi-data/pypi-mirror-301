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
        "INT8",
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
    Color -- RGBA color with 32-bit floating-point values.

    BYTE_COLOR
    Byte Color -- RGBA color with 8-bit positive integer values.

    STRING
    String -- Text string.

    BOOLEAN
    Boolean -- True or false.

    FLOAT2
    2D Vector -- 2D vector with floating-point values.

    INT8
    8-Bit Integer -- Smaller integer with a range from -128 to 127.
        :type data_type: typing.Literal['FLOAT','INT','FLOAT_VECTOR','FLOAT_COLOR','BYTE_COLOR','STRING','BOOLEAN','FLOAT2','INT8'] | None
    """

def attribute_convert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["GENERIC", "UV_MAP", "VERTEX_GROUP"] | None = "GENERIC",
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
        "INT8",
    ]
    | None = "FLOAT",
):
    """Change how the attribute is stored

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode
        :type mode: typing.Literal['GENERIC','UV_MAP','VERTEX_GROUP'] | None
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
    Color -- RGBA color with 32-bit floating-point values.

    BYTE_COLOR
    Byte Color -- RGBA color with 8-bit positive integer values.

    STRING
    String -- Text string.

    BOOLEAN
    Boolean -- True or false.

    FLOAT2
    2D Vector -- 2D vector with floating-point values.

    INT8
    8-Bit Integer -- Smaller integer with a range from -128 to 127.
        :type data_type: typing.Literal['FLOAT','INT','FLOAT_VECTOR','FLOAT_COLOR','BYTE_COLOR','STRING','BOOLEAN','FLOAT2','INT8'] | None
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

def color_attribute_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "Color",
    domain: typing.Literal["POINT", "CORNER"] | None = "POINT",
    data_type: typing.Literal["COLOR", "BYTE_COLOR"] | None = "COLOR",
    color: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0, 1.0),
):
    """Add color attribute to geometry

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of new color attribute
    :type name: str
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: typing.Literal['POINT','CORNER'] | None
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: typing.Literal['COLOR','BYTE_COLOR'] | None
    :param color: Color, Default fill color
    :type color: collections.abc.Iterable[float] | None
    """

def color_attribute_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove color attribute from geometry

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def color_attribute_render_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "Color",
):
    """Set default color attribute used for rendering

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of color attribute
    :type name: str
    """
