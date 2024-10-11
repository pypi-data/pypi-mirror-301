import typing
import collections.abc
import typing_extensions
import bpy.types
import rna_prop_ui

class CAMERA_MT_presets(bpy.types.Menu):
    COMPAT_ENGINES: typing.Any
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    preset_operator: typing.Any
    preset_subdir: typing.Any

class CameraButtonsPanel:
    bl_context: typing.Any
    bl_region_type: typing.Any
    bl_space_type: typing.Any

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class DATA_PT_camera(CameraButtonsPanel, bpy.types.Panel):
    COMPAT_ENGINES: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class DATA_PT_camera_display(CameraButtonsPanel, bpy.types.Panel):
    COMPAT_ENGINES: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class DATA_PT_camera_dof(CameraButtonsPanel, bpy.types.Panel):
    COMPAT_ENGINES: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class DATA_PT_camera_safe_areas(CameraButtonsPanel, bpy.types.Panel):
    COMPAT_ENGINES: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

    def draw_header(self, context):
        """

        :param context:
        """

class DATA_PT_camera_stereoscopy(CameraButtonsPanel, bpy.types.Panel):
    COMPAT_ENGINES: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class DATA_PT_context_camera(CameraButtonsPanel, bpy.types.Panel):
    COMPAT_ENGINES: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class DATA_PT_custom_props_camera(
    rna_prop_ui.PropertyPanel, CameraButtonsPanel, bpy.types.Panel
):
    """The subclass should have its own poll function
    and the variable '_context_path' MUST be set.
    """

    COMPAT_ENGINES: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

class DATA_PT_lens(CameraButtonsPanel, bpy.types.Panel):
    COMPAT_ENGINES: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class SAFE_AREAS_MT_presets(bpy.types.Menu):
    COMPAT_ENGINES: typing.Any
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    preset_operator: typing.Any
    preset_subdir: typing.Any

def draw_display_safe_settings(layout, safe_data, settings): ...
