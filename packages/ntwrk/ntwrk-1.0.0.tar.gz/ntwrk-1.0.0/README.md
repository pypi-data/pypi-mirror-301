# ntwrk


[![PyPI version](https://badge.fury.io/py/ntwrk.svg)](https://badge.fury.io/py/ntwrk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This library was created to simplify the concept of graphs by visualizing them in a perfect and clear way, especially for beginners in data structures.


## Installation


You can install `ntwrk` via pip:


```bash
pip install ntwrk
```


## Usage 


### For undirected unweighted graph


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges)
print(g)
```


#### Output


```bash
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k'}
Edges : {'ne', 'nt', 'nw', 'no', 'nk', 'et', 'eo', 'er', 'tw', 'tk', 'wo', 'wr', 'or', 'ok', 'rk'}
```


#### You can show all details (adjacency matrix, adjacency list)


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges, detail=True)
print(g)
```


#### Output


```bash
Adjacency matrix :
----------------

╒═════════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╕
│ Nodes   │   n │   e │   t │   w │   o │   r │   k │
╞═════════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╡
│ n       │   0 │   1 │   1 │   1 │   1 │   0 │   1 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ e       │   1 │   0 │   1 │   0 │   1 │   1 │   0 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ t       │   1 │   1 │   0 │   1 │   0 │   0 │   1 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ w       │   1 │   0 │   1 │   0 │   1 │   1 │   0 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ o       │   1 │   1 │   0 │   1 │   0 │   1 │   1 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ r       │   0 │   1 │   0 │   1 │   1 │   0 │   1 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ k       │   1 │   0 │   1 │   0 │   1 │   1 │   0 │
╘═════════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╛

Adjacency list :
--------------

╒═════════╤══════════════════╕
│ Nodes   │ Adjacent Nodes   │
╞═════════╪══════════════════╡
│ n       │ ╒═══╕            │
│         │ │ e │            │
│         │ ├───┤            │
│         │ │ t │            │
│         │ ├───┤            │
│         │ │ w │            │
│         │ ├───┤            │
│         │ │ o │            │
│         │ ├───┤            │
│         │ │ k │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ e       │ ╒═══╕            │
│         │ │ n │            │
│         │ ├───┤            │
│         │ │ t │            │
│         │ ├───┤            │
│         │ │ o │            │
│         │ ├───┤            │
│         │ │ r │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ t       │ ╒═══╕            │
│         │ │ n │            │
│         │ ├───┤            │
│         │ │ e │            │
│         │ ├───┤            │
│         │ │ w │            │
│         │ ├───┤            │
│         │ │ k │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ w       │ ╒═══╕            │
│         │ │ n │            │
│         │ ├───┤            │
│         │ │ t │            │
│         │ ├───┤            │
│         │ │ o │            │
│         │ ├───┤            │
│         │ │ r │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ o       │ ╒═══╕            │
│         │ │ n │            │
│         │ ├───┤            │
│         │ │ e │            │
│         │ ├───┤            │
│         │ │ w │            │
│         │ ├───┤            │
│         │ │ r │            │
│         │ ├───┤            │
│         │ │ k │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ r       │ ╒═══╕            │
│         │ │ e │            │
│         │ ├───┤            │
│         │ │ w │            │
│         │ ├───┤            │
│         │ │ o │            │
│         │ ├───┤            │
│         │ │ k │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ k       │ ╒═══╕            │
│         │ │ n │            │
│         │ ├───┤            │
│         │ │ t │            │
│         │ ├───┤            │
│         │ │ o │            │
│         │ ├───┤            │
│         │ │ r │            │
│         │ ╘═══╛            │
╘═════════╧══════════════════╛
```


#### You can add nodes with edges


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges)
print(g)
g.add("x", edge="kx")
print(g)
```


#### Output


```bash
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k'}
Edges : {'ne', 'nt', 'nw', 'no', 'nk', 'et', 'eo', 'er', 'tw', 'tk', 'wo', 'wr', 'or', 'ok', 'rk'}
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k', 'x'}
Edges : {'ne', 'nt', 'nw', 'no', 'nk', 'et', 'eo', 'er', 'tw', 'tk', 'wo', 'wr', 'or', 'ok', 'rk', 'kx'}
```


#### You can add nodes and edges


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges)
print(g)
g.add("x")
g.add_edge(node1="k", node2="x")
print(g)
```


