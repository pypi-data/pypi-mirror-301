import typing
import collections.abc
import typing_extensions
import bpy.types

def brush_stroke(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    | None = None,
    mode: typing.Literal["NORMAL", "INVERT", "SMOOTH"] | None = "NORMAL",
    ignore_background_click: bool | None = False,
):
    """Sculpt a stroke into the geometry

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param stroke: Stroke
        :type stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement] | None
        :param mode: Stroke Mode, Action taken when a paint stroke is made

    NORMAL Regular, Apply brush normally.

    INVERT Invert, Invert action of brush for duration of stroke.

    SMOOTH Smooth, Switch brush to smooth mode for duration of stroke.
        :type mode: typing.Literal['NORMAL','INVERT','SMOOTH'] | None
        :param ignore_background_click: Ignore Background Click, Clicks on the background do not start the stroke
        :type ignore_background_click: bool | None
    """

def detail_flood_fill(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Flood fill the mesh with the selected detail setting

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def dirty_mask(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    dirty_only: bool | None = False,
):
    """Generates a mask based on the geometry cavity and pointiness

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param dirty_only: Dirty Only, Don't calculate cleans for convex areas
    :type dirty_only: bool | None
    """

def dynamic_topology_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Dynamic topology alters the mesh topology while sculpting

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def mask_expand(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    invert: bool | None = True,
    use_cursor: bool | None = True,
    update_pivot: bool | None = True,
    smooth_iterations: int | None = 2,
    mask_speed: int | None = 5,
    use_normals: bool | None = True,
    keep_previous_mask: bool | None = False,
    edge_sensitivity: int | None = 300,
):
    """Expands a mask from the initial active vertex under the cursor

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param invert: Invert, Invert the new mask
    :type invert: bool | None
    :param use_cursor: Use Cursor, Expand the mask to the cursor position
    :type use_cursor: bool | None
    :param update_pivot: Update Pivot Position, Set the pivot position to the mask border after creating the mask
    :type update_pivot: bool | None
    :param smooth_iterations: Smooth iterations
    :type smooth_iterations: int | None
    :param mask_speed: Mask speed
    :type mask_speed: int | None
    :param use_normals: Use Normals, Generate the mask using the normals and curvature of the model
    :type use_normals: bool | None
    :param keep_previous_mask: Keep Previous Mask, Generate the new mask on top of the current one
    :type keep_previous_mask: bool | None
    :param edge_sensitivity: Edge Detection Sensitivity, Sensitivity for expanding the mask across sculpted sharp edges when using normals to generate the mask
    :type edge_sensitivity: int | None
    """

def mask_filter(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filter_type: typing.Literal[
        "SMOOTH", "SHARPEN", "GROW", "SHRINK", "CONTRAST_INCREASE", "CONTRAST_DECREASE"
    ]
    | None = "SMOOTH",
    iterations: int | None = 1,
    auto_iteration_count: bool | None = False,
):
    """Applies a filter to modify the current mask

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filter_type: Type, Filter that is going to be applied to the mask

    SMOOTH Smooth Mask, Smooth mask.

    SHARPEN Sharpen Mask, Sharpen mask.

    GROW Grow Mask, Grow mask.

    SHRINK Shrink Mask, Shrink mask.

    CONTRAST_INCREASE Increase contrast, Increase the contrast of the paint mask.

    CONTRAST_DECREASE Decrease contrast, Decrease the contrast of the paint mask.
        :type filter_type: typing.Literal['SMOOTH','SHARPEN','GROW','SHRINK','CONTRAST_INCREASE','CONTRAST_DECREASE'] | None
        :param iterations: Iterations, Number of times that the filter is going to be applied
        :type iterations: int | None
        :param auto_iteration_count: Auto Iteration Count, Use a automatic number of iterations based on the number of vertices of the sculpt
        :type auto_iteration_count: bool | None
    """

def mesh_filter(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["SMOOTH", "SCALE", "INFLATE", "SPHERE", "RANDOM"]
    | None = "INFLATE",
    strength: float | None = 1.0,
    deform_axis: set[typing.Literal["X", "Y", "Z"]] | None = {"X", "Y", "Z"},
):
    """Applies a filter to modify the current mesh

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Filter type, Operation that is going to be applied to the mesh

    SMOOTH Smooth, Smooth mesh.

    SCALE Scale, Scale mesh.

    INFLATE Inflate, Inflate mesh.

    SPHERE Sphere, Morph into sphere.

    RANDOM Random, Randomize vertex positions.
        :type type: typing.Literal['SMOOTH','SCALE','INFLATE','SPHERE','RANDOM'] | None
        :param strength: Strength, Filter Strength
        :type strength: float | None
        :param deform_axis: Deform axis, Apply the deformation in the selected axis

    X X, Deform in the X axis.

    Y Y, Deform in the Y axis.

    Z Z, Deform in the Z axis.
        :type deform_axis: set[typing.Literal['X','Y','Z']] | None
    """

def optimize(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Recalculate the sculpt BVH to improve performance

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def sample_detail_size(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    location: collections.abc.Iterable[int] | None = (0, 0),
):
    """Sample the mesh detail on clicked point

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param location: Location, Screen Coordinates of sampling
    :type location: collections.abc.Iterable[int] | None
    """

def sculptmode_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Toggle sculpt mode in 3D view

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def set_detail_size(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set the mesh detail (either relative or constant one, depending on current dyntopo mode)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def set_persistent_base(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Reset the copy of the mesh that is being sculpted on

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def set_pivot_position(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["ORIGIN", "UNMASKED", "BORDER", "ACTIVE", "SURFACE"]
    | None = "UNMASKED",
):
    """Sets the sculpt transform pivot position

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode

    ORIGIN Origin, Sets the pivot to the origin of the sculpt.

    UNMASKED Unmasked, Sets the pivot position to the average position of the unmasked vertices.

    BORDER Mask border, Sets the pivot position to the center of the border of the mask.

    ACTIVE Active vertex, Sets the pivot position to the active vertex position.

    SURFACE Surface, Sets the pivot position to the surface under the cursor.
        :type mode: typing.Literal['ORIGIN','UNMASKED','BORDER','ACTIVE','SURFACE'] | None
    """

def symmetrize(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Symmetrize the topology modifications

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def uv_sculpt_stroke(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["NORMAL", "INVERT", "RELAX"] | None = "NORMAL",
):
    """Sculpt UVs using a brush

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode, Stroke Mode

    NORMAL Regular, Apply brush normally.

    INVERT Invert, Invert action of brush for duration of stroke.

    RELAX Relax, Switch brush to relax mode for duration of stroke.
        :type mode: typing.Literal['NORMAL','INVERT','RELAX'] | None
    """
