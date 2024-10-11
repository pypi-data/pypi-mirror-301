import typing
import collections.abc
import typing_extensions
import bpy.types

class ToolActivePanelHelper:
    bl_label: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class ToolDef:
    cursor: typing.Any
    data_block: typing.Any
    description: typing.Any
    draw_cursor: typing.Any
    draw_settings: typing.Any
    icon: typing.Any
    idname: typing.Any
    keymap: typing.Any
    label: typing.Any
    operator: typing.Any
    widget: typing.Any

class ToolSelectPanelHelper:
    def draw(self, context):
        """

        :param context:
        """

    @staticmethod
    def draw_active_tool_header(
        context, layout, *, show_tool_name=False, tool_key=None
    ):
        """

        :param context:
        :param layout:
        :param show_tool_name:
        :param tool_key:
        """

    @classmethod
    def draw_cls(cls, layout, context, detect_layout=True, scale_y=1.75):
        """

        :param layout:
        :param context:
        :param detect_layout:
        :param scale_y:
        """

    @classmethod
    def keymap_ui_hierarchy(cls, context_mode):
        """

        :param context_mode:
        """

    @classmethod
    def register(cls): ...
    @staticmethod
    def tool_active_from_context(context):
        """

        :param context:
        """

class WM_MT_toolsystem_submenu(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param context:
        """

def activate_by_id(context, space_type, text): ...
def activate_by_id_or_cycle(context, space_type, idname, offset=1): ...
def description_from_id(context, space_type, idname, *, use_operator=True): ...
def item_from_flat_index(context, space_type, index): ...
def item_from_id(context, space_type, idname): ...
def item_from_index(context, space_type, index): ...
def keymap_from_id(context, space_type, idname): ...
