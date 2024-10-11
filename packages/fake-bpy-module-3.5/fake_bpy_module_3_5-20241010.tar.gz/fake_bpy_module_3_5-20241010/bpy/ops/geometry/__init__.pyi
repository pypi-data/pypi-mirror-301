import typing
import collections.abc
import typing_extensions
import bpy.types
import bpy.typing

def attribute_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "Attribute",
    domain: bpy.typing.AttributeDomainItems | None = "POINT",
    data_type: bpy.typing.AttributeTypeItems | None = "FLOAT",
):
    """Add attribute to geometry

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of new attribute
    :type name: str
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: bpy.typing.AttributeDomainItems | None
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: bpy.typing.AttributeTypeItems | None
    """

def attribute_convert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["GENERIC", "VERTEX_GROUP"] | None = "GENERIC",
    domain: bpy.typing.AttributeDomainItems | None = "POINT",
    data_type: bpy.typing.AttributeTypeItems | None = "FLOAT",
):
    """Change how the attribute is stored

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Literal['GENERIC','VERTEX_GROUP'] | None
    :param domain: Domain, Which geometry element to move the attribute to
    :type domain: bpy.typing.AttributeDomainItems | None
    :param data_type: Data Type
    :type data_type: bpy.typing.AttributeTypeItems | None
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
    domain: bpy.typing.ColorAttributeDomainItems | None = "POINT",
    data_type: bpy.typing.ColorAttributeTypeItems | None = "FLOAT_COLOR",
    color: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0, 1.0),
):
    """Add color attribute to geometry

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of new color attribute
    :type name: str
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: bpy.typing.ColorAttributeDomainItems | None
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: bpy.typing.ColorAttributeTypeItems | None
    :param color: Color, Default fill color
    :type color: collections.abc.Iterable[float] | None
    """

def color_attribute_convert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    domain: bpy.typing.ColorAttributeDomainItems | None = "POINT",
    data_type: bpy.typing.ColorAttributeTypeItems | None = "FLOAT_COLOR",
):
    """Change how the color attribute is stored

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: bpy.typing.ColorAttributeDomainItems | None
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: bpy.typing.ColorAttributeTypeItems | None
    """

def color_attribute_duplicate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Duplicate color attribute

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
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
