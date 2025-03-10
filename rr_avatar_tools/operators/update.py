import bpy


from rr_avatar_tools.operators.base import (
    RecRoomAvatarMeshOperator,
)
from rr_avatar_tools.utils import put_file_in_known_good_state


class RR_OT_UpdateRemoveArms(RecRoomAvatarMeshOperator):
    """Remove Arms From Full Body Avatar Item"""

    bl_idname = 'rr.update_remove_arms'
    bl_label = 'Remove Arms From Full Body Avatar Item'
    bl_options = {'REGISTER', 'UNDO'}

    value: bpy.props.FloatProperty(
        name="Value",
        min=0.0,
        max=1.0,
        default=0.75,
        step=0.1,
    )

    def execute(self, context):
        return self._execute(context)

    @put_file_in_known_good_state
    def _execute(self, context):
        left_side = (
            {'weight': 0.0, 'vertex_group': 'Jnt.LowerArm.Tweak.L'},
            {'weight': 0.0, 'vertex_group': 'Jnt.ForearmRoll.Tweak.L'},
            {'weight': 0.0, 'vertex_group': 'Jnt.ElbowHelper.L'},
            {'weight': 0.0, 'vertex_group': 'Jnt.Hand.Tweak.L'},
            {'weight': self.value, 'vertex_group': 'Jnt.UpperArm.Tweak.L'},
        )
        right_side = (
            {'weight': 0.0, 'vertex_group': 'Jnt.LowerArm.Tweak.R'},
            {'weight': 0.0, 'vertex_group': 'Jnt.ForearmRoll.Tweak.R'},
            {'weight': 0.0, 'vertex_group': 'Jnt.ElbowHelper.R'},
            {'weight': 0.0, 'vertex_group': 'Jnt.Hand.Tweak.R'},
            {'weight': self.value, 'vertex_group': 'Jnt.UpperArm.Tweak.R'},
        )

        sides = (left_side, right_side)

        selection = self.selected_meshes()

        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None

        for selected in selection:
            selected.select_set(True)
            bpy.context.view_layer.objects.active = selected

            for side in sides:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='VERT')
                bpy.ops.mesh.select_all(action='DESELECT')

                for args in side:
                    bpy.ops.rr.mesh_select_by_vertex_group(**args)

                bpy.ops.mesh.select_mode(type='FACE')

                bpy.ops.mesh.fill()

                bpy.ops.mesh.dissolve_faces()

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.mode_set(mode='EDIT')

                bpy.ops.object.vertex_group_add()
                bpy.ops.object.vertex_group_assign()

                bpy.ops.mesh.delete(type='FACE')

                bpy.ops.object.vertex_group_select()

                bpy.ops.mesh.mark_sharp()
                bpy.ops.mesh.fill_grid()

                bpy.ops.object.vertex_group_remove(all=False, all_unlocked=False)

                bpy.ops.mesh.select_all(action='DESELECT')

                bpy.ops.object.mode_set(mode='OBJECT')

            bpy.context.view_layer.objects.active = None
            selected.select_set(False)

        for selected in selection:
            selected.select_set(True)

        return {'FINISHED'}


classes = (RR_OT_UpdateRemoveArms,)

panel = (RR_OT_UpdateRemoveArms,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
