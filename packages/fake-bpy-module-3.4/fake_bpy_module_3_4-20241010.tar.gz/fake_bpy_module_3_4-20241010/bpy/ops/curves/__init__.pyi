import typing
import collections.abc
import typing_extensions
import bpy.types
import bpy.typing

def convert_from_particle_system(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add a new curves object based on the current state of the particle system

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def convert_to_particle_system(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add a new or update an existing hair particle system on the surface object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def disable_selection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Disable the drawing of influence of selection in sculpt mode

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def sculptmode_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Enter/Exit sculpt mode for curves

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def set_selection_domain(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    domain: bpy.typing.AttributeCurvesDomainItems | None = "POINT",
):
    """Change the mode used for selection masking in curves sculpt mode

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param domain: Domain
    :type domain: bpy.typing.AttributeCurvesDomainItems | None
    """

def snap_curves_to_surface(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    attach_mode: typing.Literal["NEAREST", "DEFORM"] | None = "NEAREST",
):
    """Move curves so that the first point is exactly on the surface mesh

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param attach_mode: Attach Mode, How to find the point on the surface to attach to

    NEAREST
    Nearest -- Find the closest point on the surface for the root point of every curve and move the root there.

    DEFORM
    Deform -- Re-attach curves to a deformed surface using the existing attachment information. This only works when the topology of the surface mesh has not changed.
        :type attach_mode: typing.Literal['NEAREST','DEFORM'] | None
    """

def surface_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Use the active object as surface for selected curves objects and set it as the parent

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """
