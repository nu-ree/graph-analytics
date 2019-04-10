

# [CS224W ] Lecture 02 — Measuring Networks, and Random Graph Models

- 강의 : http://web.stanford.edu/class/cs224w/
- 아래에 삽입된 이미지 중 출처가 따로 표기되지 않은 이미지는 강의 화면을 캡쳐하거나 강의 노트를 캡쳐한 이미지입니다. 

**2강 주제**

- Topics 1: How can we measure graph? 
- Topics 2: How can we make an artificial graph? Does it represent original graph? 



## Topics 1: How can we measure graph? 

**Key Network Properties**

- Degree distribution
- Path length
- Clustering Coefficient
- Connected Components



### (1) Degree Distribution

- Degree distribution *P(k)* : 무작위로 선택된 노드의 degree가 *k*일 확률
  - N_k = degree가 k인 노드의 수
  - Normalized histogram : 
    - P(k) = N_k / N
  - 보통은 한쪽으로 왼쪽으로 매우 치우친 분포를 가짐. 즉 대부분은 k가 매우 작음
  - x축에 k , y 축에 N_k를 두고 그래프를 그려보면 좌측 하단에 일직선으로 데이터가 분포하는 경향이 나타나는데, 이것이 의미하는 바는 나중에 중요하게 다뤄질 예정임

  

### (2)  Paths in Graph

- Path : sequence of nodes in which each node is linked to the next one
- 보통은 ***Shortest Path***에 가장 많은 관심을 가짐
- 노드가 서로 연결되어 있지 않으면? h_a,x = ***infinite***
- directed graph에서는 h_b,c 와 h_c,b는 같지 않음. 즉, b에서 c로 가는 최단경로와 c에서 b로 가는 최단경로는 다름(***Not symmetric***)

**Network diameter**

