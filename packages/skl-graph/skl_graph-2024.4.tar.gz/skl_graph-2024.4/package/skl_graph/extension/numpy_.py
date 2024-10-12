"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h

import numpy as nmpy

array_t = nmpy.ndarray
dtype_t = nmpy.dtype


def Issues(
    array: h.Any,
    /,
    *,
    expected_dtype: dtype_t | h.Sequence[dtype_t] = None,
    expected_dim: int | h.Sequence[int] = None,
    expected_size: int | h.Sequence[int] = None,
    expected_shape: h.Sequence[int] | h.Sequence[h.Sequence[int]] = None,
) -> list[str]:
    """"""
    output = []

    if not isinstance(array, array_t):
        return [f"{array}: Not a Numpy array. Actual type={type(array).__name__}."]

    if not ((expected_dtype is None) or isinstance(expected_dtype, h.Sequence)):
        expected_dtype = (expected_dtype,)
    if not ((expected_dim is None) or isinstance(expected_dim, h.Sequence)):
        expected_dim = (expected_dim,)
    if not ((expected_size is None) or isinstance(expected_size, h.Sequence)):
        expected_size = (expected_size,)
    if not ((expected_shape is None) or isinstance(expected_shape[0], h.Sequence)):
        expected_shape = (expected_shape,)

    if not (
        (expected_dtype is None)
        or any(
            (array.dtype == _tpe) or nmpy.issubdtype(array.dtype, _tpe)
            for _tpe in expected_dtype
        )
    ):
        output.append(f"{array.dtype}: Invalid Numpy dtype. Expected={expected_dtype}.")

    if not ((expected_dim is None) or (array.ndim in expected_dim)):
        output.append(f"{array.ndim}: Invalid dimension. Expected={expected_dim}.")

    if not ((expected_size is None) or (array.size in expected_size)):
        output.append(f"{array.size}: Invalid array size. Expected={expected_size}.")

    if not ((expected_shape is None) or (array.shape in expected_shape)):
        output.append(f"{array.shape}: Invalid array shape. Expected={expected_shape}.")

    return output


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
