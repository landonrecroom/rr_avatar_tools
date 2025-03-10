from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import bpy


template_blend_file = str(Path(__file__).parent / "resources" / "template.blend")

fb_library = str(Path(__file__).parent / "resources" / "fb_library.blend")

mb_library = str(Path(__file__).parent / "resources" / "mb_library.blend")

error_icon = str(Path(__file__).parent / "resources" / "icons" / "error-yellow.png")


class ResourceError(Exception):
    pass


@contextmanager
def get(name: str) -> Generator[bpy.types.Object, None, None]:
    """Returns an object with the given name from either the current scene
    or one of the resource libraries. If object is from a resource library it
    will be deleted when exiting the context manager.

    :param str name: Name of object to find
    :raises ResourceError: If no object can be found for given name
    """
    # Try current scene
    resource = bpy.data.objects.get(name)
    remove_on_exit = False

    # Try resource blend files
    if not resource:
        # Try fb_resources.blend
        with bpy.data.libraries.load(fb_library) as (data_from, data_to):
            data_to.objects = [a for a in data_from.objects if a == name]

        if not data_to.objects:
            # Try mb_resources.blend
            with bpy.data.libraries.load(mb_library) as (data_from, data_to):
                data_to.objects = [a for a in data_from.objects if a == name]

        resource = bool(data_to.objects) and data_to.objects[0] or None
        if resource:
            bpy.context.scene.collection.objects.link(resource)
            remove_on_exit = True

        else:
            raise ResourceError(f'resource "{name}" not found')

    try:
        yield resource

    finally:
        if resource and remove_on_exit:
            bpy.data.objects.remove(resource)
