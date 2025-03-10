import bpy

from rr_avatar_tools.panels.base import RecRoomOperatorPanel


class SCENE_PT_RRAvatarToolsExperimentalPanel(RecRoomOperatorPanel):
    bl_label = "Experimental"
    bl_parent_id = "SCENE_PT_RRAvatarToolsToolsPanel"

    def draw(self, context):
        layout = self.layout

        column = layout.column()
        column.operator("rr.create_modern_bean_from_full_body")
        column.operator("rr.update_remove_arms")


classes = (SCENE_PT_RRAvatarToolsExperimentalPanel,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
