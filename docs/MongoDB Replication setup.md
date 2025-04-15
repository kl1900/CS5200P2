## MongoDB Replica Set Setup

### Architecture Overview

This project uses a **MongoDB replica set** for high availability and data redundancy. The setup includes:

| Node              | Role     | Port     | Container Name     |
|-------------------|----------|----------|--------------------|
| `mongo`           | Primary  | 27017    | `mongo`            |
| `mongo-secondary` | Secondary| 27018    | `mongo-secondary`  |

These nodes are configured as members of the same replica set (`rs0`) using Docker Compose.

---

### Docker Compose Integration

The replica set is defined in `docker-compose.yml` with:

- Both `mongo` and `mongo-secondary` using `mongod --replSet rs0`
- A one-time `mongo-init` container that runs `rs.initiate()` to configure the replica set

```yaml
mongo-init:
  image: mongo
  depends_on:
    - mongo
    - mongo-secondary
  restart: "no"
  entrypoint: >
    bash -c "sleep 5 &&
    mongosh --host mongo --eval '
      rs.initiate({
        _id: \"rs0\",
        members: [
          { _id: 0, host: \"mongo:27017\" },
          { _id: 1, host: \"mongo-secondary:27017\" }
        ]
      })'"
```

---

### Connection String

Applications can connect using a replica set–aware URI:

```bash
mongodb://mongo:27017,mongo-secondary:27017/?replicaSet=rs0
```

> Even if the application connects only to the **primary**, the **secondary will still replicate data** as long as it's part of the set.

---

### Benefits of Replication

1. **High Availability**  
   If the primary node (`mongo`) fails, a secondary node can be promoted to primary automatically (if you later add voting nodes or arbiter).

2. **Data Redundancy**  
   All writes to the primary are automatically replicated to the secondary, reducing the risk of data loss.

3. **Read Scaling (Optional)**  
   Applications can read from the secondary node by specifying:
   ```bash
   readPreference=secondary
   ```

4. **Disaster Recovery**  
   You can back up data from the secondary without affecting primary workload.

---

### check Replica Status

To check the current status of the replica set:

```bash
docker exec -it mongo mongosh --eval 'rs.status()'
```

This command will show roles (`PRIMARY`, `SECONDARY`) and the health of each node.
