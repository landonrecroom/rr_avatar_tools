import operator

import bpy


def get_vertex_group_items(scene, context):
    items = []

    for group in bpy.context.active_object.vertex_groups:
        items.append((group.name, group.name, ""))

    return items


class RR_OT_MeshSelectVertexByVertexGroup(bpy.types.Operator):
    """Select by Vertex Weight"""

    bl_idname = "rr.mesh_select_by_vertex_group"
    bl_label = "Select by Vertex Weight"
    bl_options = {"REGISTER", "UNDO"}
    rr_required_mode = "OBJECT"

    weight: bpy.props.FloatProperty(
        name="Weight",
        default=0.5,
        min=0,
        max=1.0,
        step=0.1,
    )

    type: bpy.props.EnumProperty(
        name="Type",
        items=[
            ("LESS_THAN", "Less Than", ""),
            ("EQUAL", "Equal To", ""),
            ("GREATER_THAN", "Greater Than", ""),
            ("NOT_EQUAL", "Not Equal To", ""),
        ],
        default="GREATER_THAN",
    )

    vertex_group: bpy.props.EnumProperty(
        name="Vertex Group", items=get_vertex_group_items
    )

    @classmethod
    def poll(cls, context):
        if bpy.context.mode != "EDIT_MESH":
            return False

        return bool(bpy.context.active_object.vertex_groups)

    def execute(self, context):
        object_ = bpy.context.active_object

        group = object_.vertex_groups.get(self.vertex_group)
        if not group:
            return {"FINISHED"}

        op = {
            "LESS_THAN": operator.lt,
            "EQUAL": operator.eq,
            "GREATER_THAN": operator.gt,
            "NOT_EQUAL": operator.ne,
        }.get(self.type, operator.gt)

        bpy.ops.object.mode_set(mode="OBJECT")

        group_index = group.index
        for i, v in enumerate(object_.data.vertices):
            for g in v.groups:
                if g.group == group_index:
                    if op(g.weight, self.weight):
                        v.select = True

        bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}


def draw_select_by_vertex_group_button(self, context):
    self.layout.operator("rr.mesh_select_by_vertex_group", text="Vertex Weight")


classes = (RR_OT_MeshSelectVertexByVertexGroup,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)

    bpy.types.VIEW3D_MT_edit_mesh_select_by_trait.append(
        draw_select_by_vertex_group_button
    )


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)

    bpy.types.VIEW3D_MT_edit_mesh_select_by_trait.remove(
        draw_select_by_vertex_group_button
    )