#### Output


```bash
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k'}
Edges : {'ne', 'nt', 'nw', 'no', 'nk', 'et', 'eo', 'er', 'tw', 'tk', 'wo', 'wr', 'or', 'ok', 'rk'}
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k', 'x'}
Edges : {'ne', 'nt', 'nw', 'no', 'nk', 'et', 'eo', 'er', 'tw', 'tk', 'wo', 'wr', 'or', 'ok', 'rk', 'kx'}
```


#### You can delete nodes


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k", "x"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk", "kx"]


g = graph(vertices, edges)
print(g)
g.delete_node("x")
print(g)
```


#### Output


```bash
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k', 'x'}
Edges : {'ne', 'nt', 'nw', 'no', 'nk', 'et', 'eo', 'er', 'tw', 'tk', 'wo', 'wr', 'or', 'ok', 'rk', 'kx'}
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k'}
Edges : {'ne', 'nt', 'nw', 'no', 'nk', 'et', 'eo', 'er', 'tw', 'tk', 'wo', 'wr', 'or', 'ok', 'rk'}
```


#### You can delete edges


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k", "x"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk", "kx"]


g = graph(vertices, edges)
print(g)
g.delete_edge("k", "x")
print(g)
```


#### Output


```bash
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k', 'x'}
Edges : {'ne', 'nt', 'nw', 'no', 'nk', 'et', 'eo', 'er', 'tw', 'tk', 'wo', 'wr', 'or', 'ok', 'rk', 'kx'}
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k', 'x'}
Edges : {'ne', 'nt', 'nw', 'no', 'nk', 'et', 'eo', 'er', 'tw', 'tk', 'wo', 'wr', 'or', 'ok', 'rk'}
```


#### You can show how many nodes are in the graph


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges)
print(len(g))
```


#### Output


```bash
7
```


#### You can show how many edges are in the graph


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges)
print(g.edge_count())
```


#### Output


```bash
15
```


#### You can show how many degrees are in the graph


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges)
print(g.degree_count())
```


#### Output


```bash
30
```


#### You can show the node degree  


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges)
print(g.get_degree("n"))
```


#### Output


```bash
5
```


#### You can traverse the graph using different algorithms (DFS, BFS)


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges)
print(g.traverse("n"))
print(g.traverse("n", algorithm="dfs"))
print(g.traverse("n", algorithm="bfs"))
```


#### Output


```bash
['n', 'e', 't', 'w', 'o', 'r', 'k']
['n', 'k', 'r', 'o', 'w', 't', 'e']
['n', 'e', 't', 'w', 'o', 'k', 'r']
```


#### You can find the path between two nodes


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges)
print(g.find_path("n", "k"))
```


#### Output


```bash
['n', 'e', 't', 'w', 'o', 'r', 'k']
```


#### You can check whether the graph is connected or disconnected 


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges)
print(g.isConnected())
print(g.isDisconnected())
```


#### Output


```bash
True
False
```


#### You can create a complete graph


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]


g = graph(vertices, complete=True)
print(g)
```


#### Output


```bash
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k'}
Edges : {'ne', 'nt', 'nw', 'no', 'nr', 'nk', 'et', 'ew', 'eo', 'er', 'ek', 'tw', 'to', 'tr', 'tk', 'wo', 'wr', 'wk', 'or', 'ok', 'rk'}
```


### For undirected weighted graph


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = [("ne", 9), ("nt", 6), ("nw", 9), ("no", 1), ("nk", 3), ("et", 15), ("eo", 10), ("er", 13), ("tw", 3), ("tk", 9), ("wo", 8), ("wr", 5), ("or", 3), ("ok", 4), ("rk", 7)]


