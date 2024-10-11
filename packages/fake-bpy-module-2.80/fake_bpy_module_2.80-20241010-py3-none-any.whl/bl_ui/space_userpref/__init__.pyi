import typing
import collections.abc
import typing_extensions
import bpy.types

class FilePathsPanel:
    bl_region_type: typing.Any
    bl_space_type: typing.Any

    def draw(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class PreferencePanel:
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_region_type: typing.Any
    bl_space_type: typing.Any

    def draw(self, context):
        """

        :param context:
        """

class PreferenceThemeSpacePanel:
    bl_region_type: typing.Any
    bl_space_type: typing.Any
    ui_delimiters: typing.Any

    def draw(self, context):
        """

        :param context:
        """

    def draw_header(self, _context):
        """

        :param _context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class PreferenceThemeWidgetColorPanel:
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_space_type: typing.Any

    def draw(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class StudioLightPanelMixin:
    bl_region_type: typing.Any
    bl_space_type: typing.Any

    def draw(self, context):
        """

        :param context:
        """

    def draw_light_list(self, layout, lights):
        """

        :param layout:
        :param lights:
        """

    def draw_studio_light(self, layout, studio_light):
        """

        :param layout:
        :param studio_light:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class ThemeGenericClassGenerator:
    @staticmethod
    def generate_panel_classes_for_wcols(): ...
    @staticmethod
    def generate_panel_classes_from_theme_areas(): ...
    @staticmethod
    def generate_theme_area_child_panel_classes(
        parent_id, rna_type, theme_area, datapath
    ):
        """

        :param parent_id:
        :param rna_type:
        :param theme_area:
        :param datapath:
        """

class USERPREF_HT_header(bpy.types.Header):
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

    @staticmethod
    def draw_buttons(layout, context):
        """

        :param layout:
        :param context:
        """

class USERPREF_MT_interface_theme_presets(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    preset_operator: typing.Any
    preset_subdir: typing.Any
    preset_type: typing.Any
    preset_xml_map: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    @staticmethod
    def reset_cb(context):
        """

        :param context:
        """

class USERPREF_MT_keyconfigs(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    preset_operator: typing.Any
    preset_subdir: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

class USERPREF_MT_ndof_settings(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

class USERPREF_MT_save_load(bpy.types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

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

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

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

class USERPREF_PT_animation_autokey(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_animation_fcurves(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_animation_keyframes(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_animation_timeline(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_edit_annotations(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_edit_cursor(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_edit_gpencil(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_edit_misc(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_edit_objects(bpy.types.Panel):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_edit_objects_duplicate_data(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_edit_objects_new(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_edit_weight_paint(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_file_paths_applications(FilePathsPanel, bpy.types.Panel):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_file_paths_data(FilePathsPanel, bpy.types.Panel):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, _layout):
        """

        :param context:
        :param _layout:
        """

class USERPREF_PT_file_paths_development(FilePathsPanel, bpy.types.Panel):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_file_paths_render(FilePathsPanel, bpy.types.Panel):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, _layout):
        """

        :param context:
        :param _layout:
        """

class USERPREF_PT_input_keyboard(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_input_mouse(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_input_ndof(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_input_tablet(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_interface_display(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_interface_editors(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_interface_menus(bpy.types.Panel):
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_interface_menus_mouse_over(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_header(self, context):
        """

        :param context:
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_interface_menus_pie(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_interface_text(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_interface_translation(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    bl_translation_context: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_header(self, context):
        """

        :param context:
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_keymap(bpy.types.Panel):
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_navigation_bar(bpy.types.Panel):
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

class USERPREF_PT_navigation_fly_walk(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_navigation_fly_walk_gravity(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_header(self, context):
        """

        :param context:
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_navigation_fly_walk_navigation(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_navigation_orbit(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_navigation_zoom(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_save_preferences(bpy.types.Panel):
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_saveload_autorun(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

    def draw_header(self, context):
        """

        :param context:
        """

class USERPREF_PT_saveload_blend(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_saveload_blend_autosave(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_saveload_file_browser(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_studiolight_light_editor(bpy.types.Panel):
    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

    def opengl_light_buttons(self, layout, light):
        """

        :param layout:
        :param light:
        """

class USERPREF_PT_system_cycles_devices(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_system_memory(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_system_sound(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
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

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, _context):
        """

        :param _context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_theme_bone_color_sets(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_header(self, _context):
        """

        :param _context:
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_theme_interface_gizmos(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_theme_interface_icons(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_theme_interface_state(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_theme_interface_styles(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

class USERPREF_PT_theme_text_style(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_header(self, _context):
        """

        :param _context:
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_theme_user_interface(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw(self, context):
        """

        :param context:
        """

    def draw_header(self, _context):
        """

        :param _context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_viewport_display(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_viewport_quality(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_viewport_selection(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_viewport_textures(PreferencePanel, bpy.types.Panel):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_props(context, layout) function.
    """

    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_props(self, context, layout):
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class USERPREF_PT_studiolight_lights(bpy.types.Panel, StudioLightPanelMixin):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any
    sl_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_header_preset(self, _context):
        """

        :param _context:
        """

class USERPREF_PT_studiolight_matcaps(bpy.types.Panel, StudioLightPanelMixin):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any
    sl_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_header_preset(self, _context):
        """

        :param _context:
        """

class USERPREF_PT_studiolight_world(bpy.types.Panel, StudioLightPanelMixin):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any
    sl_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def draw_header_preset(self, _context):
        """

        :param _context:
        """
