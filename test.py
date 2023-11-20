import math
from geometry import EnclosedShape

SRC_PATH = [ [ -20, -10 ], [ -10, 55 ], [ 70, 55 ], [ 75, -25 ] ]
COMPARE_DELTA = 0.01

def areEqual (a, b): return abs(a - b) <= COMPARE_DELTA
def arePointsEqual (p1, p2): return areEqual(p1[0], p2[0]) and areEqual(p1[1], p2[1])
def arePathsEqual (path1, path2):
  for i, p in enumerate(path1):
    if not arePointsEqual(p, path2[i]):
      return False
  return True

print("Create shape")

shape = EnclosedShape(SRC_PATH);
shapePath = shape.getPath()
assert len(shapePath) == 5, "Length of shape created from not enclosed path should pe path length + 1."
assert shapePath[-1][0] == -20 and shapePath[-1][1] == -10, "The last shape point shoud be the same that first."

print("Check bounding box")

box = shape.getBoundingBox()
assert box[0]['min'] == -20 and box[0]['max'] == 75 and box[1]['min'] == -25 and box[1]['max'] == 55, "Wrong bounding box."

print("Scale to target size")

shape.scaleTo([ 50, 40 ], [ 190, 40 ])
assert arePathsEqual(shape.getPath(), [ [ -90, 15 ], [ -70, 47.5 ], [ 90, 47.5 ], [ 100, 7.5 ], [ -90, 15 ] ]), "Wrong scaling to size."
box = shape.getBoundingBox()
assert box[0]['max'] - box[0]['min'] == 190 and box[1]['max'] - box[1]['min'] == 40, "Wrong bounding box after scaling to size."

print("Reset shape")

shape.reset()
assert arePathsEqual(shape.getPath(), [ [ -20, -10 ], [ -10, 55 ], [ 70, 55 ], [ 75, -25 ], [ -20, -10 ] ]), "Wrong path after reset."
box = shape.getBoundingBox()
assert box[0]['min'] == -20 and box[0]['max'] == 75 and box[1]['min'] == -25 and box[1]['max'] == 55, "Wrong bounding box after reset."

print("Scale by multiplier")

shape.scaleBy([ 50, 40 ], [ 1.5, 2 ])
assert arePathsEqual(shape.getPath(), [ [ -55, -60 ], [ -40, 70 ], [ 80, 70 ], [ 87.5, -90 ], [ -55, -60 ] ]), "Wrong scaling by multiplier."
box = shape.getBoundingBox()
assert box[0]['min'] == -55 and box[0]['max'] == 87.5 and box[1]['min'] == -90 and box[1]['max'] == 70, "Wrong bounding box after scaling by multiplier."

print("Move shape from custom point to target point")

shape.reset().moveTo([ 50, 40 ], [ 150, -20 ])
assert arePathsEqual(shape.getPath(), [ [ 80, -70 ], [ 90, -5 ], [ 170, -5 ], [ 175, -85 ], [ 80, -70 ] ]), "Wrong move."
box = shape.getBoundingBox()
assert box[0]['min'] == 80 and box[0]['max'] == 175 and box[1]['min'] == -85 and box[1]['max'] == -5, "Wrong bounding box after move."

print("Rotate shape")

shape.rotate([ 50, 40 ], -math.pi / 12)
assert arePathsEqual(shape.getPath(), [ [ 50.508, -74.016 ], [ 76.990, -13.819 ], [ 154.264, -34.525 ], [ 138.388, -113.093 ], [ 50.508, -74.016 ] ]), "Wrong rotation."
box = shape.getBoundingBox()
assert areEqual(box[0]['min'], 50.508) and areEqual(box[0]['max'], 154.264), "Wrong bounding box after rotation."
assert areEqual(box[1]['min'], -113.093) and areEqual(box[1]['max'], -13.819), "Wrong bounding box after rotation."

print("Is point inside the shape")

shape.reset()
assert shape.isInside([ 15, 25 ]) == True, "Wrong inside check."
assert shape.isInside([ -25, 90 ]) == False, "Wrong inside check."
assert shape.isInside([ -5, 55 ]) == True, "Wrong inside check on the edge."

print("Is point closer to shape than R")

shape.reset()
assert shape.isCloserThan([ -5, 35 ], 10) == True, "Wrong closer than R check."
assert shape.isCloserThan([ -5, 35 ], 5) == False, "Wrong closer than R check."
assert shape.isCloserThan([ -25, -15 ], 5) == False, "Wrong closer than R check."
assert shape.isCloserThan([ -25, -15 ], 10) == True, "Wrong closer than R check."

print('Done.')

