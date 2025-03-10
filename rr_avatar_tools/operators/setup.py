import bpy

import rr_avatar_tools
from rr_avatar_tools import resources
from rr_avatar_tools.operators.base import RecRoomAvatarOperator
from rr_avatar_tools.preferences import RRAvatarToolsPreferences
from rr_avatar_tools.utils import put_file_in_known_good_state


class RR_OT_SetupSetupFile(bpy.types.Operator):
    """Setup file for avatar work"""

    bl_idname = 'rr.setup_setup_file'
    bl_label = 'Setup File'
    bl_options = {'REGISTER', 'UNDO'}

    rr_require_source_art_path = True
    rr_required_mode = 'OBJECT'

    suboperations = (
        bpy.ops.rr.setup_ensure_collections,
        bpy.ops.rr.setup_import_full_body_meshes,
        bpy.ops.rr.setup_import_modern_bean_body_meshes,
        bpy.ops.rr.setup_ensure_linked_libraries,
    )

    @classmethod
    def poll(cls, context):
        if not context.scene.get('rec_room_setup'):
            return True

        return any([op.poll() for op in cls.suboperations])

    def execute(self, context):
        bpy.ops.rr.setup_ensure_objects_in_good_state()

        for operation in self.suboperations:
            if not operation.poll():
                continue

            operation()

        context.scene['rec_room_setup'] = True

        return {'FINISHED'}


class RR_OT_SetupEnsureCollections(bpy.types.Operator):
    """Create avatar collections"""

    bl_idname = 'rr.setup_ensure_collections'
    bl_label = 'Create Avatar Collections'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def preferences(self) -> RRAvatarToolsPreferences:
        return bpy.context.preferences.addons['rr_avatar_tools'].preferences

    @classmethod
    def poll(cls, context):
        if not bpy.data.collections.get('Modern_Bean_Body'):
            return True

        if not bpy.data.collections.get('Full_Body'):
            return True

        return False

    def find_or_create_collection(self, name):
        result = bpy.data.collections.get(name)

        if not result:
            result = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(result)

        return result

    def execute(self, context):
        self.find_or_create_collection('Full_Body')
        self.find_or_create_collection('Modern_Bean_Body')

        return {'FINISHED'}


class RR_OT_SetupEnsureLinkedLibraries(bpy.types.Operator):
    bl_idname = "rr.setup_ensure_linked_libraries"
    bl_label = "Fix deprecated or missing Rec Room libraries"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (
            bpy.ops.rr.cleanup_remove_deprecated_libraries.poll()
            or bpy.ops.rr.cleanup_fix_broken_libraries.poll()
        )

    def execute(self, context):
        # Fix up old libraries
        if bpy.ops.rr.cleanup_remove_deprecated_libraries.poll():
            bpy.ops.rr.cleanup_remove_deprecated_libraries()

        # Fix any broken libraries
        if bpy.ops.rr.cleanup_fix_broken_libraries.poll():
            bpy.ops.rr.cleanup_fix_broken_libraries()

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RR_OT_SetupImportFullBodyMeshes(RecRoomAvatarOperator):
    """Imports full body meshes"""

    bl_idname = 'rr.setup_import_full_body_meshes'
    bl_label = 'Import Full_Body Avatar Meshes'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        collection = bpy.data.collections.get('FB_Resources')
        if not collection:
            return True

        if not bpy.data.actions.get('Calisthenics_MB'):
            return True

        avatar_meshes = bpy.data.objects.get('Avatar_Meshes')
        if not avatar_meshes:
            return True

        skeleton = bpy.data.objects.get('Avatar_Skeleton')
        if not skeleton:
            return True

        return False

    @classmethod
    def layer_collections(cls):
        def walk_view_layers(collection):
            return sum(
                [walk_view_layers(c) for c in collection.children], start=[collection]
            )

        return walk_view_layers(bpy.context.view_layer.layer_collection)

    @classmethod
    def get_view_layer(cls, name):
        matches = [c for c in cls.layer_collections() if c.name == name]
        return matches[0] if matches else None

    def execute(self, context):
        has_collection = bool(bpy.data.collections.get('FB_Resources'))
        has_FB_action = 'Calisthenics_FB' in bpy.data.actions
        has_MB_action = 'Calisthenics_MB' in bpy.data.actions

        # Add missing resources
        with bpy.data.libraries.load(
            resources.fb_library, link=True, relative=True
        ) as (data_from, data_to):
            if not has_collection:
                data_to.collections = [
                    c for c in data_from.collections if c == 'FB_Resources'
                ]

            data_to.actions = []

            if not has_FB_action:
                data_to.actions.append('Calisthenics_FB')

            if not has_MB_action:
                data_to.actions.append('Calisthenics_MB')

        # Configure timeline to see the entire calisthenics animations
        bpy.context.scene.frame_current = 0
        bpy.context.scene.frame_start = 0
        bpy.context.scene.frame_end = 800
        bpy.context.scene.render.fps = 30

        # Make library override
        if not has_collection:
            bpy.context.view_layer.active_layer_collection = self.get_view_layer(
                'Full_Body'
            )

            bpy.ops.object.collection_instance_add(name='FB_Resources')

            bpy.ops.object.select_all(action='DESELECT')

            # Find LayerCollection
            skin_meshes = bpy.data.objects['FB_Resources']
            skin_meshes.select_set(True)

            if bpy.ops.object.make_override_library.poll():
                bpy.ops.object.make_override_library()

        bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}


