# Senzing — Best Practices

This guide covers best practices, anti-patterns, and common pitfalls when working with Senzing.

## Best Practices

### Always Do

- Call `get_capabilities` at the start of any Senzing session
- Use `mapping_workflow` for all data mapping — never hand-code Senzing JSON attribute names
- Use `generate_scaffold` or `sdk_guide` for SDK code — never guess method signatures
- Use `search_docs` with category `anti_patterns` before recommending installation, architecture, or deployment approaches
- Use `lint_record` to validate records before loading
- Start with SQLite for evaluation; recommend PostgreSQL for production
- Test with sample data (via `get_sample_data`) before working with real data
- Back up the database before any loading operation
- Test loads with a small batch (100 records) before running full loads

### Never Do

- Hand-code Senzing attribute names from memory (they are frequently wrong)
- Guess SDK method signatures (method names differ across versions)
- Skip the `DATA_SOURCE` or `RECORD_ID` fields in mapped records
- Use SQLite for production workloads (it doesn't scale past ~100K records)
- Load data without validating with `lint_record` first
- Ignore error codes — always investigate with `explain_error_code`

## Common Pitfalls

### Wrong Attribute Names

The most common mistake is guessing Senzing attribute names. Examples of frequently incorrect names:

| Wrong | Correct |
| --- | --- |
| `BUSINESS_NAME_ORG` | `NAME_ORG` |
| `EMPLOYER_NAME` | `NAME_ORG` |
| `PHONE` | `PHONE_NUMBER` |
| `EMAIL` | `EMAIL_ADDRESS` |
| `SSN` | `SSN_NUMBER` |
| `DOB` | `DATE_OF_BIRTH` |
| `ADDRESS` | `ADDR_FULL` |
| `COMPANY` | `NAME_ORG` |

**Fix**: Always use `mapping_workflow` — it returns validated attribute names.

### Wrong SDK Method Names

SDK method names differ across versions and languages. Common mistakes:

| Wrong | Correct |
| --- | --- |
| `close_export` | `close_export_report` |
| `init` | `initialize` |
| `whyEntityByEntityID` | `why_entities` (V4) |
| `addRecord` | `add_record` (Python V4) |
| `getEntity` | `get_entity` (Python V4) |

**Fix**: Always use `generate_scaffold` or `get_sdk_reference` for method signatures.

### Missing Required Fields

Every Senzing record MUST have:

- `DATA_SOURCE` — unique identifier for the data source (e.g., "CUSTOMERS", "VENDORS")
- `RECORD_ID` — unique within the data source (e.g., "CUST001", "12345")

Records without these fields will fail to load.

**Example of correct record structure**:
```json
{
  "DATA_SOURCE": "CUSTOMERS",
  "RECORD_ID": "CUST001",
  "NAME_FULL": "John Smith",
  "EMAIL_ADDRESS": "john.smith@example.com"
}
```

### Lost Mapping Workflow State

When using `mapping_workflow`, always pass the exact `state` JSON from the previous response to the next call. Losing or modifying the state object causes errors.

**Correct approach**:
```python
# Step 1
response1 = mapping_workflow(action="start", file_paths=["data.csv"])
state = response1["state"]  # Save this

# Step 2
response2 = mapping_workflow(action="advance", state=state, data={...})
state = response2["state"]  # Update with new state

# Step 3
response3 = mapping_workflow(action="advance", state=state, data={...})
```

### Missing Environment Configuration

SDK initialization fails without proper configuration. The `SENZING_ENGINE_CONFIGURATION_JSON` environment variable (or equivalent configuration) must be set. Use `sdk_guide` with the correct platform parameter for exact setup steps.

### Incorrect Data Source Registration

Data sources must be registered in the Senzing configuration before loading records. Use `sdk_guide` with `topic: "configure"` and `data_sources: ["SOURCE1", "SOURCE2"]` to register them properly.

### Ignoring Data Quality Issues

Poor data quality leads to poor matching results. Always:
- Use `analyze_record` to check data quality before loading
- Review feature coverage (what percentage of records have names, addresses, etc.)
- Check for data standardization issues (inconsistent formats)
- Validate identifier uniqueness (RECORD_ID must be unique per DATA_SOURCE)

### Overloading SQLite

SQLite is single-threaded and file-based. It's great for evaluation but fails at scale:
- **< 10K records**: Works fine
- **10K - 50K records**: Slow but functional
- **50K - 100K records**: Very slow, not recommended
- **> 100K records**: Don't use SQLite

**Fix**: Use PostgreSQL for anything beyond evaluation.

### Not Testing with Small Batches

Always test with a small batch (100-1000 records) before loading millions of records. This helps catch:
- Mapping errors
- Configuration issues
- Performance problems
- Data quality issues

### Hardcoding Configuration

Never hardcode database credentials, paths, or configuration in your code. Use:
- Environment variables
- Configuration files
- Secret management systems

**Bad**:
```python
config = '{"PIPELINE": {"CONFIGPATH": "/home/user/senzing/config"}}'
```

**Good**:
```python
import os
config = os.environ.get("SENZING_ENGINE_CONFIGURATION_JSON")
```

### Ignoring Redo Processing

Redo processing re-evaluates entities when new data arrives. For initial loads:
- Disable redo to speed up loading
- Re-enable after initial load completes
- Process accumulated redo records

Use `search_docs` with query "redo processing" for details.

### Not Monitoring Performance

Monitor these metrics in production:
- Records loaded per second
- Entity count growth
- Database size
- Query response times
- Error rates

Use `search_docs` with category "monitoring" for detailed guidance.
