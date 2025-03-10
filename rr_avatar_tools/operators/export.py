import os

import bpy

import rr_avatar_tools
from rr_avatar_tools.operators.base import RecRoomAvatarOperator
from rr_avatar_tools.utils import put_file_in_known_good_state


class RR_OT_ExportGenericAvatarItems(RecRoomAvatarOperator):
    """Setup file for avatar work"""
    bl_idname = 'rr.export_generic_avatar_items'
    bl_label = 'Export Avatar Items'
    bl_options = { 'REGISTER', 'UNDO' }

    rr_require_source_art_path = False
    rr_require_source_art_path = False
    rr_required_mode = 'OBJECT'

    @classmethod
    def poll(cls, context):
        prefs = bpy.context.preferences.addons['rr_avatar_tools'].preferences

        any_item_selected = bpy.ops.rr.export_generic_full_body_avatar_items.poll() or bpy.ops.rr.export_generic_modern_bean_avatar_items.poll()
        export_path_set = bool(prefs.generic_export_path)

        return any_item_selected and export_path_set

    def execute(self, context):
        return self.execute_(context)

    @put_file_in_known_good_state
    def execute_(self, context):
        if bpy.ops.rr.export_generic_full_body_avatar_items.poll():
            bpy.ops.rr.export_generic_full_body_avatar_items()

        if bpy.ops.rr.export_generic_modern_bean_avatar_items.poll():
            bpy.ops.rr.export_generic_modern_bean_avatar_items()

        count = len([p for p in bpy.context.scene.export_list if p.select and p.can_export()])

        self.report({'INFO'}, f'Exported {count} item(s)')

        return { 'FINISHED' }


class RR_OT_ExportGenericFullBodyAvatarItems(RecRoomAvatarOperator):
    """Export selected"""
    bl_idname = 'rr.export_generic_full_body_avatar_items'
    bl_label = 'Export Full Body Avatar Items'
    bl_options = { 'REGISTER', 'UNDO' }

    rr_require_rec_room_path = False
    rr_required_mode = 'OBJECT'

    @classmethod
    def poll(cls, context):
        return any(g.select for g in cls.export_groups())

    @classmethod
    def export_groups(cls):
        collections = [c.get('rec_room_uuid') for c in cls.export_collections()]
        return [i for i in bpy.context.scene.export_list if i.can_export() and i.uuid in collections] or []

    @classmethod
    def export_collections(cls):
        return [c for c in rr_avatar_tools.data.avatar_items if c.name.startswith('FB_')]

    def layer_collections(self):
        def walk_view_layers(collection):
            return sum([walk_view_layers(c) for c in collection.children], start=[collection])

        return walk_view_layers(bpy.context.view_layer.layer_collection)

    def set_active_collection(self, collection):
        collections = [c for c in self.layer_collections() if c.collection == collection]

        if collections:
            bpy.context.view_layer.active_layer_collection = collections[0]

    def execute(self, context):
        from io_scene_fbx import export_fbx_bin
        from rr_avatar_tools import settings

        for collection, group in zip(self.export_collections(), self.export_groups()):
            if not group.select:
                continue

            self.set_active_collection(collection)

            basepath = self.preferences().generic_export_path

            # Create output directory if needed
            if not os.path.exists(basepath):
                os.makedirs(basepath)

            filepath = os.path.join(
                basepath,
                f'{collection.name}.fbx'
            )

            export_fbx_bin.save(
                self,
                context,
                filepath=filepath,
                **settings.full_body_export_fbx
            )

        return { 'FINISHED' }


class RR_OT_ExportGenericModernBeanAvatarItems(RecRoomAvatarOperator):
    """Export selected"""
    bl_idname = 'rr.export_generic_modern_bean_avatar_items'
    bl_label = 'Export Modern Bean Avatar Items'
    bl_options = { 'REGISTER', 'UNDO' }

    rr_require_rec_room_path = False
    rr_required_mode = 'OBJECT'

    @classmethod
    def poll(cls, context):
        return any(g.select for g in cls.export_groups())

    @classmethod
    def export_groups(cls):
        collections = [c.get('rec_room_uuid') for c in cls.export_collections()]
        return [i for i in bpy.context.scene.export_list if i.can_export() and i.uuid in collections] or []

    @classmethod
    def export_collections(cls):
        return [c for c in rr_avatar_tools.data.avatar_items if c.name.startswith('MB_')]

    def layer_collections(self):
        def walk_view_layers(collection):
            return sum([walk_view_layers(c) for c in collection.children], start=[collection])

        return walk_view_layers(bpy.context.view_layer.layer_collection)

    def set_active_collection(self, collection):
        collections = [c for c in self.layer_collections() if c.collection == collection]

        if collections:
            bpy.context.view_layer.active_layer_collection = collections[0]

    def execute(self, context):
        from io_scene_fbx import export_fbx_bin
        from rr_avatar_tools import settings

        for collection, group in zip(self.export_collections(), self.export_groups()):
            if not group.select:
                continue

            self.set_active_collection(collection)

            basepath = self.preferences().generic_export_path

            # Create output directory if needed
            if not os.path.exists(basepath):
                os.makedirs(basepath)

            filepath = os.path.join(
                basepath,
                f'{collection.name}.fbx'
            )

            export_fbx_bin.save(
                self,
                context,
                filepath=filepath,
                **settings.full_body_export_fbx
            )

        return { 'FINISHED' }


