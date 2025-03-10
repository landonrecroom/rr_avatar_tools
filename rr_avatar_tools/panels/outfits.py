import bpy

import rr_avatar_tools
from rr_avatar_tools.panels.base import RecRoomAvatarPanel
from rr_avatar_tools.properties import MaskProperty


class OutfitProperty(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    select: bpy.props.BoolProperty(default=True)


class SCENE_UL_RROutfitList(bpy.types.UIList):
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_property, index
    ):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if not (
                layer_collection := rr_avatar_tools.data.layer_collections.get(
                    item.name
                )
            ):
                return

            row = layout.row()

            row.label(text=item.name, icon='MATCLOTH')

            # Visibility
            row.prop(
                layer_collection,
                'hide_viewport',
                icon_only=True,
                emboss=False,
            )

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='')


class SCENE_PT_RRAvatarOutfitPanel(RecRoomAvatarPanel):
    bl_label = 'Outfits'
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

        if bpy.ops.rr.setup_test_outfits.poll():
            row.operator('rr.setup_test_outfits', text='Load Test Outfits')
            row.scale_y = 2
            return

        rows = 3
        row.template_list(
            'SCENE_UL_RROutfitList',
            'Outfit List',
            scene,
            'outfit_list',
            scene,
            'outfit_list_index',
            rows=rows,
        )


classes = (
    OutfitProperty,
    SCENE_UL_RROutfitList,
    SCENE_PT_RRAvatarOutfitPanel,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)

    try:
        bpy.types.Scene.outfit_list = bpy.props.CollectionProperty(type=OutfitProperty)

    # On reload Blender doesn't think MaskProperty has been registered, so register it
    except ValueError:
        bpy.utils.register_class(MaskProperty)
        bpy.types.Scene.outfit_list = bpy.props.CollectionProperty(type=OutfitProperty)

    bpy.types.Scene.outfit_list_index = bpy.props.IntProperty(
        name='Index for outfit list', default=0
    )


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
