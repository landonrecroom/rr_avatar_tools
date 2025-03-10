import bpy

from . import body
from . import bounds
from . import calisthenics
from . import cleanup
from . import create
from . import diagnostics
from . import everything
from . import experimental
from . import export
from . import main
from . import mask
from . import outfits
from . import setup
from . import tools
from . import transfer
from . import update


classes = sum(
    (
        main.classes,
        setup.classes,
        create.classes,
        export.classes,
        diagnostics.classes,
        body.classes,
        bounds.classes,
        tools.classes,
        calisthenics.classes,
        mask.classes,
        transfer.classes,
        cleanup.classes,
        update.classes,
        everything.classes,
        experimental.classes,
        outfits.classes,
    ),
    (),
)

modules = (
    main,
    setup,
    create,
    export,
    diagnostics,
    body,
    bounds,
    tools,
    calisthenics,
    mask,
    transfer,
    cleanup,
    update,
    everything,
    experimental,
    outfits,
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()
