from . import bake
from . import calisthenics
from . import cleanup
from . import create
from . import diagnostics
from . import export
from . import mesh
from . import setup
from . import transfer
from . import update
from . import weights


packages = (
    bake,
    calisthenics,
    cleanup,
    create,
    diagnostics,
    export,
    mesh,
    setup,
    transfer,
    update,
    weights,
)


classes = sum([p.classes for p in packages], ())


def register():
    bake.register()
    export.register()
    create.register()
    diagnostics.register()
    setup.register()
    transfer.register()
    weights.register()
    cleanup.register()
    update.register()
    calisthenics.register()
    mesh.register()


def unregister():
    bake.unregister()
    export.unregister()
    create.unregister()
    diagnostics.unregister()
    # setup.unregister()
    transfer.unregister()
    weights.unregister()
    cleanup.unregister()
    update.unregister()
    calisthenics.unregister()
    mesh.unregister()
