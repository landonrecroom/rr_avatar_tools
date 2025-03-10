import struct
from typing import Tuple

import bpy
import mathutils

from rr_avatar_tools.operators.base import RecRoomAvatarMeshOperator


class RR_OT_BakeCullingMaskToUVChannels(RecRoomAvatarMeshOperator):
    """Bake Culling Mask to UV Channels"""
    bl_idname = 'rr.bake_culling_mask_to_uv_channels'
    bl_label = 'Bake Culling Mask to UV Channels'
    bl_options = { 'REGISTER', 'UNDO' }
    rr_required_mode = 'OBJECT'

    @classmethod
    def active_mesh(cls):
        if bpy.context.active_object.type == 'MESH':
            return bpy.context.active_object

        return None

    @classmethod
    def mask_vertex_groups(cls):
        if not cls.active_mesh():
            return []

        vertex_groups = [g for g in cls.active_mesh().vertex_groups if g.name.startswith('Msk.')]

        return sorted(vertex_groups, key=lambda g: g.name)

    @classmethod
    def poll(cls, context):
        if not cls.active_mesh():
            return False

        if not cls.mask_vertex_groups():
            return False

        return super().poll(context)

    @classmethod
    def encode_vertex(cls, vertex:bpy.types.MeshVertex) -> int:
        # Get sequence of ordered mask groups
        mask_groups = cls.mask_vertex_groups()

        # Build mapping of group index to weight
        vertex_map = {g.group: g.weight for g in vertex.groups}

        # Build sequence of weights
        weights = [vertex_map.get(g.index, 0) for g in mask_groups]

        # Convert weights to a sequence of '1' or '0's
        chars = ['1' if w > 0.5 else '0' for w in weights]

        # Join into a single string
        bit_string = ''.join(chars)

        # Flip so least significant bit is rightmost
        flipped_bit_string = bit_string[::-1]

        # Convert binary string to integer
        value = int(flipped_bit_string, 2)

        return value

    def pack_vertex(self, vertex:bpy.types.MeshVertex) -> Tuple[mathutils.Vector, mathutils.Vector]:
        value = self.encode_vertex(vertex)
        data = struct.pack('<q', value)

        u0, v0, u1, v1 = struct.unpack('<HHHH', data)

        uv0 = mathutils.Vector((u0 + 0.5, v0 + 0.5))
        uv1 = mathutils.Vector((u1 + 0.5, v1 + 0.5))

        return uv0, uv1

    def execute(self, context):
        selected = self.active_mesh()
        data: bpy.types.Mesh = selected.data

        uv_layer1 = data.uv_layers.get('BitPackedLayerMasks_UVLayer_1') or data.uv_layers.new(name='BitPackedLayerMasks_UVLayer_1')
        uv_layer2 = data.uv_layers.get('BitPackedLayerMasks_UVLayer_2') or data.uv_layers.new(name='BitPackedLayerMasks_UVLayer_2')

        for polygon in data.polygons:
            for loop_index in polygon.loop_indices:
                vertex_index = data.loops[loop_index].vertex_index
                uv1, uv2 = self.pack_vertex(data.vertices[vertex_index])

                uv_layer1.data[loop_index].uv = uv1
                uv_layer2.data[loop_index].uv = uv2

        return { 'FINISHED' }


classes = (
    RR_OT_BakeCullingMaskToUVChannels,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
