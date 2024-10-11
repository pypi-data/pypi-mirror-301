import typing
import collections.abc
import typing_extensions
import bpy.types

class WM_OT_previews_batch_clear(bpy.types.Operator):
    """Clear selected .blend file's previews"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    directory: typing.Any
    files: typing.Any
    filter_blender: typing.Any
    filter_folder: typing.Any
    id_data: typing.Any
    order: typing.Any
    use_backups: typing.Any
    use_groups: typing.Any
    use_intern_data: typing.Any
    use_objects: typing.Any
    use_scenes: typing.Any
    use_trusted: typing.Any

    def execute(self, context):
        """

        :param context:
        """

    def invoke(self, context, event):
        """

        :param context:
        :param event:
        """

class WM_OT_previews_batch_generate(bpy.types.Operator):
    """Generate selected .blend file's previews"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    directory: typing.Any
    files: typing.Any
    filter_blender: typing.Any
    filter_folder: typing.Any
    id_data: typing.Any
    order: typing.Any
    use_backups: typing.Any
    use_groups: typing.Any
    use_intern_data: typing.Any
    use_objects: typing.Any
    use_scenes: typing.Any
    use_trusted: typing.Any

    def execute(self, context):
        """

        :param context:
        """

    def invoke(self, context, event):
        """

        :param context:
        :param event:
        """
