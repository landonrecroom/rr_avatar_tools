import bpy

import rr_avatar_tools
from rr_avatar_tools.panels.base import RecRoomAvatarPanel
from rr_avatar_tools.budgets import budgets


class SCENE_PT_RRAvatarToolsDiagnosticsPanel(RecRoomAvatarPanel):
    """Creates a panel in the object properties window."""

    bl_label = "Validation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rec Room Avatar Tools"

    @classmethod
    def selected_meshes(cls):
        return [o for o in bpy.data.objects if o.select_get() and o.type == "MESH"]

    def draw_header(self, context):
        self.layout.label(text="", icon="FUND")

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)

        if not context.scene.export_list:
            return

        # Only show diagnostics for selected avatar item
        prop = context.scene.export_list[context.scene.export_list_index]
        collections = [
            c
            for c in rr_avatar_tools.data.collections
            if c.get("rec_room_uuid") == prop.uuid
        ]

        box = column.box()

        # Statistics
        for collection in collections:
            for mesh in [
                m for m in collection.objects if m.type == "MESH" and "_LOD" in m.name
            ]:  # self.selected_meshes():
                index = mesh.name.find("LOD")
                name = mesh.name[index:]

                r = box.row()

                parts = mesh.name.upper().split("_")
                lod_level = parts[-1].upper()[:4]
                body_type = parts[0].upper()
                outfit_type = parts[-2].upper()

                body_budget = budgets.get(body_type)

                outfit_budget = body_budget.get(outfit_type)

                if not outfit_budget:
                    break

                triangle_budget = outfit_budget.get(lod_level)

                if not triangle_budget:
                    break

                triangle_count = sum([len(p.vertices) - 2 for p in mesh.data.polygons])

                icon = "CHECKMARK"
                if triangle_count > triangle_budget:
                    icon = "ERROR"

                r.label(
                    text=f"{name} Tris {triangle_count} / {triangle_budget}", icon=icon
                )

        layout.separator()
        column = layout.column()

        # Diagnostics
        for collection in collections:
            for mesh in [
                m for m in collection.objects if m.type == "MESH" and "_LOD" in m.name
            ]:  # self.selected_meshes():
                results = [
                    op
                    for op in rr_avatar_tools.operators.diagnostics.classes
                    if op.diagnose(mesh)
                ]

                if not results:
                    continue

                index = mesh.name.find("LOD")
                name = mesh.name[index:]

                s = column.split(factor=0.25)

                left = s.column()
                left.label(text=name)

                right = s.column()

                for diagnostic in results:
                    r = right.row()
                    factor = 0.75 if diagnostic.poll(context) else 1.0
                    split = r.split(factor=factor)
                    c = split.column()
                    c.label(**diagnostic.label)

                    if diagnostic.poll(context):
                        c = split.column()
                        c.operator(diagnostic.bl_idname, text="Fix").target = mesh.name

                column.separator()


classes = (SCENE_PT_RRAvatarToolsDiagnosticsPanel,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
