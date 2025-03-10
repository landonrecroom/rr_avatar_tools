import bpy

from rr_avatar_tools.panels.base import RecRoomOperatorPanel
from rr_avatar_tools import operators


class SCENE_PT_RRAvatarToolsTransferPanel(RecRoomOperatorPanel):
    bl_label = 'Transfer'
    bl_parent_id = 'SCENE_PT_RRAvatarToolsToolsPanel'

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)
        for operator in operators.weights.panel:
            column.operator(
                operator.bl_idname, text=operator.rr_label or operator.bl_label
            )

        column = layout.column(align=True)
        for operator in operators.transfer.panel:
            column.operator(
                operator.bl_idname, text=operator.rr_label or operator.bl_label
            )


classes = (SCENE_PT_RRAvatarToolsTransferPanel,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
