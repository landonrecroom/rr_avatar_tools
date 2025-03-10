import bpy

import rr_avatar_tools
from rr_avatar_tools.panels.base import RecRoomAvatarPanel


class SCENE_PT_RRAvatarToolsMainPanel(RecRoomAvatarPanel):
    """Main Rec Room Avatar Tools Panel"""
    bl_label = f'{rr_avatar_tools.bl_info["name"]} v{rr_avatar_tools.__version__}'
    bl_idname = 'SCENE_PT_RRAvatarToolsMainPanel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rec Room Avatar Tools'

    def draw(self, context):
        layout = self.layout

        layout.operator(
            'wm.url_open',
            text='Documentation',
            icon='HELP'
        ).url=rr_avatar_tools.bl_info['doc_url']


classes = (
    SCENE_PT_RRAvatarToolsMainPanel,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
