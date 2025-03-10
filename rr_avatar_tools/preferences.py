import bpy

from bpy.props import (
    BoolProperty,
    StringProperty,
)


class RRAvatarToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = 'rr_avatar_tools'

    show_all_operators: BoolProperty(
        name='Show Debug Panel',
        default=False,
        description='Show the Debug Panel in the 3D view'
    )

    rec_room_internal: BoolProperty(
        name='Use Rec Room Internal Options',
        default=False
    )

    generic_export_path: StringProperty(
        name='Export Path',
        default='',
        description='Define the path to the export folder',
        subtype='DIR_PATH'
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        split = row.split(factor=0.3)
        col = split.column()
        col.label(text='Rec Room Internal')
        col = split.column()
        col.prop(self, 'rec_room_internal', text='')

        if self.rec_room_internal:
            row = layout.row()
            split = row.split(factor=0.3)
            col = split.column()
            col.label(text='Developer Extras')
            col = split.column()
            col.prop(self, 'show_all_operators', text='')


all = (
    RRAvatarToolsPreferences,
)


def register():
    for class_ in all:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in all:
        bpy.utils.unregister_class(class_)
