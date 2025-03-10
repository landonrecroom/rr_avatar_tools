import os

from pathlib import Path

import bpy

import rr_avatar_tools.data
from rr_avatar_tools import resources
from rr_avatar_tools.operators.base import (
    RecRoomAvatarOperator,
)
from rr_avatar_tools.utils import put_file_in_known_good_state


class RR_OT_CleanupScorchFile(RecRoomAvatarOperator):
    """Delete all non-avatar item objects in the scene"""

    bl_idname = 'rr.cleanup_scorch_file'
    bl_label = 'Scorch File'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return self.execute_(context)

    @put_file_in_known_good_state
    def execute_(self, context):
        bpy.ops.object.select_all(action='DESELECT')

        # Remove all linked libraries
        while bpy.data.libraries:
            bpy.data.libraries.remove(bpy.data.libraries[0])

        def remove_object_and_children(name: str):
            ob: bpy.types.Object = bpy.data.objects.get(name)
            if not ob:
                return

            for c in ob.children_recursive:
                bpy.data.objects.remove(c)

            bpy.data.objects.remove(ob)

        for mesh in [
            o
            for o in bpy.data.objects
            if o.type == 'MESH' and o.name.upper().startswith('BB_')
        ]:
            mesh.select_set(True)
            bpy.context.view_layer.objects.active = mesh

            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            mesh.parent = None

            mesh.select_set(False)
            bpy.context.view_layer.objects.active = None

        # Remove base objects
        remove_object_and_children('GeoGroup')
        remove_object_and_children('HandGroup')
        remove_object_and_children('Avatar_Meshes')
        remove_object_and_children('Avatar_Skeleton')

        # Remove all non-mesh objects
        for o in bpy.data.objects[:]:
            if o.type == 'MESH' and (o.name.upper()[:3] in ('FB_', 'MB_', 'BB_')):
                o.hide_set(False)

                o.select_set(True)
                bpy.context.view_layer.objects.active = o
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.context.view_layer.objects.active = None
                o.select_set(False)

                collection = bpy.context.scene.collection
                if collection not in o.users_collection:
                    bpy.context.scene.collection.objects.link(o)

            else:
                bpy.data.objects.remove(o)

        # Remove all collections
        while bpy.data.collections:
            bpy.data.collections.remove(bpy.data.collections[0])

        # Clean data
        bpy.ops.outliner.orphans_purge(do_recursive=True)

        return {'FINISHED'}


class RR_OT_CleanupRecreateAvatarItems(RecRoomAvatarOperator):
    """Recreate Avatar Items"""

    bl_idname = 'rr.cleanup_recreate_avatar_items'
    bl_label = 'Recreate Avatar Items'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')

        def filter(ob):
            if ob.type != 'MESH':
                return False

            resource_collections = {'MB_Resources', 'FB_Resources'}
            object_collections = [c.name for c in ob.users_collection]

            if resource_collections.intersection(object_collections):
                return False

            n = ob.name[:3].upper()

            return n in ('FB_', 'MB_')

        for m in [o for o in bpy.data.objects if filter(o)]:
            m.select_set(True)
            bpy.context.view_layer.objects.active = m

            bpy.ops.rr.create_avatar_item()
            bpy.ops.object.select_all(action='DESELECT')

            bpy.context.view_layer.objects.active = None
            m.select_set(False)

        return {'FINISHED'}


class RR_OT_CleanupPutOrphanedObjectInLegacyCollection(RecRoomAvatarOperator):
    """Put orphan objects in legacy collection"""

    bl_idname = 'rr.cleanup_put_orphan_objects_in_legacy_collection'
    bl_label = 'Put Orphan Objects in Legacy Collection'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')

        scene_collection = bpy.context.scene.collection

        legacy_collection = bpy.data.collections.get('Legacy_Items')
        if not legacy_collection:
            legacy_collection = bpy.data.collections.new('Legacy_Items')
            scene_collection.children.link(legacy_collection)

        for m in [o for o in bpy.context.scene.collection.objects if o.type == 'MESH']:
            legacy_collection.objects.link(m)
            scene_collection.objects.unlink(m)

        lc = rr_avatar_tools.data.layer_collections.get('Legacy_Items')
        lc.hide_viewport = True

        return {'FINISHED'}


class RR_OT_CleanupRebuildFile(RecRoomAvatarOperator):
    """Delete all non-avatar item objects, setup file, and recreate all avatar items"""

    bl_idname = 'rr.cleanup_rebuild_files'
    bl_label = 'Rebuild File'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.rr.cleanup_scorch_file()
        bpy.ops.rr.setup_setup_file()
        bpy.ops.rr.cleanup_recreate_avatar_items()
        bpy.ops.rr.cleanup_put_orphan_objects_in_legacy_collection()

        return {'FINISHED'}


class RR_OT_CleanupFixBrokenLibraries(RecRoomAvatarOperator):
    """Fix Broken Libraries"""

    bl_idname = 'rr.cleanup_fix_broken_libraries'
    bl_label = 'Fix Broken Libraries'
    bl_options = {'REGISTER'}

    @classmethod
    def libraries(cls):
        library_files = (
            os.path.basename(resources.mb_library),
            os.path.basename(resources.fb_library),
        )

        return [
            l
            for l in bpy.data.libraries
            if os.path.basename(l.filepath) in library_files
        ]

    @classmethod
    def broken_libraries(cls):
        return [l for l in cls.libraries() if l.is_missing]

    @classmethod
    def poll(cls, context):
        return any(cls.broken_libraries())

    def execute(self, context):
        broken = self.broken_libraries()
        directory = str(Path(__file__).parent.parent / 'resources')
        bpy.ops.file.find_missing_files(directory=directory)

        # Reload all our libraries
        for library in broken:
            library.reload()

        return {'FINISHED'}


class RR_OT_CleanupRemoveDeprecatedLibraries(RecRoomAvatarOperator):
    """Remove deprecated  Libraries"""

    bl_idname = 'rr.cleanup_remove_deprecated_libraries'
    bl_label = 'Remove Deprecated Libraries'
    bl_options = {'REGISTER'}

    @classmethod
    def broken_libraries(cls):
        library_files = (
            'Avatar_Rig.blend',
            'FB_Avatar_Skin.blend',
        )

        return [
            l
            for l in bpy.data.libraries
            if os.path.basename(l.filepath) in library_files
        ]

    @classmethod
    def poll(cls, context):
        return any(cls.broken_libraries())

    def execute(self, context):
        broken = self.broken_libraries()

        # Remove old libraries
        for library in broken:
            bpy.data.libraries.remove(library)

        return {'FINISHED'}


classes = (
    RR_OT_CleanupScorchFile,
    RR_OT_CleanupRecreateAvatarItems,
    RR_OT_CleanupRebuildFile,
    RR_OT_CleanupFixBrokenLibraries,
    RR_OT_CleanupRemoveDeprecatedLibraries,
    RR_OT_CleanupPutOrphanedObjectInLegacyCollection,
)

panel = (
    RR_OT_CleanupRebuildFile,
    RR_OT_CleanupScorchFile,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
