import typing
import collections.abc
import typing_extensions
import bpy.types

class USERPREF_HT_header(bpy.types.Header):
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class USERPREF_MT_addons_online_resources(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class USERPREF_MT_appconfigs(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    preset_operator: typing.Any
    preset_subdir: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class USERPREF_MT_interaction_presets(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    preset_operator: typing.Any
    preset_subdir: typing.Any

class USERPREF_MT_interface_theme_presets(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    preset_operator: typing.Any
    preset_subdir: typing.Any
    preset_type: typing.Any
    preset_xml_map: typing.Any

class USERPREF_MT_keyconfigs(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    preset_operator: typing.Any
    preset_subdir: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class USERPREF_MT_ndof_settings(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class USERPREF_MT_splash(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class USERPREF_MT_splash_footer(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class USERPREF_PT_addons(bpy.types.Panel):
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

    @staticmethod
    def draw_error(layout, message):
        """

        :param layout:
        :param message:
        """

    @staticmethod
    def is_user_addon(mod, user_addon_paths):
        """

        :param mod:
        :param user_addon_paths:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_edit(bpy.types.Panel):
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

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_file(bpy.types.Panel):
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

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_input(bpy.types.Panel):
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

    @staticmethod
    def draw_input_prefs(inputs, layout):
        """

        :param inputs:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_interface(bpy.types.Panel):
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

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_system(bpy.types.Panel):
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

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_tabs(bpy.types.Panel):
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

class USERPREF_PT_theme(bpy.types.Panel):
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any
    ui_delimiters: typing.Any

    def draw(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

def opengl_lamp_buttons(column, lamp): ...
