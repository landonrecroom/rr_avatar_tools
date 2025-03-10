import bpy

from rr_avatar_tools.preferences import RRAvatarToolsPreferences


class RecRoomAvatarOperator(bpy.types.Operator):
    """Base operator class. Operators that need to ensure the project is
    correctly setup should derive from this."""

    rr_require_rec_room_path = False
    rr_require_source_art_path = False
    rr_required_mode = None
    rr_label = ""

    @classmethod
    def preferences(self) -> RRAvatarToolsPreferences:
        return bpy.context.preferences.addons["rr_avatar_tools"].preferences

    @classmethod
    def poll(cls, context):
        if cls.rr_required_mode:
            if not bpy.context.object:
                return False

            if cls.rr_required_mode != bpy.context.object.mode:
                return False

        return True


class RecRoomAvatarMeshOperator(RecRoomAvatarOperator):
    """Base mesh operator class."""

    @classmethod
    def poll(cls, context):
        return super().poll(context) and bool(cls.selected_meshes())

    @classmethod
    def selected_meshes(cls):
        return [o for o in bpy.data.objects if o.select_get() and o.type == "MESH"]
