# Senzing — Quick Command Reference

This cheat sheet provides copy-paste ready commands for common Senzing tasks.

## First-Time Setup (Complete Workflow)

```python
# 1. Discover capabilities
get_capabilities(version="current")

# 2. Get sample data
get_sample_data(dataset="las-vegas", limit=100)

# 3. Install Senzing (Linux/apt)
sdk_guide(topic="install", platform="linux_apt", version="current")

# 4. Configure engine
sdk_guide(topic="configure", data_sources=["SAMPLE"], version="current")

# 5. Load sample data
sdk_guide(topic="load", input_file="sample_data.jsonl", record_count=100, version="current")

# 6. Query results
sdk_guide(topic="export", version="current")
```

## Data Mapping (Quick Start)

```python
# Start mapping workflow
mapping_workflow(
    action="start",
    file_paths=["customers.csv"],
    version="current"
)

# Advance through steps (repeat for each step)
mapping_workflow(
    action="advance",
    state=<previous_state>,
    data=<step_data>,
    version="current"
)

# Check status
mapping_workflow(
    action="status",
    state=<current_state>,
    version="current"
)

# Validate mapped data
lint_record(file_paths=["customers_mapped.jsonl"], version="current")

# Analyze data quality
analyze_record(file_paths=["customers_mapped.jsonl"], version="current")
```

## Code Generation (One-Liners)

```python
# Python full pipeline
generate_scaffold(language="python", workflow="full_pipeline", version="current")

# Python loader only
generate_scaffold(language="python", workflow="add_records", version="current")

# Python query code
generate_scaffold(language="python", workflow="query", version="current")

# Java full pipeline
generate_scaffold(language="java", workflow="full_pipeline", version="current")

# C# full pipeline
generate_scaffold(language="csharp", workflow="full_pipeline", version="current")

# Rust full pipeline
generate_scaffold(language="rust", workflow="full_pipeline", version="current")
```

## Documentation Search (Common Queries)

```python
# General concepts
search_docs(query="entity resolution basics", category="general", version="current")

# Data mapping help
search_docs(query="attribute names", category="data_mapping", version="current")

# Performance tuning
search_docs(query="loading performance", category="performance", version="current")

# Database setup
search_docs(query="postgresql configuration", category="database", version="current")

# Troubleshooting
search_docs(query="connection error", category="troubleshooting", version="current")

# Anti-patterns
search_docs(query="common mistakes", category="anti_patterns", version="current")

# Deployment
search_docs(query="production deployment", category="deployment", version="current")

# Pricing
search_docs(query="DSR pricing", category="pricing", version="current")
```

## Error Diagnosis (Quick Lookup)

```python
# Configuration error
explain_error_code(error_code="SENZ0001", version="current")

# Database connection error
explain_error_code(error_code="SENZ0002", version="current")

# Invalid record format
explain_error_code(error_code="SENZ0005", version="current")

# Data source not registered
explain_error_code(error_code="SENZ0037", version="current")

# License limit exceeded
explain_error_code(error_code="SENZ0040", version="current")

# Shorthand formats also work
explain_error_code(error_code="5", version="current")
explain_error_code(error_code="0005", version="current")
```

## Finding Examples (Common Searches)

```python
# Python loading examples
find_examples(query="load records", language="python")

# Error handling patterns
find_examples(query="error handling retry", language="python")

# Multi-threading examples
find_examples(query="multi-threaded loader", language="python")

# Kafka integration
find_examples(query="kafka consumer", language="python")

# REST API examples
find_examples(query="flask api", language="python")

# Search by repository
find_examples(repo="brianmacy/sz_mem-v4", list_files=True)

# Get specific file
find_examples(repo="brianmacy/sz_mem-v4", file_path="sz_mem.py")
```

## SDK Reference (Quick Lookups)

```python
# Check method signatures
get_sdk_reference(topic="functions", filter="add_record", version="current")

# Check flags
get_sdk_reference(topic="flags", version="current")

# Check specific flag
get_sdk_reference(topic="flags", filter="SZ_EXPORT", version="current")

# Migration info (V4 updates)
get_sdk_reference(topic="migration", version="current")

# Response schemas
get_sdk_reference(topic="response_schemas", version="current")

# All reference data
get_sdk_reference(topic="all", version="current")
```

## Sample Data (Quick Access)

