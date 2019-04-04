# Chapter 4. Social Networks

이번 장에서는 소셜 네트워크의 특성, 데이터 수집, 데이터 샘플링, 소셜네트워크 분석 등을 다룬다.



## 4.1. Social Networks

- 인간관게 혹은 커뮤니케이션 등 '사람'과 관련된 거의 모든 시스템은  소셜네트워크로 볼 수 있음
- 노드 : 보통 사람 혹은 조직. 웹페이지, 논문, 부서, 이웃, 국가 등이 될 수 있음
- 링크 : directed(source --> destination), undirected(reciprocated)
- 두가지 유형으로 그루핑 될 수 있음: 
  - one mode : include **one type of nodes** to represent actors (usually people), subgroups, or communities.
  - multimode : includes **two different sets of nodes**(=bimodal)
    - 조직 & 조직 멤버
    - 이벤트 & 이벤트 참석자
    - 사람 & 그 사람이 가진 정보와 자원
    - multilevel...???????



## 4.2 Properties of a Social Network

### 4.2.1. Scale - Free Networks

- 노드별 엣지의 수(=degree)의 distribution이 ***power law*** 를 따르는 네트워크

- 즉, degree가 낮은 노드가 많고(k가 작은 쪽, 즉 왼쪽에 P(k)가 높음) degree가 높은 노드는 적은(k가 큰 쪽, 오른쪽에 P(k)가 낮음) 형태를 띔

- ***멱법칙(冪法則, power law)***은 한 수가 다른 수의 거듭제곱으로 표현되는 두 수의 함수적 관계

  ==> 양쪽에 로그를 취하면 직선의 관계로

  > linear in log-log plot! 

- 소셜 네트워크에서는 이렇게 극히 일부의 잘 연결된 노드(hub)가 존재 --> 전체 네트워크의 diameter를 줄여줌. 

- 파이썬에선 `nx.scale_free_graph` 이용하여 만들 수 있음



### 4.2.2. Small-World Networks

- 대부분의 노드가 동질적(homogeneous)이고 몇 다리 안간너서 모든 노드에 도달할 수 있는 네트워크.
- 즉, 대부분의 노드가 비슷한 수의 링크를 가지고, the distance between any two nodes grows proportionally to the logarithm ,,,? 

- clustering coefficient 가 매우 높음
- average path length 가 짧고 
- 허브 노드가 매우 많음
- 밀도있는 커뮤니티 혹은 크

### 4.10 Historical Development





### 4.11 Importance of Social Network Analysis

-  SNA에서는 개인 > 가족 > 그룹 > 국가 까지 다양한 레벨로 데이터를 분석함
- health, cybercrime, business, animal social networks, communications 등의 분야에서 연구

### 4.12 Social Network Analysis Modeling Tools

- UCINET, StOCENT, Gephi, Network Workbench, and NodeXL 등이 있음
- 이런 툴들은 주로 subgraph, knowledge networks, hidden population, kinship networks, structural networks 등을 찾아내는 기능이 있음
- 소셜네트워크 역시 수학적인 그래프 이론에 기반하기 때문에 그래프 이론의 주요 컨셉을 이해하는 것이 중요함. 
- SNA의 목적은 네트워크의 지역적 또는 전반적인 패턴이나 인플루언서, 네트워크 다이나믹 등을 찾아내는데 있음. 