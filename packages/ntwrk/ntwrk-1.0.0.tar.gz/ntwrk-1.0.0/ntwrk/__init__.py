# Copyright (c) 2024 Khiat Mohammed Abderrezzak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Khiat Mohammed Abderrezzak <khiat.dev@gmail.com>


"""Sophisticate Graph"""


from hashtbl import (
    tabulate,
    hashMap,
    singlyLinkedList,
    _red,
    _green,
    _blue,
    _cyan,
    _white,
    List,
    Tuple,
    Self,
    NoReturn,
    Any,
)
from typing import Set


__all__: List = ["graph"]


class graph:
    def __init__(
        self: "graph",
        vertices: List | Tuple | Set = [],
        edges: List | Tuple | Set = [],
        *,
        detail: bool = False,
        directed: bool = False,
        weighted: bool = False,
        complete: bool = False,
    ) -> None:
        self.directed: bool = directed
        self.weighted: bool = weighted
        self.complete: bool = complete
        self.graph: Tuple = (vertices, edges)
        self.degree: int = 0
        self.degrees: List = []
        self.detail: bool = detail

    @property
    def graph(self: "graph") -> Self:
        return self

    @graph.setter
    def graph(self: "graph", data: Tuple) -> None | NoReturn:
        if len(data[0]) > 0:
            if len(data[1]) > 0:
                if not isinstance(data[1], set):
                    pre_edges: List = hashMap().fromkeys(data[1]).keys
                else:
                    pre_edges: List = list(data[1])
                edges: List = []
            else:
                pre_edges: List = []
                if self.complete:
                    edges: List = []
            if not isinstance(data[0], set):
                vertices: List = hashMap().fromkeys(data[0]).keys
            else:
                vertices: List = list(data[0])
            if not self.complete:
                self._adjacency_matrix: List = [
                    [0 for _ in range(len(vertices))] for _ in range(len(vertices))
                ]
            else:
                if not self.weighted:
                    self._adjacency_matrix: List = [
                        [
                            (1 if vertices[i] != vertices[j] else 0)
                            for j in range(len(vertices))
                        ]
                        for i in range(len(vertices))
                    ]
                else:
                    counter: int = 0
                    self._adjacency_matrix: List = [
                        [0 for _ in range(len(vertices))] for _ in range(len(vertices))
                    ]
            self._adjacency_list: hashMap = hashMap().fromkeys(
                vertices, [[] for _ in range(len(vertices))]
            )
            for i in range(len(vertices)):
                for j in range(len(vertices)):
                    try:
                        pre_edge: str = vertices[i] + vertices[j]
                        inverse_pre_edge: str = vertices[j] + vertices[i]
                        if not self.complete:
                            for k in range(len(pre_edges)):
                                if not self.directed and not self.weighted:
                                    if pre_edge == pre_edges[k]:
                                        if inverse_pre_edge not in edges:
                                            edges.append(pre_edge)
                                        (
                                            self._adjacency_matrix[i][j],
                                            self._adjacency_matrix[j][i],
                                        ) = (1, 1)
                                        if (
                                            vertices[j]
                                            not in self._adjacency_list[vertices[i]]
                                        ):
                                            self._adjacency_list[vertices[i]].append(
                                                vertices[j]
                                            )
                                        if (
                                            vertices[i]
                                            not in self._adjacency_list[vertices[j]]
                                        ):
                                            self._adjacency_list[vertices[j]].append(
                                                vertices[i]
                                            )
                                elif not self.directed and self.weighted:
                                    if pre_edge == pre_edges[k][0]:
                                        for l in range(len(edges)):
                                            if inverse_pre_edge == edges[l][0]:
                                                edges[l][1] = pre_edges[k][1]
                                                break
                                        else:
                                            edges.append([pre_edge, pre_edges[k][1]])
                                        (
                                            self._adjacency_matrix[i][j],
                                            self._adjacency_matrix[j][i],
                                        ) = (pre_edges[k][1], pre_edges[k][1])
                                        for m in range(
                                            len(self._adjacency_list[vertices[j]])
                                        ):
                                            if (
                                                self._adjacency_list[vertices[j]][m][0]
                                                is vertices[i]
                                            ):
                                                self._adjacency_list[vertices[j]][m][
                                                    1
                                                ] = pre_edges[k][1]
                                                break
                                        else:
                                            self._adjacency_list[vertices[j]].append(
                                                [vertices[i], pre_edges[k][1]]
                                            )
                                        for n in range(
                                            len(self._adjacency_list[vertices[i]])
                                        ):
                                            if (
                                                self._adjacency_list[vertices[i]][n][0]
                                                is vertices[j]
                                            ):
                                                self._adjacency_list[vertices[i]][n][
                                                    1
                                                ] = pre_edges[k][1]
                                                break
                                        else:
                                            self._adjacency_list[vertices[i]].append(
                                                [vertices[j], pre_edges[k][1]]
                                            )
                                elif self.directed and not self.weighted:
                                    if pre_edge == pre_edges[k]:
                                        edges.append(pre_edge)
                                        self._adjacency_matrix[i][j] = 1
                                        if (
                                            vertices[j]
                                            not in self._adjacency_list[vertices[i]]
                                        ):
                                            self._adjacency_list[vertices[i]].append(
                                                vertices[j]
                                            )
                                else:
                                    if pre_edge == pre_edges[k][0]:
                                        edges.append([pre_edge, pre_edges[k][1]])
                                        self._adjacency_matrix[i][j] = pre_edges[k][1]
                                        for n in range(
                                            len(self._adjacency_list[vertices[i]])
                                        ):
                                            if (
                                                self._adjacency_list[vertices[i]][n][0]
                                                is vertices[j]
                                            ):
                                                self._adjacency_list[vertices[i]][n][
                                                    1
                                                ] = pre_edges[k][1]
                                                break
                                        else:
                                            self._adjacency_list[vertices[i]].append(
                                                [vertices[j], pre_edges[k][1]]
                                            )
                        else:
                            if not self.weighted:
                                if vertices[i] != vertices[j]:
                                    if not self.directed:
                                        if inverse_pre_edge not in edges:
                                            edges.append(pre_edge)
                                    else:
                                        edges.append(pre_edge)
                                    self._adjacency_list[vertices[i]].append(
                                        vertices[j]
                                    )
                            else:
                                if not self.directed:
                                    if len(pre_edges) == (
                                        ((len(vertices) ** 2) - len(vertices)) / 2
                                    ):
                                        if vertices[i] != vertices[j]:
                                            for k in range(len(edges)):
                                                if inverse_pre_edge == edges[k][0]:
                                                    break
                                            else:
                                                edges.append(
                                                    [pre_edge, pre_edges[counter]]
                                                )
                                                (
                                                    self._adjacency_matrix[i][j],
                                                    self._adjacency_matrix[j][i],
                                                ) = (
                                                    pre_edges[counter],
                                                    pre_edges[counter],
                                                )
                                                self._adjacency_list[
                                                    vertices[i]
                                                ].append(
                                                    [vertices[j], pre_edges[counter]]
                                                )
                                                self._adjacency_list[
                                                    vertices[j]
                                                ].append(
                                                    [vertices[i], pre_edges[counter]]
                                                )
                                                counter += 1
                                    else:
                                        if len(pre_edges) == 0:
                                            raise ValueError("Weights not found !")
                                        elif len(pre_edges) > (
                                            ((len(vertices) ** 2) - len(vertices)) / 2
                                        ):
                                            raise ValueError(
                                                "The number of weights is bigger than edges !"
                                            )
                                        else:
                                            raise ValueError(
                                                "The number of weights is smaller than edges !"
                                            )
                                else:
                                    if len(pre_edges) == (len(vertices) ** 2) - len(
                                        vertices
                                    ):
                                        if vertices[i] != vertices[j]:
                                            self._adjacency_matrix[i][j] = pre_edges[
                                                counter
                                            ]
                                            self._adjacency_list[vertices[i]].append(
                                                [vertices[j], pre_edges[counter]]
                                            )
                                            edges.append([pre_edge, pre_edges[counter]])
                                            counter += 1
                                    elif len(pre_edges) == (
                                        ((len(vertices) ** 2) - len(vertices)) / 2
                                    ):
                                        if vertices[i] != vertices[j]:
                                            for k in range(len(edges)):
                                                if inverse_pre_edge == edges[k][0]:
                                                    edges.append(
                                                        [pre_edge, edges[k][1]]
                                                    )
                                                    break
                                            else:
                                                edges.append(
                                                    [pre_edge, pre_edges[counter]]
                                                )
                                                (
                                                    self._adjacency_matrix[i][j],
                                                    self._adjacency_matrix[j][i],
                                                ) = (
                                                    pre_edges[counter],
                                                    pre_edges[counter],
                                                )
                                                self._adjacency_list[
                                                    vertices[i]
                                                ].append(
                                                    [vertices[j], pre_edges[counter]]
                                                )
                                                self._adjacency_list[
                                                    vertices[j]
                                                ].append(
                                                    [vertices[i], pre_edges[counter]]
                                                )
                                                counter += 1
                                    else:
                                        if len(pre_edges) == 0:
                                            raise ValueError("Weights not found !")
                                        elif len(pre_edges) > (len(vertices) ** 2):
                                            raise ValueError(
                                                "The number of weights is bigger than edges !"
                                            )
                                        else:
                                            raise ValueError(
                                                "The number of weights is smaller than edges !"
                                            )
                    except TypeError as e0:
                        raise TypeError("Invalid format.") from None
                    except KeyError as e1:
                        raise TypeError("Invalid format.") from None
                    except IndexError as e2:
                        raise TypeError("Weights not found !") from None
            self._graph: Tuple = (vertices, edges)
        else:
            self._adjacency_matrix: List = []
            self._adjacency_list: hashMap = hashMap()
            self._graph: Tuple = ([], [])

    @property
    def vertices(self: "graph") -> List:
        return self._graph[0]

    @vertices.setter
    def vertices(self: "graph", data: Any) -> NoReturn:
        raise ValueError("read-only")

    @vertices.deleter
    def vertices(self: "graph") -> NoReturn:
        raise ValueError("read-only")

    @property
    def edges(self: "graph") -> List:
        return self._graph[1]

    @edges.setter
    def edges(self: "graph", data: Any) -> NoReturn:
        raise ValueError("read-only")

    @edges.deleter
    def edges(self: "graph") -> NoReturn:
        raise ValueError("read-only")

    @property
    def adjacency_matrix(self: "graph") -> List:
        return self._adjacency_matrix

    @adjacency_matrix.setter
    def adjacency_matrix(self: "graph", data: Any) -> NoReturn:
        raise ValueError("read-only")

    @adjacency_matrix.deleter
    def adjacency_matrix(self: "graph") -> NoReturn:
        raise ValueError("read-only")

    @property
    def adjacency_list(self: "graph") -> hashMap:
        return self._adjacency_list

    @adjacency_list.setter
    def adjacency_list(self: "graph", data: Any) -> NoReturn:
        raise ValueError("read-only")

    @adjacency_list.deleter
    def adjacency_list(self: "graph") -> NoReturn:
        raise ValueError("read-only")

    def edge_count(self: "graph") -> int:
        return len(self._graph[1])

    def degree_count(self: "graph") -> int:
        if not self.degree:
            if not self.directed:
                for i in self._adjacency_list.values:
                    self.degree += len(i)
            else:
                for i in range(len(self._adjacency_list.values)):
                    self.degree += len(
                        self._adjacency_list[self._adjacency_list.keys[i]]
                    )
                    self.degrees.append(
                        [len(self._adjacency_list[self._adjacency_list.keys[i]]), 0]
                    )
                    for j, k in self._adjacency_list.items:
                        if not self.weighted:
                            if self._adjacency_list.keys[i] in k:
                                self.degree += 1
                                self.degrees[i][1] += 1
                        else:
                            for l in range(len(k)):
                                if self._adjacency_list.keys[i] in k[l][0]:
                                    self.degree += 1
                                    self.degrees[i][1] += 1
        return self.degree

    def get_degree(self: "graph", node: str) -> int | NoReturn:
        try:
            if not self.directed:
                return len(self._adjacency_list[node])
            else:
                if self.degrees:
                    return (
                        self.degrees[self._graph[0].index(node)][0]
                        + self.degrees[self._graph[0].index(node)][1]
                    )
                else:
                    self.degree_count()
                    return self.get_degree(node)
        except ValueError as e3:
            raise ValueError(f"Invalid node {node!r} !") from None
        except KeyError as e4:
            raise ValueError(f"Invalid node {node!r} !") from None

    def get_indegree(self: "graph", node: str) -> int | NoReturn:
        if not self.directed:
            raise TypeError("Invalid operation.")
        try:
            return self.degrees[self._graph[0].index(node)][1]
        except ValueError as e5:
            raise ValueError(f"Invalid node {node!r} !") from None
        except IndexError as e6:
            self.degree_count()
            return self.get_indegree(node)

    def get_outdegree(self: "graph", node: str) -> int | NoReturn:
        if not self.directed:
            raise TypeError("Invalid operation.")
        try:
            return self.degrees[self._graph[0].index(node)][0]
        except ValueError as e7:
            raise ValueError(f"Invalid node {node!r} !") from None
        except IndexError as e8:
            self.degree_count()
            return self.get_outdegree(node)

    def _edges_checker(
        self: "graph",
        node: str,
        edge: str | List[str] | Tuple[str] | Set[str] | None = None,
        weight: Any | List[Any] | Tuple[Any] | Set[str] | None = None,
    ) -> None | NoReturn:
        try:
            nodes: Tuple = edge.partition(node)
        except AttributeError as e9:
            if not isinstance(edge, (list, tuple, set)):
                raise ValueError("Only str data type accepted as edge.") from None
            else:
                if self.weighted:
                    try:
                        if len(edge) == len(weight):
                            for i, j in zip(edge, weight):
                                self._edges_checker(node, i, j)
                        else:
                            raise ValueError(
                                "The number of edges and weights is not the same."
                            ) from None
                    except TypeError as e10:
                        raise ValueError(
                            "The number of edges and weights is not the same."
                        ) from None
                else:
                    for i in edge:
                        self._edges_checker(node, i)
                return
        except TypeError as e11:
            raise ValueError("Only str data type accepted as node.") from None
        if node == nodes[1]:
            if nodes[2] in self._graph[0]:
                if not self.directed and not self.weighted:
                    if (nodes[2] + nodes[1]) not in self._graph[
                        1
                    ] and edge not in self._graph[1]:
                        self._graph[1].append(edge)
                        self._adjacency_matrix[self._graph[0].index(node)][
                            self._graph[0].index(nodes[2])
                        ] = 1
                        self._adjacency_list[node].append(nodes[2])
                        if self.degree:
                            self.degree += 1
                        if nodes[2] != nodes[1]:
                            self._adjacency_matrix[self._graph[0].index(nodes[2])][
                                self._graph[0].index(node)
                            ] = 1
                            self._adjacency_list[nodes[2]].append(node)
                            if self.degree:
                                self.degree += 1
                elif not self.directed and self.weighted:
                    for i in range(len(self._graph[1])):
                        if (nodes[2] + nodes[1]) == self._graph[1][i][
                            0
                        ] or edge == self._graph[1][i][0]:
                            self._graph[1][i][1] = weight
                            self._adjacency_matrix[self._graph[0].index(nodes[2])][
                                self._graph[0].index(nodes[1])
                            ] = weight
                            self._adjacency_matrix[self._graph[0].index(nodes[1])][
                                self._graph[0].index(nodes[2])
                            ] = weight
                            for j in range(len(self._adjacency_list[nodes[2]])):
                                if self._adjacency_list[nodes[2]][j][0] == nodes[1]:
                                    self._adjacency_list[nodes[2]][j][1] = weight
                                    break
                            for j in range(len(self._adjacency_list[nodes[1]])):
                                if self._adjacency_list[nodes[1]][j][0] == nodes[2]:
                                    self._adjacency_list[nodes[1]][j][1] = weight
                                    break
                            break
                    else:
                        self._graph[1].append([edge, weight])
                        self._adjacency_matrix[self._graph[0].index(node)][
                            self._graph[0].index(nodes[2])
                        ] = weight
                        self._adjacency_list[node].append([nodes[2], weight])
                        if self.degree:
                            self.degree += 1
                        if nodes[2] != nodes[1]:
                            self._adjacency_matrix[self._graph[0].index(nodes[2])][
                                self._graph[0].index(node)
                            ] = weight
                            self._adjacency_list[nodes[2]].append([node, weight])
                            if self.degree:
                                self.degree += 1
                elif self.directed and not self.weighted:
                    if edge not in self._graph[1]:
                        self._graph[1].append(edge)
                        self._adjacency_matrix[self._graph[0].index(node)][
                            self._graph[0].index(nodes[2])
                        ] = 1
                        self._adjacency_list[node].append(nodes[2])
                        if self.degree and self.degrees:
                            self.degree += 2
                            try:
                                self.degrees[self._graph[0].index(nodes[2])][1] += 1
                            except IndexError as e12:
                                self.degrees.append([0, 1])
                            try:
                                self.degrees[self._graph[0].index(node)][0] += 1
                            except IndexError as e13:
                                self.degrees.append([1, 0])
                else:
                    for i in range(len(self._graph[1])):
                        if edge == self._graph[1][i][0]:
                            self._graph[1][i][1] = weight
                            self._adjacency_matrix[self._graph[0].index(nodes[1])][
                                self._graph[0].index(nodes[2])
                            ] = weight
                            for j in range(len(self._adjacency_list[nodes[1]])):
                                if self._adjacency_list[nodes[1]][j][0] == nodes[2]:
                                    self._adjacency_list[nodes[1]][j][1] = weight
                                    break
                            break
                    else:
                        self._graph[1].append([edge, weight])
                        self._adjacency_matrix[self._graph[0].index(node)][
                            self._graph[0].index(nodes[2])
                        ] = weight
                        self._adjacency_list[node].append([nodes[2], weight])
                        if self.degree and self.degrees:
                            self.degree += 2
                            try:
                                self.degrees[self._graph[0].index(nodes[2])][1] += 1
                            except IndexError as e14:
                                self.degrees.append([0, 1])
                            try:
                                self.degrees[self._graph[0].index(node)][0] += 1
                            except IndexError as e15:
                                self.degrees.append([1, 0])
            elif nodes[0] in self._graph[0]:
                if not self.directed and not self.weighted:
                    if (nodes[1] + nodes[0]) not in self._graph[
                        1
                    ] and edge not in self._graph[1]:
                        self._graph[1].append(edge)
                        self._adjacency_matrix[self._graph[0].index(nodes[1])][
                            self._graph[0].index(nodes[0])
                        ] = 1
                        self._adjacency_list[nodes[1]].append(nodes[0])
                        if self.degree:
                            self.degree += 1
                        if nodes[1] != nodes[0]:
                            self._adjacency_matrix[self._graph[0].index(nodes[0])][
                                self._graph[0].index(nodes[1])
                            ] = 1
                            self._adjacency_list[nodes[0]].append(nodes[1])
                            if self.degree:
                                self.degree += 1
                elif not self.directed and self.weighted:
                    for i in range(len(self._graph[1])):
                        if (nodes[1] + nodes[0]) == self._graph[1][i][
                            0
                        ] or edge == self._graph[1][i][0]:
                            self._graph[1][i][1] = weight
                            self._adjacency_matrix[self._graph[0].index(nodes[1])][
                                self._graph[0].index(nodes[0])
                            ] = weight
                            self._adjacency_matrix[self._graph[0].index(nodes[0])][
                                self._graph[0].index(nodes[1])
                            ] = weight
                            for j in range(len(self._adjacency_list[nodes[1]])):
                                if self._adjacency_list[nodes[1]][j][0] == nodes[0]:
                                    self._adjacency_list[nodes[1]][j][1] = weight
                                    break
                            for j in range(len(self._adjacency_list[nodes[0]])):
                                if self._adjacency_list[nodes[0]][j][0] == nodes[1]:
                                    self._adjacency_list[nodes[0]][j][1] = weight
                                    break
                            break
                    else:
                        self._graph[1].append([edge, weight])
                        self._adjacency_matrix[self._graph[0].index(nodes[1])][
                            self._graph[0].index(nodes[0])
                        ] = weight
                        self._adjacency_list[nodes[1]].append([nodes[0], weight])
                        if self.degree:
                            self.degree += 1
                        if nodes[1] != nodes[0]:
                            self._adjacency_matrix[self._graph[0].index(nodes[0])][
                                self._graph[0].index(nodes[1])
                            ] = weight
                            self._adjacency_list[nodes[0]].append([nodes[1], weight])
                            if self.degree:
                                self.degree += 1
                elif self.directed and not self.weighted:
                    if edge not in self._graph[1]:
                        self._graph[1].append(edge)
                        self._adjacency_matrix[self._graph[0].index(nodes[0])][
                            self._graph[0].index(nodes[1])
                        ] = 1
                        self._adjacency_list[nodes[0]].append(nodes[1])
                        if self.degree and self.degrees:
                            self.degree += 2
                            try:
                                self.degrees[self._graph[0].index(nodes[0])][0] += 1
                            except IndexError as e16:
                                self.degrees.append([1, 0])
                            try:
                                self.degrees[self._graph[0].index(nodes[1])][1] += 1
                            except IndexError as e17:
                                self.degrees.append([0, 1])
                else:
                    for i in range(len(self._graph[1])):
                        if edge == self._graph[1][i][0]:
                            self._graph[1][i][1] = weight
                            self._adjacency_matrix[self._graph[0].index(nodes[0])][
                                self._graph[0].index(nodes[1])
                            ] = weight
                            for j in range(len(self._adjacency_list[nodes[0]])):
                                if self._adjacency_list[nodes[0]][j][0] == nodes[1]:
                                    self._adjacency_list[nodes[0]][j][1] = weight
                                    break
                            break
                    else:
                        self._graph[1].append([edge, weight])
                        self._adjacency_matrix[self._graph[0].index(nodes[0])][
                            self._graph[0].index(nodes[1])
                        ] = weight
                        self._adjacency_list[nodes[0]].append([nodes[1], weight])
                        if self.degree and self.degrees:
                            self.degree += 2
                            try:
                                self.degrees[self._graph[0].index(nodes[0])][0] += 1
                            except IndexError as e18:
                                self.degrees.append([1, 0])
                            try:
                                self.degrees[self._graph[0].index(nodes[1])][1] += 1
                            except IndexError as e19:
                                self.degrees.append([0, 1])
            else:
                raise ValueError(
                    f"Node {nodes[0] if nodes[0] != '' else nodes[2]} not in the set of vertices !"
                ) from None
        else:
            raise ValueError(f"The node ({node}) not found in the edge!") from None

    def add(
        self: "graph",
        node: str,
        *,
        edge: str | List[str] | Tuple[str] | None = None,
        weight: Any | List[Any] | Tuple[Any] | None = None,
    ) -> None | NoReturn:
        if self._adjacency_matrix and self._adjacency_list:
            if node not in self._graph[0]:
                self._graph[0].append(node)
                self._adjacency_matrix.append([0 for _ in range(len(self._graph[0]))])
                for i in range(len(self._graph[0])):
                    self._adjacency_matrix[i].append(0)
                self._adjacency_list[node] = []
                if edge is not None:
                    self._edges_checker(node, edge, weight)
            else:
                raise ValueError(f"Node ({node}) is already in the set of vertices.")
        else:
            if not isinstance(node, str):
                raise ValueError("Only str data type accepted as node.")
            self._graph[0].append(node)
            self._adjacency_matrix.append([0])
            self._adjacency_list[node] = []
            if edge is not None:
                if edge == (node + node):
                    if self.weighted:
                        self._graph[1].append([edge, weight])
                        self._adjacency_matrix[0][0] = weight
                        self._adjacency_list[node].append([node, weight])
                    else:
                        if weight is None:
                            self._graph[1].append(edge)
                            self._adjacency_matrix[0][0] = 1
                            self._adjacency_list[node].append(node)
                        else:
                            raise ValueError(
                                "You can't set a weight in unweighted graph !"
                            )
                else:
                    raise ValueError("You can't add edge with only one node.")

    def add_edge(
        self: "graph",
        *,
        node1: str | List[str] | Tuple[str],
        node2: str | List[str] | Tuple[str],
        weight: Any | List[Any] | Tuple[Any] | None = None,
    ) -> None | NoReturn:
        if node1 not in self._adjacency_list:
            raise ValueError("node1 not in the set of vertices !")
        if isinstance(node1, (list, tuple, set)):
            if isinstance(node2, (list, tuple, set)):
                if len(node1) == len(node2):
                    if self.weighted:
                        try:
                            if len(weight) == ((len(node1) + len(node2)) / 2):
                                for i, j, k in zip(node1, node2, weight):
                                    try:
                                        self._edges_checker(i, (i + j), k)
                                    except TypeError as e20:
                                        raise ValueError(
                                            "Only str data type accepted as nodes."
                                        ) from None
                            else:
                                for i, j in zip(node1, node2):
                                    try:
                                        self._edges_checker(i, (i + j), weight)
                                    except TypeError as e21:
                                        raise ValueError(
                                            "Only str data type accepted as nodes."
                                        ) from None
                        except TypeError as e22:
                            for i, j in zip(node1, node2):
                                try:
                                    self._edges_checker(i, (i + j), weight)
                                except TypeError as e23:
                                    raise ValueError(
                                        "Only str data type accepted as nodes."
                                    ) from None
                    else:
                        for i, j in zip(node1, node2):
                            try:
                                self._edges_checker(i, (i + j), weight)
                            except TypeError as e24:
                                raise ValueError(
                                    "Only str data type accepted as nodes."
                                ) from None
                else:
                    raise ValueError(
                        "The number of nodes in (node1) and (node2) are not the same."
                    )
            else:
                raise ValueError(
                    "The number of nodes in (node1) and (node2) are not the same."
                )
        else:
            if isinstance(node2, (list, tuple, set)):
                raise ValueError(
                    "The number of nodes in (node1) and (node2) are not the same."
                )
            else:
                try:
                    self._edges_checker(node1, (node1 + node2), weight)
                except TypeError as e25:
                    raise ValueError("Only str data type accepted as nodes.") from None

    def delete_node(
        self: "graph", node: str | List[str] | Tuple[str] | Set[str]
    ) -> None | NoReturn:
        if not isinstance(node, (list, tuple, set)):
            try:
                node_index: int = self._graph[0].index(node)
                self._adjacency_matrix.pop(node_index)
                for i in range(len(self._adjacency_matrix)):
                    self._adjacency_matrix[i].pop(node_index)
                adjacent_nodes: List = self._adjacency_list.pop(node)
                if self.degree:
                    if not self.degrees:
                        self.degree -= len(adjacent_nodes)
                    else:
                        self.degree -= len(adjacent_nodes) * 2
            except ValueError as e26:
                raise ValueError(f"Invalid node {node!r} !") from None
            if not self.directed and not self.weighted:
                for i, j in self._adjacency_list.items:
                    for k in range(len(j)):
                        if j[k] == node:
                            try:
                                self._graph[1].remove(i + j[k])
                            except ValueError as e27:
                                self._graph[1].remove(j[k] + i)
                            self._adjacency_list[i].pop(k)
                            if self.degree:
                                self.degree -= 1
                            break
            elif not self.directed and self.weighted:
                for i, j in self._adjacency_list.items:
                    for k in range(len(j)):
                        if j[k][0] == node:
                            try:
                                self._graph[1].remove([i + j[k][0], j[k][1]])
                            except ValueError as e28:
                                self._graph[1].remove([j[k][0] + i, j[k][1]])
                            self._adjacency_list[i].pop(k)
                            if self.degree:
                                self.degree -= 1
                            break
            elif self.directed and not self.weighted:
                for i, j in self._adjacency_list.items:
                    for k in range(len(j)):
                        if j[k] == node:
                            self._graph[1].remove(i + j[k])
                            try:
                                self._graph[1].remove(j[k] + i)
                            except ValueError as e29:
                                pass
                            self._adjacency_list[i].pop(k)
                            if self.degree:
                                self.degree -= 2
                            if self.degrees:
                                self.degrees[self._graph[0].index(i)][0] -= 1
                            break
            else:
                for i, j in self._adjacency_list.items:
                    for k in range(len(j)):
                        if j[k][0] == node:
                            self._graph[1].remove([i + j[k][0], j[k][1]])
                            self._adjacency_list[i].pop(k)
                            if self.degree:
                                self.degree -= 2
                            if self.degrees:
                                self.degrees[self._graph[0].index(i)][0] -= 1
                            break
                for i in range(len(adjacent_nodes)):
                    self._graph[1].remove(
                        [node + adjacent_nodes[i][0], adjacent_nodes[i][1]]
                    )
                    if self.degrees:
                        self.degrees[self._graph[0].index(adjacent_nodes[i][0])][1] -= 1
            if self.degrees:
                self.degrees.pop(node_index)
            self._graph[0].pop(node_index)
        else:
            for ver in node:
                self.delete_node(ver)

    def delete_edge(self: "graph", node1: str, node2: str) -> None | NoReturn:
        try:
            node1_index: int = self._graph[0].index(node1)
        except ValueError as e30:
            raise ValueError(f"Invalid node {node1!r} !") from None
        try:
            node2_index: int = self._graph[0].index(node2)
        except ValueError as e31:
            raise ValueError(f"Invalid node {node2!r} !") from None
        if not self.directed and not self.weighted:
            try:
                self._adjacency_list[node1].remove(node2)
                self._adjacency_list[node2].remove(node1)
            except ValueError as ee:
                raise ValueError(
                    f"There is no edge between {node1} and {node2} !"
                ) from None
            try:
                self._graph[1].remove(node1 + node2)
            except ValueError as ee:
                self._graph[1].remove(node2 + node1)
            self._adjacency_matrix[node2_index][node1_index] = 0
        elif not self.directed and self.weighted:
            try:
                self._adjacency_list[node1].remove(
                    [node2, self._adjacency_matrix[node1_index][node2_index]]
                )
                self._adjacency_list[node2].remove(
                    [node1, self._adjacency_matrix[node2_index][node1_index]]
                )
            except ValueError as ee:
                raise ValueError(
                    f"There is no edge between {node1} and {node2} !"
                ) from None
            try:
                self._graph[1].remove(
                    [
                        node1 + node2,
                        self._adjacency_matrix[node1_index][node2_index],
                    ]
                )
            except ValueError as ee:
                self._graph[1].remove(
                    [
                        node2 + node1,
                        self._adjacency_matrix[node2_index][node1_index],
                    ]
                )
            self._adjacency_matrix[node2_index][node1_index] = 0
        elif self.directed and not self.weighted:
            try:
                self._adjacency_list[node1].remove(node2)
                self._graph[1].remove(node1 + node2)
            except ValueError as ee:
                raise ValueError(
                    f"There is no edge between {node1} and {node2} !"
                ) from None
        else:
            try:
                self._adjacency_list[node1].remove(
                    [node2, self._adjacency_matrix[node1_index][node2_index]]
                )
                self._graph[1].remove(
                    [node1 + node2, self._adjacency_matrix[node1_index][node2_index]]
                )
            except ValueError as ee:
                raise ValueError(
                    f"There is no edge between {node1} and {node2} !"
                ) from None
        self._adjacency_matrix[node1_index][node2_index] = 0
        if self.degree:
            self.degree -= 2
        if self.degrees:
            self.degrees[node1_index][0] -= 1
            self.degrees[node2_index][1] -= 1

    def __search(
        self: "graph",
        node: str,
        node2: str | None = None,
        *,
        algorithm: str = "rec-dfs",
        is_bool: bool = False,
        visited: Set | hashMap | None = None,
        reversed_adj_lst: hashMap | None = None,
    ) -> List | str | NoReturn:
        if node not in self._adjacency_list:
            raise ValueError(f"Node {node!r} is not in the set of vertices !")
        if node2 is not None:
            if node2 not in self._adjacency_list:
                raise ValueError(f"Node {node2!r} is not in the set of vertices !")
        if algorithm == "rec-dfs":
            disconnected: List = []
            stack: List = [node]
            if visited:
                visited.update(hashMap([[node, 0]]))
            visited_nodes: hashMap = (
                hashMap([[node, 0]]) if visited is None else visited
            )
            while stack:
                if node2 is not None:
                    if visited_nodes._keys[-1] == node2:
                        break
                else:
                    if len(visited_nodes) == len(self._adjacency_list):
                        break
                if not reversed_adj_lst:
                    for i in range(
                        visited_nodes[stack[-1]], len(self._adjacency_list[stack[-1]])
                    ):
                        if not self.weighted:
                            if self._adjacency_list[stack[-1]][i] not in visited_nodes:
                                visited_nodes[stack[-1]] = i + 1
                                stack.append(self._adjacency_list[stack[-1]][i])
                                visited_nodes[stack[-1]] = 0
                                break
                        else:
                            if self._adjacency_list[stack[-1]][i][0] not in visited_nodes:
                                visited_nodes[stack[-1]] = i + 1
                                stack.append(self._adjacency_list[stack[-1]][i][0])
                                visited_nodes[stack[-1]] = 0
                                break
                    else:
                        stack.pop()
                else:
                    for i in range(
                        visited_nodes[stack[-1]], len(reversed_adj_lst[stack[-1]])
                    ):
                        if not self.weighted:
                            if reversed_adj_lst[stack[-1]][i] not in visited_nodes:
                                visited_nodes[stack[-1]] = i + 1
                                stack.append(reversed_adj_lst[stack[-1]][i])
                                visited_nodes[stack[-1]] = 0
                                break
                        else:
                            if reversed_adj_lst[stack[-1]][i][0] not in visited_nodes:
                                visited_nodes[stack[-1]] = i + 1
                                stack.append(reversed_adj_lst[stack[-1]][i][0])
                                visited_nodes[stack[-1]] = 0
                                break
                    else:
                        stack.pop()
            else:
                if node2 is not None:
                    return f"No path found from {node} to {node2}"
                else:
                    if len(visited_nodes) == len(self._adjacency_list):
                        pass
                    else:
                        if is_bool:
                            return False
                        for vertex in self._adjacency_list:
                            if vertex not in visited_nodes:
                                disconnected.append(vertex)
            if is_bool:
                return True
            return list(visited_nodes), visited_nodes, disconnected
        elif algorithm == "dfs":
            disconnected: List = []
            stack: List = [node]
            path: List = []
            visited_nodes: Set = set(node) if visited is None else visited.union(node)
            while stack:
                current = stack.pop()
                path.append(current)
                if node2 is not None:
                    if path[-1] == node2:
                        break
                else:
                    if len(path) == len(self._graph[0]):
                        break
                if not self.weighted:
                    for vertex in self._adjacency_list[current]:
                        if vertex not in visited_nodes:
                            stack.append(vertex)
                            visited_nodes.add(vertex)
                else:
                    for vertex, _ in self._adjacency_list[current]:
                            if vertex not in visited_nodes:
                                stack.append(vertex)
                                visited_nodes.add(vertex)
            else:
                if node2 is not None:
                    return f"No path found from {node} to {node2}"
                else:
                    if len(path) == len(self._graph[0]):
                        pass
                    else:
                        if is_bool:
                            return False
                        for vertex in self._adjacency_list:
                            if vertex not in visited_nodes:
                                disconnected.append(vertex)
            if is_bool:
                return True
            return path, visited_nodes, disconnected
        elif algorithm == "bfs":
            disconnected: List = []
            stack: singlyLinkedList = singlyLinkedList([node])
            visited_nodes: Set = set(node) if visited is None else visited.union(node)
            path: List = []
            while stack:
                current: str = stack.pop(0)
                path.append(current)
                if node2 is not None:
                    if path[-1] == node2:
                        break
                else:
                    if len(path) == len(self._graph[0]):
                        break
                if not self.weighted:
                    for vertex in self._adjacency_list[current]:
                        if vertex not in visited_nodes:
                            stack.append(vertex)
                            visited_nodes.add(vertex)
                else:
                    for vertex, _ in self._adjacency_list[current]:
                        if vertex not in visited_nodes:
                            stack.append(vertex)
                            visited_nodes.add(vertex)
            else:
                if node2 is not None:
                    return f"No path found from {node} to {node2}"
                else:
                    if len(path) == len(self._graph[0]):
                        pass
                    else:
                        if is_bool:
                            return False
                        for vertex in self._adjacency_list:
                            if vertex not in visited_nodes:
                                disconnected.append(vertex)
            if is_bool:
                return True
            return path, visited_nodes, disconnected
        else:
            raise ValueError("No algorithm with this name !")

    def traverse(
        self: "graph", node: str, *, algorithm: str = "rec-dfs"
    ) -> List | NoReturn:
        path, vis, dis = self.__search(node, algorithm=algorithm)
        if not dis:
            return path
        for vertex in dis:
            if vertex in vis:
                continue
            another_path, vis, dis = self.__search(
                vertex, algorithm=algorithm, visited=vis
            )
            if algorithm != "rec-dfs":
                path.extend(another_path)
            else:
                path: List = another_path
            if len(vis) == len(self._adjacency_list):
                break
        return path

    def find_path(
        self: "graph", node1: str, node2: str, *, algorithm: str = "rec-dfs"
    ) -> List | str | NoReturn:
        if not isinstance(node1, str):
            raise ValueError(f"Invalid node {node1} !")
        if not isinstance(node2, str):
            raise ValueError(f"Invalid node {node2} !")
        result: Tuple | str = self.__search(node1, node2, algorithm=algorithm)
        if isinstance(result, str):
            return result
        return result[0]

    def isConnected(self: "graph") -> bool | NoReturn:
        if self.directed:
            raise ValueError("This graph is directed !")
        return self.__search(self._graph[0][0], is_bool=True)

    def isDisconnected(self: "graph") -> bool | NoReturn:
        return not self.isConnected()

    def __reverse_adj_list(self: "graph") -> hashMap:
        reversed_hashMap: hashMap = hashMap()
        for key, value in self._adjacency_list.items:
            if key not in reversed_hashMap:
                reversed_hashMap[key] = []
            for i in range(len(value)):
                if not self.weighted:
                    if value[i] not in reversed_hashMap:
                        reversed_hashMap[value[i]] = [key]
                    else:
                        reversed_hashMap[value[i]].append(key)
                else:
                    if value[i][0] not in reversed_hashMap:
                        reversed_hashMap[value[i][0]] = [key]
                    else:
                        reversed_hashMap[value[i][0]].append(key)
        return reversed_hashMap

    def isStronglyConnected(self: "graph") -> bool | NoReturn:
        if not self.directed:
            raise ValueError("This graph is not directed !")
        if self.__search(self._graph[0][0], is_bool=True):
            if self.__search(
                self._graph[0][0],
                is_bool=True,
                reversed_adj_lst=self.__reverse_adj_list(),
            ):
                return True
        return False

    def isWeaklyConnected(self: "graph") -> bool | NoReturn:
        return not self.isStronglyConnected()

    def __len__(self: "graph") -> int:
        return len(self._graph[0])

    def __str__(self: "graph") -> str:
        if self._graph:
            if not self.detail:
                return f"Vertices : {{{str(self._graph[0])[1:-1]}}}\nEdges : {{{str(self._graph[1])[1:-1]}}}"
            else:
                if self._adjacency_matrix and self._adjacency_list:
                    print(
                        _white("Adjacency matrix :")
                        + "\n"
                        + _cyan("-" * len("Adjacency matrix") + "\n")
                    )
                    adj_mat: List = [[_white("Nodes")]]
                    for i in range(len(self._graph[0])):
                        adj_mat[0].append(_white(self._graph[0][i]))
                    for i in range(len(self._adjacency_matrix)):
                        adj_mat.append([_white(self._graph[0][i])])
                        for j in range(len(self._adjacency_matrix)):
                            if not isinstance(self._adjacency_matrix[i][j], str):
                                if self._adjacency_matrix[i][j] != 0:
                                    adj_mat[i + 1].append(
                                        _green(self._adjacency_matrix[i][j])
                                    )
                                else:
                                    adj_mat[i + 1].append(
                                        _red(self._adjacency_matrix[i][j])
                                    )
                            else:
                                if len(self._adjacency_matrix[i][j]) == 0:
                                    adj_mat[i + 1].append(
                                        _green(self._adjacency_matrix[i][j])
                                    )
                                elif len(self._adjacency_matrix[i][j]) == 1:
                                    adj_mat[i + 1].append(
                                        _green(f"'{self._adjacency_matrix[i][j]}'")
                                    )
                                else:
                                    adj_mat[i + 1].append(
                                        _green(f'"{self._adjacency_matrix[i][j]}"')
                                    )
                    print(tabulate(adj_mat, headers="firstrow", tablefmt="fancy_grid"))
                    print(
                        _white("\nAdjacency list :")
                        + "\n"
                        + _cyan("-" * len("Adjacency list"))
                        + "\n"
                    )
                    if self.weighted:
                        adj_lst: List = [
                            [
                                _white("Nodes"),
                                tabulate(
                                    [[_white("Adjacent Nodes"), _white("Weights")]],
                                    tablefmt="fancy_grid",
                                ),
                            ]
                        ]
                    else:
                        adj_lst: List = [[_white("Nodes"), _white("Adjacent Nodes")]]
                    for i, j in self._adjacency_list.items:
                        adjacent_nodes: List = []
                        if len(j) > 1:
                            for k in range(len(j)):
                                try:
                                    if not isinstance(j[k][1], str):
                                        adjacent_nodes.append(
                                            [_white(j[k][0]), _blue(j[k][1])]
                                        )
                                    else:
                                        if len(j[k][1]) == 0:
                                            adjacent_nodes.append(
                                                [_white(j[k][0]), j[k][1]]
                                            )
                                        elif len(j[k][1]) == 1:
                                            adjacent_nodes.append(
                                                [_white(j[k][0]), _blue(f"'{j[k][1]}'")]
                                            )
                                        else:
                                            adjacent_nodes.append(
                                                [_white(j[k][0]), _blue(f'"{j[k][1]}"')]
                                            )
                                except IndexError as e32:
                                    adjacent_nodes.append([_white(j[k][0])])
                        else:
                            try:
                                if not isinstance(j[0][1], str):
                                    adjacent_nodes.append(
                                        [_white(j[0][0]), _blue(j[0][1])]
                                    )
                                else:
                                    if len(j[0][1]) == 0:
                                        adjacent_nodes.append(
                                            [_white(j[0][0]), j[0][1]]
                                        )
                                    elif len(j[0][1]) == 1:
                                        adjacent_nodes.append(
                                            [_white(j[0][0]), _blue(f"'{j[0][1]}'")]
                                        )
                                    else:
                                        adjacent_nodes.append(
                                            [_white(j[0][0]), _blue(f'"{j[0][1]}"')]
                                        )
                            except IndexError as e33:
                                try:
                                    adjacent_nodes.append(j[0])
                                except IndexError as e34:
                                    pass
                        try:
                            adj_lst.append(
                                [
                                    _white(i),
                                    (
                                        tabulate(adjacent_nodes, tablefmt="fancy_grid")
                                        if len(adjacent_nodes) > 1
                                        or len(adjacent_nodes[0]) > 1
                                        else _white(adjacent_nodes[0])
                                    ),
                                ]
                            )
                        except IndexError as e35:
                            pass
                    return tabulate(adj_lst, headers="firstrow", tablefmt="fancy_grid")
                else:
                    return "[]\n{}"


def _main() -> None:
    print("ntwrk")


if __name__ == "__main__":
    _main()
