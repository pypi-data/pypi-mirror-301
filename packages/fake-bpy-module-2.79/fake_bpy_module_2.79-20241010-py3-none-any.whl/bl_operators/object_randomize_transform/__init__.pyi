import typing
import collections.abc
import typing_extensions
import bpy.types

class RandomizeLocRotSize(bpy.types.Operator):
    """Randomize objects loc/rot/scale"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    loc: typing.Any
    order: typing.Any
    random_seed: typing.Any
    rot: typing.Any
    scale: typing.Any
    scale_even: typing.Any
    use_delta: typing.Any
    use_loc: typing.Any
    use_rot: typing.Any
    use_scale: typing.Any

    def execute(self, context):
        """

        :param context:
        """

def randomize_selected(
    context, seed, delta, loc, rot, scale, scale_even, scale_min
): ...
