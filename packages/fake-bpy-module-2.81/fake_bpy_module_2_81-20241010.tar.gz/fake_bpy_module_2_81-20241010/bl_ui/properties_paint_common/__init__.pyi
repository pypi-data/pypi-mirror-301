import typing
import collections.abc
import typing_extensions
import bpy.types

class UnifiedPaintPanel:
    @staticmethod
    def paint_settings(context):
        """

        :param context:
        """

    @staticmethod
    def prop_unified_color(parent, context, brush, prop_name, *, text=None):
        """

        :param parent:
        :param context:
        :param brush:
        :param prop_name:
        :param text:
        """

    @staticmethod
    def prop_unified_color_picker(parent, context, brush, prop_name, value_slider=True):
        """

        :param parent:
        :param context:
        :param brush:
        :param prop_name:
        :param value_slider:
        """

    @staticmethod
    def prop_unified_size(
        parent, context, brush, prop_name, *, icon="NONE", text=None, slider=False
    ):
        """

        :param parent:
        :param context:
        :param brush:
        :param prop_name:
        :param icon:
        :param text:
        :param slider:
        """

    @staticmethod
    def prop_unified_strength(
        parent, context, brush, prop_name, *, icon="NONE", text=None, slider=False
    ):
        """

        :param parent:
        :param context:
        :param brush:
        :param prop_name:
        :param icon:
        :param text:
        :param slider:
        """

    @staticmethod
    def prop_unified_weight(
        parent, context, brush, prop_name, *, icon="NONE", text=None, slider=False
    ):
        """

        :param parent:
        :param context:
        :param brush:
        :param prop_name:
        :param icon:
        :param text:
        :param slider:
        """

    @staticmethod
    def unified_paint_settings(parent, context):
        """

        :param parent:
        :param context:
        """

class VIEW3D_MT_tools_projectpaint_clone(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

def brush_basic_gpencil_paint_settings(layout, _context, brush, *, compact=True): ...
def brush_basic_gpencil_sculpt_settings(layout, context, brush, *, compact=False): ...
def brush_basic_gpencil_weight_settings(layout, _context, brush, *, compact=False): ...
def brush_basic_sculpt_settings(layout, context, brush, *, compact=False): ...
def brush_basic_texpaint_settings(layout, context, brush, *, compact=False): ...
def brush_basic_vpaint_settings(layout, context, brush, *, compact=False): ...
def brush_basic_wpaint_settings(layout, context, brush, *, compact=False): ...
def brush_mask_texture_settings(layout, brush): ...
def brush_texpaint_common(
    panel, context, layout, brush, _settings, *, projpaint=False
): ...
def brush_texpaint_common_clone(
    _panel, context, layout, _brush, settings, *, projpaint=False
): ...
def brush_texpaint_common_color(
    _panel, context, layout, brush, _settings, *, projpaint=False
): ...
def brush_texpaint_common_gradient(
    _panel, context, layout, brush, _settings, *, projpaint=False
): ...
def brush_texpaint_common_options(
    _panel, _context, layout, brush, _settings, *, projpaint=False
): ...
def brush_texture_settings(layout, brush, sculpt): ...
