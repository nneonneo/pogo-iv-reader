''' Positions and sizes of various objects within the screenshot '''
# Sizes for an iPhone 6S+ (1242x2208px screen)

from common import Rectangle, Point

ScreenWidth = 1242

# Height of various objects in the image
StatusBarHeight = 0
ErrorMsgHeight = 163

MeterBounds = Rectangle(118, 285, 1006, 503)
MeterBallRadius = 12 # slight underestimate

CPBounds = Rectangle(364, 121, 480, 126)
HPBounds = Rectangle(314, 1162, 618, 62)
DustBounds = Rectangle(686, 1756, 172, 77)

CandyNameBounds = Rectangle(580, 1616, 598, 47)
EvolveButtonPixel = Point(373, 1897)
EvolveCandyBounds = Rectangle(933, 1945, 74, 48)
TypeBounds = Rectangle(53, 1293, 390, 85)
