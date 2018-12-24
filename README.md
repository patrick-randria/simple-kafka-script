# simple-kafka-script
Monitor empty velo stations from JCDecaux API with kafka

## Usage
Tested with Kafka [kafka_2.11-2.1.0](https://kafka.apache.org/)

Make sure to install python module for kafka
```
pip install kafka-python
```

Start zookeeper
```
$ ./bin/zookeeper-server-start.sh ./config/zookeeper.properties
```
Start kafka
```
$ ./bin/kafka-server-start.sh ./config/server.properties
```

Create topics with desired partitions number (here 10)
```
$ ./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 10 --topic empty-stations
```
