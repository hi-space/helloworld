# Redis

### Single Instance Architecture

![](.gitbook/assets/image%20%2822%29.png)

Redis Server : Responsible for storing data and serving to the client



### Redis Replication

![](.gitbook/assets/image%20%283%29.png)

Master - Slave 구조로, 모든 Slave에는 Master와 동일한 데이터가 포함된다. 모든 쿼리는 Master 서버로 리디렉션되고, 쓰기 작업이 발생하면 Master는 새로 작성된 데이터를 모든 Slave에 동기화 한다. Master에 문제가 생기게 되면 다른 Slave가 Master를 대신하게 된다.

데이터 장애 복구를 위해 사용하는 구

### Redis Clustering

![](.gitbook/assets/image%20%282%29.png)

데이터르 여러 컴퓨터에 분할 저장하기 위함이다. 더 많은 데이터들을 클러스트에게 저장하고자 한다. Node\(Redis Server\)가 4개 이기 때문에 하나의 Node라도 장애가 발생하게 되면 전체 클러스터 작동이 중지된다. 



## Link

{% embed url="http://qnimate.com/overview-of-redis-architecture/\#prettyPhoto" %}



