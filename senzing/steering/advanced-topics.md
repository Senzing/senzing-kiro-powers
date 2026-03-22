# Senzing — Advanced Topics

This guide covers advanced Senzing concepts and techniques for experienced users.

## Table of Contents

- [Custom Configuration Tuning](#custom-configuration-tuning)
- [Advanced Matching Rules](#advanced-matching-rules)
- [Custom Entity Types](#custom-entity-types)
- [Network Analysis Techniques](#network-analysis-techniques)
- [Graph Traversal Patterns](#graph-traversal-patterns)
- [Advanced Export Patterns](#advanced-export-patterns)
- [Performance Optimization](#performance-optimization)
- [Advanced Troubleshooting](#advanced-troubleshooting)

---

## Custom Configuration Tuning

### Understanding Configuration Layers

Senzing configuration consists of:
1. **Base configuration**: Default matching rules and thresholds
2. **Data source configuration**: Registered data sources
3. **Custom rules**: Optional custom matching logic

### Viewing Current Configuration

```python
from senzing import SzConfig, SzConfigManager
import json

config_mgr = SzConfigManager()
config_mgr.initialize("ConfigViewer", config_json)

sz_config = SzConfig()
sz_config.initialize("ConfigViewer", config_json)

try:
    # Get current config
    config_id = config_mgr.get_default_config_id()
    config_str = config_mgr.get_config(config_id)
    
    # Parse and view
    config_data = json.loads(config_str)
    
    # View data sources
    print("Data Sources:")
    for ds in config_data.get("G2_CONFIG", {}).get("CFG_DSRC", []):
        print(f"  - {ds['DSRC_CODE']}: {ds['DSRC_DESC']}")
    
    # View feature types
    print("\nFeature Types:")
    for ft in config_data.get("G2_CONFIG", {}).get("CFG_FTYPE", []):
        print(f"  - {ft['FTYPE_CODE']}: {ft['FTYPE_DESC']}")
    
finally:
    sz_config.destroy()
    config_mgr.destroy()
```

### Adding Custom Data Sources

```python
def add_data_source(data_source_code, description):
    """Add a new data source to configuration"""
    
    config_mgr = SzConfigManager()
    config_mgr.initialize("AddDataSource", config_json)
    
    sz_config = SzConfig()
    sz_config.initialize("AddDataSource", config_json)
    
    try:
        # Get current config
        config_id = config_mgr.get_default_config_id()
        config_str = config_mgr.get_config(config_id)
        config_handle = sz_config.import_config(config_str)
        
        # Add data source
        ds_def = json.dumps({
            "DSRC_CODE": data_source_code,
            "DSRC_DESC": description
        })
        
        sz_config.add_data_source(config_handle, ds_def)
        
        # Export and save
        new_config_str = sz_config.export_config(config_handle)
        new_config_id = config_mgr.add_config(
            new_config_str,
            f"Added data source: {data_source_code}"
        )
        config_mgr.set_default_config_id(new_config_id)
        
        print(f"Added data source: {data_source_code}")
        print(f"New config ID: {new_config_id}")
        
        sz_config.close_config(config_handle)
        
    finally:
        sz_config.destroy()
        config_mgr.destroy()

# Usage
add_data_source("NEW_SOURCE", "Description of new source")
```

### Custom Matching Thresholds

**Note**: Custom threshold tuning requires Senzing support. Contact Senzing for advanced configuration assistance.

```python
# Conceptual example - actual implementation requires Senzing support
def adjust_matching_threshold(feature_type, threshold):
    """
    Adjust matching threshold for a feature type
    
    WARNING: This is conceptual. Custom threshold tuning
    requires Senzing support and should not be attempted
    without guidance.
    """
    
    # This would modify the configuration to adjust
    # how strongly a feature type influences matching
    
    # Example: Make email matches stronger
    # feature_type = "EMAIL"
    # threshold = 95  # Higher threshold = stricter matching
    
    pass  # Implementation requires Senzing support
```

## Advanced Matching Rules

### Understanding Match Levels

Senzing assigns match levels to entity relationships:

1. **Resolved (Match Level 1)**: High confidence match, same entity
2. **Possibly Same (Match Level 2)**: Moderate confidence, likely same entity
3. **Possibly Related (Match Level 3)**: Low confidence, may be related
4. **Name Only (Match Level 4)**: Only name matches, likely different entities

### Analyzing Match Keys

```python
def analyze_match_key(entity_id_1, entity_id_2):
    """Analyze what features caused entities to match"""
    
    engine = SzEngine()
    engine.initialize("MatchAnalysis", config_json)
    
    try:
        # Get why analysis
        result = engine.why_entities(entity_id_1, entity_id_2)
        why_data = json.loads(result)
        
        match_info = why_data.get("MATCH_INFO", {})
        
        print(f"Match Level: {match_info.get('MATCH_LEVEL_CODE')}")
        print(f"Match Key: {match_info.get('MATCH_KEY')}")
        print(f"Rule Code: {match_info.get('RULE_CODE')}")
        
        # Analyze feature scores
        print("\nFeature Scores:")
        for feature in match_info.get("FEATURE_SCORES", []):
            print(f"  {feature['FEATURE_TYPE']}: {feature.get('SCORE', 'N/A')}")
            print(f"    Candidate: {feature.get('CANDIDATE_FEAT', 'N/A')}")
            print(f"    Inbound: {feature.get('INBOUND_FEAT', 'N/A')}")
        
        return match_info
        
    finally:
        engine.destroy()

# Usage
match_info = analyze_match_key(1001, 1002)
```

### Custom Entity Types

**Note**: Custom entity types require configuration changes. Contact Senzing support.

```python
# Conceptual example for different entity types
# In practice, this requires configuration support

# Person entity
person_record = {
    "DATA_SOURCE": "CUSTOMERS",
    "RECORD_ID": "PERSON001",
    "ENTITY_TYPE": "PERSON",  # Conceptual
    "NAME_FULL": "John Smith",
    "DATE_OF_BIRTH": "1980-01-15"
}

# Organization entity
org_record = {
    "DATA_SOURCE": "VENDORS",
    "RECORD_ID": "ORG001",
    "ENTITY_TYPE": "ORGANIZATION",  # Conceptual
    "NAME_ORG": "Acme Corporation",
    "TAX_ID_NUMBER": "12-3456789"
}

# Vehicle entity (custom)
vehicle_record = {
    "DATA_SOURCE": "DMV",
    "RECORD_ID": "VEH001",
    "ENTITY_TYPE": "VEHICLE",  # Conceptual
    "VIN": "1HGBH41JXMN109186",
    "OWNER_NAME": "John Smith"
}
```

## Network Analysis Techniques

### Finding Entity Networks

```python
def find_entity_network(seed_entity_id, max_depth=3):
    """
    Find network of related entities
    
    Args:
        seed_entity_id: Starting entity
        max_depth: Maximum relationship depth to traverse
    
    Returns:
        Network graph with entities and relationships
    """
    
    engine = SzEngine()
    engine.initialize("NetworkAnalysis", config_json)
    
    try:
        visited = set()
        network = {
            "entities": {},
            "relationships": []
        }
        
        def traverse(entity_id, depth):
            if depth > max_depth or entity_id in visited:
                return
            
            visited.add(entity_id)
            
            # Get entity details
            result = engine.get_entity_by_entity_id(entity_id)
            entity = json.loads(result)
            
            network["entities"][entity_id] = {
                "id": entity_id,
                "record_count": len(entity["RESOLVED_ENTITY"]["RECORDS"]),
                "data_sources": list(set(
                    r["DATA_SOURCE"] 
                    for r in entity["RESOLVED_ENTITY"]["RECORDS"]
                ))
            }
            
            # Find related entities
            # Note: This is conceptual - actual implementation
            # would use network traversal methods
            
            # Get possibly related entities
            for record in entity["RESOLVED_ENTITY"]["RECORDS"]:
                # Search for similar records
                search_result = engine.search_by_attributes(
                    json.dumps({
                        "NAME_FULL": record.get("NAME_FULL", ""),
                        "ADDR_FULL": record.get("ADDR_FULL", "")
                    })
                )
                
                search_data = json.loads(search_result)
                
                for related in search_data.get("RESOLVED_ENTITIES", [])[:5]:
                    related_id = related["ENTITY_ID"]
                    
                    if related_id != entity_id and related_id not in visited:
                        # Add relationship
                        network["relationships"].append({
                            "from": entity_id,
                            "to": related_id,
                            "strength": related.get("MATCH_SCORE", 0)
                        })
                        
                        # Traverse related entity
                        traverse(related_id, depth + 1)
        
        # Start traversal
        traverse(seed_entity_id, 0)
        
        return network
        
    finally:
        engine.destroy()

# Usage
network = find_entity_network(1001, max_depth=2)
print(f"Network size: {len(network['entities'])} entities")
print(f"Relationships: {len(network['relationships'])}")
```

### Network Visualization

```python
def export_network_for_visualization(network, output_file="network.json"):
    """Export network in format suitable for visualization tools"""
    
    # Format for D3.js, Cytoscape, etc.
    viz_data = {
        "nodes": [
            {
                "id": entity_id,
                "label": f"Entity {entity_id}",
                "size": data["record_count"],
                "sources": data["data_sources"]
            }
            for entity_id, data in network["entities"].items()
        ],
        "edges": [
            {
                "source": rel["from"],
                "target": rel["to"],
                "weight": rel["strength"]
            }
            for rel in network["relationships"]
        ]
    }
    
    with open(output_file, "w") as f:
        json.dump(viz_data, f, indent=2)
    
    print(f"Network exported to {output_file}")
    return viz_data

# Usage
viz_data = export_network_for_visualization(network)
```

### Clustering Analysis

```python
def find_entity_clusters(min_cluster_size=5):
    """
    Find clusters of highly connected entities
    
    Useful for fraud ring detection, community detection, etc.
    """
    
    engine = SzEngine()
    engine.initialize("ClusterAnalysis", config_json)
    
    try:
        # This is conceptual - actual implementation would
        # export all entities and analyze connections
        
        clusters = []
        
        # Conceptual clustering algorithm:
        # 1. Export all entities
        # 2. Build adjacency matrix
        # 3. Apply clustering algorithm (e.g., Louvain, DBSCAN)
        # 4. Identify clusters above minimum size
        
        # Example cluster structure
        cluster = {
            "id": 1,
            "size": 15,
            "entities": [1001, 1002, 1003, ...],
            "density": 0.85,  # Connection density
            "shared_features": ["ADDRESS", "PHONE"]
        }
        
        clusters.append(cluster)
        
        return clusters
        
    finally:
        engine.destroy()

# Usage
clusters = find_entity_clusters(min_cluster_size=10)
for cluster in clusters:
    print(f"Cluster {cluster['id']}: {cluster['size']} entities")
```

## Graph Traversal Patterns

### Breadth-First Search (BFS)

```python
from collections import deque

def bfs_entity_search(start_entity_id, target_attribute, target_value):
    """
    Find entities with specific attribute using BFS
    
    Args:
        start_entity_id: Starting entity
        target_attribute: Attribute to search for (e.g., "PHONE_NUMBER")
        target_value: Value to match
    
    Returns:
        List of entities with matching attribute
    """
    
    engine = SzEngine()
    engine.initialize("BFS_Search", config_json)
    
    try:
        visited = set()
        queue = deque([start_entity_id])
        matches = []
        
        while queue:
            entity_id = queue.popleft()
            
            if entity_id in visited:
                continue
            
            visited.add(entity_id)
            
            # Get entity
            result = engine.get_entity_by_entity_id(entity_id)
            entity = json.loads(result)
            
            # Check for target attribute
            for record in entity["RESOLVED_ENTITY"]["RECORDS"]:
                if record.get(target_attribute) == target_value:
                    matches.append(entity_id)
                    break
            
            # Add related entities to queue
            # (Implementation depends on how you define "related")
            
        return matches
        
    finally:
        engine.destroy()
```

### Depth-First Search (DFS)

```python
def dfs_entity_search(start_entity_id, max_depth=5):
    """
    Deep traversal of entity relationships
    
    Useful for finding distant connections
    """
    
    engine = SzEngine()
    engine.initialize("DFS_Search", config_json)
    
    try:
        visited = set()
        paths = []
        
        def dfs(entity_id, path, depth):
            if depth > max_depth or entity_id in visited:
                return
            
            visited.add(entity_id)
            current_path = path + [entity_id]
            
            # Get entity
            result = engine.get_entity_by_entity_id(entity_id)
            entity = json.loads(result)
            
            # Record path
            if len(current_path) > 1:
                paths.append(current_path.copy())
            
            # Continue traversal
            # (Find related entities and recurse)
            
        dfs(start_entity_id, [], 0)
        
        return paths
        
    finally:
        engine.destroy()
```

### Shortest Path Finding

```python
def find_shortest_path(entity_id_1, entity_id_2, max_depth=6):
    """
    Find shortest path between two entities
    
    Useful for understanding relationships between entities
    """
    
    engine = SzEngine()
    engine.initialize("ShortestPath", config_json)
    
    try:
        # BFS from both ends
        queue1 = deque([(entity_id_1, [entity_id_1])])
        queue2 = deque([(entity_id_2, [entity_id_2])])
        
        visited1 = {entity_id_1: [entity_id_1]}
        visited2 = {entity_id_2: [entity_id_2]}
        
        depth = 0
        
        while queue1 or queue2:
            if depth > max_depth:
                return None  # No path found within max_depth
            
            # Expand from entity_id_1
            if queue1:
                current, path = queue1.popleft()
                
                # Check if we've met the other search
                if current in visited2:
                    # Found path!
                    return path + visited2[current][::-1][1:]
                
                # Expand neighbors
                # (Implementation depends on relationship definition)
            
            # Expand from entity_id_2
            if queue2:
                current, path = queue2.popleft()
                
                if current in visited1:
                    return visited1[current] + path[::-1][1:]
            
            depth += 1
        
        return None  # No path found
        
    finally:
        engine.destroy()
```

## Advanced Export Patterns

### Incremental Export

```python
def incremental_export(last_export_time):
    """
    Export only entities modified since last export
    
    Note: Requires tracking modification times in your system
    """
    
    engine = SzEngine()
    engine.initialize("IncrementalExport", config_json)
    
    try:
        # This is conceptual - actual implementation depends on
        # how you track entity modifications
        
        modified_entities = []
        
        # Query for entities modified since last_export_time
        # This would require custom tracking in your application
        
        for entity_id in get_modified_entity_ids(last_export_time):
            result = engine.get_entity_by_entity_id(entity_id)
            entity = json.loads(result)
            modified_entities.append(entity)
        
        return modified_entities
        
    finally:
        engine.destroy()
```

### Filtered Export

```python
def filtered_export(data_source=None, min_records=None, max_records=None):
    """
    Export entities matching specific criteria
    
    Args:
        data_source: Only entities with records from this source
        min_records: Minimum number of records per entity
        max_records: Maximum number of records per entity
    """
    
    engine = SzEngine()
    engine.initialize("FilteredExport", config_json)
    
    try:
        filtered_entities = []
        
        # This is conceptual - actual implementation would
        # use export methods and filter results
        
        # Pseudo-code for filtering logic
        for entity in all_entities:
            record_count = len(entity["RESOLVED_ENTITY"]["RECORDS"])
            
            # Check record count filters
            if min_records and record_count < min_records:
                continue
            if max_records and record_count > max_records:
                continue
            
            # Check data source filter
            if data_source:
                sources = [r["DATA_SOURCE"] for r in entity["RESOLVED_ENTITY"]["RECORDS"]]
                if data_source not in sources:
                    continue
            
            filtered_entities.append(entity)
        
        return filtered_entities
        
    finally:
        engine.destroy()
```

### Hierarchical Export

```python
def export_with_hierarchy(root_entity_id, max_depth=3):
    """
    Export entity with all related entities in hierarchical structure
    
    Useful for understanding entity relationships
    """
    
    engine = SzEngine()
    engine.initialize("HierarchicalExport", config_json)
    
    try:
        def build_hierarchy(entity_id, depth):
            if depth > max_depth:
                return None
            
            # Get entity
            result = engine.get_entity_by_entity_id(entity_id)
            entity = json.loads(result)
            
            # Build hierarchy node
            node = {
                "entity_id": entity_id,
                "records": entity["RESOLVED_ENTITY"]["RECORDS"],
                "children": []
            }
            
            # Find related entities
            # (Implementation depends on relationship definition)
            related_ids = find_related_entities(entity_id)
            
            for related_id in related_ids[:10]:  # Limit children
                child = build_hierarchy(related_id, depth + 1)
                if child:
                    node["children"].append(child)
            
            return node
        
        hierarchy = build_hierarchy(root_entity_id, 0)
        return hierarchy
        
    finally:
        engine.destroy()
```

## Performance Optimization Techniques

### Connection Pooling

```python
from queue import Queue
import threading

class SenzingConnectionPool:
    """Connection pool for Senzing engines"""
    
    def __init__(self, config_json, pool_size=10):
        self.config_json = config_json
        self.pool = Queue(maxsize=pool_size)
        
        # Initialize pool
        for i in range(pool_size):
            engine = SzEngine()
            engine.initialize(f"PooledEngine_{i}", config_json)
            self.pool.put(engine)
    
    def get_engine(self):
        """Get an engine from the pool"""
        return self.pool.get()
    
    def return_engine(self, engine):
        """Return an engine to the pool"""
        self.pool.put(engine)
    
    def close_all(self):
        """Close all engines in pool"""
        while not self.pool.empty():
            engine = self.pool.get()
            engine.destroy()

# Usage
pool = SenzingConnectionPool(config_json, pool_size=10)

def process_record(record):
    engine = pool.get_engine()
    try:
        engine.add_record(
            record["DATA_SOURCE"],
            record["RECORD_ID"],
            json.dumps(record)
        )
    finally:
        pool.return_engine(engine)

# Process records with pooled connections
threads = []
for record in records:
    t = threading.Thread(target=process_record, args=(record,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

pool.close_all()
```

### Batch Processing Optimization

```python
def optimized_batch_load(records, batch_size=5000, num_threads=8):
    """
    Highly optimized batch loading
    
    Techniques:
    - Large batch sizes
    - Multi-threading
    - Connection pooling
    - Progress monitoring
    """
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time
    
    pool = SenzingConnectionPool(config_json, pool_size=num_threads)
    
    def load_batch(batch):
        engine = pool.get_engine()
        loaded = 0
        errors = 0
        
        try:
            for record in batch:
                try:
                    engine.add_record(
                        record["DATA_SOURCE"],
                        record["RECORD_ID"],
                        json.dumps(record)
                    )
                    loaded += 1
                except Exception as e:
                    errors += 1
                    print(f"Error loading {record['RECORD_ID']}: {e}")
        finally:
            pool.return_engine(engine)
        
        return loaded, errors
    
    # Split into batches
    batches = [
        records[i:i + batch_size]
        for i in range(0, len(records), batch_size)
    ]
    
    # Process batches in parallel
    total_loaded = 0
    total_errors = 0
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(load_batch, batch) for batch in batches]
        
        for i, future in enumerate(as_completed(futures)):
            loaded, errors = future.result()
            total_loaded += loaded
            total_errors += errors
            
            # Progress update
            elapsed = time.time() - start_time
            throughput = total_loaded / elapsed if elapsed > 0 else 0
            
            print(f"Progress: {total_loaded}/{len(records)} "
                  f"({100*total_loaded/len(records):.1f}%) "
                  f"Throughput: {throughput:.0f} rec/sec "
                  f"Errors: {total_errors}")
    
    pool.close_all()
    
    return total_loaded, total_errors

# Usage
loaded, errors = optimized_batch_load(my_records, batch_size=5000, num_threads=8)
```

## Advanced Troubleshooting

### Performance Profiling

```python
import time
import cProfile
import pstats

def profile_loading_performance(records):
    """Profile loading performance to identify bottlenecks"""
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    engine = SzEngine()
    engine.initialize("Profiling", config_json)
    
    start_time = time.time()
    
    try:
        for i, record in enumerate(records):
            record_start = time.time()
            
            engine.add_record(
                record["DATA_SOURCE"],
                record["RECORD_ID"],
                json.dumps(record)
            )
            
            record_time = time.time() - record_start
            
            if record_time > 1.0:  # Flag slow records
                print(f"Slow record: {record['RECORD_ID']} took {record_time:.2f}s")
    
    finally:
        engine.destroy()
    
    profiler.disable()
    
    # Print profiling results
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    
    total_time = time.time() - start_time
    throughput = len(records) / total_time
    
    print(f"\nTotal time: {total_time:.2f}s")
    print(f"Throughput: {throughput:.2f} records/sec")

# Usage
profile_loading_performance(test_records[:1000])
```

For more advanced topics and custom configuration assistance, contact Senzing support or use:
```python
search_docs(query="advanced configuration", category="general", version="current")
```
