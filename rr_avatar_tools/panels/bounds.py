import bpy

from rr_avatar_tools.panels.base import RecRoomAvatarPanel


class BoundingBoxProperty(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    select: bpy.props.BoolProperty(default=False)


class SCENE_UL_RRBoundsList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()

            row.label(
                text=item.name,
                icon='CUBE'
            )

            # Visibility
            row.prop(item, 'select', text='')

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='')

class SCENE_PT_RRBoundsPanel(RecRoomAvatarPanel):
    bl_label = 'Bounds'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rec Room Avatar Tools'
    bl_parent_id = 'SCENE_PT_RRAvatarToolsBodyPanel'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return super().poll(context)

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()

        rows = 3
        row.template_list(
            'SCENE_UL_RRBoundsList',
            'Bounding Box List',
            scene,
            'bounding_box_list',
            scene,
            'bounding_box_list_index',
            rows=rows
        )


classes = (
    BoundingBoxProperty,
    SCENE_UL_RRBoundsList,
    SCENE_PT_RRBoundsPanel,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)

    try:
        bpy.types.Scene.bounding_box_list = bpy.props.CollectionProperty(type=BoundingBoxProperty)

    except ValueError:
        bpy.utils.register_class(BoundingBoxProperty)
        bpy.types.Scene.bounding_box_list = bpy.props.CollectionProperty(type=BoundingBoxProperty)

    bpy.types.Scene.bounding_box_list_index = bpy.props.IntProperty(name='Index for bounding box list', default=0)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
