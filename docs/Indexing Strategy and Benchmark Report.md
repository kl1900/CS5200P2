This report documents our comprehensive indexing strategy and its impact on query performance using three aggregation queries for an e-commerce application. We have focused on:
1. **Top Selling Products (Last 30 Days)**
2. **Most Active Buyers (Last 30 Days)**
3. **Orders per Day (Last 7 Days)**

Each query was benchmarked using MongoDB’s $explain command with the "executionStats" verbosity mode both before and after creating indexes. The performance metrics collected include:
executionTimeMillis
totalDocsExamined
totalKeysExamined

## Step 1: Preparation

### Data
- `orders`: 100,000 fake orders
- `products`: Product information
- `users`: User information

### Environment
- MongoDB v8.0.6
- Docker containerized environment
- Used `$explain("executionStats")` for benchmarking

cd backend

Then run the benchmark script:

docker exec -it flask-backend python3 benchmark_all_pipelines.py

This would add 100000 fake orders

enter mongodb shell:

docker exec -it mongo mongosh

switch to mydb dataset:
use mydb

use 7-day-orders as an example:

db.orders.explain("executionStats").aggregate([
  {
    $match: {
      transaction_date: {
        $gte: new Date(new Date().setHours(0, 0, 0, 0) - 7 * 24 * 60 * 60 * 1000),
        $lt: new Date(new Date().setHours(0, 0, 0, 0))
      }
    }
  },
  {
    $group: {
      _id: { $dateToString: { format: "%Y-%m-%d", date: "$transaction_date" } },
      count: { $sum: 1 }
    }
  },
  {
    $sort: { _id: 1 }
  }
])


db.orders.createIndex({ transaction_date: 1 })

Index Creation Scripts:

Top Selling Products:
orders: { transaction_date: 1 }
products: { product_id: 1 }

Most Active Buyers:
orders: { transaction_date: 1, user_id: 1 }
users: { user_id: 1 }

Orders Last 7 Days
orders: { transaction_date: 1 }
db.orders.createIndex({ transaction_date: 1 })

Query Execution Plans and Analysis:(The specific logs are stored in docs/logs for queries)
Top Selling Products (Last 30 Days)
Stage:
Before Index: COLLSCAN
After Index: IXSCAN

Total Docs Examined:
Before Index: 100,000
After Index: 16,535

Total Keys Examined:
Before Index: 0
After Index: 16,535

Execution Time:
Before Index: ~69 ms
After Index: ~45 ms

$lookup Docs Examined:
Before Index: 100
After Index: 5

$lookup Index Used:
Before Index: No
After Index: Yes { product_id: 1 }

Improvement:
Approximately ~35% faster




2️⃣ Most Active Buyers (Last 30 Days)
Stage:
Before Index: COLLSCAN
After Index: IXSCAN (compound index)

Total Docs Examined:
Before Index: 100,000
After Index: 0

Total Keys Examined:
Before Index: 0
After Index: 16,535

Execution Time:
Before Index: ~53 ms
After Index: ~8 ms

$lookup Docs Examined:
Before Index: 105
After Index: 5

$lookup Index Used:
Before Index: No
After Index: Yes { user_id: 1 }

Improvement:
Approximately ~85% faster



3️⃣ Orders per Day (Last 7 Days)
Stage:
Before Index: COLLSCAN
After Index: IXSCAN

Total Docs Examined:
Before Index: 100,000
After Index: 0

Total Keys Examined:
Before Index: 0
After Index: 3,840

Execution Time:
Before Index: ~41 ms
After Index: ~3 ms

Improvement:
Approximately ~92% faster

Summary Comparison
Top Selling Products:
Improvement: ~35% faster
Execution Time Before: ~69 ms
Execution Time After: ~45 ms
Indexes Used: transaction_date, product_id

Most Active Buyers:
Improvement: ~85% faster
Execution Time Before: ~53 ms
Execution Time After: ~8 ms
Indexes Used: transaction_date + user_id, user_id

Orders Last 7 Days:
Improvement: ~92% faster
Execution Time Before: ~41 ms
Execution Time After: ~3 ms
Indexes Used: transaction_date

Analysis of Execution Plans
Before Indexing
Queries used COLLSCAN (full collection scan).
High totalDocsExamined, low efficiency.
$lookup stages scanned entire foreign collections.

After Indexing
Queries use IXSCAN.
Drastically reduced documents examined — even 0 in some cases (covered query).
$lookup stages benefit from foreign collection indexes.
Execution time reduced by 35%–92%.

Indexes dramatically improved performance for all tested aggregation queries.
Compound indexes on filter + grouping fields yielded the biggest improvements.
$lookup operations were significantly optimized with proper foreign indexes.
The database is now well-prepared for scalable analytics workloads.