g = graph(vertices, edges, weighted=True)
print(g)
```


#### Output


```bash
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k'}
Edges : {['ne', 9], ['nt', 6], ['nw', 9], ['no', 1], ['nk', 3], ['et', 15], ['eo', 10], ['er', 13], ['tw', 3], ['tk', 9], ['wo', 8], ['wr', 5], ['or', 3], ['ok', 4], ['rk', 7]}
```


#### You can show all details (adjacency matrix, adjacency list)


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = [("ne", 9), ("nt", 6), ("nw", 9), ("no", 1), ("nk", 3), ("et", 15), ("eo", 10), ("er", 13), ("tw", 3), ("tk", 9), ("wo", 8), ("wr", 5), ("or", 3), ("ok", 4), ("rk", 7)]


g = graph(vertices, edges, weighted=True, detail=True)
print(g)
```


#### Output


```bash
Adjacency matrix :
----------------

╒═════════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╕
│ Nodes   │   n │   e │   t │   w │   o │   r │   k │
╞═════════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╡
│ n       │   0 │   9 │   6 │   9 │   1 │   0 │   3 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ e       │   9 │   0 │  15 │   0 │  10 │  13 │   0 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ t       │   6 │  15 │   0 │   3 │   0 │   0 │   9 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ w       │   9 │   0 │   3 │   0 │   8 │   5 │   0 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ o       │   1 │  10 │   0 │   8 │   0 │   3 │   4 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ r       │   0 │  13 │   0 │   5 │   3 │   0 │   7 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ k       │   3 │   0 │   9 │   0 │   4 │   7 │   0 │
╘═════════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╛

Adjacency list :
--------------

╒═════════╤════════════════════════════════╕
│ Nodes   │ ╒════════════════╤═════════╕   │
│         │ │ Adjacent Nodes │ Weights │   │
│         │ ╘════════════════╧═════════╛   │
╞═════════╪════════════════════════════════╡
│ n       │ ╒═══╤═══╕                      │
│         │ │ e │ 9 │                      │
│         │ ├───┼───┤                      │
│         │ │ t │ 6 │                      │
│         │ ├───┼───┤                      │
│         │ │ w │ 9 │                      │
│         │ ├───┼───┤                      │
│         │ │ o │ 1 │                      │
│         │ ├───┼───┤                      │
│         │ │ k │ 3 │                      │
│         │ ╘═══╧═══╛                      │
├─────────┼────────────────────────────────┤
│ e       │ ╒═══╤════╕                     │
│         │ │ n │  9 │                     │
│         │ ├───┼────┤                     │
│         │ │ t │ 15 │                     │
│         │ ├───┼────┤                     │
│         │ │ o │ 10 │                     │
│         │ ├───┼────┤                     │
│         │ │ r │ 13 │                     │
│         │ ╘═══╧════╛                     │
├─────────┼────────────────────────────────┤
│ t       │ ╒═══╤════╕                     │
│         │ │ n │  6 │                     │
│         │ ├───┼────┤                     │
│         │ │ e │ 15 │                     │
│         │ ├───┼────┤                     │
│         │ │ w │  3 │                     │
│         │ ├───┼────┤                     │
│         │ │ k │  9 │                     │
│         │ ╘═══╧════╛                     │
├─────────┼────────────────────────────────┤
│ w       │ ╒═══╤═══╕                      │
│         │ │ n │ 9 │                      │
│         │ ├───┼───┤                      │
│         │ │ t │ 3 │                      │
│         │ ├───┼───┤                      │
│         │ │ o │ 8 │                      │
│         │ ├───┼───┤                      │
│         │ │ r │ 5 │                      │
│         │ ╘═══╧═══╛                      │
├─────────┼────────────────────────────────┤
│ o       │ ╒═══╤════╕                     │
│         │ │ n │  1 │                     │
│         │ ├───┼────┤                     │
│         │ │ e │ 10 │                     │
│         │ ├───┼────┤                     │
│         │ │ w │  8 │                     │
│         │ ├───┼────┤                     │
│         │ │ r │  3 │                     │
│         │ ├───┼────┤                     │
│         │ │ k │  4 │                     │
│         │ ╘═══╧════╛                     │
├─────────┼────────────────────────────────┤
│ r       │ ╒═══╤════╕                     │
│         │ │ e │ 13 │                     │
│         │ ├───┼────┤                     │
│         │ │ w │  5 │                     │
│         │ ├───┼────┤                     │
│         │ │ o │  3 │                     │
│         │ ├───┼────┤                     │
│         │ │ k │  7 │                     │
│         │ ╘═══╧════╛                     │
├─────────┼────────────────────────────────┤
│ k       │ ╒═══╤═══╕                      │
│         │ │ n │ 3 │                      │
│         │ ├───┼───┤                      │
│         │ │ t │ 9 │                      │
│         │ ├───┼───┤                      │
│         │ │ o │ 4 │                      │
│         │ ├───┼───┤                      │
│         │ │ r │ 7 │                      │
│         │ ╘═══╧═══╛                      │
╘═════════╧════════════════════════════════╛
```


