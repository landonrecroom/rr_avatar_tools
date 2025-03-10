import os

import bpy

from rr_avatar_tools import resources
from rr_avatar_tools.operators.base import (
    RecRoomAvatarMeshOperator,
)

from rr_avatar_tools.utils import put_file_in_known_good_state


fb_transfermeshes = {
    'BELT': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Belt_Apron', 'Belt Apron', ''),
        ('FB_TransferMesh_Belt_Floatie', 'Belt Floatie', ''),
        ('FB_TransferMesh_Belt_Rigid', 'Belt Rigid', ''),
        ('FB_TransferMesh_Belt_Standard', 'Belt Standard', ''),
    ],
    'EAR': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Ear_Standard', 'Ear Standard', ''),
    ],
    'EYE': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Eye_Standard', 'Eye Standard', ''),
    ],
    'HAIR': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Hair_Long', 'Hair Long', ''),
        ('FB_TransferMesh_Hair_Short', 'Hair Short', ''),
    ],
    'HAT': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Hat_FaceMask', 'Hat FaceMask', ''),
        ('FB_TransferMesh_Hat_Rigid', 'Hat Rigid', ''),
    ],
    'LEG': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Legs_Standard', 'Legs Standard', ''),
    ],
    'MOUTH': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Mouth_Standard', 'Mouth Standard', ''),
    ],
    'NECK': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Neck_Large', 'Neck Large', ''),
        ('FB_TransferMesh_Neck_Medium', 'Neck Medium', ''),
        ('FB_TransferMesh_Neck_Standard', 'Neck Standard', ''),
    ],
    'SHOE': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Shoes_Boots', 'Shoes Boots', ''),
        ('FB_TransferMesh_Shoes_KneeHigh', 'Shoes Knee High', ''),
        ('FB_TransferMesh_Shoes_Standard', 'Shoes Standard', ''),
    ],
    'SHOULDER': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Shoulder_Long', 'Shoulder Long', ''),
        ('FB_TransferMesh_Shoulder_Rigid', 'Shoulder Rigid', ''),
        ('FB_TransferMesh_Shoulder_Standard', 'Shoulder Standard', ''),
    ],
    'SHIRT': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Torso_BodyRigid', 'Torso Body Rigid', ''),
        ('FB_TransferMesh_Torso_BodySemiRigid', 'Torso Body SemiRigid', ''),
        ('FB_TransferMesh_Torso_Dress', 'Torso Dress', ''),
        ('FB_TransferMesh_Torso_Sleeveless', 'Torso Sleeveless', ''),
        ('FB_TransferMesh_Torso_Standard', 'Torso Standard', ''),
    ],
    'WRIST': [
        ('BodyMesh_LOD0', 'Body Mesh', ''),
        ('FB_TransferMesh_Wrist_Long', 'Wrist Long', ''),
        ('FB_TransferMesh_Wrist_Mitten', 'Wrist Mitten', ''),
        ('FB_TransferMesh_Wrist_Standard', 'Wrist Standard', ''),
    ],
}

mb_transfermeshes = {
    'BELT': [
        ('MB_BodyMesh_LOD0', 'Body Mesh', ''),
        ('MB_TransferMesh_Belt_Apron', 'Belt Apron', ''),
        ('MB_TransferMesh_Belt_Floatie', 'Belt Floatie', ''),
        ('MB_TransferMesh_Belt_Rigid', 'Belt Rigid', ''),
        ('MB_TransferMesh_Belt_Standard', 'Belt Standard', ''),
    ],
    'NECK': [
        ('MB_BodyMesh_LOD0', 'Body Mesh', ''),
        ('MB_TransferMesh_Neck_Large', 'Neck Large', ''),
        ('MB_TransferMesh_Neck_Medium', 'Neck Medium', ''),
        ('MB_TransferMesh_Neck_Standard', 'Neck Standard', ''),
    ],
    'SHOULDER': [
        ('MB_BodyMesh_LOD0', 'Body Mesh', ''),
        ('MB_TransferMesh_Shoulder_Long', 'Shoulder Long', ''),
        ('MB_TransferMesh_Shoulder_Rigid', 'Shoulder Rigid', ''),
        ('MB_TransferMesh_Shoulder_Standard', 'Shoulder Standard', ''),
    ],
    'SHIRT': [
        ('MB_BodyMesh_LOD0', 'Body Mesh', ''),
        ('MB_TransferMesh_Torso_BodyRigid', 'Torso BodyRigid', ''),
        ('MB_TransferMesh_Torso_BodySemiRigid', 'Torso BodySemiRigid', ''),
        ('MB_TransferMesh_Torso_Dress', 'Torso Dress', ''),
        ('MB_TransferMesh_Torso_Sleeveless', 'Torso Sleeveless', ''),
        ('MB_TransferMesh_Torso_Standard', 'Torso Standard', ''),
    ],
    'WRIST': [
        ('MB_BodyMesh_LOD0', 'Body Mesh', ''),
        ('MB_TransferMesh_Wrist_Long', 'Wrist Long', ''),
        ('MB_TransferMesh_Wrist_Mitten', 'Wrist Mitten', ''),
        ('MB_TransferMesh_Wrist_Standard', 'Wrist Standard', ''),
    ],
}


