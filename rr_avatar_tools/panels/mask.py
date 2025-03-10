import re

import bpy

from rr_avatar_tools.panels.base import RecRoomAvatarPanel
from rr_avatar_tools.properties import MaskProperty


def cleanup_name(name):
    patt = r'Msk\.\d+\.(.*)'
    matches = re.match(patt, name)

    if not matches:
        return name

    return matches.groups()[0]


class SCENE_UL_RRMaskList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()

            col = row.column()
            col.enabled = item.select

            col.label(
                text=cleanup_name(item.name),
                icon='GROUP_VERTEX'
            )

            col = row.column()
            col.prop(item, 'select', text='')

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='')

class SCENE_PT_RRAvatarMaskPanel(RecRoomAvatarPanel):
    bl_label = 'Skin Culling'
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

        rows = 3

        row = layout.row()
        row.template_list(
            'SCENE_UL_RRMaskList',
            'Mask List',
            scene,
            'mask_list',
            scene,
            'mask_list_index',
            rows=rows
        )


classes = (
    SCENE_UL_RRMaskList,
    SCENE_PT_RRAvatarMaskPanel,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)

    try:
        bpy.types.Scene.mask_list = bpy.props.CollectionProperty(type=MaskProperty)

    # On reload Blender doesn't think MaskProperty has been registered, so register it
    except ValueError:
        bpy.utils.register_class(MaskProperty)
        bpy.types.Scene.mask_list = bpy.props.CollectionProperty(type=MaskProperty)

    bpy.types.Scene.mask_list_index = bpy.props.IntProperty(name='Index for mask list', default=0)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
