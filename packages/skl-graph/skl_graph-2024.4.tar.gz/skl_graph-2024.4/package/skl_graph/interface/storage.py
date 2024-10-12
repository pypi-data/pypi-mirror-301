"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

"""
>>> import numpy as nmpy
>>> from documentation.wiki.example.minimal import skl_graph, skl_map
>>> from json_any import JsonStringOf, ObjectFromJsonString
>>> from skl_graph.task.storage import DescriptionForJSON, NewFromJsonDescription
>>> from skl_graph.type.graph import skl_graph_t
>>>
>>> jsoned, history = JsonStringOf(skl_graph, descriptors={"": DescriptionForJSON})
>>> print(history)
None
>>> un_jsoned = ObjectFromJsonString(jsoned, builders={"": NewFromJsonDescription})
>>> print(type(un_jsoned).__name__)
skl_graph_t
>>> (un_jsoned.n_nodes == skl_graph.n_nodes) and (un_jsoned.n_edges == skl_graph.n_edges)
True
>>> nmpy.array_equal(un_jsoned.RebuiltSkeletonMap().astype(skl_map.dtype), skl_map)
True
"""

import typing as h

import networkx as ntkx
from skl_graph.type.graph import skl_graph_t


def DescriptionForJSON(graph: skl_graph_t, /) -> tuple[h.Any, ...]:
    """"""
    slots = []
    for slot in graph.__slots__:
        slots.extend((slot, getattr(graph, slot)))

    # If it was not taken care of by json-any:
    # node_details = {_nde: _dtl for _nde, _dtl in graph.nodes.data(SKL_GRAPH)}
    # edge_details = {
    #     tuple(_dge): _dtl for *_dge, _dtl in graph.edges.data(SKL_GRAPH, keys=True)
    # }
    # Then add node_details and edge_details to the description.

    return tuple(slots) + (graph.AsNetworkX(),)


def NewFromJsonDescription(description: tuple[h.Any, ...], /) -> skl_graph_t:
    """"""
    output = skl_graph_t()

    *slots, graph = description

    for s_idx in range(0, slots.__len__(), 2):
        setattr(output, slots[s_idx], slots[s_idx + 1])

    output.add_edges_from(graph.edges(data=True, keys=True))
    attributes = {_nde: _ttr for _nde, _ttr in graph.nodes(data=True)}
    ntkx.set_node_attributes(output, attributes)

    # If it was not taken care of by json-any ( after retrieving node_details and
    # edge_details from the description).
    # for node, details in node_details.items():
    #     output.nodes[node][SKL_GRAPH] = details
    # for (node_0, node_1, uid), details in edge_details.items():
    #     output.edges[node_0, node_1, uid][SKL_GRAPH] = details

    return output


if __name__ == "__main__":
    #
    import doctest

    doctest.testmod()


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
