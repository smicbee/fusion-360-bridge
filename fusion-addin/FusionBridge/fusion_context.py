import adsk.core
import adsk.fusion

import fusion_helpers


def _base_context():
    app = adsk.core.Application.get()
    ui = app.userInterface
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    root_comp = design.rootComponent if design else None
    document = app.activeDocument

    return {
        'app': app,
        'ui': ui,
        'product': product,
        'design': design,
        'rootComp': root_comp,
        'document': document,
    }


def get_context():
    ctx = _base_context()
    return {
        'adsk': adsk,
        **ctx,
        'helpers': fusion_helpers,
        'app_info': lambda: fusion_helpers.app_info(ctx['app'], ctx['document'], ctx['design'], ctx['rootComp']),
        'show_message': lambda text: fusion_helpers.show_message(ctx['ui'], text),
        'list_occurrences': lambda: fusion_helpers.list_occurrences(ctx['rootComp']),
        'list_bodies': lambda: fusion_helpers.list_bodies(ctx['rootComp']),
        'create_box': lambda width, height, depth: fusion_helpers.create_box(ctx['rootComp'], width, height, depth),
        'result': None,
    }


def get_state(queue_size=0, is_busy=False, current_job_id=None, pump_mode=None):
    ctx = _base_context()
    document = ctx['document']
    design = ctx['design']
    root_comp = ctx['rootComp']

    return {
        'ok': True,
        'fusionRunning': True,
        'documentName': document.name if document else None,
        'hasActiveDesign': design is not None,
        'rootComponentName': root_comp.name if root_comp else None,
        'queueSize': queue_size,
        'busy': is_busy,
        'currentJobId': current_job_id,
        'pumpMode': pump_mode,
    }
