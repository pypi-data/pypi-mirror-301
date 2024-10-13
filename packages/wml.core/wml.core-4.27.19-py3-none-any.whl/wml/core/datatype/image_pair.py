# pylint: disable=import-outside-toplevel

'''Modules dealing with image pairs.

An image pair within Winnow's context is a pair of images, identified by their ids
`(before_image_id, after_image_id)` such that the before image is designed to cover as much of old
food as possible, and the after image contains as much information about the new food as possible.
'''


import mmh3
import pandas as pd
from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class ImagePair:
    '''A pair of before and after images.

    An image pair within Winnow's context is a pair of images, identified by their ids
    `(before_image_id, after_image_id)` such that the before image is designed to cover as much of
    old food as possible, and the after image contains as much information about the new food as
    possible.

    Parameters
    ----------
    before_image_id : int
        id of the before image
    after_image_id : int
        id of the after image
    '''

    before_image_id: int
    after_image_id: int

    def to_str(self) -> str:
        return '{:09d}_{:09d}'.format(int(self.before_image_id), int(self.after_image_id))

    def hash_i63(self) -> int:
        return mmh3.hash128(self.to_str()) & ((1 << 63)-1)
