import typing
import collections.abc
import typing_extensions
import bpy.types

class SequencerCrossfadeSounds(bpy.types.Operator):
    """Do cross-fading volume animation of two selected sound strips"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    order: typing.Any

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class SequencerCutMulticam(bpy.types.Operator):
    """Cut multi-cam strip and select camera"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    camera: typing.Any
    id_data: typing.Any
    order: typing.Any

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class SequencerDeinterlaceSelectedMovies(bpy.types.Operator):
    """Deinterlace all selected movie sources"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    order: typing.Any

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """
