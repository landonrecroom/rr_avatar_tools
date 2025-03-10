import bpy

import rr_avatar_tools
import rr_avatar_tools.operators


class SCENE_PT_RRAvatarToolsEverythingPanel(bpy.types.Panel):
    """Creates a panel in the object properties window."""
    bl_label = 'Debug'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rec Room Avatar Tools'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return bpy.context.preferences.addons['rr_avatar_tools'].preferences.show_all_operators

    def draw_header(self, context):
            self.layout.label(text='', icon='EXPERIMENTAL')

    def draw(self, context):
        layout = self.layout

        for package in rr_avatar_tools.operators.packages:
            col = layout.column(align=True)
            name = package.__name__.split('.')[-1]
            col.label(text=name.capitalize())

            for operator in package.classes:
                col.operator(operator.bl_idname, text=operator.bl_label)


classes = (
    SCENE_PT_RRAvatarToolsEverythingPanel,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