-  Diameter : maximum (shortest path) distance between any pair of nodes in a graph
- "longest shortest path"
- Average path length(Average shortest path): 
  - E_max : 그래프 내의 엣지 수의 총합(max # of edges = total # of node pairs) = n(n-1) / 2
  - h_ij = *shortest(?)* distance from node - to node j.  
  - 보통은 연결된 노드 페어 안에서만 계산. 연결 안되어있어서 length paths가 infinite면은 무시. 계산 안함



### (3)  Clustering Coefficient

- 내 친구중 얼마만큼이 서로 친구일까? 내 친구가 서로 친구일 확률은?

- 내 친구 중에 서로 친구인 pair의 수 / 내 친구가 서로 친구가 되는 가능한 모든 pair의 수

- C_i = 0 이면? 내 친구중에 서로 연결된 친구는 없는것. 내가 ***bridge*** 역할을 함. 모든 정보는 나를 통해서 전달될 수 밖에 없음 

  - 그럼 C_i = 0이면 무조건 bridge 노드일까? No. 이런 경우 있음. 

     ![1553661834783](C:\Users\nrchu\Documents\GitHub\graph-analytics\images\1553661834783.png)


​    

- C_i = 1/2이면? 

  - 내 친구가 4명(=node degree k_i = 4). 
  - 친구가 서로 친구일 가능  pair의 수는 6 (=4*3/2).
  - 실제로 서로 친구인 pair의 수는 3

    $$C_i  = 3 * (2/4*3) = 1/2$$

- 소셜네트워크는 C_i가 상당히 높음. 즉, 나와 연결된 노드(=친구)가 서로 친구일 확률이 높은 네트워크임 

- 전체 그래프의 Average clustering coefficient 로 graph를 측정할 수도 있음

- 연결된 노드가 하나뿐인 경우  C_i는 어떻게 측정? 

  - 무시하거나, 0이라고 보거나. 보통은 0이라고 봄

- 방향성 있는 그래프(directed graph)에서는?

  - 방향성 있는 그래프에서는 C_i 를 보통 계산하지 않음. 다른 방법으로 클러스터링하고 속성 측정함. 향후 수업에서 다룰 주제.

### (4) Connectivity

- size of the largest connected component
- connected components 는 어떻게 찾는가? 
  - 랜덤노드에서 시작해서 너비 우선 탐색(BFS, Breadth-First Search)를 하면서 방문한 노드마다 레이블링. 모든 노드를 방문했다면, 그 네트워크는 connected network 만들어짐. 그 다음에 다시 방문 안한 노드 찾고, BFS 반복
  - BFS 참고자료: <https://gmlwjd9405.github.io/2018/08/15/algorithm-bfs.html>



### 사례 : MSN 메신저 이용자 그래프

- 메신저 데이터에서 **친구 관계(contact)** 또는 **대화(conversation)**를 엣지로 표현할 수 있음

- 이 사례에서는 대화를 가지고 노드를 연결

(1) Degree Distribution => ***Heavily skewed. avg degree = 14.4***

-  MSN 메신저 이용자 대화 그래프에서 각 노드의 degree 분포를 시각화하면?
  -  x 축 : 한달 동안 대화한 사람의 수 
  - 한달에 2000명 이상과 대화한 가입자는 로봇으로 의심해볼만함
  - 딱히 아래 그래프에서는 그외 딱히 찾을 수 있는 인사이트가 없음. 대부분이 2000 안쪽에 겹쳐있어서. 

![1553694237395](C:\Users\nrchu\Documents\GitHub\graph-analytics\images\1553694237395.png)



- 그런데, 양쪽에 모두  log 를 취해주면 네트워크의 구조가 보임
  - 대부분의 사람들은 상대적으로 낮은 수준의 degree를 가지는 것을 확인할 수 있음(좌측 상단)
  - 아주 적은 수의 사람들(800 정도?)만 높은 수준의 degree를 가짐

![1553697776730](C:\Users\nrchu\AppData\Roaming\Typora\typora-user-images\1553697776730.png)

(2) Clustering Coefficient => ***Avg C = 0.11***

- degree가 k인 노드의 평균 C_i의 분포(?)
- x,y축 모두 log 취함

![1553698217686](C:\Users\nrchu\AppData\Roaming\Typora\typora-user-images\1553698217686.png)

(3) Connected Components => ***One Giant Component(99.9% nodes)***

- x축: 각 connected component에 속한 노드의 수
- x,y축 모두 log 취함
  - largest component에 99.9%의 노드가 속해있음
  - small component(구성 노드 100개 미만)는 몇개 없음

![1553698587420](C:\Users\nrchu\AppData\Roaming\Typora\typora-user-images\1553698587420.png)



(4) Diameter of WCC => ***path length = 6.6***

- x축: 최단경로(diameter) 길이
- x,y축 모두 log 취함

- 평균 6.6 정도 길이의 최단경로를 가짐. 즉 노드 안에 있는 모든 사람은 평균 6다리 안에 있음 



- 이런 네트워크의 속성값은 특이한 것일까? 일반적인 것(expected)일까?
  - 소셜 네트워크 뿐만 아니라 단백질 네트워크(?)에서도 비슷한 분포가 나타나고 있음
  - 예:
    - a. Undirected network N=2,018 proteins as nodes E=2,930 binding interactions as links.
      b. Degree distribution: Skewed. Average degree =2.90
      c. Diameter: Avg. path length = 5.8
      d. Clustering: Avg. clustering = 0.12
      Connectivity: 185 components , the largest component 1,647 nodes (81% of nodes)
  - MSN 데이터와 크기부터 다른데 속성값은 비슷한 수치를 나타내고 있음. 





### 그럼, 랜덤 네트워크를 만들어보고 위에서 배운 4가지 속성값을 측정해보자

- 랜덤 네트워크를 만드는 가장 간단한 방법 : *Erdös-Renyi*의  *Random Graphs* [Erdös-Renyi, ‘60]
- Two variants : 
  - G_n,p : 
    - undirected graph on ***n*** nodes and each edge(u,v) appears i.i.d. with probability ***p***
    - n개의 노드를 그린 후에, 노드 2개를 선택하고 그 노드를 연결할 것인지 말것인지 동전 던져서 결정(확률  ***p***) 
    - 예: 노드 10개이고, 두 노드가 서로 연결될 확률이 1/6인 그래프를 그리면? 매번 매우 다른 형태의 그래프가 그려질것.
    -  특히, ***그래프 사이즈(n의 갯수)가 무한대***가 되면 어떻게 될까? 관점에서 생각해보기
  - G_n,m:
    - undirected graph with ***n*** nodes and ***m*** uniformly at random picked edges
- 이렇게 하면 어떤 그래프가 그려질까? 



***(1) Degree distribution***:

- Fact : G_np의 분포는 이항분포(binomial distribution)을 따른다
- ***그래프 사이즈(n의 갯수)가 무한대가 되면?***
  - n이 커질수록 평균 degree 당 분산(sigma / mean k)은 0에 수렴하게 된다. 
  - 즉 평균 k값을 중심으로 분산이 점점 작아짐(분포가 뾰족해짐)

***(2) Clustering Coefficient***: 

- 노드 i의 친구가 서로 연결된 경우의 수( e_i)의 기대감 E[e_i] 는 
  - p x (k_i x(k_i -1))/2 .
  - 즉, (각 페어가 서로 연결될 확률 p ) X (연결될 수 있는 페어의 총 갯수)
  - C = p = man(k) / n

***(3) Path Length***:

- 노드간 최단거리의 분포는 어떻게 생겼을까? 
  - O(log n)의 형태를 가짐. 
- 노드간 최단거리를 찾아내는 방법은? 
- 1) Expansion이라는 속성을 정의해야 함
  - 어떻게 계산할까? 
    - 노드 중 어떤 subset을 골랐을 때, 얼마나 많은 엣지가 그 셋을 빠져나갈까? 
    - 선택한 셋에서 빠져나가는 노드의 수(# of edges leaving S) 는 알파(=expansion) x min()
    - for all possible subsets of nodes에 대해서 얼마나 많은 노드가 그 서브셋 밖으로 나가는지 측정
    - 이를 set의 사이즈로 나눔. 이걸 expansion. 
    - 왜  min(set, v\s)로 나눌까? set의 크기가 전체 그래프의 절반 이상으로 커지면, 그 셋의 크기로 나눠주지 않고 smaller half of the graph로 노멀라이즈 해줌. 이렇게 하지않으면  ???????????????????? 45분에 설명, 51분쯤에 다시 설명
  - Expansion은 robustness를 특정하는 방법. 어떤 노드를 disconnect 하기 위해서 몇 개의 엣지를 잘라야 하는지 알려줌. 
  - Low expansion : 하나만 끊어줘도 두 그래프다 분리됨
  - High expansion : 어떤 서브셋을 선택하건, 끊어야 할 선이 너무 많음
  - 소셜네트워크는 '커뮤니티'구조를 가지고 있어서, 중간정도의 expansion을 가짐. 커뮤니티 내에서는 높고, 커뮤니티 간에는 낮고

- Random Graph에 Expansion 적용해보자
  - Fact ! 랜덤 그래프는 일반적으로 큰 expansion을 가짐
  - 



***(4) Connected Components***

- 





## 사례를 살펴보자



--- 1:00:32

## The small-world model

> can we have high clustering while also having short paths? 

