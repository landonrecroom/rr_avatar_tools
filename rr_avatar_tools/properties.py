import uuid

import bpy

import rr_avatar_tools


class ExportGroupProperty(bpy.types.PropertyGroup):
    uuid: bpy.props.StringProperty(default=str(uuid.uuid4()))

    select: bpy.props.BoolProperty(default=True)

    @classmethod
    def layer_collections(cls):
        def walk_view_layers(collection):
            return sum(
                [walk_view_layers(c) for c in collection.children], start=[collection]
            )

        return walk_view_layers(bpy.context.view_layer.layer_collection)

    @classmethod
    def get_view_layer(cls, name):
        matches = [c for c in cls.layer_collections() if c.name == name]
        return matches[0] if matches else None

    def collection(self):
        collections = [
            c
            for c in rr_avatar_tools.data.collections
            if c.get("rec_room_uuid") == self.uuid
        ]
        return collections and collections[0] or None

    def layer_collection(self):
        collection = self.collection()
        return collection and self.get_view_layer(collection.name) or None

    def type(self):
        collection = self.collection()

        if not collection:
            return "UNKNOWN"

        t = collection.name.split("_")[-1].upper()

        if t not in (
            "BELT",
            "EAR",
            "EYE",
            "HAIR",
            "HAT",
            "MOUTH",
            "NECK",
            "WRIST",
            "SHIRT",
            "SHOULDER",
            "LEG",
            "SHOE",
        ):
            return "UNKNOWN"

        return t

    def has_errors(self):
        return bool(self.collection() and self.collection().get("has_errors"))

    def valid(self):
        return self.type() != "UNKNOWN" and not self.has_errors()

    def can_export(self):
        prefs = bpy.context.preferences.addons["rr_avatar_tools"].preferences
        if prefs.rec_room_internal:
            return True

        return self.valid()


class MaskProperty(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()

    select: bpy.props.BoolProperty(default=True)


def register():
    bpy.utils.register_class(ExportGroupProperty)
    bpy.utils.register_class(MaskProperty)


def unregister():
    bpy.utils.unregister_class(ExportGroupProperty)
    bpy.utils.unregister_class(MaskProperty)