### For directed unweighted graph


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges, directed=True)
print(g)
```


#### Output


```bash
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k'}
Edges : {'ne', 'nt', 'nw', 'no', 'nk', 'et', 'eo', 'er', 'tw', 'tk', 'wo', 'wr', 'or', 'ok', 'rk'}
```


#### You can show all details (adjacency matrix, adjacency list)


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges, directed=True, detail=True)
print(g)
```


#### Output


```bash
Adjacency matrix :
----------------

╒═════════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╕
│ Nodes   │   n │   e │   t │   w │   o │   r │   k │
╞═════════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╡
│ n       │   0 │   1 │   1 │   1 │   1 │   0 │   1 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ e       │   0 │   0 │   1 │   0 │   1 │   1 │   0 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ t       │   0 │   0 │   0 │   1 │   0 │   0 │   1 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ w       │   0 │   0 │   0 │   0 │   1 │   1 │   0 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ o       │   0 │   0 │   0 │   0 │   0 │   1 │   1 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ r       │   0 │   0 │   0 │   0 │   0 │   0 │   1 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ k       │   0 │   0 │   0 │   0 │   0 │   0 │   0 │
╘═════════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╛

Adjacency list :
--------------

╒═════════╤══════════════════╕
│ Nodes   │ Adjacent Nodes   │
╞═════════╪══════════════════╡
│ n       │ ╒═══╕            │
│         │ │ e │            │
│         │ ├───┤            │
│         │ │ t │            │
│         │ ├───┤            │
│         │ │ w │            │
│         │ ├───┤            │
│         │ │ o │            │
│         │ ├───┤            │
│         │ │ k │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ e       │ ╒═══╕            │
│         │ │ t │            │
│         │ ├───┤            │
│         │ │ o │            │
│         │ ├───┤            │
│         │ │ r │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ t       │ ╒═══╕            │
│         │ │ w │            │
│         │ ├───┤            │
│         │ │ k │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ w       │ ╒═══╕            │
│         │ │ o │            │
│         │ ├───┤            │
│         │ │ r │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ o       │ ╒═══╕            │
│         │ │ r │            │
│         │ ├───┤            │
│         │ │ k │            │
│         │ ╘═══╛            │
├─────────┼──────────────────┤
│ r       │ k                │
╘═════════╧══════════════════╛
```


#### You can check whether the graph is strongly connected or weakly disconnected 


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges, directed=True, detail=True)
print(g.isStronglyConnected())
print(g.isWeaklyConnected())
```


#### Output


```bash
False
True
```


#### You can show the node indegree, outdegree  


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = ["ne", "nt", "nw", "no", "nk", "et", "eo", "er", "tw", "tk", "wo", "wr", "or", "ok", "rk"]


g = graph(vertices, edges, directed=True)
print(g.get_indegree("n"))
print(g.get_outdegree("n"))
```


#### Output


```bash
0
5
```


### For directed weighted graph


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = [("ne", 9), ("nt", 6), ("nw", 9), ("no", 1), ("nk", 3), ("et", 15), ("eo", 10), ("er", 13), ("tw", 3), ("tk", 9), ("wo", 8), ("wr", 5), ("or", 3), ("ok", 4), ("rk", 7)]


