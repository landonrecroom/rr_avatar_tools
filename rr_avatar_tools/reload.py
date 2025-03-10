import rr_avatar_tools


def all():
    import importlib as il

    # Reload package
    il.reload(rr_avatar_tools)

    il.reload(rr_avatar_tools.budgets)

    # Reload operators subpackage
    il.reload(rr_avatar_tools.operators)
    il.reload(rr_avatar_tools.operators.base)
    il.reload(rr_avatar_tools.operators.bake)
    il.reload(rr_avatar_tools.operators.calisthenics)
    il.reload(rr_avatar_tools.operators.cleanup)
    il.reload(rr_avatar_tools.operators.create)
    il.reload(rr_avatar_tools.operators.diagnostics)
    il.reload(rr_avatar_tools.operators.export)
    il.reload(rr_avatar_tools.operators.mesh)
    il.reload(rr_avatar_tools.operators.setup)
    il.reload(rr_avatar_tools.operators.transfer)
    il.reload(rr_avatar_tools.operators.update)
    il.reload(rr_avatar_tools.operators.weights)

    # Reload panels subpackage
    il.reload(rr_avatar_tools.panels)
    il.reload(rr_avatar_tools.panels.base)
    il.reload(rr_avatar_tools.panels.body)
    il.reload(rr_avatar_tools.panels.bounds)
    il.reload(rr_avatar_tools.panels.calisthenics)
    il.reload(rr_avatar_tools.panels.cleanup)
    il.reload(rr_avatar_tools.panels.create)
    il.reload(rr_avatar_tools.panels.diagnostics)
    il.reload(rr_avatar_tools.panels.everything)
    il.reload(rr_avatar_tools.panels.experimental)
    il.reload(rr_avatar_tools.panels.export)
    il.reload(rr_avatar_tools.panels.main)
    il.reload(rr_avatar_tools.panels.mask)
    il.reload(rr_avatar_tools.panels.outfits)
    il.reload(rr_avatar_tools.panels.setup)
    il.reload(rr_avatar_tools.panels.tools)
    il.reload(rr_avatar_tools.panels.transfer)
    il.reload(rr_avatar_tools.panels.update)

    # Reload handlers subpackage
    il.reload(rr_avatar_tools.handlers)

    # Reload preferences subpackage
    il.reload(rr_avatar_tools.preferences)

    # Reload properties subpackage
    il.reload(rr_avatar_tools.properties)

    il.reload(rr_avatar_tools.data)

    il.reload(rr_avatar_tools.bounds)

    il.reload(rr_avatar_tools.draw)

    il.reload(rr_avatar_tools.resources)

    il.reload(rr_avatar_tools.utils)

    print('rr_avatar_tools: Reload finished.')
