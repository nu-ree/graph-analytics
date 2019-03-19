

# [AN] Lecture 01 — Structure of Graphs

- Stanford / CS224W  / Analysis of Networks 를 듣고 정리한 자료입니다.
- 강의 : http://web.stanford.edu/class/cs224w/

- Reading List : https://docs.google.com/document/d/1peGN55M4pLjdWgEI3Mnw5BtnlW6YOBYDldEm5znGxV0/edit

## Class Outline

- Graph concepts, models and measurements (1-3)
-  Network Construction and Inference (4)
- Link Analysis: PageRank and SimRank (5)
-  Network Motifs: Structural roles in Networks (6)
- Community Detection (7, 8)
-  Link Prediction (9)
-  Node Representation Learning: Node2Vec (10)
-  Information Cascades (11, 12)
-  Influence & Outbreak Detection (13, 14)
-  Network Robustness (15)
-  Network Evolution (16)
-  Node Centrality and Anomaly Detection (17)
-  Knowledge Graphs and Metapaths (18)
-  Message passing and Node classification (19)
-  Graph Convolutional Neural Networks (20)



## Why Network?

- 복잡한 데이터를 설명하는  universal language임

- 다양한 분야에서 사용되고 있음(컴공, 사회과학, 물리학, 경제학, 통계학 등등)
- 네트워크로 분석할 수 있는 데이터 존재 + 컴퓨팅 파워도 있음
- 컴퓨팅 파워의 증가에 따라 다양한 네트워크(power grid 등)를 연구할 수 있게 되었음



## Ways to Analyze Networks

- 그래프로 할 수 있는 분석에는 크게 4가지가 있음

- 1)  Node Classification: 이 노드는 어떤 유형에 속할까? 

  2) Link Prediction : 얘랑 쟤는 연결되어 있을까? (페이스북의 친구 추천)

  3) Community Detection :  맨날 모여서 노는 애들은 누굴까? (뉴런의 functional unit 찾기)

  4) Network Similarity : 이 두 노드는 혹은 이 두 무리는 얼마나 닮았을까?  



## Applications

1) 위키피디아에서 가짜 페이지를 어떻게 찾을 수 있을까? 

 - knowledge graph structure를 이용하면 86%는 찾을 수 있음!
 - 가짜 페이지는 out link만 존재하고 in-link를 받지 못하는 경향이 있음

2)  콘텐츠 추천 시스템에도 link prediction 활용

3) 정보가 어떻게 전파 될까? (Information virality)

4) 누구가 얼리어답터고 누가 얼리어답터의 추천을 받아서 제품을 구매할까? (product adoption) 





## How do we mine networks? 

- Empirically (how do we measure and quantify network?)
- with mathematical models (graph theory, statistical models)
- with algorithms (computational challenge!)



## Graph Components

- Node / vertex 
- Link / Edges
- G(N, E)

## Network or Graph?

- Network : 보통 실제 시스템을 나타내는 의미로 사용
- Graph : 네트워크를 수학적으로 표현한 것



## How to represent graph

**Directed vs Undirected**

- Directed : 친구 관계
- Undirected: 팔로워 관계



**Node Degrees**

- 노드 i에 연결된 엣지의 수

- Directed networks의 경우, in-degree 와 out-degree가 있음. 이 경우 node degree는 in-degree와 out-degree의 합!

- 그래프 전체 차원에서 봤을 때, In-degree의 합 = out-degree의 합

- Avg. degree:

  - Directed graph : E / N. 엣지의 수 / 노드의 수
  - Undirected graph: 2E / N

- 두 노드 사이에 엣지가 여러개라면? multigraph 라고 함

  

**Complete Graph**

- 엣지의 최대 수만큼 연결된 그래프 (Clique라고도 부름)



**Directness & Average Degrees**

- 일반적으로 그래프의 average degree는 10 안팍임
- 즉 대부분의 그래프는 sparse한 게 일반적



**Bipartite Graph**

- 노드가 두 가지 disjoint sets로 구성
- 보통 연결하고자 하는 노드의 종류가 서로 다를 때 이렇게 나타남
- 예를 들어 
  - 연구자 - 연구 논문
  - 배우 - 영화
  - 관객 - 영화
  - 재료 - 요리
- Bipartite Graph를 통해 Folded graph를 도출할 수 있음
  - 동그라미 = 저자 / 네모 = 논문이라고 하면 Projection U는 Author Collaboration Network
  - 동그라미 = 요리재료 / 네모 = 맛이라고 하면 Projection V는 Flavor Network 

<img src = "https://slideplayer.com/slide/9811759/32/images/43/BIPARTITE+GRAPHS.jpg"> </img>





## Graph를 나타내는 방법

### 1) Adjacency Matrix

- 노드 간의 연결 관계를 매트릭스로 표현
- undirected 면 symmetric, directed면 not symmetric
- Node degree는 undirected면 row 또는 column 의 합. directed graph면 out-degree는 row의 합, in-degree는 column의 합

- 대부분의 그래프는 매우 sparse함. 공간낭비

### 2) Edge List

- 엣지 리스트로 표현할 수도 있음
  - (1,2)
  - (2,3)
  - (3,4)
- 특정 엣지에 접근하려면 리스트를 전부 탐색할 수 밖에 없음



### 3) Adjacency List

