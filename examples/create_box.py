import adsk.core
import adsk.fusion

sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
lines = sketch.sketchCurves.sketchLines

p1 = adsk.core.Point3D.create(0, 0, 0)
p2 = adsk.core.Point3D.create(10, 0, 0)
p3 = adsk.core.Point3D.create(10, 5, 0)
p4 = adsk.core.Point3D.create(0, 5, 0)

lines.addByTwoPoints(p1, p2)
lines.addByTwoPoints(p2, p3)
lines.addByTwoPoints(p3, p4)
lines.addByTwoPoints(p4, p1)

profile = sketch.profiles.item(0)
extrudes = rootComp.features.extrudeFeatures
distance = adsk.core.ValueInput.createByReal(2)
extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
extrude_input.setDistanceExtent(False, distance)
feature = extrudes.add(extrude_input)

body = feature.bodies.item(0)
print(f'created body: {body.name}')
result = {
    'bodyName': body.name,
    'bodyCount': rootComp.bRepBodies.count,
}
