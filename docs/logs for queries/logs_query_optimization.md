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
            transaction_date: { '$gte': ISODate('2025-03-12T01:14:19.300Z') }
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
                    '[new Date(1741742059300), new Date(9223372036854775807)]'
                  ]
                }
              }
            }
          },
          rejectedPlans: []
        },
        executionStats: {
          executionSuccess: true,
          nReturned: 16500,
          executionTimeMillis: 50,
          totalKeysExamined: 16500,
          totalDocsExamined: 16500,
          executionStages: {
            isCached: false,
            stage: 'PROJECTION_SIMPLE',
            nReturned: 16500,
            executionTimeMillisEstimate: 10,
            works: 16501,
            advanced: 16500,
            needTime: 0,
            needYield: 0,
            saveState: 11,
            restoreState: 11,
            isEOF: 1,
            transformBy: { items: 1, _id: 0 },
            inputStage: {
              stage: 'FETCH',
              nReturned: 16500,
              executionTimeMillisEstimate: 10,
              works: 16501,
              advanced: 16500,
              needTime: 0,
              needYield: 0,
              saveState: 11,
              restoreState: 11,
              isEOF: 1,
              docsExamined: 16500,
              alreadyHasObj: 0,
              inputStage: {
                stage: 'IXSCAN',
                nReturned: 16500,
                executionTimeMillisEstimate: 0,
                works: 16501,
                advanced: 16500,
                needTime: 0,
                needYield: 0,
                saveState: 11,
                restoreState: 11,
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
                    '[new Date(1741742059300), new Date(9223372036854775807)]'
                  ]
                },
                keysExamined: 16500,
                seeks: 1,
                dupsTested: 0,
                dupsDropped: 0
              }
            }
          }
        }
      },
      nReturned: Long('16500'),
      executionTimeMillisEstimate: Long('49')
    },
    {
      '$unwind': { path: '$items' },
      nReturned: Long('49640'),
      executionTimeMillisEstimate: Long('50')
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
      executionTimeMillisEstimate: Long('50')
    },
    {
      '$sort': { sortKey: { totalSold: -1 }, limit: Long('5') },
      totalDataSizeSortedBytesEstimate: Long('1265'),
      usedDisk: false,
      spills: Long('0'),
      spilledDataStorageSize: Long('0'),
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('50')
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
      executionTimeMillisEstimate: Long('51')
    },
    {
      '$project': { totalSold: true, productName: '$product.name', _id: false },
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('51')
    }
  ],
  queryShapeHash: '4405A614CAD489AF279DE4FB2899F25E7BA29CA5654D56906B927825619365C9',
  serverInfo: {
    host: '3980364fffa8',
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
          transaction_date: { '$gte': ISODate('2025-03-12T01:14:19.300Z') }
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
            transaction_date: { '$gte': ISODate('2025-03-12T01:14:54.061Z') }
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
                    '[new Date(1741742094061), new Date(9223372036854775807)]'
                  ]
                }
              }
            }
          },
          rejectedPlans: []
        },
        executionStats: {
          executionSuccess: true,
          nReturned: 16500,
          executionTimeMillis: 46,
          totalKeysExamined: 16500,
          totalDocsExamined: 16500,
          executionStages: {
            isCached: false,
            stage: 'PROJECTION_SIMPLE',
            nReturned: 16500,
            executionTimeMillisEstimate: 9,
            works: 16501,
            advanced: 16500,
            needTime: 0,
            needYield: 0,
            saveState: 12,
            restoreState: 12,
            isEOF: 1,
            transformBy: { items: 1, _id: 0 },
            inputStage: {
              stage: 'FETCH',
              nReturned: 16500,
              executionTimeMillisEstimate: 9,
              works: 16501,
              advanced: 16500,
              needTime: 0,
              needYield: 0,
              saveState: 12,
              restoreState: 12,
              isEOF: 1,
              docsExamined: 16500,
              alreadyHasObj: 0,
              inputStage: {
                stage: 'IXSCAN',
                nReturned: 16500,
                executionTimeMillisEstimate: 6,
                works: 16501,
                advanced: 16500,
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
                    '[new Date(1741742094061), new Date(9223372036854775807)]'
                  ]
                },
                keysExamined: 16500,
                seeks: 1,
                dupsTested: 0,
                dupsDropped: 0
              }
            }
          }
        }
      },
      nReturned: Long('16500'),
      executionTimeMillisEstimate: Long('29')
    },
    {
      '$unwind': { path: '$items' },
      nReturned: Long('49640'),
      executionTimeMillisEstimate: Long('46')
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
      executionTimeMillisEstimate: Long('46')
    },
    {
      '$sort': { sortKey: { totalSold: -1 }, limit: Long('5') },
      totalDataSizeSortedBytesEstimate: Long('1265'),
      usedDisk: false,
      spills: Long('0'),
      spilledDataStorageSize: Long('0'),
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('46')
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
      executionTimeMillisEstimate: Long('47')
    },
    {
      '$project': { totalSold: true, productName: '$product.name', _id: false },
      nReturned: Long('5'),
      executionTimeMillisEstimate: Long('47')
    }
  ],
  queryShapeHash: '4405A614CAD489AF279DE4FB2899F25E7BA29CA5654D56906B927825619365C9',
  serverInfo: {
    host: '3980364fffa8',
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
          transaction_date: { '$gte': ISODate('2025-03-12T01:14:54.061Z') }
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
mydb>