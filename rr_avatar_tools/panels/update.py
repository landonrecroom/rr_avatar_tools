import bpy


class SCENE_PT_RRAvatarToolsUpdatePanel(bpy.types.Panel):
    """Creates a panel in the object properties window."""

    bl_label = "Modern Bean Update"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rec Room Avatar Tools"
    bl_parent_id = "SCENE_PT_RRAvatarToolsToolsPanel"

    @classmethod
    def poll(cls, context):
        return False  # bpy.context.preferences.addons['rr_avatar_tools'].preferences.show_all_operators

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)


classes = (SCENE_PT_RRAvatarToolsUpdatePanel,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