```python
# List available datasets
get_sample_data(dataset="list")

# Las Vegas data (100 records)
get_sample_data(dataset="las-vegas", limit=100)

# London data (500 records)
get_sample_data(dataset="london", limit=500)

# Moscow data (random sample)
get_sample_data(dataset="moscow", limit=100, offset="random")

# List sources in a dataset
get_sample_data(dataset="las-vegas", source="list")

# Filter by specific source
get_sample_data(dataset="las-vegas", source="equifax", limit=100)
```

## Platform-Specific Installation

```python
# Linux (apt-based: Ubuntu, Debian)
sdk_guide(topic="install", platform="linux_apt", version="current")

# Linux (yum-based: RHEL, CentOS)
sdk_guide(topic="install", platform="linux_yum", version="current")

# macOS (ARM/M1/M2)
sdk_guide(topic="install", platform="macos_arm", version="current")

# Windows
sdk_guide(topic="install", platform="windows", version="current")

# Docker
sdk_guide(topic="install", platform="docker", version="current")
```

## Common Parameter Combinations

### Mapping Workflow (Complete Session)

```python
# Step 1: Start
response1 = mapping_workflow(
    action="start",
    file_paths=["data.csv", "data2.json"],
    version="current"
)
state = response1["state"]

# Step 2-7: Advance through each step
response2 = mapping_workflow(
    action="advance",
    state=state,
    data={"selected_option": "value"},
    version="current"
)
state = response2["state"]

# Go back if needed
response_back = mapping_workflow(
    action="back",
    state=state,
    version="current"
)
state = response_back["state"]

# Check status anytime
status = mapping_workflow(
    action="status",
    state=state,
    version="current"
)

# Reset if needed
mapping_workflow(action="reset", version="current")
```

### SDK Guide (Full Pipeline)

```python
# Complete setup for Python on Linux
sdk_guide(topic="full_pipeline", platform="linux_apt", language="python", version="current")

# Load specific file with record limit
sdk_guide(
    topic="load",
    platform="linux_apt",
    language="python",
    input_file="/path/to/data.jsonl",
    record_count=10000,
    sample_only=False,
    version="current"
)

# Configure with multiple data sources
sdk_guide(
    topic="configure",
    platform="linux_apt",
    language="python",
    data_sources=["CUSTOMERS", "VENDORS", "PARTNERS"],
    version="current"
)
```

## Bash Command Shortcuts

### Quick Validation

```bash
# Validate JSON syntax
python sz_json_linter.py customers_mapped.jsonl

# Analyze data quality
python sz_json_analyzer.py customers_mapped.jsonl

# Check specific fields
python sz_json_analyzer.py customers_mapped.jsonl --fields NAME_FULL,EMAIL_ADDRESS
```

### Quick Testing

```bash
# Test with first 100 records
head -n 100 large_file.jsonl > test_sample.jsonl

# Count records
wc -l data.jsonl

# Check for required fields
grep -c '"DATA_SOURCE"' data.jsonl
grep -c '"RECORD_ID"' data.jsonl

# Find records missing fields
grep -v '"EMAIL_ADDRESS"' data.jsonl | head -n 10
```

### Database Quick Checks

```bash
# PostgreSQL - Check connection
psql -h localhost -U senzing -d senzing -c "SELECT 1;"

# PostgreSQL - Count records
psql -h localhost -U senzing -d senzing -c "SELECT COUNT(*) FROM dsrc_record;"

# PostgreSQL - Check data sources
psql -h localhost -U senzing -d senzing -c "SELECT dsrc_code FROM dsrc_record GROUP BY dsrc_code;"

# PostgreSQL - Database size
psql -h localhost -U senzing -d senzing -c "SELECT pg_size_pretty(pg_database_size('senzing'));"
```

## Python Quick Snippets

### Load Single Record

```python
from senzing import SzEngine
import json

engine = SzEngine()
engine.initialize("QuickLoad", config_json)

record = {
    "DATA_SOURCE": "TEST",
    "RECORD_ID": "001",
    "NAME_FULL": "John Smith"
}

engine.add_record("TEST", "001", json.dumps(record))
engine.destroy()
```

### Search for Entity

```python
from senzing import SzEngine
import json

engine = SzEngine()
engine.initialize("QuickSearch", config_json)

result = engine.search_by_attributes(
    json.dumps({"NAME_FULL": "John Smith"})
)

print(json.dumps(json.loads(result), indent=2))
engine.destroy()
```

### Get Entity by Record

