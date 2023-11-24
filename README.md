# Python linepath geometry
Python library of linepath geometry.
The addition for https://github.com/hirve/py-functional-mill to limit cut area by a shape, where the shape is a path from lines.

### Features
- Creating an enclosed shape from path of lines (polyline).
  ```python
  from geometry import EnclosedShape
  SRC_PATH = [ [ -20, -10 ], [ -10, 55 ], [ 70, 55 ], [ 75, -25 ] ]
  shape = EnclosedShape(SRC_PATH);
  ```
- Moving, scaling, rotation of the shape.
  ```python
  shape.scaleTo([ 50, 40 ], [ 190, 40 ])
  shape.scaleBy([ 50, 40 ], [ 1.5, 2 ])
  shape.moveTo([ 50, 40 ], [ 150, -20 ])
  shape.rotate([ 50, 40 ], -math.pi / 12)

  # Builder style
  shape.reset().moveTo([ 50, 40 ], [ 150, -20 ]).rotate([ 50, 40 ], -math.pi / 12)
  ```
- Taking bounding box of the shape.
  ```python
  box = shape.getBoundingBox()
  ```
- Testing if the point is inside the shape.
  ```python
  shape.isInside([ 15, 25 ])
  ```
- Testing if the point is closer to shape edge than R value.
  ```python
  shape.isCloserThan([ -5, 35 ], 5)
  ```