class RR_OT_ExportSelectAvatarItemMeshes(RecRoomAvatarOperator):
    """Select all meshes for given avatar item"""
    bl_idname = 'rr.export_select_avatar_item_meshes'
    bl_label = 'Select Avatar Item Meshes'
    bl_options = { 'REGISTER', 'UNDO' }

    rr_require_rec_room_path = False
    rr_required_mode = 'OBJECT'

    target: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        collection = bpy.data.collections[self.target]

        for mesh in [o for o in collection.objects if o.type == 'MESH']:
            # Set active if None
            bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.active or mesh

            # Select mesh object
            mesh.select_set(True)

        return { 'FINISHED' }


class RR_OT_ExportDeleteAvatarItem(RecRoomAvatarOperator):
    """Delete Avatar Item"""
    bl_idname = 'rr.export_delete_avatar_item'
    bl_label = 'Delete Avatar Item'
    bl_options = { 'REGISTER', 'UNDO' }

    rr_require_rec_room_path = False
    rr_required_mode = 'OBJECT'

    target: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        collection = bpy.data.collections[self.target]

        scene_collection = context.scene.collection

        for mesh in [m for m in collection.objects if m.type == 'MESH']:
            scene_collection.objects.link(mesh)

        bpy.data.collections.remove(collection)

        return { 'FINISHED' }


class RR_OT_ExportToggleAvatarItemVisibilityByLOD(RecRoomAvatarOperator):
    """Toggle visibility"""
    bl_idname = 'rr.export_toggle_avatar_item_visibility_by_lod'
    bl_label = 'Toggle Avatar Item Visibility'
    bl_options = { 'REGISTER', 'UNDO' }

    rr_require_rec_room_path = False
    rr_required_mode = 'OBJECT'

    lod: bpy.props.EnumProperty(
        name='Target LOD',
        items=[
            ('ALL', 'ALL', ''),
            ('LOD0', 'LOD0', ''),
            ('LOD1', 'LOD1', ''),
            ('LOD2', 'LOD2', ''),
        ],
        default='ALL'
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Avatar items
        for collection in rr_avatar_tools.data.avatar_items:
            for object_ in [o for o in collection.objects if o.type == 'MESH' and 'LOD' in o.name]:
                if self.lod == 'ALL':
                    object_.hide_set(False)
                    continue

                object_.hide_set(not self.lod in object_.name)

        # Modern bean body meshes
        for object_ in [o for o in rr_avatar_tools.data.collections['MB_Resources'].objects if o.type == 'MESH' and 'LOD' in o.name]:
            if self.lod == 'ALL':
                object_.hide_set(False)
                continue

            object_.hide_set(not self.lod in object_.name)

        # Full body meshes
        for object_ in [o for o in rr_avatar_tools.data.collections['FB_Resources'].objects if o.type == 'MESH' and 'LOD' in o.name]:
            if self.lod == 'ALL':
                object_.hide_set(False)
                continue

            object_.hide_set(not self.lod in object_.name)

        # FB Test outfits
        if fb_collection := rr_avatar_tools.data.collections.get('FB_TestOutfits'):
            for avatar_item in [o for o in fb_collection.children]:
                for object_ in [o for o in avatar_item.objects if o.type == 'MESH' and 'LOD' in o.name]:
                    if self.lod == 'ALL':
                        object_.hide_set(False)
                        continue

                    object_.hide_set(not self.lod in object_.name)

        # MB Test outfits
        if mb_collection := rr_avatar_tools.data.collections.get('MB_TestOutfits'):
            for avatar_item in [o for o in mb_collection.children]:
                for object_ in [o for o in avatar_item.objects if o.type == 'MESH' and 'LOD' in o.name]:
                    if self.lod == 'ALL':
                        object_.hide_set(False)
                        continue

                    object_.hide_set(not self.lod in object_.name)

        return { 'FINISHED' }


classes = (
    RR_OT_ExportGenericAvatarItems,
    RR_OT_ExportGenericFullBodyAvatarItems,
    RR_OT_ExportGenericModernBeanAvatarItems,
    RR_OT_ExportSelectAvatarItemMeshes,
    RR_OT_ExportDeleteAvatarItem,
    RR_OT_ExportToggleAvatarItemVisibilityByLOD,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
