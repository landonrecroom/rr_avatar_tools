import bpy

import rr_avatar_tools
import rr_avatar_tools.resources
from rr_avatar_tools.panels.base import RecRoomAvatarPanel
from rr_avatar_tools.properties import ExportGroupProperty


class SCENE_UL_RRExportGroupList(bpy.types.UIList):
    nop: bpy.props.BoolProperty(default=False)

    def get_bounding_box_prop(self, name):
        parts = name.upper().split('_')
        item_type = parts[0].upper()
        outfit_type = parts[-1].upper()

        target = outfit_type

        if target == 'SHIRT':
            if item_type == 'FB':
                target = 'FB_SHIRT'
            elif item_type == 'MB':
                target = 'MB_SHIRT'

        if target == 'WRIST':
            target = 'WRIST.BOTH'

        for item in bpy.context.scene.bounding_box_list:
            if item.name.upper() == target:
                return item

        return None

    def draw_item(
        self,
        context,
        layout: bpy.types.UILayout,
        data,
        item,
        icon,
        active_data,
        active_property,
        index,
    ):
        collection = item.collection()
        layer_collection = item.layer_collection()

        prefs = bpy.context.preferences.addons['rr_avatar_tools'].preferences

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)

            # Checkbox
            subrow = row.row(align=True)
            subrow.enabled = item.valid() or prefs.rec_room_internal

            if subrow.enabled:
                subrow.prop(item, 'select', text='')
            else:
                # Show checkbox as unchecked
                subrow.prop(self, 'nop', text='')

            icon = {
                'NONE': 'OUTLINER_COLLECTION',
                'COLOR_01': 'COLLECTION_COLOR_01',
                'COLOR_02': 'COLLECTION_COLOR_02',
                'COLOR_03': 'COLLECTION_COLOR_03',
                'COLOR_04': 'COLLECTION_COLOR_04',
                'COLOR_05': 'COLLECTION_COLOR_05',
                'COLOR_06': 'COLLECTION_COLOR_06',
                'COLOR_07': 'COLLECTION_COLOR_07',
                'COLOR_08': 'COLLECTION_COLOR_08',
            }.get(collection.color_tag) or 'OUTLINER_COLLECTION'

            kwargs = {
                'emboss': False,
                'text': '',
            }

            if not item.valid():
                error_icon = preview_collection["error_yellow"]
                kwargs['icon_value'] = error_icon.icon_id
            else:
                kwargs['icon'] = icon

            # Name
            subrow.prop(collection, 'name', **kwargs)

            if not layer_collection:
                row.label(text="Missing LayerCollection")
                return

            # Visibility
            subrow = row.row(align=True)
            subrow.prop(
                layer_collection,
                'hide_viewport',
                icon_only=True,
                emboss=False,
            )

            # Selectability
            subrow.operator(
                'rr.export_select_avatar_item_meshes',
                icon='RESTRICT_SELECT_OFF',
                text='',
            ).target = collection.name

            # Bounding box
            if bounds := self.get_bounding_box_prop(collection.name):
                icon = 'MATPLANE'
                if not bounds.select:
                    icon = 'SELECT_SET'

                subrow.prop(bounds, 'select', icon_only=True, icon=icon)
            else:
                col = subrow.column()
                col.enabled = False
                col.prop(self, 'nop', icon_only=True, icon='X')

            # Delete
            subrow.operator(
                'rr.export_delete_avatar_item', icon='TRASH', text=''
            ).target = collection.name

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='')


class SCENE_PT_RRAvatarToolsExportPanel(RecRoomAvatarPanel):
    """Creates a panel in the object properties window."""

    bl_label = 'Avatar Items'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rec Room Avatar Tools'

    def draw_header(self, context):
        self.layout.label(text='', icon='MATCLOTH')

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # LOD Toggle buttons
        row = layout.row(align=True)
        row.operator(
            'rr.export_toggle_avatar_item_visibility_by_lod', text='ALL'
        ).lod = 'ALL'
        row.operator(
            'rr.export_toggle_avatar_item_visibility_by_lod', text='LOD0'
        ).lod = 'LOD0'
        row.operator(
            'rr.export_toggle_avatar_item_visibility_by_lod', text='LOD1'
        ).lod = 'LOD1'
        row.operator(
            'rr.export_toggle_avatar_item_visibility_by_lod', text='LOD2'
        ).lod = 'LOD2'

        # Collection visibility buttons
        row = layout.row(align=True)
        row.emboss = 'PULLDOWN_MENU'
        fb_collection = bpy.context.view_layer.layer_collection.children.get(
            'Full_Body'
        )
        if fb_collection:
            row.prop(fb_collection, 'hide_viewport', text='Full Body')

        mb_collection = bpy.context.view_layer.layer_collection.children.get(
            'Modern_Bean_Body'
        )
        if mb_collection:
            row.prop(mb_collection, 'hide_viewport', text='Modern Bean')

        children = rr_avatar_tools.data.avatar_items
        rows = 5 if children else 3

        row = layout.row()
        row.template_list(
            'SCENE_UL_RRExportGroupList',
            'Export List',
            scene,
            'export_list',
            scene,
            'export_list_index',
            rows=rows,
        )

        prefs = bpy.context.preferences.addons['rr_avatar_tools'].preferences

        # Export button here?
        row = layout.row()
        row.scale_y = 2

        row.operator('rr.export_generic_avatar_items', text='Export Avatar Items')
        row = layout.row()
        row.prop(prefs, 'generic_export_path', text='Path')


classes = (
    SCENE_PT_RRAvatarToolsExportPanel,
    SCENE_UL_RRExportGroupList,
)

preview_collections = None


def register():
    global preview_collection

    import bpy.utils.previews

    preview_collection = bpy.utils.previews.new()
    preview_collection.load(
        "error_yellow", rr_avatar_tools.resources.error_icon, 'IMAGE'
    )

    for class_ in classes:
        bpy.utils.register_class(class_)

    try:
        bpy.types.Scene.export_list = bpy.props.CollectionProperty(
            type=ExportGroupProperty
        )

    # On reload Blender doesn't think ExportGroupProperty has been registered, so register it
    except ValueError:
        bpy.utils.register_class(ExportGroupProperty)
        bpy.types.Scene.export_list = bpy.props.CollectionProperty(
            type=ExportGroupProperty
        )

    bpy.types.Scene.export_list_index = bpy.props.IntProperty(
        name='Index for my_list', default=0
    )


def unregister():
    global preview_collection
    bpy.utils.previews.remove(preview_collection)

    del bpy.types.Scene.export_list
    del bpy.types.Scene.export_list_index

    for class_ in classes:
        bpy.utils.unregister_class(class_)
