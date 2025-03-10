bl_info = {
    'name': 'Rec Room Avatar Tools',
    'author': 'Joshua Skelton',
    'version': (0, 11, 0),
    'blender': (3, 6, 5),
    'location': '',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'doc_url': 'https://rec.net/blender-addon-docs',
    'support': 'COMMUNITY',
    'category': 'Scene',
}

__version__ = '.'.join(map(str, bl_info['version']))


# Handle Reload Scripts
if 'reload' in locals():
    import importlib as il

    il.reload(reload)
    reload.all()

import rr_avatar_tools.reload as reload


def register():
    from rr_avatar_tools import draw
    from rr_avatar_tools import handlers
    from rr_avatar_tools import operators
    from rr_avatar_tools import panels
    from rr_avatar_tools import preferences
    from rr_avatar_tools import properties

    modules = (
        properties,
        preferences,
        operators,
        panels,
        draw,
        handlers,
    )

    for module in modules:
        try:
            module.register()
        except Exception as e:
            print(e)


def unregister():
    from rr_avatar_tools import draw
    from rr_avatar_tools import handlers
    from rr_avatar_tools import operators
    from rr_avatar_tools import panels
    from rr_avatar_tools import preferences
    from rr_avatar_tools import properties

    modules = (
        properties,
        preferences,
        operators,
        panels,
        draw,
        handlers,
    )

    for module in modules:
        try:
            module.unregister()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    register()
