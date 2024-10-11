import typing
import collections.abc
import typing_extensions
import bpy.types

class PlayRenderedAnim(bpy.types.Operator):
    """Play back rendered frames/movies using an external player"""

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

def guess_player_path(preset): ...