def transfer_mesh_items(scene, context):
    def filter(name):
        return name[:2] in ('MB', 'FB')

    selection = [o for o in bpy.data.objects if o.select_get() and filter(o.name)]

    first = selection[0]

    parts = first.name.split('_')
    item_type = parts[-2].upper()

    presets = fb_transfermeshes

    # For now, limit modern bean transfer meshes
    if first.name.upper().startswith('MB_'):
        presets = mb_transfermeshes

    results = presets.get(
        item_type,
        [
            ('BodyMesh_LOD0', 'Body Mesh', ''),
        ],
    )

    return results


transfer_mesh_default_item = 'BodyMesh_LOD0'


class RR_OT_WeightsTransferWeightsFromPresets(RecRoomAvatarMeshOperator):
    """Weights From Presets"""

    bl_idname = 'rr.weights_transfer_weights_from_skin_mesh'
    bl_label = 'Weights From Presets'
    bl_options = {'REGISTER', 'UNDO'}

    transfer_mesh: bpy.props.EnumProperty(
        name='Transfer Mesh', items=transfer_mesh_items
    )

    @classmethod
    def poll(cls, context):
        return (
            bpy.ops.rr.weights_transfer_fb_weights_from_skin_mesh.poll()
            or bpy.ops.rr.weights_transfer_mb_weights_from_skin_mesh.poll()
        )

    def execute(self, context):
        if bpy.ops.rr.weights_transfer_fb_weights_from_skin_mesh.poll():
            bpy.ops.rr.weights_transfer_fb_weights_from_skin_mesh(
                transfer_mesh=self.transfer_mesh or transfer_mesh_default_item
            )

        elif bpy.ops.rr.weights_transfer_mb_weights_from_skin_mesh.poll():
            bpy.ops.rr.weights_transfer_mb_weights_from_skin_mesh(
                transfer_mesh=self.transfer_mesh or transfer_mesh_default_item
            )

        return {'FINISHED'}


class RR_OT_WeightsTransferFBWeightsFromSkinMesh(RecRoomAvatarMeshOperator):
    """Transfer weights from skin mesh"""

    bl_idname = 'rr.weights_transfer_fb_weights_from_skin_mesh'
    bl_label = 'Transfer Weights From Full Body Skin Mesh'
    bl_options = {'REGISTER', 'UNDO'}

    transfer_mesh: bpy.props.StringProperty(
        name='Transfer Mesh', default='BodyMesh_LOD0'
    )

    @classmethod
    def poll(cls, context):
        skin_mesh = bpy.data.objects.get('BodyMesh_LOD0')

        def is_full_body(obj):
            if obj.name.startswith('FB_'):
                return True

            return any(map(lambda x: x.name.startswith('FB_'), obj.users_collection))

        any_full_body = any(map(lambda x: is_full_body(x), cls.selected_meshes()))

        return super().poll(context) and bool(skin_mesh) and any_full_body

    def execute(self, context):
        # Cache selection
        active = bpy.context.active_object
        selected_meshes = [
            o for o in bpy.data.objects if o.select_get() and o.type == 'MESH'
        ]

        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')

        target = self.transfer_mesh

        with resources.get(target) as skin_meshes:
            mask_selection = [m.select for m in bpy.context.scene.mask_list]
            for m in bpy.context.scene.mask_list:
                m.select = True

            for selected in selected_meshes:
                selected.select_set(True)

                selected.vertex_groups.clear()

                # Transfer vertex groups from skin mesh to selection
                skin_meshes.select_set(True)
                bpy.context.view_layer.objects.active = skin_meshes

                bpy.ops.object.data_transfer(
                    data_type='VGROUP_WEIGHTS',
                    layers_select_src='ALL',
                    layers_select_dst='NAME',
                )

                # Remove culling mask groups
                mask_groups = [
                    g for g in selected.vertex_groups if g.name.startswith('Msk.')
                ]
                for mask in mask_groups:
                    selected.vertex_groups.remove(mask)

                selected.select_set(False)

        # Restore selection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = active
        for selected in selected_meshes:
            selected.select_set(True)

        for select, mask in zip(mask_selection, bpy.context.scene.mask_list):
            mask.select = select

        return {'FINISHED'}