class RR_OT_SetupImportModernBeanBodyMeshes(RecRoomAvatarOperator):
    """Imports modern bean body meshes"""

    bl_idname = 'rr.setup_import_modern_bean_body_meshes'
    bl_label = 'Import Modern Bean Body Avatar Meshes'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        collection = bpy.data.collections.get('MB_Resources')
        if not collection:
            return True

        return False

    @classmethod
    def layer_collections(cls):
        def walk_view_layers(collection):
            return sum(
                [walk_view_layers(c) for c in collection.children], start=[collection]
            )

        return walk_view_layers(bpy.context.view_layer.layer_collection)

    @classmethod
    def get_view_layer(cls, name):
        matches = [c for c in cls.layer_collections() if c.name == name]
        return matches[0] if matches else None

    def execute(self, context):
        # Grab the MB_Resources collection
        with bpy.data.libraries.load(
            resources.mb_library, link=True, relative=True
        ) as (data_from, data_to):
            data_to.collections = [
                c for c in data_from.collections if c == 'MB_Resources'
            ]

        bpy.context.view_layer.active_layer_collection = self.get_view_layer(
            'Modern_Bean_Body'
        )

        bpy.ops.object.collection_instance_add(name='MB_Resources')

        bpy.ops.object.select_all(action='DESELECT')

        # Find LayerCollection
        skin_meshes = bpy.data.objects['MB_Resources']
        skin_meshes.select_set(True)

        bpy.ops.object.make_override_library()

        bpy.ops.object.select_all(action='DESELECT')

        # Ensure armature modifers are correctly configured
        col = bpy.data.collections['MB_Resources']
        for obj in col.objects:
            for modifier in [m for m in obj.modifiers if m.type == 'ARMATURE']:
                modifier.object = bpy.data.objects.get('Avatar_Skeleton')

        return {'FINISHED'}


class RR_OT_SetupEnsureObjectsInGoodState(bpy.types.Operator):
    """Setup file for avatar work"""

    bl_idname = 'rr.setup_ensure_objects_in_good_state'
    bl_label = 'Ensure Objects are in a good state'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        cached = bpy.context.view_layer.objects.active

        for o in bpy.data.objects[:]:
            o: bpy.types.Object

            try:
                bpy.context.view_layer.objects.active = o
                o.select_set(True)

                o.hide_set(False)
                o.hide_viewport = False

                if bpy.ops.object.mode_set.poll():
                    bpy.ops.object.mode_set()

                o.select_set(False)
                bpy.context.view_layer.objects.active = None
            except:
                pass

        bpy.context.view_layer.objects.active = cached

        return {'FINISHED'}


class RR_OT_SetupTestOutfits(bpy.types.Operator):
    bl_idname = "rr.setup_test_outfits"
    bl_label = "Link in test outfits"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        parent = bpy.data.collections.get('Full_Body')
        if not parent:
            return False

        return 'FB_TestOutfits' not in {c.name for c in parent.children}

    def execute(self, context):
        return self.execute_(context)

    @put_file_in_known_good_state
    def execute_(self, context):
        outfit_list = bpy.context.scene.outfit_list
        outfit_list.clear()

        # Full body test outfits
        collection = rr_avatar_tools.data.layer_collections.get('Full_Body')
        bpy.context.view_layer.active_layer_collection = collection

        with bpy.data.libraries.load(
            resources.fb_library, link=True, relative=True
        ) as (data_from, data_to):
            data_to.collections = [
                c for c in data_from.collections if c == 'FB_TestOutfits'
            ]

        bpy.ops.object.collection_instance_add(name='FB_TestOutfits')

        bpy.ops.object.select_all(action='DESELECT')

        # Find LayerCollection
        t = bpy.data.objects['FB_TestOutfits']
        t.select_set(True)

        if bpy.ops.object.make_override_library.poll():
            bpy.ops.object.make_override_library()

        c = bpy.data.collections.get('FB_TestOutfits')

        test_outfits = []

        for child in c.children:
            test_outfits.append(child.name)

            child.override_hierarchy_create(bpy.context.scene, bpy.context.view_layer)

            rr_avatar_tools.data.layer_collections[child.name].hide_viewport = True

            for o in child.objects:
                mod = o.modifiers.get('Armature')
                mod.object = bpy.data.objects.get('Avatar_Skeleton')

        # Modern bean test outfits
        collection = rr_avatar_tools.data.layer_collections.get('Modern_Bean_Body')
        bpy.context.view_layer.active_layer_collection = collection

        with bpy.data.libraries.load(
            resources.mb_library, link=True, relative=True
        ) as (data_from, data_to):
            data_to.collections = [
                c for c in data_from.collections if c == 'MB_TestOutfits'
            ]

        bpy.ops.object.collection_instance_add(name='MB_TestOutfits')

        bpy.ops.object.select_all(action='DESELECT')

        # Find LayerCollection
        t = bpy.data.objects['MB_TestOutfits']
        t.select_set(True)

        if bpy.ops.object.make_override_library.poll():
            bpy.ops.object.make_override_library()

        c = bpy.data.collections.get('MB_TestOutfits')

        for child in c.children:
            test_outfits.append(child.name)

            child.override_hierarchy_create(bpy.context.scene, bpy.context.view_layer)

            rr_avatar_tools.data.layer_collections[child.name].hide_viewport = True

            for o in child.objects:
                mod = o.modifiers.get('Armature')
                mod.object = bpy.data.objects.get('Avatar_Skeleton')

        for outfit in sorted(test_outfits):
            c = bpy.data.collections[outfit]
            outfit_list.add()
            outfit_list[-1].name = outfit
            outfit_list[-1].select = False

        return {'FINISHED'}


classes = (
    RR_OT_SetupSetupFile,
    RR_OT_SetupEnsureCollections,
    RR_OT_SetupImportFullBodyMeshes,
    RR_OT_SetupImportModernBeanBodyMeshes,
    RR_OT_SetupEnsureLinkedLibraries,
    RR_OT_SetupEnsureObjectsInGoodState,
    RR_OT_SetupTestOutfits,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
