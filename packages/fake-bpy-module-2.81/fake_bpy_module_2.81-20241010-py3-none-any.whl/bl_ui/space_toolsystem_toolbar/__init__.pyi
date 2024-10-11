import typing
import collections.abc
import typing_extensions
import bl_ui.space_toolsystem_common
import bpy.types

class IMAGE_PT_tools_active(
    bl_ui.space_toolsystem_common.ToolSelectPanelHelper, bpy.types.Panel
):
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any
    keymap_prefix: typing.Any

    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    @classmethod
    def tools_all(cls): ...
    @classmethod
    def tools_from_context(cls, context, mode=None):
        """

        :param context:
        :param mode:
        """

class NODE_PT_tools_active(
    bl_ui.space_toolsystem_common.ToolSelectPanelHelper, bpy.types.Panel
):
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any
    keymap_prefix: typing.Any

    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    @classmethod
    def tools_all(cls): ...
    @classmethod
    def tools_from_context(cls, context, mode=None):
        """

        :param context:
        :param mode:
        """

class VIEW3D_PT_tools_active(
    bl_ui.space_toolsystem_common.ToolSelectPanelHelper, bpy.types.Panel
):
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any
    keymap_prefix: typing.Any

    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    @classmethod
    def tools_all(cls): ...
    @classmethod
    def tools_from_context(cls, context, mode=None):
        """

        :param context:
        :param mode:
        """

class _defs_annotate:
    eraser: typing.Any
    line: typing.Any
    poly: typing.Any
    scribble: typing.Any

    def draw_settings_common(self, context, layout, tool):
        """

        :param context:
        :param layout:
        :param tool:
        """

class _defs_edit_armature:
    bone_envelope: typing.Any
    bone_size: typing.Any
    extrude: typing.Any
    extrude_cursor: typing.Any
    roll: typing.Any

class _defs_edit_curve:
    curve_radius: typing.Any
    curve_vertex_randomize: typing.Any
    draw: typing.Any
    extrude: typing.Any
    extrude_cursor: typing.Any
    tilt: typing.Any

class _defs_edit_mesh:
    bevel: typing.Any
    bisect: typing.Any
    cube_add: typing.Any
    edge_slide: typing.Any
    extrude: typing.Any
    extrude_cursor: typing.Any
    extrude_individual: typing.Any
    extrude_normals: typing.Any
    inset: typing.Any
    knife: typing.Any
    loopcut_slide: typing.Any
    offset_edge_loops_slide: typing.Any
    poly_build: typing.Any
    push_pull: typing.Any
    rip_edge: typing.Any
    rip_region: typing.Any
    shear: typing.Any
    shrink_fatten: typing.Any
    spin: typing.Any
    spin_duplicate: typing.Any
    tosphere: typing.Any
    vert_slide: typing.Any
    vertex_randomize: typing.Any
    vertex_smooth: typing.Any

class _defs_gpencil_edit:
    bend: typing.Any
    box_select: typing.Any
    circle_select: typing.Any
    extrude: typing.Any
    lasso_select: typing.Any
    radius: typing.Any
    select: typing.Any
    shear: typing.Any
    tosphere: typing.Any

class _defs_gpencil_paint:
    arc: typing.Any
    box: typing.Any
    circle: typing.Any
    curve: typing.Any
    cutter: typing.Any
    line: typing.Any

    @staticmethod
    def generate_from_brushes(context):
        """

        :param context:
        """

class _defs_gpencil_sculpt:
    @staticmethod
    def generate_from_brushes(context):
        """

        :param context:
        """

    @staticmethod
    def poll_select_mask(context):
        """

        :param context:
        """

class _defs_gpencil_weight:
    @staticmethod
    def generate_from_brushes(context):
        """

        :param context:
        """

class _defs_image_generic:
    cursor: typing.Any
    sample: typing.Any

    @staticmethod
    def poll_uvedit(context):
        """

        :param context:
        """

class _defs_image_uv_sculpt:
    @staticmethod
    def generate_from_brushes(context):
        """

        :param context:
        """

class _defs_image_uv_select:
    box: typing.Any
    circle: typing.Any
    lasso: typing.Any
    select: typing.Any

class _defs_image_uv_transform:
    rotate: typing.Any
    scale: typing.Any
    transform: typing.Any
    translate: typing.Any

class _defs_node_edit:
    links_cut: typing.Any

class _defs_node_select:
    box: typing.Any
    circle: typing.Any
    lasso: typing.Any
    select: typing.Any

class _defs_particle:
    @staticmethod
    def generate_from_brushes(context):
        """

        :param context:
        """

class _defs_pose:
    breakdown: typing.Any
    push: typing.Any
    relax: typing.Any

class _defs_sculpt:
    hide_border: typing.Any
    mask_border: typing.Any
    mask_lasso: typing.Any
    mesh_filter: typing.Any

    @staticmethod
    def generate_from_brushes(context):
        """

        :param context:
        """

class _defs_texture_paint:
    @staticmethod
    def generate_from_brushes(context):
        """

        :param context:
        """

    @staticmethod
    def poll_select_mask(context):
        """

        :param context:
        """

class _defs_transform:
    rotate: typing.Any
    scale: typing.Any
    scale_cage: typing.Any
    transform: typing.Any
    translate: typing.Any

class _defs_vertex_paint:
    @staticmethod
    def generate_from_brushes(context):
        """

        :param context:
        """

    @staticmethod
    def poll_select_mask(context):
        """

        :param context:
        """

class _defs_view3d_generic:
    cursor: typing.Any
    cursor_click: typing.Any
    ruler: typing.Any

class _defs_view3d_select:
    box: typing.Any
    circle: typing.Any
    lasso: typing.Any
    select: typing.Any

class _defs_weight_paint:
    gradient: typing.Any
    sample_weight: typing.Any
    sample_weight_group: typing.Any

    @staticmethod
    def generate_from_brushes(context):
        """

        :param context:
        """

    @staticmethod
    def poll_select_mask(context):
        """

        :param context:
        """

class _template_widget:
    def VIEW3D_GGT_xform_extrude(self): ...
    def VIEW3D_GGT_xform_gizmo(self): ...

def generate_from_enum_ex(
    _context,
    *,
    idname_prefix,
    icon_prefix,
    type,
    attr,
    cursor="DEFAULT",
    tooldef_keywords={},
): ...
def kmi_to_string_or_none(kmi): ...
