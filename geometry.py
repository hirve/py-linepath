import sys, math
from typing import List, Tuple, TypedDict, Optional, cast

Vector = List [ float ]
Point = Vector
Size = Vector
Line = Tuple [ Point, Point ]
Path = List [ Point ]

BoundingRangeOptional = TypedDict('BoundingRangeOptional', { 'min': Optional [ float ], 'max': Optional [ float ] })
BoundingBoxOptional = Tuple [ BoundingRangeOptional, BoundingRangeOptional ]
BoundingRange = TypedDict('BoundingRange', { 'min': float, 'max': float })
BoundingBox = Tuple [ BoundingRange, BoundingRange ]

def pathBoundingBox (path: Path) -> BoundingBox:
    box: BoundingBoxOptional = ( { 'min': None, 'max': None }, { 'min': None, 'max': None } )
    for p in path:
        box[0]['min'] = p[0] if box[0]['min'] is None else min(box[0]['min'], p[0])
        box[1]['min'] = p[1] if box[1]['min'] is None else min(box[1]['min'], p[1])
        box[0]['max'] = p[0] if box[0]['max'] is None else max(box[0]['max'], p[0])
        box[1]['max'] = p[1] if box[1]['max'] is None else max(box[1]['max'], p[1])
    return cast(BoundingBox, box)

def pointsDistance2 (p1: Point, p2: Point) -> float:
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

def isPointLineDistanceLessThan (p: Point, line: Line, distance: float) -> bool:
    d2 = distance ** 2
    if line[0][0] == line[1][0] and line[0][1] == line[1][1]:
        return pointsDistance2(p, line[0]) < d2
    else:
        lineLen2 = pointsDistance2 (*line)
        t = ((p[0] - line[0][0]) * (line[1][0] - line[0][0]) + (p[1] - line[0][1]) * (line[1][1] - line[0][1])) / lineLen2
        t01 = max(0, min(1, t))
        return pointsDistance2(p, [ line[0][0] + t01 * (line[1][0] - line[0][0]), line[0][1] + t01 * (line[1][1] - line[0][1]) ]) < d2

class EnclosedShape:

    def __init__ (self, path):
        self.__pathSrc: Path = path.copy()
        self.__path: Path = path.copy()
        if path[0][0] != path[len(path) - 1][0] or path[0][1] != path[len(path) - 1][1]:
            self.__path.append(path[0])
        self.__box: BoundingBox = pathBoundingBox(path)

    def getPath (self) -> Path:
        return self.__path

    def getBoundingBox (self) -> BoundingBox:
        return self.__box

    def isInside (self, p: Point) -> bool:
        count = 0
        prevPoint = None
        for curPoint in self.__path:
            if prevPoint is not None:
                line: Line = (prevPoint, curPoint)
                if line[0][1] < p[1] and line[1][1] >= p[1] or line[0][1] >= p[1] and line[1][1] < p[1]:
                    if line[0][0] <= p[0] or line[1][0] <= p[0]:
                        if line[0][0] <= p[0] and line[1][0] <= p[0] or (p[1] - line[0][1]) / (line[1][1] - line[0][1]) * (line[1][0] - line[0][0]) + line[0][0] <= p[0]:
                            count += 1
            prevPoint = curPoint
        return count & 1 == 1

    def isCloserThan (self, p: Point, distance: float) -> bool:
        prevPoint = None
        for curPoint in self.__path:
            if prevPoint is not None:
                line: Line = (prevPoint, curPoint)
                if not (line[0][0] < p[0] - distance and line[1][0] < p[0] - distance) \
                        and not (line[0][0] > p[0] + distance and line[1][0] > p[0] + distance) \
                        and not (line[0][1] < p[1] - distance and line[1][1] < p[1] - distance) \
                        and not (line[0][1] > p[1] + distance and line[1][1] > p[1] + distance):
                    if isPointLineDistanceLessThan(p, line, distance):
                        return True
            prevPoint = curPoint
        return False

    def reset (self) -> 'EnclosedShape':
        self.__path = self.__pathSrc.copy()
        self.__box = pathBoundingBox(self.__path)
        return self

    def scaleTo (self, c: Point, s: Size) -> 'EnclosedShape':
        box = self.__box
        path: Path = []
        curSize = [ d['max'] - d['min'] for d in box ]
        if s[0] is None and s[1] is None:
            raise Exception('At least one of scale dimensions should be defined.')
        toSize = [ s[0], s[1] ]
        k: List = [ None if s[i] is None else toSize[i] / curSize[i] for i in [ 0, 1 ] ]
        if k[0] is None:
            k[0] = k[1]
        if k[1] is None:
            k[1] = k[0]
        for p in self.__path:
            path.append([ (p[i] - c[i]) * k[i] + c[i] for i in [ 0, 1 ] ])
        self.__path = path
        self.__box = pathBoundingBox(self.__path)
        return self

    def scaleBy (self, c: Point, m: Vector) -> 'EnclosedShape':
        box = self.__box
        size = [ (box[0]['max'] - box[0]['min']) * m[0], (box[1]['max'] - box[1]['min']) * m[1] ]
        self.scaleTo(c, size)
        return self

    def rotate (self, c: Point, a: float) -> 'EnclosedShape':
        path: Path = []
        for p in self.__path:
            path.append([
                c[0] + (p[0] - c[0]) * math.cos(a) - (p[1] - c[1]) * math.sin(a),
                c[1] + (p[1] - c[1]) * math.cos(a) + (p[0] - c[0]) * math.sin(a)
            ])
        self.__path = path
        self.__box = pathBoundingBox(self.__path)
        return self

    def moveTo (self, c: Point, to: Point) -> 'EnclosedShape':
        shift = (to[0] - c[0], to[1] - c[1])
        path: Path = []
        for p in self.__path:
            path.append([ p[0] + shift[0], p[1] + shift[1] ])
        self.__path = path
        self.__box = pathBoundingBox(self.__path)
        return self