g = graph(vertices, edges, directed=True, weighted=True)
print(g)
```


#### Output


```bash
Vertices : {'n', 'e', 't', 'w', 'o', 'r', 'k'}
Edges : {['ne', 9], ['nt', 6], ['nw', 9], ['no', 1], ['nk', 3], ['et', 15], ['eo', 10], ['er', 13], ['tw', 3], ['tk', 9], ['wo', 8], ['wr', 5], ['or', 3], ['ok', 4], ['rk', 7]}
```


#### You can show all details (adjacency matrix, adjacency list)


```python
from ntwrk import graph


vertices = ["n", "e", "t", "w", "o", "r", "k"]
edges = [("ne", 9), ("nt", 6), ("nw", 9), ("no", 1), ("nk", 3), ("et", 15), ("eo", 10), ("er", 13), ("tw", 3), ("tk", 9), ("wo", 8), ("wr", 5), ("or", 3), ("ok", 4), ("rk", 7)]


g = graph(vertices, edges, directed=True, weighted=True, detail=True)
print(g)
```


#### Output


```bash
Adjacency matrix :
----------------

╒═════════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╕
│ Nodes   │   n │   e │   t │   w │   o │   r │   k │
╞═════════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╡
│ n       │   0 │   9 │   6 │   9 │   1 │   0 │   3 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ e       │   0 │   0 │  15 │   0 │  10 │  13 │   0 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ t       │   0 │   0 │   0 │   3 │   0 │   0 │   9 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ w       │   0 │   0 │   0 │   0 │   8 │   5 │   0 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ o       │   0 │   0 │   0 │   0 │   0 │   3 │   4 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ r       │   0 │   0 │   0 │   0 │   0 │   0 │   7 │
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ k       │   0 │   0 │   0 │   0 │   0 │   0 │   0 │
╘═════════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╛

Adjacency list :
--------------

╒═════════╤════════════════════════════════╕
│ Nodes   │ ╒════════════════╤═════════╕   │
│         │ │ Adjacent Nodes │ Weights │   │
│         │ ╘════════════════╧═════════╛   │
╞═════════╪════════════════════════════════╡
│ n       │ ╒═══╤═══╕                      │
│         │ │ e │ 9 │                      │
│         │ ├───┼───┤                      │
│         │ │ t │ 6 │                      │
│         │ ├───┼───┤                      │
│         │ │ w │ 9 │                      │
│         │ ├───┼───┤                      │
│         │ │ o │ 1 │                      │
│         │ ├───┼───┤                      │
│         │ │ k │ 3 │                      │
│         │ ╘═══╧═══╛                      │
├─────────┼────────────────────────────────┤
│ e       │ ╒═══╤════╕                     │
│         │ │ t │ 15 │                     │
│         │ ├───┼────┤                     │
│         │ │ o │ 10 │                     │
│         │ ├───┼────┤                     │
│         │ │ r │ 13 │                     │
│         │ ╘═══╧════╛                     │
├─────────┼────────────────────────────────┤
│ t       │ ╒═══╤═══╕                      │
│         │ │ w │ 3 │                      │
│         │ ├───┼───┤                      │
│         │ │ k │ 9 │                      │
│         │ ╘═══╧═══╛                      │
├─────────┼────────────────────────────────┤
│ w       │ ╒═══╤═══╕                      │
│         │ │ o │ 8 │                      │
│         │ ├───┼───┤                      │
│         │ │ r │ 5 │                      │
│         │ ╘═══╧═══╛                      │
├─────────┼────────────────────────────────┤
│ o       │ ╒═══╤═══╕                      │
│         │ │ r │ 3 │                      │
│         │ ├───┼───┤                      │
│         │ │ k │ 4 │                      │
│         │ ╘═══╧═══╛                      │
├─────────┼────────────────────────────────┤
│ r       │ ╒═══╤═══╕                      │
│         │ │ k │ 7 │                      │
│         │ ╘═══╧═══╛                      │
╘═════════╧════════════════════════════════╛
```


### Note


You can use all the methods we use for undirected unweighted graph with other types of graphs as well.


## License


This project is licensed under the MIT LICENSE - see the [LICENSE](https://opensource.org/licenses/MIT) for more details.