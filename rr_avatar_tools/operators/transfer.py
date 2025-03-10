import bpy

from bpy.props import (
    BoolProperty,
)

from bpy.types import (
    MirrorModifier,
)

from rr_avatar_tools.operators.base import RecRoomAvatarMeshOperator


class RR_OT_TransferUVs(RecRoomAvatarMeshOperator):
    """UVs from active to selected"""
    bl_idname = 'rr.transfer_uvs_from_active_mesh'
    bl_label = 'UVs From Active Mesh'
    bl_options = { 'REGISTER', 'UNDO' }

    @classmethod
    def poll(cls, context):
        active = bpy.context.view_layer.objects.active
        selection = [o for o in cls.selected_meshes() if o != active]

        return super().poll(context) and active and active.type == 'MESH' and selection

    def execute(self, context):
        # Cache selection
        active = bpy.context.active_object
        selected_meshes = [o for o in bpy.data.objects if o.select_get() and o.type == 'MESH' and o != active]

        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')

        for selected in selected_meshes:
            selected.select_set(True)

            # Transfer UVs from skin mesh to selection
            active.select_set(True)
            bpy.context.view_layer.objects.active = active

            bpy.ops.object.data_transfer(
                data_type='UV'
            )

            selected.select_set(False)

        # Restore selection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = active
        for selected in selected_meshes:
            selected.select_set(True)

        return { 'FINISHED' }


class RR_OT_TransferMakeSymmetricKeepUVs(RecRoomAvatarMeshOperator):
    """Mirror mesh geometry but keep UV layout"""
    bl_idname = 'rr.transfer_make_symmetric_keep_uvs'
    bl_label = 'Mirror Mesh Keep UVs'
    bl_options = { 'REGISTER', 'UNDO' }

    flip:BoolProperty(
        name='Flip',
        default=False
    )

    def execute(self, context):
        # Cache selection
        active = bpy.context.active_object
        selected_meshes = self.selected_meshes()

        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')

        for selected in selected_meshes:
            selected.select_set(True)

            # Duplicate selection
            bpy.ops.object.duplicate()
            duplicate = bpy.context.active_object
            duplicate.select_set(False)

            # Mirror original with bisect + clipping
            modifier: MirrorModifier = selected.modifiers.new('Mirror', 'MIRROR')
            modifier.use_bisect_axis[0] = True
            modifier.use_clip = True
            modifier.use_bisect_flip_axis[0] = self.flip

            bpy.context.view_layer.objects.active = selected
            bpy.ops.object.modifier_apply(modifier=modifier.name)

            # Transfer UVs from duplicate to selection
            duplicate.select_set(True)
            bpy.context.view_layer.objects.active = duplicate
            selected.select_set(True)

            bpy.ops.object.data_transfer(
                data_type='UV'
            )

            selected.select_set(False)

            # Delete duplicate
            bpy.ops.object.delete()

        # Restore selection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = active
        for selected in selected_meshes:
            selected.select_set(True)

        return { 'FINISHED' }


classes = (
    RR_OT_TransferUVs,
    RR_OT_TransferMakeSymmetricKeepUVs,
)

panel = (
    RR_OT_TransferUVs,
    RR_OT_TransferMakeSymmetricKeepUVs,
)


@bpy.app.handlers.persistent
def update_label(cls, scene):
    """Update RR_OT_TransferUVs label based on selection"""
    active = bpy.context.view_layer.objects.active

    if not active:
        RR_OT_TransferUVs.bl_label = f'Transfer UVs'
    else:
        RR_OT_TransferUVs.bl_label = f'UVs from {active.name}'


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)

    if update_label not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(update_label)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)

    if update_label in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(update_label)
