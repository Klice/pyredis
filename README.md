# Python REDIS implementation

## Test commands
```bash
docker run --network=host -it redis:latest redis-benchmark -t SET,GET -r 100000
```
```bash
(printf "PING\r\nPING\r\nPING\r\n"; sleep 1) | nc localhost 6379
```

