import adsk.core
import adsk.fusion


def app_info(app, document=None, design=None, root_comp=None):
    return {
        'documentName': document.name if document else None,
        'hasDesign': design is not None,
        'rootComponentName': root_comp.name if root_comp else None,
        'bodyCount': root_comp.bRepBodies.count if root_comp else 0,
        'occurrenceCount': root_comp.occurrences.count if root_comp else 0,
    }


def show_message(ui, text):
    # Release mode: no debug popup side effects.
    # Returning False signals "not shown" while keeping API compatibility.
    return False


def list_occurrences(root_comp):
    if not root_comp:
        return []

    items = []
    for occ in root_comp.occurrences:
        items.append({
            'name': occ.name,
            'componentName': occ.component.name if occ.component else None,
            'isVisible': occ.isLightBulbOn,
        })
    return items


def list_bodies(root_comp):
    if not root_comp:
        return []

    items = []
    for body in root_comp.bRepBodies:
        items.append({
            'name': body.name,
            'isSolid': body.isSolid,
            'isVisible': body.isVisible,
        })
    return items


def create_box(root_comp, width, height, depth):
    if not root_comp:
        raise RuntimeError('No active root component available')

    sketch = root_comp.sketches.add(root_comp.xYConstructionPlane)
    lines = sketch.sketchCurves.sketchLines

    p1 = adsk.core.Point3D.create(0, 0, 0)
    p2 = adsk.core.Point3D.create(width, 0, 0)
    p3 = adsk.core.Point3D.create(width, height, 0)
    p4 = adsk.core.Point3D.create(0, height, 0)

    lines.addByTwoPoints(p1, p2)
    lines.addByTwoPoints(p2, p3)
    lines.addByTwoPoints(p3, p4)
    lines.addByTwoPoints(p4, p1)

    profile = sketch.profiles.item(0)
    extrudes = root_comp.features.extrudeFeatures
    distance = adsk.core.ValueInput.createByReal(depth)
    extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(False, distance)
    feature = extrudes.add(extrude_input)

    body = feature.bodies.item(0)
    return {
        'bodyName': body.name,
        'bodyCount': root_comp.bRepBodies.count,
        'width': width,
        'height': height,
        'depth': depth,
    }
