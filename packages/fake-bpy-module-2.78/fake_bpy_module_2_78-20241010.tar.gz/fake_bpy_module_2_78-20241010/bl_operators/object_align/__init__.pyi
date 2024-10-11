import typing
import collections.abc
import typing_extensions
import bpy.types

class AlignObjects(bpy.types.Operator):
    """Align Objects"""

    align_axis: typing.Any
    align_mode: typing.Any
    bb_quality: typing.Any
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    order: typing.Any
    relative_to: typing.Any

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

def GlobalBB_HQ(obj): ...
def GlobalBB_LQ(bb_world): ...
def align_objects(
    context, align_x, align_y, align_z, align_mode, relative_to, bb_quality
): ...
