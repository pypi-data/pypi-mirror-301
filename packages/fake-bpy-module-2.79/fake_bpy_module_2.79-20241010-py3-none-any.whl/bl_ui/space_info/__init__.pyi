import typing
import collections.abc
import typing_extensions
import bpy.types

class INFO_HT_header(bpy.types.Header):
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class INFO_MT_editor_menus(bpy.types.Menu):
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

class INFO_MT_file(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class INFO_MT_file_export(bpy.types.Menu):
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

class INFO_MT_file_external_data(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class INFO_MT_file_import(bpy.types.Menu):
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

class INFO_MT_file_previews(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class INFO_MT_game(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class INFO_MT_help(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class INFO_MT_opengl_render(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class INFO_MT_render(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class INFO_MT_window(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """
