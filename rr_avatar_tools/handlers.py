import time
import uuid

from typing import List

import bpy

import rr_avatar_tools
from rr_avatar_tools.bounds import bounding_boxes


@bpy.app.handlers.persistent
def fix_up_export_list(scene):
    avatar_item_collections: List[bpy.types.Collection]
    avatar_item_collections = [c for c in rr_avatar_tools.data.collections if c.get('rec_room_uuid', False) or c.get('rec_room_avatar_item', False)]

    for collection in avatar_item_collections:
        if collection.get('rec_room_avatar_item'):
            # Update old style data
            if type(collection['rec_room_avatar_item']) == bool:
                collection['rec_room_uuid'] = str(uuid.uuid4())

            # Migrate property name
            else:
                collection['rec_room_uuid'] = collection.get('rec_room_avatar_item')

            # Remove old property
            collection['rec_room_avatar_item'] = None


@bpy.app.handlers.persistent
def setup_bounds_list(scene):
    bb_list = bpy.context.scene.bounding_box_list
    bb_list.clear()

    for name in bounding_boxes:
        bb_list.add()
        bb_list[-1].name = name

    bb_list.add()
    bb_list[-1].name = 'WRIST.BOTH'
    bb_list[-1].select = False


@bpy.app.handlers.persistent
def update_export_list(scene):
    def get_type_from_name(name):
        return name.split('_')[-1].upper()

    export_list = scene.export_list

    avatar_item_collections: List[bpy.types.Collection]
    avatar_item_collections = [i for i in rr_avatar_tools.data.avatar_items if not i.name.startswith('BB')]

    # Check if the export list and child collections are still in sync
    if len(avatar_item_collections) == len(export_list):
        uuids = [c.get('rec_room_uuid') for c in avatar_item_collections]
        types = [get_type_from_name(c.name) for c in avatar_item_collections]

        data = zip(uuids, types, export_list)

        # Ensure uuids and types are in sync
        if all(uuid_ == prop.uuid and type_ == prop.type() for uuid_, type_, prop in data):
            return

    lookup = {prop.uuid: prop.select for prop in export_list}

    # Recreate export list from collections
    export_list.clear()

    for i, collection in enumerate(avatar_item_collections):
        valid = collection.name[:3] in ('FB_', 'MB_')

        # Add to export list
        export_list.add()
        export_list[i].name = collection.name
        export_list[i].uuid = collection['rec_room_uuid']

        # Preserve selection
        select = lookup.get(collection['rec_room_uuid'])
        if select != None:
            export_list[i].select = select

        export_list[i].select &= valid

    if scene.export_list_index >= len(export_list):
        scene.export_list_index = len(export_list) - 1


def body_meshes() -> List[bpy.types.Object]:
    names = (
        'BodyMesh_LOD0',
        'BodyMesh_LOD1',
        'BodyMesh_LOD2',
        'FacialSpritesMesh_LOD0',
        'FacialSpritesMesh_LOD1',
        'FacialSpritesMesh_LOD2',
        'Nose_01Base_LOD0',
        'Nose_01Base_LOD1',
        'Nose_01Base_LOD2',
        'MB_BodyMesh_LOD0',
        'MB_BodyMesh_LOD1',
        'MB_BodyMesh_LOD2',
        'MB_FacialSpritesMesh_LOD0',
        'MB_FacialSpritesMesh_LOD1',
        'MB_FacialSpritesMesh_LOD2',
        'MB_Nose_01Base_LOD0',
        'MB_Nose_01Base_LOD1',
        'MB_Nose_01Base_LOD2',
    )

    meshes = [bpy.data.objects.get(n) for n in names]
    meshes = [m for m in meshes if m]

    return meshes


def mask_vertex_groups():
    name_sets = []
    for mesh in body_meshes():
        vg = {g.name for g in mesh.vertex_groups if g.name.startswith('Msk.')}
        name_sets.append(vg)

    if not name_sets:
        return []

    return sorted(set.union(*name_sets))


def update_mask_modifiers(scene):
    for _, group in enumerate(scene.mask_list):
        for body_mesh in body_meshes():
            group:bpy.types.VertexGroup

            mask_modifiers: List[bpy.types.MaskModifier]
            mask_modifiers = [m for m in body_mesh.modifiers if m.type == 'MASK']
            mm = [m for m in mask_modifiers if m.name == group.name]
            modifier: bpy.types.MaskModifier
            modifier = mm and mm[0] or None

            if group.select and modifier:
                body_mesh.modifiers.remove(modifier)

            if not group.select and not modifier:
                modifier = body_mesh.modifiers.new(group.name, 'MASK')
                modifier.vertex_group = group.name


def update_masks(scene):
    mask_list = scene.mask_list
    mask_groups = mask_vertex_groups()

    lookup = {c.name:c.select for c in mask_list}

    mask_list.clear()

    for i, name in enumerate(mask_groups):
        # Add to mask list
        mask_list.add()
        mask_list[i].name = name

        # Preserve selection
        select = lookup.get(name)
        if select != None:
            mask_list[i].select = select


@bpy.app.handlers.persistent
def update_mask_list(scene):
    mask_list = scene.mask_list

    mask_groups = mask_vertex_groups()

    # Check if the mask list and child collections are still in sync
    if len(mask_groups) == len(mask_list):
        # Ensure ordering
        names = zip(mask_groups, [e.name for e in mask_list])
        if not all(a == b for a, b in names):
            update_masks(scene)

    else:
        update_masks(scene)

    update_mask_modifiers(scene)


@bpy.app.handlers.persistent
def fix_up_old_style_avatar_item_collections(scene):
    for collection in rr_avatar_tools.data.collections:
        # Good state
        if collection.get('rec_room_uuid'):
            continue

        # Ignore resources
        if collection.name in ('MB_Resources', 'FB_Resources'):
            continue

        prefix = collection.name.upper()[:2]

        if prefix not in ('MB', 'FB'):
            continue

        # Ignore collections without LOD meshes
        if not any([o for o in collection.objects if 'LOD0' in o.name]):
            continue

        # Mark as avatar item
        collection['rec_room_uuid'] = str(uuid.uuid4())


@bpy.app.handlers.persistent
def setup_file(filepath):
    # Only fix up files that have at least once manually clicked setup file
    if not bpy.context.scene.get('rec_room_setup'):
        return

    if bpy.ops.rr.setup_setup_file.poll():
        bpy.ops.rr.setup_setup_file()

    # Hack. Force depsgraph update
    bpy.data.collections[0].hide_viewport = not bpy.data.collections[0].hide_viewport
    bpy.data.collections[0].hide_viewport = not bpy.data.collections[0].hide_viewport


def run_diagnostics(old, new):
    # Do not run diagnostics in edit mode
    if bpy.context.active_object and bpy.context.active_object.mode == 'EDIT':
        return

    collections = [c for c in rr_avatar_tools.data.collections if c.get('rec_room_uuid')]
    for collection in collections:
        collection['has_errors'] = False

        for mesh in [m for m in collection.objects if m.type == 'MESH' and '_LOD' in m.name]:
            collection['has_errors'] |= any([op for op in rr_avatar_tools.operators.diagnostics.classes if op.diagnose(mesh)])

next_run_diagnostics = float('inf')

@bpy.app.handlers.persistent
def run_diagnostics_on_scene_update(scene):
    global next_run_diagnostics
    next_run_diagnostics = time.time() + 0.125


avatar_item_selection_handlers = [
    run_diagnostics,
]

@bpy.app.handlers.persistent
def check_for_avatar_item_selection_change(scene):
    old_index = bpy.context.scene.get('export_list_index_old')
    index = bpy.context.scene.get('export_list_index')

    if old_index == index:
        return

    bpy.context.scene['export_list_index_old'] = index

    for handler in avatar_item_selection_handlers:
        handler(old_index, index)


@bpy.app.handlers.persistent
def check_for_next_diagnostic_run():
    global next_run_diagnostics

    now = time.time()
    if now > next_run_diagnostics:
        run_diagnostics(None, None)
        next_run_diagnostics = float('inf')

    return 0.5

depsgraph_handlers = (
    update_export_list,
    update_mask_list,
    check_for_avatar_item_selection_change,
    run_diagnostics_on_scene_update,
)

load_post_handlers = (
    setup_file,
    fix_up_export_list,
    fix_up_old_style_avatar_item_collections,
    setup_bounds_list,
)

timers = (
    check_for_next_diagnostic_run,
)

def register():
    for handler in depsgraph_handlers:
        if handler not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(handler)

    for handler in load_post_handlers:
        if handler not in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.append(handler)

    for timer in timers:
        bpy.app.timers.register(timer, persistent=True)


def unregister():
    for handler in depsgraph_handlers:
        if handler in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(handler)

    for handler in load_post_handlers:
        if handler in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.remove(handler)

    for timer in timers:
        bpy.app.timers.unregister(timer)