```python
from senzing import SzEngine
import json

engine = SzEngine()
engine.initialize("QuickGet", config_json)

result = engine.get_entity_by_record_id("CUSTOMERS", "CUST001")
entity = json.loads(result)

print(f"Entity ID: {entity['RESOLVED_ENTITY']['ENTITY_ID']}")
print(f"Record count: {len(entity['RESOLVED_ENTITY']['RECORDS'])}")

engine.destroy()
```

### Why Analysis

```python
from senzing import SzEngine
import json

engine = SzEngine()
engine.initialize("QuickWhy", config_json)

result = engine.why_entities(entity_id_1=1001, entity_id_2=1002)
why = json.loads(result)

print(f"Match Level: {why['MATCH_INFO']['MATCH_LEVEL_CODE']}")
print(f"Match Key: {why['MATCH_INFO']['MATCH_KEY']}")

engine.destroy()
```

## Docker Quick Commands

```bash
# Run Senzing in Docker
docker run -it --rm \
  -v $(pwd)/data:/data \
  senzing/senzing-tools:latest

# Docker Compose (basic setup)
docker-compose up -d

# Check logs
docker-compose logs -f senzing

# Stop services
docker-compose down
```

## Environment Variables (Quick Setup)

```bash
# Linux/macOS
export SENZING_ENGINE_CONFIGURATION_JSON='{
  "PIPELINE": {
    "CONFIGPATH": "/opt/senzing/data",
    "RESOURCEPATH": "/opt/senzing/resources",
    "SUPPORTPATH": "/opt/senzing/data"
  },
  "SQL": {
    "CONNECTION": "postgresql://senzing:password@localhost:5432/senzing"
  }
}'

# Windows (PowerShell)
$env:SENZING_ENGINE_CONFIGURATION_JSON = '{
  "PIPELINE": {
    "CONFIGPATH": "C:\\senzing\\data",
    "RESOURCEPATH": "C:\\senzing\\resources",
    "SUPPORTPATH": "C:\\senzing\\data"
  },
  "SQL": {
    "CONNECTION": "postgresql://senzing:password@localhost:5432/senzing"
  }
}'
```

## Common Workflows (Copy-Paste Ready)

### Workflow: Evaluate Senzing (30 minutes)

```python
# 1. Get capabilities
get_capabilities(version="current")

# 2. Get sample data
get_sample_data(dataset="las-vegas", limit=100)

# 3. Install (choose your platform)
sdk_guide(topic="install", platform="linux_apt", version="current")

# 4. Run full pipeline
sdk_guide(topic="full_pipeline", platform="linux_apt", language="python", version="current")
```

### Workflow: Map and Load New Data (45 minutes)

```python
# 1. Start mapping
response = mapping_workflow(action="start", file_paths=["data.csv"], version="current")

# 2. Complete mapping steps (interactive)
# ... follow prompts ...

# 3. Validate
lint_record(file_paths=["data_mapped.jsonl"], version="current")

# 4. Analyze quality
analyze_record(file_paths=["data_mapped.jsonl"], version="current")

# 5. Generate loader
generate_scaffold(language="python", workflow="add_records", version="current")

# 6. Run generated loader code
```

### Workflow: Troubleshoot Production Issue (20 minutes)

```python
# 1. Identify error code from logs
error_code = "SENZ0005"

# 2. Explain error
explain_error_code(error_code=error_code, version="current")

# 3. Search for solutions
search_docs(query="invalid record format", category="troubleshooting", version="current")

# 4. Find working examples
find_examples(query="error handling", language="python")

# 5. Check method signatures
get_sdk_reference(topic="functions", filter="add_record", version="current")
```

## Tips for Efficiency

1. **Save state objects**: Always save the `state` from `mapping_workflow` responses
2. **Use filters**: Add `filter` parameter to narrow `get_sdk_reference` results
3. **Batch operations**: Use `limit` and `offset` with `get_sample_data` for large datasets
4. **Cache results**: Save `generate_scaffold` output to avoid regenerating
5. **Use categories**: Add `category` to `search_docs` for faster, more relevant results
6. **Check examples first**: Use `find_examples` before writing custom code
7. **Validate early**: Run `lint_record` before attempting to load data
8. **Test small**: Use `limit=100` for initial testing, then scale up

## Keyboard Shortcuts (for interactive tools)

When using interactive MCP tools:
- Save responses to variables for easy reference
- Use tab completion for parameter names
- Copy state objects immediately after receiving them
- Keep a scratch file for frequently used commands
