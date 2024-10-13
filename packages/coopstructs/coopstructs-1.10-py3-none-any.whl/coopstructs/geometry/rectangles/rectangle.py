from typing import Tuple
from cooptools.coopEnum import CardinalPosition
import cooptools.geometry_utils.rect_utils as rect
import cooptools.geometry_utils.vector_utils as vect
from cooptools.anchor import Anchor2D

class Rectangle:

    def from_meta(self, x, y, width, height):
        return Rectangle.from_tuple(rect=(x, y, width, height))

    @classmethod
    def from_tuple(cls, rect: Tuple[float, float, float, float],
                   anchor_cardinality: CardinalPosition = None,
                   inverted_y: bool = False):
        anchor = Anchor2D(
            pt=(rect[0], rect[1]),
            dims=(rect[2], rect[3]),
            cardinality=anchor_cardinality,
            inverted_y=inverted_y
        )
        return Rectangle(anchor)

    def with_margin(self, margin: int):
        ''' get the rectangle object representing the grid position that was input'''
        return Rectangle.from_tuple((  self.x + margin
                                     , self.y + margin
                                     , self.width - margin * 2
                                     , self.height - margin * 2))

    def __init__(self, anchor: Anchor2D):
        self.anchor = anchor

    def points_tuple(self):
        return self.anchor.Corners

    def contains_point(self, point: Tuple[float, float]):
        return rect.rect_contains_point(self.as_tuple(), point)

    def overlaps(self, other):
        if not type(other) == Rectangle and not type(other) == Tuple:
            raise TypeError(f"Cannot compare object of type {type(other)} to Rectangle for overlaps()")

        if type(other) == Rectangle:
            other = other.as_tuple()

        return rect.overlaps(self.as_tuple(), other)

    def align(self, pt: Tuple[float, float], alignment: CardinalPosition):
        self.anchor = Anchor2D.from_anchor(self.anchor,
                                           pt=pt,
                                           cardinality=alignment)

    def corner_generator(self):
        return self.anchor.corner_generator()

    @property
    def Center(self) -> Tuple[float, float]:
        return self.anchor.pos(CardinalPosition.CENTER)

    @property
    def TopRight(self) -> Tuple[float, float]:
        return self.anchor.pos(CardinalPosition.TOP_RIGHT)

    @property
    def TopLeft(self) -> Tuple[float, float]:
        return self.anchor.pos(CardinalPosition.TOP_LEFT)

    @property
    def BottomRight(self) -> Tuple[float, float]:
        return self.anchor.pos(CardinalPosition.BOTTOM_RIGHT)

    @property
    def BottomLeft(self) -> Tuple[float, float]:
        return self.anchor.pos(CardinalPosition.BOTTOM_LEFT)

    @property
    def TopCenter(self) -> Tuple[float, float]:
        return self.anchor.pos(CardinalPosition.TOP_CENTER)

    @property
    def BottomCenter(self) -> Tuple[float, float]:
        return self.anchor.pos(CardinalPosition.BOTTOM_CENTER)

    @property
    def RightCenter(self) -> Tuple[float, float]:
        return self.anchor.pos(CardinalPosition.RIGHT_CENTER)

    @property
    def LeftCenter(self) -> Tuple[float, float]:
        return self.anchor.pos(CardinalPosition.LEFT_CENTER)

    @property
    def Corners(self):
        return [
            self.TopLeft,
            self.TopRight,
            self.BottomRight,
            self.BottomLeft
        ]

    @property
    def Dims(self):
        return self.anchor.dims

    @property
    def BoundingCircleRadius(self) -> float:
        return vect.distance_between(self.TopLeft, self.Center)

    @property
    def CornerTuples(self):
        return [x for x in self.Corners]

    def as_tuple(self):
        return (self.x, self.y, self.width, self.height)

    @property
    def x(self):
        return self.anchor.pt[0]

    @x.setter
    def x(self, value):
        self.anchor = Anchor2D.from_anchor(self.anchor, pt=(value, self.anchor.pt[1]))

    @property
    def y(self):
        return self.anchor.pt[1]

    @y.setter
    def y(self, value):
        self.anchor = Anchor2D.from_anchor(self.anchor, pt=(self.anchor.pt[0], value))
    @property
    def width(self):
        return self.anchor.dims[0]

    @property
    def height(self):
        return self.anchor.dims[1]

    def __str__(self):
        return f"{self.anchor.cardinality.name}: <{self.x}, {self.y}>, Size: W{self.width} x H{self.height}"







