import bpy

from rr_avatar_tools.panels.base import RecRoomOperatorPanel
from rr_avatar_tools import operators


class SCENE_PT_RRAvatarToolsCalisthenicsPanel(RecRoomOperatorPanel):
    bl_label = "Calisthenics"
    rr_operators = operators.cleanup.panel
    bl_parent_id = "SCENE_PT_RRAvatarToolsBodyPanel"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.scale_y = 1.3

        row.operator(
            "rr.calisthenics_set_active_action", text="Full Body", icon="ARMATURE_DATA"
        ).action = "Calisthenics_FB"

        row.operator(
            "rr.calisthenics_set_active_action",
            text="Modern Bean",
            icon="ARMATURE_DATA",
        ).action = "Calisthenics_MB"


classes = (SCENE_PT_RRAvatarToolsCalisthenicsPanel,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
