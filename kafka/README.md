# Installation

## Java 
```sh
sudo apt update
# sudo apt install default-jdk
sudo apt install openjdk-8-jdk -y 
```

## Zookeeper, Kafka
```sh
sudo apt install zookeeperd -y
wget http://www-eu.apache.org/dist/kafka/2.0.0/kafka_2.11-2.3.0.tgz
tar -xvf kafka_2.11-2.3.0.tgz
```

# Configuration

## Default Port

| Zookeeper | Kafka |
|:---------:|:-----:|
|    2181   |  9092 |

## Zookeeper

`config/zookeeper.properties`

```properties
# the directory where the snapshot is stored.
dataDir=/tmp/zookeeper

# the port at which the clients will connect
clientPort=2181

# disable the per-ip limit on the number of connections since this is a non-production config
maxClientCnxns=0
```

2개 이상의 cluster를 구성할 경우 위 파일에 아래와 같이 추가해준다.

```properties
server.1="host name or ip":2888:3888
server.2="host name or ip":2888:3888
server.3="host name or ip":2888:3888
```

## Kafka

`config/server.properties`

```properties
broker.id=0
log.dirs=/tmp/kafka-logs
zookeeper.connect=localhost:2181

# topic 삭제 허용 여부 추가
delete.topic.enable = true
```

`delete.topic.enable` default 값은 false 이다. 
topic 삭제 명령을 했을 때 표면적으로 지워진 것으로 보이나 실제로 topic과 데이터는 지워지지 않는다. 

```properties
zookeeper.connect="hostname or ip":2181,"hostname or ip":2181, ....
```

여러개의 cluster를 구성했을 때는 `zookeeper.connect` 에 cluster 들을 기입해준다.

## Systemd 서비스 등록

`vi /etc/systemd/system/zookeeper.service`

```properties
[Unit]
Requires=network.target remote-fs.target
After=network.target remote-fs.target

[Service]
Type=simple
User=kafka
ExecStart=$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties
ExecStop=$KAFKA_HOME/bin/zookeeper-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
```

`vi /etc/systemd/system/kafka.service`

```properties
[Unit]
Requires=zookeeper.service
After=zookeeper.service

[Service]
Type=simple
User=kafka
ExecStart=$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
ExecStop=$KAFKA_HOME/bin/kafka-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
```

컴퓨터 재시작 시 zookeeper, kafka가 자동으로 실행되게 하기 위해 systemd 서비스로 등록

```
systemctl daemon-reload
systemctl start zookeeper
systemctl enable zookeeper
systemctl start kafka
systemctl enable kafka
```

파일 저장 후 Zookeeper, Kafka 서비스 재시작

# Started

## 1. Start Zookeeper / Kafka Server

```sh
bin/zookeeper-server-start.sh -daemon config/zookeeper.properties 
bin/kafka-server-start.sh -daemon config/server.properties
```

## 2. Create Topic

```sh
bin/kafka-topic.sh --create 
                    --zokeeper localhost:2181 
                    --replication-factor 1 
                    --partitions 1 
                    --topic test
```

## 3. Kafka Topic List

```sh
bin/kafka-topics.sh --list 
                    --zookeeper localhost:2181
```

## 4. Kafka Producer

```sh
bin/kafka-console-producer.sh --broker-list localhost:9092
                                --topic test
```

## 5. Kafka Consumer

```sh
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092
                                --topic test
                                --from-beginning
```