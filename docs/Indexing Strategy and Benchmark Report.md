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

python benchmark_all_pipelines.py

This would add 100000 fake orders

Index Creation Scripts:

Top Selling Products:
orders: { transaction_date: 1 }
products: { product_id: 1 }

Most Active Buyers:
orders: { transaction_date: 1, user_id: 1 }
users: { user_id: 1 }

Orders Last 7 Days
orders: { transaction_date: 1 }

Query Execution Plans and Analysis:(The specific logs are stored in docs/logs for queries)
1️⃣ Top Selling Products (Last 30 Days)
Metric	Before Index	After Index
Stage	COLLSCAN	IXSCAN
Total Docs Examined	100,000	16,535
Total Keys Examined	0	16,535
Execution Time	~69 ms	~45 ms
$lookup Docs Examined	100	5
$lookup Index Used	No	Yes { product_id: 1 }
Improvement	~35% faster


2️⃣ Most Active Buyers (Last 30 Days)
Metric	Before Index	After Index
Stage	COLLSCAN	IXSCAN (compound index)
Total Docs Examined	100,000	0
Total Keys Examined	0	16,535
Execution Time	~53 ms	~8 ms
$lookup Docs Examined	105	5
$lookup Index Used	No	Yes { user_id: 1 }
Improvement	~85% faster

3️⃣ Orders per Day (Last 7 Days)
Metric	Before Index	After Index
Stage	COLLSCAN	IXSCAN
Total Docs Examined	100,000	0
Total Keys Examined	0	3,840
Execution Time	~41 ms	~3 ms
Improvement	~92% faster

Query	Improvement	Execution Time Before	Execution Time After	Indexes Used
Top Selling Products	~35% faster	~69 ms	~45 ms	transaction_date, product_id
Most Active Buyers	~85% faster	~53 ms	~8 ms	transaction_date + user_id, user_id
Orders Last 7 Days	~92% faster	~41 ms	~3 ms	transaction_date

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