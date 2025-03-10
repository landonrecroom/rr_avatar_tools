import bpy


class RecRoomAvatarPanel(bpy.types.Panel):
    @classmethod
    def poll(cls, context):
        # Ensure that the addon and file is correctly setup
        return not bpy.ops.rr.setup_setup_file.poll()


class RecRoomOperatorPanel(RecRoomAvatarPanel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rec Room Avatar Tools"

    rr_operators = []

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)

        for operator in self.rr_operators:
            column.operator(
                operator.bl_idname, text=operator.rr_label or operator.bl_label
            )
