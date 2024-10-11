import typing
import collections.abc
import typing_extensions
import bpy.types

class MeshMirrorUV(bpy.types.Operator):
    """Copy mirror UV coordinates on the X axis based on a mirrored mesh"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    direction: typing.Any
    id_data: typing.Any
    order: typing.Any
    precision: typing.Any

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class MeshSelectNext(bpy.types.Operator):
    """Select the next element (using selection order)"""

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

class MeshSelectPrev(bpy.types.Operator):
    """Select the next element (using selection order)"""

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
