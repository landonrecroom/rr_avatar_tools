import bpy

from rr_avatar_tools.panels.base import RecRoomAvatarPanel


class SCENE_PT_RRAvatarToolsBodyPanel(RecRoomAvatarPanel):
    """Avatar Body Panel"""
    bl_label = 'Avatar Body'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rec Room Avatar Tools'

    def draw_header(self, context):
        self.layout.label(text='', icon='OUTLINER_OB_ARMATURE')

    def draw(self, context):
        layout = self.layout


classes = (
    SCENE_PT_RRAvatarToolsBodyPanel,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
