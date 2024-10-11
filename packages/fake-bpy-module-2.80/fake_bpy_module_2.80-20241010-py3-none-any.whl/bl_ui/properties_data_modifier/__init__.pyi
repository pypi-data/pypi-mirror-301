import typing
import collections.abc
import typing_extensions
import bpy.types

class DATA_PT_gpencil_modifiers(ModifierButtonsPanel, bpy.types.Panel):
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def GP_ARMATURE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_ARRAY(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_BUILD(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_COLOR(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_HOOK(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_LATTICE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_MIRROR(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_NOISE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_OFFSET(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_OPACITY(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_SIMPLIFY(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_SMOOTH(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_SUBDIV(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_THICK(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_TIME(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def GP_TINT(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

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

    def check_conflicts(self, layout, ob):
        """

        :param layout:
        :param ob:
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

class DATA_PT_modifiers(ModifierButtonsPanel, bpy.types.Panel):
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def ARMATURE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def ARRAY(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def BEVEL(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def BOOLEAN(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def BUILD(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def CAST(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def CLOTH(self, layout, _ob, _md):
        """

        :param layout:
        :param _ob:
        :param _md:
        """

    def COLLISION(self, layout, _ob, _md):
        """

        :param layout:
        :param _ob:
        :param _md:
        """

    def CORRECTIVE_SMOOTH(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def CURVE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def DATA_TRANSFER(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def DECIMATE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def DISPLACE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def DYNAMIC_PAINT(self, layout, _ob, _md):
        """

        :param layout:
        :param _ob:
        :param _md:
        """

    def EDGE_SPLIT(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def EXPLODE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def FLUID_SIMULATION(self, layout, _ob, _md):
        """

        :param layout:
        :param _ob:
        :param _md:
        """

    def HOOK(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def LAPLACIANDEFORM(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def LAPLACIANSMOOTH(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def LATTICE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def MASK(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def MESH_CACHE(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def MESH_DEFORM(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def MESH_SEQUENCE_CACHE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def MIRROR(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def MULTIRES(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def NORMAL_EDIT(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def OCEAN(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def PARTICLE_INSTANCE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def PARTICLE_SYSTEM(self, layout, _ob, _md):
        """

        :param layout:
        :param _ob:
        :param _md:
        """

    def REMESH(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def SCREW(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def SHRINKWRAP(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def SIMPLE_DEFORM(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def SKIN(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def SMOKE(self, layout, _ob, _md):
        """

        :param layout:
        :param _ob:
        :param _md:
        """

    def SMOOTH(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def SOFT_BODY(self, layout, _ob, _md):
        """

        :param layout:
        :param _ob:
        :param _md:
        """

    def SOLIDIFY(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def SUBSURF(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def SURFACE(self, layout, _ob, _md):
        """

        :param layout:
        :param _ob:
        :param _md:
        """

    def SURFACE_DEFORM(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def TRIANGULATE(self, layout, _ob, md):
        """

        :param layout:
        :param _ob:
        :param md:
        """

    def UV_PROJECT(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def UV_WARP(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def VERTEX_WEIGHT_EDIT(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def VERTEX_WEIGHT_MIX(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def VERTEX_WEIGHT_PROXIMITY(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def WARP(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def WAVE(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def WEIGHTED_NORMAL(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

    def WIREFRAME(self, layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

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

    @staticmethod
    def vertex_weight_mask(layout, ob, md):
        """

        :param layout:
        :param ob:
        :param md:
        """

class ModifierButtonsPanel:
    bl_context: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_space_type: typing.Any
