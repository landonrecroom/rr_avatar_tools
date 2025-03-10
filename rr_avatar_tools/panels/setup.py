import bpy

from rr_avatar_tools.panels.base import RecRoomAvatarPanel
from rr_avatar_tools import operators


class SCENE_PT_RRAvatarToolsSetupPanel(RecRoomAvatarPanel):
    bl_label = 'Setup'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rec Room Avatar Tools'

    @classmethod
    def poll(cls, context):
        return not super().poll(context)

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)
        column.scale_y = 2

        # Ensure file is correctly set up
        operator = operators.setup.RR_OT_SetupSetupFile

        column.operator(
            operator.bl_idname,
            text=operator.bl_label,
            icon='FILE_TICK'
        )

classes = (
    SCENE_PT_RRAvatarToolsSetupPanel,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)