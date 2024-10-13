'''Geolocation as a dataclass
'''

import math
from dataclasses import dataclass

from mt import np, pd


@dataclass(order=True, frozen=True)
class Geolocation:
    '''The geolocation.

    A geolocation is a pair of (latitude, longitude) which can be null in at least one component,
    in which case it is invalid. When a geolocation is valid, it is assumed that latitude takes
    values between -90 (south) and +90 and longitude takes values between -180 (west) and +180
    (east).

    MT defines that a geolocation can be "vectorised" into a 3D point in the following way. If
    the geolocation is invalid, it is mapped to (0,0,0). Otherwise, it is mapped to a point on
    the unit sphere (x,y,z) via the following formula:

        z = sin(lat in radian)
        r = cos(lat in radian)
        x = r*sin(lng in radian)
        y = r*cos(lng in radian)

    That's it for now. Engjoy.
    '''

    lng: float = None
    lat: float = None

    def is_valid(self):
        return not (pd.isnull(self.lat) or pd.isnull(self.lng))

    def vectorise(self):
        '''Returns a 3D vector representing the geolocation.'''

        if not self.is_valid():
            return np.zeros(3)
        c = math.pi/180
        lat = self.lat*c
        z = math.sin(lat)
        r = math.cos(lat)
        lng = self.lng*c
        x = r*math.sin(lng)
        y = r*math.cos(lng)
        return np.array([x,y,z])
