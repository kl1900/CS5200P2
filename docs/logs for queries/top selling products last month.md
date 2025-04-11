PS C:\Users\TX129\git\CS5200P2> cd backend
PS C:\Users\TX129\git\CS5200P2\backend> python benchmark_all_pipelines.py
Existing orders cleared.
Inserted 100000 fake orders.
PS C:\Users\TX129\git\CS5200P2\backend> docker exec -it mongo mongosh
Current Mongosh Log ID: 67f86df0186349d0cd6b140a
Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.4.2
Using MongoDB:          8.0.6
Using Mongosh:          2.4.2

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/


To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

------
   The server generated these startup warnings when booting
   2025-04-11T01:17:29.019+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2025-04-11T01:17:29.656+00:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
   2025-04-11T01:17:29.656+00:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2025-04-11T01:17:29.656+00:00: We suggest setting the contents of sysfsFile to 0.
   2025-04-11T01:17:29.656+00:00: vm.max_map_count is too low
   2025-04-11T01:17:29.657+00:00: We suggest setting swappiness to 0 or 1, as swapping can cause performance problems.
------

test> use mydb
switched to db mydb
mydb> db.orders.explain("executionStats").aggregate([
...   { $match: { transaction_date: { $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) } } },
...   { $unwind: "$items" },
...   { $group: { _id: "$items.product_id", totalSold: { $sum: "$items.quantity" } } },
...   { $sort: { totalSold: -1 } },
...   { $limit: 5 },
...   { $lookup: {
...       from: "products",
...       localField: "_id",
...       foreignField: "product_id",
...       as: "product"
...   }},
...   { $unwind: "$product" },
...   { $project: { _id: 0, productName: "$product.name", totalSold: 1 } }
... ]);
...
{
  explainVersion: '1',
  stages: [
    {
      '$cursor': {
        queryPlanner: {
          namespace: 'mydb.orders',
          parsedQuery: {
            transaction_date: { '$gte': ISODate('2025-03-12T01:19:20.094Z') }
          },
          indexFilterSet: false,
          queryHash: 'FD0AA76E',
          planCacheShapeHash: 'FD0AA76E',
          planCacheKey: 'CF253A6E',
          optimizationTimeMillis: 0,
          maxIndexedOrSolutionsReached: false,
          maxIndexedAndSolutionsReached: false,
          maxScansToExplodeReached: false,
          prunedSimilarIndexes: false,
          winningPlan: {
            isCached: false,
            stage: 'PROJECTION_SIMPLE',
            transformBy: { items: 1, _id: 0 },
            inputStage: {
              stage: 'COLLSCAN',
              filter: {
                transaction_date: { '$gte': ISODate('2025-03-12T01:19:20.094Z') }
              },
              direction: 'forward'
            }
          },
          rejectedPlans: []
        },
        executionStats: {
          executionSuccess: true,
          nReturned: 16535,
          executionTimeMillis: 69,
          totalKeysExamined: 0,
          totalDocsExamined: 100000,
          executionStages: {
            isCached: false,
            stage: 'PROJECTION_SIMPLE',
            nReturned: 16535,
            executionTimeMillisEstimate: 20,
            works: 100001,
            advanced: 16535,
            needTime: 83465,
            needYield: 0,
            saveState: 13,
            restoreState: 13,
            isEOF: 1,
            transformBy: { items: 1, _id: 0 },
            inputStage: {
              stage: 'COLLSCAN',
              filter: {
                transaction_date: { '$gte': ISODate('2025-03-12T01:19:20.094Z') }
              },
              nReturned: 16535,
              executionTimeMillisEstimate: 18,
              works: 100001,
              advanced: 16535,
              needTime: 83465,
              needYield: 0,
              saveState: 13,
              restoreState: 13,
              isEOF: 1,
              direction: 'forward',
              docsExamined: 100000
            }
          }
        }
      },
      nReturned: Long('16535'),
      executionTimeMillisEstimate: Long('42')
    },
    {
      '$unwind': { path: '$items' },
      nReturned: Long('49710'),
      executionTimeMillisEstimate: Long('42')
    },
    {
      '$group': {
        _id: '$items.product_id',
        totalSold: { '$sum': '$items.quantity' }
      },
      maxAccumulatorMemoryUsageBytes: { totalSold: Long('2560') },
      totalOutputDataSizeBytes: Long('4900'),
      usedDisk: false,
      spills: Long('0'),
      spilledDataStorageSize: Long('0'),
      numBytesSpilledEstimate: Long('0'),
      spilledRecords: Long('0'),
      nReturned: Long('20'),
      executionTimeMillisEstimate: Long('66')
    },
    {
      '$sort': { sortKey: { totalSold: -1 }, limit: Long('5') },
      totalDataSizeSortedBytesEstimate: Long('1265'),
      usedDisk: false,
      spills: Long('0'),
      spilledDataStorageSize: Long('0'),
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('66')
    },
    {
      '$lookup': {
        from: 'products',
        as: 'product',
        localField: '_id',
        foreignField: 'product_id',
        unwinding: { preserveNullAndEmptyArrays: false }
      },
      totalDocsExamined: Long('100'),
      totalKeysExamined: Long('0'),
      collectionScans: Long('5'),
      indexesUsed: [],
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('69')
    },
    {
      '$project': { totalSold: true, productName: '$product.name', _id: false },
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('69')
    }
  ],
  queryShapeHash: '4405A614CAD489AF279DE4FB2899F25E7BA29CA5654D56906B927825619365C9',
  serverInfo: {
    host: '21cb7c55198d',
    port: 27017,
    version: '8.0.6',
    gitVersion: '80f21521ad4a3dfd5613f5d649d7058c6d46277f'
  },
  serverParameters: {
    internalQueryFacetBufferSizeBytes: 104857600,
    internalQueryFacetMaxOutputDocSizeBytes: 104857600,
    internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
    internalDocumentSourceGroupMaxMemoryBytes: 104857600,
    internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
    internalQueryProhibitBlockingMergeOnMongoS: 0,
    internalQueryMaxAddToSetBytes: 104857600,
    internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600,
    internalQueryFrameworkControl: 'trySbeRestricted',
    internalQueryPlannerIgnoreIndexWithCollationForRegex: 1
  },
  command: {
    aggregate: 'orders',
    pipeline: [
      {
        '$match': {
          transaction_date: { '$gte': ISODate('2025-03-12T01:19:20.094Z') }
        }
      },
      { '$unwind': '$items' },
      {
        '$group': {
          _id: '$items.product_id',
          totalSold: { '$sum': '$items.quantity' }
        }
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
      {
        '$lookup': {
          from: 'products',
          localField: '_id',
          foreignField: 'product_id',
          as: 'product'
        }
      },
      { '$unwind': '$product' },
      {
        '$project': { _id: 0, productName: '$product.name', totalSold: 1 }
      }
    ],
    cursor: {},
    '$db': 'mydb'
  },
  ok: 1
}
mydb> db.orders.createIndex({ transaction_date: 1 });
...
transaction_date_1
mydb> db.orders.explain("executionStats").aggregate([
...   { $match: { transaction_date: { $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) } } },
...   { $unwind: "$items" },
...   { $group: { _id: "$items.product_id", totalSold: { $sum: "$items.quantity" } } },
...   { $sort: { totalSold: -1 } },
...   { $limit: 5 },
...   { $lookup: {
...       from: "products",
...       localField: "_id",
...       foreignField: "product_id",
...       as: "product"
...   }},
...   { $unwind: "$product" },
...   { $project: { _id: 0, productName: "$product.name", totalSold: 1 } }
... ]);
...
{
  explainVersion: '1',
  stages: [
    {
      '$cursor': {
        queryPlanner: {
          namespace: 'mydb.orders',
          parsedQuery: {
            transaction_date: { '$gte': ISODate('2025-03-12T01:20:00.227Z') }
          },
          indexFilterSet: false,
          queryHash: 'FD0AA76E',
          planCacheShapeHash: 'FD0AA76E',
          planCacheKey: '85C95104',
          optimizationTimeMillis: 0,
          maxIndexedOrSolutionsReached: false,
          maxIndexedAndSolutionsReached: false,
          maxScansToExplodeReached: false,
          prunedSimilarIndexes: false,
          winningPlan: {
            isCached: false,
            stage: 'PROJECTION_SIMPLE',
            transformBy: { items: 1, _id: 0 },
            inputStage: {
              stage: 'FETCH',
              inputStage: {
                stage: 'IXSCAN',
                keyPattern: { transaction_date: 1 },
                indexName: 'transaction_date_1',
                isMultiKey: false,
                multiKeyPaths: { transaction_date: [] },
                isUnique: false,
                isSparse: false,
                isPartial: false,
                indexVersion: 2,
                direction: 'forward',
                indexBounds: {
                  transaction_date: [
                    '[new Date(1741742400227), new Date(9223372036854775807)]'
                  ]
                }
              }
            }
          },
          rejectedPlans: []
        },
        executionStats: {
          executionSuccess: true,
          nReturned: 16535,
          executionTimeMillis: 45,
          totalKeysExamined: 16535,
          totalDocsExamined: 16535,
          executionStages: {
            isCached: false,
            stage: 'PROJECTION_SIMPLE',
            nReturned: 16535,
            executionTimeMillisEstimate: 13,
            works: 16536,
            advanced: 16535,
            needTime: 0,
            needYield: 0,
            saveState: 12,
            restoreState: 12,
            isEOF: 1,
            transformBy: { items: 1, _id: 0 },
            inputStage: {
              stage: 'FETCH',
              nReturned: 16535,
              executionTimeMillisEstimate: 4,
              works: 16536,
              advanced: 16535,
              needTime: 0,
              needYield: 0,
              saveState: 12,
              restoreState: 12,
              isEOF: 1,
              docsExamined: 16535,
              alreadyHasObj: 0,
              inputStage: {
                stage: 'IXSCAN',
                nReturned: 16535,
                executionTimeMillisEstimate: 0,
                works: 16536,
                advanced: 16535,
                needTime: 0,
                needYield: 0,
                saveState: 12,
                restoreState: 12,
                isEOF: 1,
                keyPattern: { transaction_date: 1 },
                indexName: 'transaction_date_1',
                isMultiKey: false,
                multiKeyPaths: { transaction_date: [] },
                isUnique: false,
                isSparse: false,
                isPartial: false,
                indexVersion: 2,
                direction: 'forward',
                indexBounds: {
                  transaction_date: [
                    '[new Date(1741742400227), new Date(9223372036854775807)]'
                  ]
                },
                keysExamined: 16535,
                seeks: 1,
                dupsTested: 0,
                dupsDropped: 0
              }
            }
          }
        }
      },
      nReturned: Long('16535'),
      executionTimeMillisEstimate: Long('32')
    },
    {
      '$unwind': { path: '$items' },
      nReturned: Long('49710'),
      executionTimeMillisEstimate: Long('32')
    },
    {
      '$group': {
        _id: '$items.product_id',
        totalSold: { '$sum': '$items.quantity' }
      },
      maxAccumulatorMemoryUsageBytes: { totalSold: Long('2560') },
      totalOutputDataSizeBytes: Long('4900'),
      usedDisk: false,
      spills: Long('0'),
      spilledDataStorageSize: Long('0'),
      numBytesSpilledEstimate: Long('0'),
      spilledRecords: Long('0'),
      nReturned: Long('20'),
      executionTimeMillisEstimate: Long('45')
    },
    {
      '$sort': { sortKey: { totalSold: -1 }, limit: Long('5') },
      totalDataSizeSortedBytesEstimate: Long('1265'),
      usedDisk: false,
      spills: Long('0'),
      spilledDataStorageSize: Long('0'),
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('45')
    },
    {
      '$lookup': {
        from: 'products',
        as: 'product',
        localField: '_id',
        foreignField: 'product_id',
        unwinding: { preserveNullAndEmptyArrays: false }
      },
      totalDocsExamined: Long('100'),
      totalKeysExamined: Long('0'),
      collectionScans: Long('5'),
      indexesUsed: [],
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('46')
    },
    {
      '$project': { totalSold: true, productName: '$product.name', _id: false },
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('46')
    }
  ],
  queryShapeHash: '4405A614CAD489AF279DE4FB2899F25E7BA29CA5654D56906B927825619365C9',
  serverInfo: {
    host: '21cb7c55198d',
    port: 27017,
    version: '8.0.6',
    gitVersion: '80f21521ad4a3dfd5613f5d649d7058c6d46277f'
  },
  serverParameters: {
    internalQueryFacetBufferSizeBytes: 104857600,
    internalQueryFacetMaxOutputDocSizeBytes: 104857600,
    internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
    internalDocumentSourceGroupMaxMemoryBytes: 104857600,
    internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
    internalQueryProhibitBlockingMergeOnMongoS: 0,
    internalQueryMaxAddToSetBytes: 104857600,
    internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600,
    internalQueryFrameworkControl: 'trySbeRestricted',
    internalQueryPlannerIgnoreIndexWithCollationForRegex: 1
  },
  command: {
    aggregate: 'orders',
    pipeline: [
      {
        '$match': {
          transaction_date: { '$gte': ISODate('2025-03-12T01:20:00.227Z') }
        }
      },
      { '$unwind': '$items' },
      {
        '$group': {
          _id: '$items.product_id',
          totalSold: { '$sum': '$items.quantity' }
        }
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
      {
        '$lookup': {
          from: 'products',
          localField: '_id',
          foreignField: 'product_id',
          as: 'product'
        }
      },
      { '$unwind': '$product' },
      {
        '$project': { _id: 0, productName: '$product.name', totalSold: 1 }
      }
    ],
    cursor: {},
    '$db': 'mydb'
  },
  ok: 1
}
mydb> db.products.createIndex({ product_id: 1 })
...
product_id_1
mydb> db.orders.explain("executionStats").aggregate([
...   { $match: { transaction_date: { $gte: new Date(Date.now() - 30 * 24 * 60 * 60 *
 1000) } } },
...   { $unwind: "$items" },
...   { $group: { _id: "$items.product_id", totalSold: { $sum: "$items.quantity" } } },
...   { $sort: { totalSold: -1 } },
...   { $limit: 5 },
...   { $lookup: {
...       from: "products",
...       localField: "_id",
...       foreignField: "product_id",
...       as: "product"
...   }},
...   { $unwind: "$product" },
...   { $project: { _id: 0, productName: "$product.name", totalSold: 1 } }
... ]);
...
{
  explainVersion: '1',
  stages: [
    {
      '$cursor': {
        queryPlanner: {
          namespace: 'mydb.orders',
          parsedQuery: {
            transaction_date: { '$gte': ISODate('2025-03-12T01:22:22.056Z') }        
          },
          indexFilterSet: false,
          queryHash: 'FD0AA76E',
          planCacheShapeHash: 'FD0AA76E',
          planCacheKey: '85C95104',
          optimizationTimeMillis: 0,
          maxIndexedOrSolutionsReached: false,
          maxIndexedAndSolutionsReached: false,
          maxScansToExplodeReached: false,
          prunedSimilarIndexes: false,
          winningPlan: {
            isCached: false,
            stage: 'PROJECTION_SIMPLE',
            transformBy: { items: 1, _id: 0 },
            inputStage: {
              stage: 'FETCH',
              inputStage: {
                stage: 'IXSCAN',
                keyPattern: { transaction_date: 1 },
                indexName: 'transaction_date_1',
                isMultiKey: false,
                multiKeyPaths: { transaction_date: [] },
                isUnique: false,
                isSparse: false,
                isPartial: false,
                indexVersion: 2,
                direction: 'forward',
                indexBounds: {
                  transaction_date: [
                    '[new Date(1741742542056), new Date(9223372036854775807)]'       
                  ]
                }
              }
            }
          },
          rejectedPlans: []
        },
        executionStats: {
          executionSuccess: true,
          nReturned: 16535,
          executionTimeMillis: 64,
          totalKeysExamined: 16535,
          totalDocsExamined: 16535,
          executionStages: {
            isCached: false,
            stage: 'PROJECTION_SIMPLE',
            nReturned: 16535,
            executionTimeMillisEstimate: 36,
            works: 16536,
            advanced: 16535,
            needTime: 0,
            needYield: 0,
            saveState: 13,
            restoreState: 13,
            isEOF: 1,
            transformBy: { items: 1, _id: 0 },
            inputStage: {
              stage: 'FETCH',
              nReturned: 16535,
              executionTimeMillisEstimate: 26,
              works: 16536,
              advanced: 16535,
              needTime: 0,
              needYield: 0,
              saveState: 13,
              restoreState: 13,
              isEOF: 1,
              docsExamined: 16535,
              alreadyHasObj: 0,
              inputStage: {
                stage: 'IXSCAN',
                nReturned: 16535,
                executionTimeMillisEstimate: 0,
                works: 16536,
                advanced: 16535,
                needTime: 0,
                needYield: 0,
                saveState: 13,
                restoreState: 13,
                isEOF: 1,
                keyPattern: { transaction_date: 1 },
                indexName: 'transaction_date_1',
                isMultiKey: false,
                multiKeyPaths: { transaction_date: [] },
                isUnique: false,
                isSparse: false,
                isPartial: false,
                indexVersion: 2,
                direction: 'forward',
                indexBounds: {
                  transaction_date: [
                    '[new Date(1741742542056), new Date(9223372036854775807)]'       
                  ]
                },
                keysExamined: 16535,
                seeks: 1,
                dupsTested: 0,
                dupsDropped: 0
              }
            }
          }
        }
      },
      nReturned: Long('16535'),
      executionTimeMillisEstimate: Long('60')
    },
    {
      '$unwind': { path: '$items' },
      nReturned: Long('49710'),
      executionTimeMillisEstimate: Long('62')
    },
    {
      '$group': {
        _id: '$items.product_id',
        totalSold: { '$sum': '$items.quantity' }
      },
      maxAccumulatorMemoryUsageBytes: { totalSold: Long('2560') },
      totalOutputDataSizeBytes: Long('4900'),
      usedDisk: false,
      spills: Long('0'),
      spilledDataStorageSize: Long('0'),
      numBytesSpilledEstimate: Long('0'),
      spilledRecords: Long('0'),
      nReturned: Long('20'),
      executionTimeMillisEstimate: Long('62')
    },
    {
      '$sort': { sortKey: { totalSold: -1 }, limit: Long('5') },
      totalDataSizeSortedBytesEstimate: Long('1265'),
      usedDisk: false,
      spills: Long('0'),
      spilledDataStorageSize: Long('0'),
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('62')
    },
    {
      '$lookup': {
        from: 'products',
        as: 'product',
        localField: '_id',
        foreignField: 'product_id',
        unwinding: { preserveNullAndEmptyArrays: false }
      },
      totalDocsExamined: Long('5'),
      totalKeysExamined: Long('5'),
      collectionScans: Long('0'),
      indexesUsed: [ 'product_id_1' ],
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('64')
    },
    {
      '$project': { totalSold: true, productName: '$product.name', _id: false },     
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('64')
    }
  ],
  queryShapeHash: '4405A614CAD489AF279DE4FB2899F25E7BA29CA5654D56906B927825619365C9',
  serverInfo: {
    host: '21cb7c55198d',
    port: 27017,
    version: '8.0.6',
    gitVersion: '80f21521ad4a3dfd5613f5d649d7058c6d46277f'
  },
  serverParameters: {
    internalQueryFacetBufferSizeBytes: 104857600,
    internalQueryFacetMaxOutputDocSizeBytes: 104857600,
    internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
    internalDocumentSourceGroupMaxMemoryBytes: 104857600,
    internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
    internalQueryProhibitBlockingMergeOnMongoS: 0,
    internalQueryMaxAddToSetBytes: 104857600,
    internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600,
    internalQueryFrameworkControl: 'trySbeRestricted',
    internalQueryPlannerIgnoreIndexWithCollationForRegex: 1
  },
  command: {
    aggregate: 'orders',
    pipeline: [
      {
        '$match': {
          transaction_date: { '$gte': ISODate('2025-03-12T01:22:22.056Z') }
        }
      },
      { '$unwind': '$items' },
      {
        '$group': {
          _id: '$items.product_id',
          totalSold: { '$sum': '$items.quantity' }
        }
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
      {
        '$match': {
          transaction_date: { '$gte': ISODate('2025-03-12T01:22:22.056Z') }
        }
      },
      { '$unwind': '$items' },
      {
        '$group': {
          _id: '$items.product_id',
          totalSold: { '$sum': '$items.quantity' }
        }
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
          transaction_date: { '$gte': ISODate('2025-03-12T01:22:22.056Z') }
        }
      },
      { '$unwind': '$items' },
      {
        '$group': {
          _id: '$items.product_id',
          totalSold: { '$sum': '$items.quantity' }
        }
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
        }
      },
      { '$unwind': '$items' },
      {
        '$group': {
          _id: '$items.product_id',
          totalSold: { '$sum': '$items.quantity' }
        }
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
      },
      { '$unwind': '$items' },
      {
        '$group': {
          _id: '$items.product_id',
          totalSold: { '$sum': '$items.quantity' }
        }
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
      {
        '$group': {
          _id: '$items.product_id',
          totalSold: { '$sum': '$items.quantity' }
        }
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
        '$group': {
          _id: '$items.product_id',
          totalSold: { '$sum': '$items.quantity' }
        }
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
      {
        '$lookup': {
          totalSold: { '$sum': '$items.quantity' }
        }
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
      {
        '$lookup': {
          from: 'products',
          localField: '_id',
      },
      { '$sort': { totalSold: -1 } },
      { '$limit': 5 },
      {
        '$lookup': {
          from: 'products',
          localField: '_id',
          foreignField: 'product_id',
          as: 'product'
      {
        '$lookup': {
          from: 'products',
          localField: '_id',
          foreignField: 'product_id',
          as: 'product'
          from: 'products',
          localField: '_id',
          foreignField: 'product_id',
          as: 'product'
        }
      },
      { '$unwind': '$product' },
          foreignField: 'product_id',
          as: 'product'
        }
      },
      { '$unwind': '$product' },
      {
        }
      },
      { '$unwind': '$product' },
      {
      },
      { '$unwind': '$product' },
      {
        '$project': { _id: 0, productName: '$product.name', totalSold: 1 }
      {
        '$project': { _id: 0, productName: '$product.name', totalSold: 1 }
      }
        '$project': { _id: 0, productName: '$product.name', totalSold: 1 }
      }
      }
    ],
    cursor: {},
    '$db': 'mydb'
  },
  ok: 1
}
mydb>