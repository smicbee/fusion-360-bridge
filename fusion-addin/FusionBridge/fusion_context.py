import adsk.core
import adsk.fusion


def get_context():
    app = adsk.core.Application.get()
    ui = app.userInterface
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    root_comp = design.rootComponent if design else None

    return {
        'adsk': adsk,
        'app': app,
        'ui': ui,
        'product': product,
        'design': design,
        'rootComp': root_comp,
        'result': None,
    }


def get_state():
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    root_comp = design.rootComponent if design else None
    document = app.activeDocument

    return {
        'ok': True,
        'fusionRunning': True,
        'documentName': document.name if document else None,
        'hasActiveDesign': design is not None,
        'rootComponentName': root_comp.name if root_comp else None,
    }
