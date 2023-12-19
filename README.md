# PyREDIS

Python implementation of Redis server. This project was implemented for education purposes as part of Coding Challenges: https://codingchallenges.fyi/challenges/challenge-redis

## Install

```bash
pip install .
```

## Run

```bash
pyredis
```

## Supported commands

This not full implementation of Redis, just a subset of commands is supported.
List of supported commands:
- GET
- SET (including TTL)
- DEL
- EXISTS
- INCR
- DECR
- LPUSH
- RPUSH
- LRANGE

## Test commands
```bash
docker run --network=host -it redis:latest redis-benchmark -t SET,GET -r 100000
```
```bash
(printf "PING\r\nPING\r\nPING\r\n"; sleep 1) | nc localhost 6379
```

