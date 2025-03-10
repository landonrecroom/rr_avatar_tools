import bpy

from bpy.props import (
    StringProperty,
)


class RR_OT_CalisthenicsSetActiveAction(bpy.types.Operator):
    """Set active action"""

    bl_idname = "rr.calisthenics_set_active_action"
    bl_label = "Set Active Action"
    bl_options = {"REGISTER", "UNDO"}

    action: StringProperty(name="Action Name")

    @classmethod
    def description(cls, context, properties):
        body_type = "Full Body"

        if properties.action.endswith("MB"):
            body_type = "Modern Bean"

        return f"Load {body_type} Calisthenics/Range-of-Motion Action"

    def execute(self, context):
        rig: bpy.types.Object = bpy.data.objects.get("Avatar_Skeleton")
        action = bpy.data.actions.get(self.action)

        rig.animation_data.action = action

        return {"FINISHED"}


classes = (RR_OT_CalisthenicsSetActiveAction,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
