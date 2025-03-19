from . import rigui

packages = (rigui,)

classes = sum([p.classes for p in packages], ())


def register():
    rigui.register()


def unregister():
    rigui.unregister()
