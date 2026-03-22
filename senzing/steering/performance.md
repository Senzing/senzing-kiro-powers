# Senzing — Performance Guide

This guide covers performance tuning, database selection, and optimization strategies.

## Database Backend Selection

| Database | Record Capacity | Use Case | Performance Notes |
| --- | --- | --- | --- |
| SQLite | < 100K records | Evaluation, POC, demos | Single-threaded, file-based, no tuning needed |
| PostgreSQL | 100K - 100M+ records | Production, multi-user | Requires tuning, supports clustering, best overall performance |
| MS SQL Server | 100K - 100M+ records | Windows environments | Good performance with proper indexing |

## Loading Performance

### Expected Throughput

- **Small datasets** (< 10K records): 100-500 records/second (single-threaded)
- **Medium datasets** (10K - 1M records): 500-2000 records/second (multi-threaded)
- **Large datasets** (> 1M records): 2000-5000+ records/second (optimized, multi-threaded)

### Optimization Tips

1. **Use batch loading**: Load 1000+ records per transaction
2. **Disable redo during initial load**: Re-enable after loading completes
3. **Use multiple loader threads**: 4-8 threads typical for balanced systems
4. **Tune database connection pools**: Match thread count
5. **Optimize database configuration**: Use `search_docs` with category `database` for tuning guides
6. **Use SSD storage**: Significantly faster than HDD
7. **Allocate sufficient memory**: 8GB+ recommended for production
8. **Monitor system resources**: CPU, memory, disk I/O

### Loading Strategy for Large Datasets

```
1. Prepare environment
   ├─ Tune database (shared_buffers, work_mem, etc.)
   ├─ Disable redo processing
   └─ Set up monitoring

2. Initial load
   ├─ Use multiple threads (4-8)
   ├─ Load in batches (1000-5000 records)
   └─ Monitor throughput

3. Post-load processing
   ├─ Re-enable redo processing
   ├─ Process accumulated redo records
   └─ Verify entity counts

4. Optimize database
   ├─ Run VACUUM ANALYZE (PostgreSQL)
   ├─ Update statistics
   └─ Check index health
```

## Query Performance

### Expected Response Times

- **Entity lookup by ID**: < 10ms
- **Search by name/attributes**: 50-500ms (depends on data size and search criteria)
- **Why analysis**: 100-1000ms (depends on entity complexity)
- **Network analysis**: Seconds to minutes (depends on network size)

### Query Optimization

1. **Use specific search criteria**: More attributes = faster, more accurate results
2. **Limit result sets**: Use appropriate flags to control output size
3. **Cache frequently accessed entities**: Implement application-level caching
4. **Use appropriate search methods**:
   - `get_entity_by_record_id`: Fastest (direct lookup)
   - `search_by_attributes`: Moderate (indexed search)
   - Network traversal: Slowest (graph analysis)

## Timing Expectations

| Operation | Typical Duration |
| --- | --- |
| `mapping_workflow` (new dataset) | 2-5 minutes (interactive) |
| `lint_record` (1000 records) | 1-2 seconds |
| `analyze_record` (1000 records) | 2-5 seconds |
| `generate_scaffold` | < 1 second |
| SDK initialization | 1-3 seconds |
| Loading 10K records (SQLite) | 30-60 seconds |
| Loading 10K records (PostgreSQL) | 10-20 seconds |
| Loading 1M records (PostgreSQL, optimized) | 10-30 minutes |

## PostgreSQL Tuning

### Essential Configuration Parameters

```ini
# Memory settings
shared_buffers = 4GB              # 25% of system RAM
effective_cache_size = 12GB       # 75% of system RAM
work_mem = 64MB                   # Per operation
maintenance_work_mem = 1GB        # For VACUUM, CREATE INDEX

# Checkpoint settings
checkpoint_completion_target = 0.9
wal_buffers = 16MB
max_wal_size = 4GB

# Query planner
random_page_cost = 1.1            # For SSD storage
effective_io_concurrency = 200    # For SSD storage

# Connection settings
max_connections = 100
```

### Index Maintenance

```sql
-- Rebuild indexes periodically
REINDEX DATABASE senzing;

-- Update statistics
ANALYZE;

-- Reclaim space
VACUUM FULL;
```

## Monitoring Metrics

### Key Performance Indicators

1. **Loading metrics**:
   - Records loaded per second
   - Total records loaded
   - Error rate
   - Thread utilization

2. **Database metrics**:
   - Database size
   - Table sizes
   - Index sizes
   - Connection count
   - Query execution times

3. **System metrics**:
   - CPU utilization
   - Memory usage
   - Disk I/O
   - Network throughput

4. **Entity metrics**:
   - Total entity count
   - Entities per data source
   - Average records per entity
   - Match distribution

### Monitoring Tools

- **Database**: pgAdmin, pg_stat_statements (PostgreSQL)
- **System**: top, htop, iostat, vmstat
- **Application**: Custom logging, metrics exporters
- **Senzing**: Built-in statistics via SDK methods

## Scaling Strategies

### Vertical Scaling (Scale Up)

- Add more CPU cores
- Increase RAM
- Use faster storage (NVMe SSD)
- Optimize database configuration

**Good for**: Up to 50M records, single-server deployments

### Horizontal Scaling (Scale Out)

- Multiple loader instances
- Database replication (read replicas)
- Load balancing
- Distributed processing

**Good for**: > 50M records, high-availability requirements

### Partitioning

For very large datasets (> 100M records):
- Partition by data source
- Partition by date ranges
- Use table inheritance (PostgreSQL)

**Consult Senzing support** for architecture guidance on large-scale deployments.

## Performance Testing

### Baseline Testing

1. **Small batch test** (100 records):
   - Verify configuration
   - Check for errors
   - Measure baseline throughput

2. **Medium batch test** (10K records):
   - Test multi-threading
   - Monitor resource usage
   - Identify bottlenecks

3. **Large batch test** (100K+ records):
   - Measure sustained throughput
   - Test database performance
   - Validate scaling assumptions

### Load Testing

```python
# Example load test structure
import time

start_time = time.time()
records_loaded = 0
batch_size = 1000

for batch in data_batches:
    load_batch(batch)
    records_loaded += len(batch)
    
    # Calculate throughput
    elapsed = time.time() - start_time
    throughput = records_loaded / elapsed
    print(f"Throughput: {throughput:.2f} records/sec")
```

### Stress Testing

- Test with maximum thread count
- Test with maximum data volume
- Test with complex entity networks
- Test with concurrent queries during loading

## Troubleshooting Performance Issues

| Symptom | Likely Cause | Solution |
| --- | --- | --- |
| Slow loading | Database not tuned | Tune PostgreSQL parameters |
| High CPU usage | Too many threads | Reduce thread count |
| High memory usage | Large work_mem | Reduce work_mem setting |
| Slow queries | Missing indexes | Check index health, rebuild if needed |
| Disk I/O bottleneck | Slow storage | Use SSD, optimize checkpoint settings |
| Connection errors | Too many connections | Increase max_connections, use connection pooling |

Use `search_docs` with category "performance" for detailed troubleshooting guides.