class RR_OT_WeightsTransferMBWeightsFromSkinMesh(RecRoomAvatarMeshOperator):
    """Transfer weights from skin mesh"""

    bl_idname = 'rr.weights_transfer_mb_weights_from_skin_mesh'
    bl_label = 'Transfer Weights From Modern Bean Skin Mesh'
    bl_options = {'REGISTER', 'UNDO'}

    transfer_mesh: bpy.props.StringProperty(
        name='Transfer Mesh', default='MB_BodyMesh_LOD0'
    )

    @classmethod
    def poll(cls, context):
        skin_mesh = bpy.data.objects.get('MB_BodyMesh_LOD0')

        def is_modern_bean_body(obj):
            if obj.name.startswith('MB_'):
                return True

            return any(map(lambda x: x.name.startswith('MB_'), obj.users_collection))

        any_modern_bean_body = any(
            map(lambda x: is_modern_bean_body(x), cls.selected_meshes())
        )

        return super().poll(context) and bool(skin_mesh) and any_modern_bean_body

    def execute(self, context):
        # Cache selection
        active = bpy.context.active_object
        selected_meshes = [
            o for o in bpy.data.objects if o.select_get() and o.type == 'MESH'
        ]

        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')

        target = self.transfer_mesh

        with resources.get(target) as skin_meshes:
            mask_selection = [m.select for m in bpy.context.scene.mask_list]
            for m in bpy.context.scene.mask_list:
                m.select = True

            for selected in selected_meshes:
                selected.select_set(True)

                selected.vertex_groups.clear()

                # Transfer vertex groups from skin mesh to selection
                skin_meshes.select_set(True)
                bpy.context.view_layer.objects.active = skin_meshes

                bpy.ops.object.data_transfer(
                    data_type='VGROUP_WEIGHTS',
                    layers_select_src='ALL',
                    layers_select_dst='NAME',
                )

                # Remove culling mask groups
                mask_groups = [
                    g for g in selected.vertex_groups if g.name.startswith('Msk.')
                ]
                for mask in mask_groups:
                    selected.vertex_groups.remove(mask)

                selected.select_set(False)

        # Restore selection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = active
        for selected in selected_meshes:
            selected.select_set(True)

        for select, mask in zip(mask_selection, bpy.context.scene.mask_list):
            mask.select = select

        return {'FINISHED'}


class RR_OT_WeightsTransferWeightsFromActiveMesh(RecRoomAvatarMeshOperator):
    """Transfer weights from active mesh"""

    bl_idname = 'rr.weights_transfer_weights_from_active_mesh'
    bl_label = 'Transfer Weights From Active Mesh'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        active = bpy.context.view_layer.objects.active
        selection = [o for o in cls.selected_meshes() if o != active]

        return super().poll(context) and active and active.type == 'MESH' and selection

    def execute(self, context):
        return self.execute_(context)

    @put_file_in_known_good_state
    def execute_(self, context):
        # Cache selection
        active = bpy.context.active_object
        selected_meshes = [
            o
            for o in bpy.data.objects
            if o.select_get() and o.type == 'MESH' and o != active
        ]

        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')

        for selected in selected_meshes:
            selected.select_set(True)

            selected.vertex_groups.clear()

            # Transfer vertex groups from skin mesh to selection
            active.select_set(True)
            bpy.context.view_layer.objects.active = active

            bpy.ops.object.data_transfer(
                data_type='VGROUP_WEIGHTS',
                layers_select_src='ALL',
                layers_select_dst='NAME',
            )

            # Remove culling mask groups
            mask_groups = [
                g for g in selected.vertex_groups if g.name.startswith('Msk.')
            ]
            for mask in mask_groups:
                selected.vertex_groups.remove(mask)

            selected.select_set(False)

        # Restore selection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = active
        for selected in selected_meshes:
            selected.select_set(True)

        return {'FINISHED'}


