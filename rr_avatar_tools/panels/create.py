import bpy

from rr_avatar_tools.panels.base import RecRoomOperatorPanel
from rr_avatar_tools import operators


class SCENE_PT_RRAvatarToolsCreatePanel(RecRoomOperatorPanel):
    bl_label = 'Create'
    rr_operators = operators.create.panel

    def draw_header(self, context):
        self.layout.label(text='', icon='PLUS')

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.scale_y = 1.3
        row.operator(
            'rr.create_avatar_item',
            text='Create Avatar Item',
            icon='COLLECTION_NEW',
        )

        layout.operator(
            'rr.create_left_side_avatar_item',
            text='Create Left Side Item',
            icon='MOD_MIRROR',
        )


classes = (SCENE_PT_RRAvatarToolsCreatePanel,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
