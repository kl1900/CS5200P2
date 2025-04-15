# MongoDB replica documentation

To view the replica status, run the following command
```
docker exec -it mongo mongosh --eval 'rs.status()'
```