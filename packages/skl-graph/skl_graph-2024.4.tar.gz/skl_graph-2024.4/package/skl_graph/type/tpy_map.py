"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

"""
A map is a Numpy ndarray representing one or several object on a background. It has several variants. The ones concerned
here are:
- Binary   map (bmp): ndarray of type int8  where the object(s) are labeled 1 and the background is 0.
- Topology map (tmp): ndarray of type int8  where each object site (pixel, voxel...) has a value between 0
and 3**D - 1, where D is the number of dimensions of the array, and the background is 3**D. The values correspond to
the number of neighboring sites in the object with the weakest connectivity (8 in 2-D, 26 in 3-D...).

It is implicit that all the functions below require the map(s) to be valid (i.e., follow(s) the definitions above).
"""

import typing as h

import numpy as nmpy
import scipy.ndimage as spim

array_t = nmpy.ndarray
labeling_fct_t = h.Callable[[array_t], tuple[array_t, int]]


_SQUARE_3x3 = nmpy.ones((3, 3), dtype=nmpy.uint8)
_SQUARE_3x3x3 = nmpy.ones((3, 3, 3), dtype=nmpy.uint8)
_LABELING_FCT_2D: labeling_fct_t = lambda a_map: spim.label(
    a_map, structure=_SQUARE_3x3, output=nmpy.int64
)
_LABELING_FCT_3D: labeling_fct_t = lambda a_map: spim.label(
    a_map, structure=_SQUARE_3x3x3, output=nmpy.int64
)
LABELING_FCT_FOR_DIM = (None, None, _LABELING_FCT_2D, _LABELING_FCT_3D)


_FULL_SHIFTS_FOR_2D_NEIGHBORS = tuple(
    (i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0
)
_FULL_SHIFTS_FOR_3D_NEIGHBORS = tuple(
    (i, j, k)
    for i in (-1, 0, 1)
    for j in (-1, 0, 1)
    for k in (-1, 0, 1)
    if i != 0 or j != 0 or k != 0
)
_FULL_SHIFTS_FOR_NEIGHBORS_FOR_DIM = (
    None,
    None,
    _FULL_SHIFTS_FOR_2D_NEIGHBORS,
    _FULL_SHIFTS_FOR_3D_NEIGHBORS,
)

_MIN_SHIFTS_FOR_2D_NEIGHBORS = tuple(
    elm for elm in _FULL_SHIFTS_FOR_2D_NEIGHBORS if nmpy.abs(elm).sum() == 1
)
_MIN_SHIFTS_FOR_3D_NEIGHBORS = tuple(
    elm for elm in _FULL_SHIFTS_FOR_3D_NEIGHBORS if nmpy.abs(elm).sum() == 1
)
_MIN_SHIFTS_FOR_NEIGHBORS_FOR_DIM = (
    None,
    None,
    _MIN_SHIFTS_FOR_2D_NEIGHBORS,
    _MIN_SHIFTS_FOR_3D_NEIGHBORS,
)


def TopologyMapOfMap(
    a_map: array_t, /, *, full_connectivity: bool = True, return_bg_label: bool = False
) -> array_t | tuple[array_t, int]:
    """
    The topology map is labeled as follows: background=TMapBackgroundLabel(a_map); Pixels of the objects=number of
    neighboring pixels that belong to the given object (as expected, isolated pixels receive 0).

    Output dtype is int instead of uint to allow for subtraction

    Works for multi-object maps.

    Note: using a_map avoids shadowing Python's map.
    """
    output = nmpy.array(a_map, dtype=nmpy.int8)

    if full_connectivity:
        shifts_for_dim = _FULL_SHIFTS_FOR_NEIGHBORS_FOR_DIM
    else:
        shifts_for_dim = _MIN_SHIFTS_FOR_NEIGHBORS_FOR_DIM
    padded_sm = nmpy.pad(a_map, 1)
    unpadding_domain = a_map.ndim * (slice(1, -1),)
    rolling_axes = tuple(range(a_map.ndim))
    for shifts in shifts_for_dim[a_map.ndim]:
        output += nmpy.roll(padded_sm, shifts, axis=rolling_axes)[unpadding_domain]

    background_label = TMapBackgroundLabel(a_map)
    output[a_map == 0] = background_label + 1
    output -= 1

    if return_bg_label:
        return output, background_label

    return output


def TMapBackgroundLabel(a_map: array_t, /) -> int:
    """
    Must be equal to the max number of neighbors in a map, + 1.
    Note: using a_map avoids shadowing Python's map.
    """
    return 3**a_map.ndim


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
