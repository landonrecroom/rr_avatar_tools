import bpy

from rr_avatar_tools.panels.base import RecRoomOperatorPanel
from rr_avatar_tools import operators


class SCENE_PT_RRAvatarToolsCleanupPanel(RecRoomOperatorPanel):
    bl_label = "File Cleanup"
    rr_operators = operators.cleanup.panel
    bl_parent_id = "SCENE_PT_RRAvatarToolsToolsPanel"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator(
            "rr.cleanup_rebuild_files",
            text="Rebuild File",
            icon="MOD_BUILD",
        )

        col.operator(
            "rr.cleanup_scorch_file",
            text="Scorch File",
            icon="SEQ_HISTOGRAM",
        )


classes = (SCENE_PT_RRAvatarToolsCleanupPanel,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
