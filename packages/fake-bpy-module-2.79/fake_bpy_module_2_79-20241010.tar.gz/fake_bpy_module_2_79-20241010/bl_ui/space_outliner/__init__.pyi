import typing
import collections.abc
import typing_extensions
import bpy.types

class OUTLINER_HT_header(bpy.types.Header):
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class OUTLINER_MT_edit_datablocks(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class OUTLINER_MT_editor_menus(bpy.types.Menu):
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

    @staticmethod
    def draw_menus(layout, context):
        """

        :param layout:
        :param context:
        """

class OUTLINER_MT_search(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class OUTLINER_MT_view(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """
