import sys
import bpy

import rr_avatar_tools.utils


class Collection:
    def __init__(self, data):
        self.data = tuple(data)

    def __iter__(self):
        for data in self.data:
            yield data

    def __getitem__(self, key):
        if type(key) == str:
            return {o.name: o for o in self.data}[key]

        return self.data[key]

    def __len__(self):
        return len(self.data)

    def get(self, name, default=None):
        try:
            return self[name]

        except:
            return default


class Data(sys.__class__):
    @property
    def collections(self):
        return Collection(c for c in bpy.data.collections if not c.library)

    @property
    def objects(self):
        return Collection(o for o in bpy.data.objects if not o.library)

    @property
    def layer_collections(self):
        return Collection(o for o in rr_avatar_tools.utils.layer_collections_recursive())

    @property
    def avatar_items(self):
        return Collection(c for c in bpy.data.collections if not c.library and c.get('rec_room_uuid', False))


sys.modules[__name__].__class__ = Data
