from collections import namedtuple

Point = namedtuple('Point', 'x y')
class Rectangle(namedtuple('Rectangle', 'x y w h')):
    def to_bounds(self):
        ''' Return rectangle as PIL bounds '''
        return (self.x, self.y, self.x + self.w, self.y + self.h)