class RR_OT_WeightsApplyModernBeanTorsoWeights(RecRoomAvatarMeshOperator):
    """Apply modern bean torso weights"""

    bl_idname = 'rr.weights_apply_modern_bean_torso_weights'
    bl_label = 'Apply Modern Bean Torso Weights'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        resource_exists = os.path.exists(resources.mb_library)

        return super().poll(context) and resource_exists

    def execute(self, context):
        # Cache selection
        active = bpy.context.active_object
        selected_meshes = [
            o for o in bpy.data.objects if o.select_get() and o.type == 'MESH'
        ]

        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')

        # Get weight transfer mesh
        with bpy.data.libraries.load(resources.mb_library) as (data_from, data_to):
            data_to.objects = [
                a for a in data_from.objects if a == 'MB_Torso_Weight_Transfer'
            ]

        source = data_to.objects and data_to.objects[0] or None
        if source:
            bpy.context.scene.collection.objects.link(source)

        else:
            return {'CANCELLED'}

        for selected in selected_meshes:
            selected.select_set(True)

            selected.vertex_groups.clear()

            # Transfer weights from source
            source.select_set(True)
            bpy.context.view_layer.objects.active = source

            bpy.ops.object.data_transfer(
                data_type='VGROUP_WEIGHTS',
                vert_mapping='POLYINTERP_NEAREST',
                layers_select_src='ALL',
                layers_select_dst='NAME',
            )

            # Remove culling mask groups
            mask_groups = [
                g for g in selected.vertex_groups if g.name.startswith('Msk.')
            ]
            for mask in mask_groups:
                selected.vertex_groups.remove(mask)

            selected.select_set(False)

        # Restore selection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = active
        for selected in selected_meshes:
            selected.select_set(True)

        bpy.data.objects.remove(source)

        return {'FINISHED'}


class RR_OT_WeightsApplyModernBeanHandWeights(RecRoomAvatarMeshOperator):
    """Apply modern bean hand weights"""

    bl_idname = 'rr.weights_apply_modern_bean_hand_weights'
    bl_label = 'Apply Modern Bean Hand Weights'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        resource_exists = os.path.exists(resources.mb_library)

        return super().poll(context) and resource_exists

    def execute(self, context):
        # Cache selection
        active = bpy.context.active_object
        selected_meshes = [
            o for o in bpy.data.objects if o.select_get() and o.type == 'MESH'
        ]

        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')

        # Get weight transfer mesh
        with bpy.data.libraries.load(resources.mb_library) as (data_from, data_to):
            data_to.meshes = [
                a for a in data_from.meshes if a == 'MB_Hand_Weight_Transfer'
            ]

        # Process imported meshes
        for mesh in [a for a in data_to.meshes if a]:
            # Create a new object for the mesh data
            source = bpy.data.objects.new(mesh.name, mesh)
            bpy.context.scene.collection.objects.link(source)

        for selected in selected_meshes:
            selected.select_set(True)

            selected.vertex_groups.clear()

            # Transfer weights from source
            source.select_set(True)
            bpy.context.view_layer.objects.active = source

            bpy.ops.object.data_transfer(
                data_type='VGROUP_WEIGHTS',
                vert_mapping='POLYINTERP_NEAREST',
                layers_select_src='ALL',
                layers_select_dst='NAME',
            )

            # Remove culling mask groups
            mask_groups = [
                g for g in selected.vertex_groups if g.name.startswith('Msk.')
            ]
            for mask in mask_groups:
                selected.vertex_groups.remove(mask)

            selected.select_set(False)

        # Restore selection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = active
        for selected in selected_meshes:
            selected.select_set(True)

        bpy.data.objects.remove(source)

        return {'FINISHED'}


@bpy.app.handlers.persistent
def update_label(cls, scene):
    """Update RR_OT_WeightsTransferWeightsFromActiveMesh label based on selection"""
    active = bpy.context.view_layer.objects.active

    if not active:
        RR_OT_WeightsTransferWeightsFromActiveMesh.bl_label = f'Transfer Weights'
    else:
        RR_OT_WeightsTransferWeightsFromActiveMesh.bl_label = (
            f'Weights from {active.name}'
        )


classes = (
    RR_OT_WeightsTransferWeightsFromPresets,
    RR_OT_WeightsTransferFBWeightsFromSkinMesh,
    RR_OT_WeightsTransferMBWeightsFromSkinMesh,
    RR_OT_WeightsTransferWeightsFromActiveMesh,
    RR_OT_WeightsApplyModernBeanHandWeights,
    RR_OT_WeightsApplyModernBeanTorsoWeights,
)

panel = (
    RR_OT_WeightsTransferWeightsFromPresets,
    RR_OT_WeightsTransferWeightsFromActiveMesh,
)


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
