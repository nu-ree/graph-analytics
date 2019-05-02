# 2. Network Basics

## 2.3 Properties of Networks

- Networks are characterized by two types of properties: static and dynamic.
  - Static properties : 
    - fixed. 네트워크가 구성된 이후로 변하지 않음
    - Node & Edges
  - Dynamic properties : 
    - not fixed. 
    - 인구 이동, 전염병 감염 등의 processes
    - 시간의 흐름에 따라 변화
- 이 외에 다음과 같은 특성을 공통적으로 가짐
  - Transitivity : A - B 연결 + B - C 연결 --> A-C도 연결되어 있는가?
  - Network robustness & vulnerability:
    - 외부 압력(노드 제거 등)에 의한 dynamic topological changes에 민감한 네트워크인가? 
    - 노드 제거는 (1) 오류 (2) 공격 등에 의해 발생 가능
    - 노드가 없어지면 path length 와 connectivity에 변동 생김
    - 노드 제거가 계속 되면 결국 네트워크는 fall apart(fragmentation)
    - 하지만 모든 네트워크가 노드 제거에 동일하게 반응하진 x
  - Mixing patterns : 유사한 사람들끼리 서로 섞이는 경향성 파악
  - Community Structure : 커뮤니티 내부적으로는 Node 간에 edge density가 높고, 외부와는 density가 낮음
  - Clique
  - Node degree



## 2.4 Network Measures

- aggregate constraint : the sum of the dyadic constraint on all the ties of a particular vertex.??
- Average degree: A measure of the structural cohesion of a network. To calculate the average degree, all degrees are summed up first and then divided by the total
  number of nodes in the network.

3. Degree distribution: frequency of the degrees of nodes. Graphs with power law
  degree distribution are called scale-free. It gives a rough profile of how the connectivity
  is distributed within the network.
4. Average shortest path. Average shortest path length over all pairs of nodes characterizes
  how large the world represented by the network is, where a small
  length implies that the network is well connected globally.
5. Eccentricity: max shortest path length from each node.
6. Diameter: the longest shortest-path distance over all pairs of nodes in the network
  (or max eccentricity in the network). The goal of measuring diameter
  measure is to index the extensiveness of the network, which means how far
  apart the two furthest nodes in the network are from each other. Radius is the
  min eccentricity in the network.
7. Dyad: A dyad is a pair of nodes connected via one or more ties.
8. Dyadic constraint: The dyadic constraint on vertex u projected by the tie
  between vertex u and vertex v is the extent to which u has more and stronger ties
  with neighbors that are strongly connected with vertex v.
9. Geodesic. A geodesic is the shortest path between two vertices.
10. Average geodesic distance: the mean of the shortest path lengths among all connected
    pairs in the ego network.
11. Multiplicity: the number of times a particular (ordered or unordered pair of
    vertices) line occurs in a network.
12. Popularity: The popularity of a vertex in a directed network is the number of
    arcs that it receives.
13. Triad: a subnetwork consisting of three nodes.

## 2.7 Matrices

- column matrix
- row matrix
- square matrix
- identity matrix
- diagonal matrix : square matrix. 대각선을 기준으로 
- symmetric matrix
- skew-symmetrix : square matrix.  negative is equal to its transpose
- null matrix : all elements are zero.



## 2.8 Types of Matrices in Social Networks

- Adjacency Matrix 
- Edge List : {노드1, 노드2, weight}로 표현. 비어있으면 {}로 표현

- Adjacency List : 각 노드에서 뻗어나가 엣지로 연결된 노드의 리스트  

  `g.adjacency_list()`

- Numpy Matrix

  `nx.to_numpy_matrix(g)`

- Sparse Matrix

  `nx.to_scipy_sparse_matrix(g)`











## 2.9 Basic Matrix Operations

- 행,렬의 크기가 주어지지 않으면 모든 행렬은 square matrix. 
- Matrix permutation : 네트워크의 tie 패턴이 명확해보이지 않을 때 로우와 칼럼을 permute 할 수 있음
- Matrix transpose : 행과 열의 변환. 이렇게 만들어진 Diagraph matrix는 원본과 모양이 다르기도 함. (direction이 동일하지 않아서)
- Matrix addition : 동일한 크기의 matrix를 더할 때. 같은 cell의 값이 더해짐 
- Matrix multiplication  : 두 matrix의 곱. **reachability**를 뜻함. relational algebra에서는 **the basis for compunding relations**을 나타냄
-  



## 2.10 Data Visualization

- graph : 네트워크 사이즈가 매우 클 때 
- trees : undirected graphs. 데이터가 작을 때. polytree, rooted, labeled, recursive, directed, free, binary, ternary trees
- Matrices : 각 칸 = cell, column-matrices, square mat., identity mat., diagonal mat., symmetric mat., skew-symmetric mat., triangle mat., diagonal mat., adjacency mat, edgelist mat., adjacency list
- 
- 
