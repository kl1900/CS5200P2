mydb> db.orders.explain("executionStats").aggregate([
...   {
...     $match: {
...       transaction_date: {
...         $gte: new Date(new Date().setHours(0, 0, 0, 0) - 7 * 24 * 60 * 60 * 1000),
...         $lt: new Date(new Date().setHours(0, 0, 0, 0))
...       }
...     }
...   },
...   {
...     $group: {
...       _id: { $dateToString: { format: "%Y-%m-%d", date: "$transaction_date" } },
...       count: { $sum: 1 }
...     }
...   },
...   {
...     $sort: { _id: 1 }
...   }
... ])
...
{
  explainVersion: '2',
  stages: [
    {
      '$cursor': {
        queryPlanner: {
          namespace: 'mydb.orders',
          parsedQuery: {
            '$and': [
              {
                transaction_date: { '$lt': ISODate('2025-04-11T00:00:00.000Z') }     
              },
              {
                transaction_date: { '$gte': ISODate('2025-04-04T00:00:00.000Z') }    
              }
            ]
          },
          indexFilterSet: false,
          queryHash: '418D6041',
          planCacheShapeHash: '418D6041',
          planCacheKey: '0C6ABC35',
          optimizationTimeMillis: 0,
          maxIndexedOrSolutionsReached: false,
          maxIndexedAndSolutionsReached: false,
          maxScansToExplodeReached: false,
          prunedSimilarIndexes: false,
          winningPlan: {
            isCached: false,
            queryPlan: {
              stage: 'GROUP',
              planNodeId: 3,
              inputStage: {
                stage: 'COLLSCAN',
                planNodeId: 1,
                filter: {
                  '$and': [
                    {
                      transaction_date: { '$lt': ISODate('2025-04-11T00:00:00.000Z') }
                    },
                    {
                      transaction_date: { '$gte': ISODate('2025-04-04T00:00:00.000Z') }
                    }
                  ]
                },
                direction: 'forward'
              }
            },
            slotBasedPlan: {
              slots: '$$RESULT=s11 env: { s4 = 1744329600000, s5 = 1743724800000, s6 = TimeZoneDatabase(Europe/Helsinki...Europe/Tirane) (timeZoneDB) }',
              stages: '[3] project [s11 = newObj("_id", s8, "count", s10)] \n' +     
                '[3] project [s10 = (convert ( s9, int32) ?: s9)] \n' +
                '[3] group [s8] [s9 = count()] spillSlots[s7] mergingExprs[sum(s7)] \n' +
                '[3] project [s8 = (\n' +
                '    let [\n' +
                '        l9.0 = dateToString(s6, s1, "%Y-%m-%d", "UTC") \n' +        
                '    ] \n' +
                '    in \n' +
                '        if exists(l9.0) \n' +
                '        then makeOwn(move(l9.0)) \n' +
                '        else \n' +
                '            if (typeMatch(s1, 1088) ?: true) \n' +
                '            then null \n' +
                '            else \n' +
                '                if typeMatch(s1, 131712) \n' +
                '                then Nothing \n' +
                `                else fail(4997901, "$dateToString parameter 'date' must be coercible to date") \n` +
                '?: null)] \n' +
                '[1] filter {(traverseF(s1, lambda(l3.0) { ((move(l3.0) < s4) ?: false) }, false) && traverseF(s1, lambda(l4.0) { ((move(l4.0) >= s5) ?: false) }, false))} \n' +
                '[1] scan s2 s3 none none none none none none lowPriority [s1 = transaction_date] @"aa563a01-2b5a-43a4-b9fa-fc2e88fa10d5" true false '
            }
          },
          rejectedPlans: []
        },
        executionStats: {
          executionSuccess: true,
          nReturned: 7,
          executionTimeMillis: 41,
          totalKeysExamined: 0,
          totalDocsExamined: 100000,
          executionStages: {
            stage: 'project',
            planNodeId: 3,
            nReturned: 7,
            executionTimeMillisEstimate: 39,
            opens: 1,
            closes: 1,
            saveState: 3,
            restoreState: 3,
            isEOF: 1,
            projections: { '11': 'newObj("_id", s8, "count", s10) ' },
            inputStage: {
              stage: 'project',
              planNodeId: 3,
              nReturned: 7,
              executionTimeMillisEstimate: 39,
              opens: 1,
              closes: 1,
              saveState: 3,
              restoreState: 3,
              isEOF: 1,
              projections: { '10': '(convert ( s9, int32) ?: s9) ' },
              inputStage: {
                stage: 'group',
                planNodeId: 3,
                nReturned: 7,
                executionTimeMillisEstimate: 39,
                opens: 1,
                closes: 1,
                saveState: 3,
                restoreState: 3,
                isEOF: 1,
                groupBySlots: [ Long('8') ],
                expressions: { '9': 'count() ', initExprs: { '9': null } },
                mergingExprs: { '7': 'sum(s7) ' },
                usedDisk: false,
                spills: 0,
                spilledBytes: 0,
                spilledRecords: 0,
                spilledDataStorageSize: 0,
                inputStage: {
                  stage: 'project',
                  planNodeId: 3,
                  nReturned: 3840,
                  executionTimeMillisEstimate: 39,
                  opens: 1,
                  closes: 1,
                  saveState: 3,
                  restoreState: 3,
                  isEOF: 1,
                  projections: {
                    '8': '(\n' +
                      '    let [\n' +
                      '        l9.0 = dateToString(s6, s1, "%Y-%m-%d", "UTC") \n' +  
                      '    ] \n' +
                      '    in \n' +
                      '        if exists(l9.0) \n' +
                      '        then makeOwn(move(l9.0)) \n' +
                      '        else \n' +
                      '            if (typeMatch(s1, 1088) ?: true) \n' +
                      '            then null \n' +
                      '            else \n' +
                      '                if typeMatch(s1, 131712) \n' +
                      '                then Nothing \n' +
                      `                else fail(4997901, "$dateToString parameter 'date' must be coercible to date") \n` +
                      '?: null) '
                  },
                  inputStage: {
                    stage: 'filter',
                    planNodeId: 1,
                    nReturned: 3840,
                    executionTimeMillisEstimate: 39,
                    opens: 1,
                    closes: 1,
                    saveState: 3,
                    restoreState: 3,
                    isEOF: 1,
                    numTested: 100000,
                    filter: '(traverseF(s1, lambda(l3.0) { ((move(l3.0) < s4) ?: false) }, false) && traverseF(s1, lambda(l4.0) { ((move(l4.0) >= s5) ?: false) }, false)) ',
                    inputStage: {
                      stage: 'scan',
                      planNodeId: 1,
                      nReturned: 100000,
                      executionTimeMillisEstimate: 37,
                      opens: 1,
                      closes: 1,
                      saveState: 3,
                      restoreState: 3,
                      isEOF: 1,
                      numReads: 100000,
                      recordSlot: 2,
                      recordIdSlot: 3,
                      scanFieldNames: [ 'transaction_date' ],
                      scanFieldSlots: [ Long('1') ]
                    }
                  }
                }
              }
            }
          }
        }
      },
      nReturned: Long('7'),
      executionTimeMillisEstimate: Long('40')
    },
    {
      '$sort': { sortKey: { _id: 1 } },
      totalDataSizeSortedBytesEstimate: Long('1771'),
      usedDisk: false,
      spills: Long('0'),
      spilledDataStorageSize: Long('0'),
      nReturned: Long('7'),
      executionTimeMillisEstimate: Long('40')
    }
  ],
  queryShapeHash: '00A7A978C40FC8E5ECF14D2262ADDFB59555FBCE217E1E52AFFC82DFE141E86B',
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
          transaction_date: {
            '$gte': ISODate('2025-04-04T00:00:00.000Z'),
            '$lt': ISODate('2025-04-11T00:00:00.000Z')
          }
        }
      },
      {
        '$group': {
          _id: {
            '$dateToString': { format: '%Y-%m-%d', date: '$transaction_date' }       
          },
          count: { '$sum': 1 }
        }
      },
      { '$sort': { _id: 1 } }
    ],
    cursor: {},
    '$db': 'mydb'
  },
  ok: 1
}
mydb> db.orders.createIndex({ transaction_date: 1 })
...
transaction_date_1
mydb> db.orders.explain("executionStats").aggregate([
...   {
...     $match: {
...       transaction_date: {
...         $gte: new Date(new Date().setHours(0, 0, 0, 0) - 7 * 24 * 60 * 60 * 1000),
...         $lt: new Date(new Date().setHours(0, 0, 0, 0))
...       }
...     }
...   },
...   {
...     $group: {
...       _id: { $dateToString: { format: "%Y-%m-%d", date: "$transaction_date" } },
...       count: { $sum: 1 }
...     }
...   },
...   {
...     $sort: { _id: 1 }
...   }
... ])
...
{
  explainVersion: '2',
  stages: [
    {
      '$cursor': {
        queryPlanner: {
          namespace: 'mydb.orders',
          parsedQuery: {
            '$and': [
              {
                transaction_date: { '$lt': ISODate('2025-04-11T00:00:00.000Z') }     
              },
              {
                transaction_date: { '$gte': ISODate('2025-04-04T00:00:00.000Z') }    
              }
            ]
          },
          indexFilterSet: false,
          queryHash: '418D6041',
          planCacheShapeHash: '418D6041',
          planCacheKey: 'D04735ED',
          optimizationTimeMillis: 0,
          maxIndexedOrSolutionsReached: false,
          maxIndexedAndSolutionsReached: false,
          maxScansToExplodeReached: false,
          prunedSimilarIndexes: false,
          winningPlan: {
            isCached: false,
            queryPlan: {
              stage: 'GROUP',
              planNodeId: 3,
              inputStage: {
                stage: 'PROJECTION_COVERED',
                planNodeId: 2,
                transformBy: { transaction_date: true, _id: false },
                inputStage: {
                  stage: 'IXSCAN',
                  planNodeId: 1,
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
                      '[new Date(1743724800000), new Date(1744329600000))'
                    ]
                  }
                }
              }
            },
            slotBasedPlan: {
              slots: '$$RESULT=s10 env: { s2 = KS(7880000195FE18E8000104), s3 = KS(788000019622256C000104), s5 = TimeZoneDatabase(Europe/Helsinki...Europe/Tirane) (timeZoneDB) }',
              stages: '[3] project [s10 = newObj("_id", s7, "count", s9)] \n' +      
                '[3] project [s9 = (convert ( s8, int32) ?: s8)] \n' +
                '[3] group [s7] [s8 = count()] spillSlots[s6] mergingExprs[sum(s6)] \n' +
                '[3] project [s7 = (\n' +
                '    let [\n' +
                '        l5.0 = dateToString(s5, s1, "%Y-%m-%d", "UTC") \n' +        
                '    ] \n' +
                '    in \n' +
                '        if exists(l5.0) \n' +
                '        then makeOwn(move(l5.0)) \n' +
                '        else \n' +
                '            if (typeMatch(s1, 1088) ?: true) \n' +
                '            then null \n' +
                '            else \n' +
                '                if typeMatch(s1, 131712) \n' +
                '                then Nothing \n' +
                `                else fail(4997901, "$dateToString parameter 'date' must be coercible to date") \n` +
                '?: null)] \n' +
                '[1] cfilter {(exists(s2) && exists(s3))} \n' +
                '[1] ixseek s2 s3 none s4 none none [s1 = 0] @"aa563a01-2b5a-43a4-b9fa-fc2e88fa10d5" @"transaction_date_1" true '
            }
          },
          rejectedPlans: []
        },
        executionStats: {
          executionSuccess: true,
          nReturned: 7,
          executionTimeMillis: 3,
          totalKeysExamined: 3840,
          totalDocsExamined: 0,
          executionStages: {
            stage: 'project',
            planNodeId: 3,
            nReturned: 7,
            executionTimeMillisEstimate: 0,
            opens: 1,
            closes: 1,
            saveState: 1,
            restoreState: 1,
            isEOF: 1,
            projections: { '10': 'newObj("_id", s7, "count", s9) ' },
            inputStage: {
              stage: 'project',
              planNodeId: 3,
              nReturned: 7,
              executionTimeMillisEstimate: 0,
              opens: 1,
              closes: 1,
              saveState: 1,
              restoreState: 1,
              isEOF: 1,
              projections: { '9': '(convert ( s8, int32) ?: s8) ' },
              inputStage: {
                stage: 'group',
                planNodeId: 3,
                nReturned: 7,
                executionTimeMillisEstimate: 0,
                opens: 1,
                closes: 1,
                saveState: 1,
                restoreState: 1,
                isEOF: 1,
                groupBySlots: [ Long('7') ],
                expressions: { '8': 'count() ', initExprs: { '8': null } },
                mergingExprs: { '6': 'sum(s6) ' },
                usedDisk: false,
                spills: 0,
                spilledBytes: 0,
                spilledRecords: 0,
                spilledDataStorageSize: 0,
                inputStage: {
                  stage: 'project',
                  planNodeId: 3,
                  nReturned: 3840,
                  executionTimeMillisEstimate: 0,
                  opens: 1,
                  closes: 1,
                  saveState: 1,
                  restoreState: 1,
                  isEOF: 1,
                  projections: {
                    '7': '(\n' +
                      '    let [\n' +
                      '        l5.0 = dateToString(s5, s1, "%Y-%m-%d", "UTC") \n' +  
                      '    ] \n' +
                      '    in \n' +
                      '        if exists(l5.0) \n' +
                      '        then makeOwn(move(l5.0)) \n' +
                      '        else \n' +
                      '            if (typeMatch(s1, 1088) ?: true) \n' +
                      '            then null \n' +
                      '            else \n' +
                      '                if typeMatch(s1, 131712) \n' +
                      '                then Nothing \n' +
                      `                else fail(4997901, "$dateToString parameter 'date' must be coercible to date") \n` +
                      '?: null) '
                  },
                  inputStage: {
                    stage: 'cfilter',
                    planNodeId: 1,
                    nReturned: 3840,
                    executionTimeMillisEstimate: 0,
                    opens: 1,
                    closes: 1,
                    saveState: 1,
                    restoreState: 1,
                    isEOF: 1,
                    numTested: 1,
                    filter: '(exists(s2) && exists(s3)) ',
                    inputStage: {
                      stage: 'ixseek',
                      planNodeId: 1,
                      nReturned: 3840,
                      executionTimeMillisEstimate: 0,
                      opens: 1,
                      closes: 1,
                      saveState: 1,
                      restoreState: 1,
                      isEOF: 1,
                      indexName: 'transaction_date_1',
                      keysExamined: 3840,
                      seeks: 1,
                      numReads: 3841,
                      recordIdSlot: 4,
                      outputSlots: [ Long('1') ],
                      indexKeysToInclude: '00000000000000000000000000000001',        
                      seekKeyLow: 's2 ',
                      seekKeyHigh: 's3 '
                    }
                  }
                }
              }
            }
          }
        }
      },
      nReturned: Long('7'),
      executionTimeMillisEstimate: Long('1')
    },
    {
      '$sort': { sortKey: { _id: 1 } },
      totalDataSizeSortedBytesEstimate: Long('1771'),
      usedDisk: false,
      spills: Long('0'),
      spilledDataStorageSize: Long('0'),
      nReturned: Long('7'),
      executionTimeMillisEstimate: Long('1')
    }
  ],
  queryShapeHash: '00A7A978C40FC8E5ECF14D2262ADDFB59555FBCE217E1E52AFFC82DFE141E86B',
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
          transaction_date: {
            '$gte': ISODate('2025-04-04T00:00:00.000Z'),
            '$lt': ISODate('2025-04-11T00:00:00.000Z')
          }
        }
      },
      {
        '$group': {
          _id: {
            '$dateToString': { format: '%Y-%m-%d', date: '$transaction_date' }       
          },
          count: { '$sum': 1 }
        }
      },
      { '$sort': { _id: 1 } }
    ],
    cursor: {},
    '$db': 'mydb'
  },
  ok: 1
}
mydb>