import typing
import collections.abc
import typing_extensions
import bpy.types

class PROPERTIES_HT_header(bpy.types.Header):
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

def register(): ...
def unregister(): ...
