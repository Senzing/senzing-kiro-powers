# Senzing — Troubleshooting Guide

This guide covers error handling, debugging strategies, and typical troubleshooting sessions.

## Quick Troubleshooting Reference

| Symptom | Tool to Use | Details |
| --- | --- | --- |
| Wrong attribute names in mapped data | `mapping_workflow` | Re-map using the interactive workflow |
| SDK method not found or wrong signature | `generate_scaffold` or `get_sdk_reference` | Get validated method signatures |
| Senzing error code (e.g., SENZ0005) | `explain_error_code` | Accepts `SENZ0005`, `0005`, or `5` |
| Configuration or database issues | `search_docs` | Use category `configuration` or `database` |
| Installation problems | `sdk_guide` | Specify your platform for correct steps |
| Anti-pattern concerns | `search_docs` | Use category `anti_patterns` |
| Understanding why records matched | `get_sdk_reference` | Look up `why_entities` method and flags |
| Need working code examples | `find_examples` | Search 27 Senzing GitHub repositories |

## Error Handling Beyond Error Codes

### When MCP Tools Fail

**Tool returns empty or unexpected results**:
- Verify input parameters match the tool's schema
- Check that file paths are accessible and files are not empty
- Use `get_capabilities` to confirm tool availability
- Try with a smaller dataset or simpler query

**Tool times out**:
- Check network connectivity to mcp.senzing.com
- Increase timeout in `mcp.json` (default: 30 seconds)
- For `mapping_workflow`, break large files into smaller chunks
- For `search_docs`, make queries more specific

**Mapping workflow state lost**:
- Always save the `state` JSON from each response
- Never modify the state object manually
- If state is lost, restart with `action: "start"`
- Use `action: "status"` to check current workflow position

**Generated code doesn't work**:
- Verify you're using the correct Senzing SDK version
- Check that all dependencies are installed
- Use `get_sdk_reference` to verify method signatures
- Look for similar patterns with `find_examples`

**Sample data download fails**:
- Check the `download_url` in the citation
- Verify network access to the CORD repository
- Try a different dataset or smaller limit
- Use `get_sample_data` with `dataset: "list"` to see available options

### General Debugging Strategy

1. **Isolate the problem**: Test with minimal data/code
2. **Check the basics**: File paths, permissions, network connectivity
3. **Consult documentation**: Use `search_docs` with specific error messages
4. **Find examples**: Use `find_examples` to see working patterns
5. **Get help**: Use `submit_feedback` with detailed reproduction steps

## Common Error Codes

### SENZ0001 - Configuration Error
**Cause**: Invalid or missing configuration
**Solution**: 
- Verify `SENZING_ENGINE_CONFIGURATION_JSON` is set
- Use `sdk_guide` to generate correct configuration
- Check database connection parameters

### SENZ0002 - Database Connection Error
**Cause**: Cannot connect to database
**Solution**:
- Verify database is running
- Check connection string (host, port, credentials)
- Test database connectivity outside Senzing
- Check firewall rules

### SENZ0005 - Invalid Record Format
**Cause**: Record doesn't match expected JSON structure
**Solution**:
- Use `lint_record` to validate records
- Ensure `DATA_SOURCE` and `RECORD_ID` are present
- Check for invalid JSON syntax
- Use `mapping_workflow` to generate correct format

### SENZ0037 - Data Source Not Registered
**Cause**: Attempting to load records for unregistered data source
**Solution**:
- Use `sdk_guide` with `topic: "configure"` to register data sources
- Verify data source name matches exactly (case-sensitive)
- Check configuration includes the data source

### SENZ0040 - License Limit Exceeded
**Cause**: Exceeded evaluation license limit (typically 500 records)
**Solution**:
- Contact Senzing sales for production license
- Delete existing records to stay under limit
- Use different database for testing

For any error code, use `explain_error_code` with the code number for detailed diagnosis.

## Typical Troubleshooting Sessions

### Session 1: First-Time User Evaluating Senzing

**Goal**: Understand Senzing capabilities and see entity resolution in action

**Steps**:
1. `get_capabilities` (version: "current") — Discover available tools
2. `search_docs` (query: "entity resolution basics", category: "general") — Learn core concepts
3. `get_sample_data` (dataset: "las-vegas", limit: 100) — Get test data
4. `sdk_guide` (topic: "install", platform: "linux_apt" or your platform) — Install Senzing
5. `sdk_guide` (topic: "configure", data_sources: ["SAMPLE"]) — Configure engine
6. `sdk_guide` (topic: "load", input_file: "sample_data.jsonl", record_count: 100) — Load data
7. `sdk_guide` (topic: "export") — Query and export results

**Expected time**: 30-60 minutes

**Outcome**: Working local Senzing installation with sample data loaded and queryable

### Session 2: Experienced User Mapping New Data Source

**Goal**: Map a new CSV/JSON data source to Senzing format

**Steps**:
1. `mapping_workflow` (action: "start", file_paths: ["customers.csv"]) — Start mapping
2. `mapping_workflow` (action: "advance", state: {...}, data: {...}) — Progress through 7 steps
3. `lint_record` (file_paths: ["customers_mapped.jsonl"]) — Validate mapped records
4. `analyze_record` (file_paths: ["customers_mapped.jsonl"]) — Check data quality
5. `generate_scaffold` (language: "python", workflow: "add_records", version: "current") — Generate loader
6. Run generated loader code to load records
7. `generate_scaffold` (language: "python", workflow: "query", version: "current") — Generate query code

**Expected time**: 15-30 minutes (depending on data complexity)

**Outcome**: Validated Senzing JSON records and working loader code

### Session 3: Production Deployment Troubleshooting

**Goal**: Diagnose and fix issues in a production deployment

**Steps**:
1. Identify error code from logs (e.g., SENZ0005)
2. `explain_error_code` (error_code: "SENZ0005", version: "current") — Understand the error
3. `search_docs` (query: "database connection", category: "troubleshooting") — Find solutions
4. `get_sdk_reference` (topic: "flags", version: "current") — Check flag usage
5. `find_examples` (query: "error handling retry", language: "python") — Find retry patterns
6. Apply fix and test
7. `submit_feedback` (if issue was unclear or documentation needs improvement)

**Expected time**: 15-45 minutes (depending on issue complexity)

**Outcome**: Issue diagnosed and resolved with proper error handling

## Network and Connectivity Issues

### MCP Server Connectivity

**Cannot reach mcp.senzing.com**:
- Check internet connectivity
- Verify firewall allows HTTPS (port 443)
- Check proxy settings if behind corporate firewall
- Try accessing https://mcp.senzing.com/status in browser

**Frequent timeouts**:
- Increase timeout in `mcp.json` (e.g., 60000 for 60 seconds)
- Check network latency to mcp.senzing.com
- Try during off-peak hours
- Break large operations into smaller chunks

**SSL/TLS errors**:
- Verify system certificates are up to date
- Check corporate SSL inspection isn't interfering
- Ensure system time is correct (affects certificate validation)

### Database Connectivity

**PostgreSQL connection refused**:
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check if port is open
netstat -an | grep 5432

# Test connection
psql -h localhost -U senzing -d senzing
```

**Connection pool exhausted**:
- Increase `max_connections` in postgresql.conf
- Implement connection pooling (pgBouncer)
- Reduce number of loader threads
- Check for connection leaks in application code

## Data Quality Issues

### Low Match Rates

**Symptom**: Few entities being resolved/matched

**Causes**:
- Poor data quality (missing or inconsistent data)
- Incorrect attribute mapping
- Insufficient matching criteria

**Solutions**:
1. Use `analyze_record` to check feature coverage
2. Review mapping with `mapping_workflow`
3. Standardize data before loading (addresses, phone numbers)
4. Add more identifying attributes
5. Use `search_docs` with query "matching rules" for tuning guidance

### High Match Rates (Over-matching)

**Symptom**: Too many records resolving to same entity

**Causes**:
- Generic or missing data (e.g., all records have same phone number)
- Incorrect attribute types
- Configuration too aggressive

**Solutions**:
1. Review data quality with `analyze_record`
2. Check for placeholder values (000-000-0000, test@test.com)
3. Verify attribute types in mapping
4. Use `why_entities` to understand why records matched
5. Consider custom configuration (contact Senzing support)

## Performance Issues

See [performance.md](performance.md) for detailed performance troubleshooting.

**Quick checks**:
- Monitor CPU, memory, disk I/O
- Check database query performance
- Verify thread count is appropriate
- Ensure database is properly tuned
- Check for disk space issues

## Installation Issues

### SDK Installation Fails

**Python SDK**:
```bash
# Verify Python version (3.8+)
python --version

# Check pip
pip --version

# Install with verbose output
pip install senzing -v
```

**Missing dependencies**:
- Use `sdk_guide` with your platform for complete dependency list
- Check system package manager (apt, yum, brew)
- Verify compiler toolchain for native extensions

### Configuration Issues

**Invalid configuration JSON**:
- Use `sdk_guide` to generate valid configuration
- Validate JSON syntax (use online validator)
- Check for missing required fields
- Verify paths exist and are accessible

**Database schema not initialized**:
- Use `sdk_guide` with `topic: "configure"` to initialize schema
- Verify database user has CREATE TABLE permissions
- Check database connection before initialization

## Getting Help

### Before Submitting Feedback

Gather this information:
1. Senzing SDK version
2. Operating system and version
3. Database type and version
4. Error messages (full text)
5. Steps to reproduce
6. Sample data (if applicable, anonymized)

### Submit Feedback

Use `submit_feedback` with:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Any error messages
- Your environment details

### Support Resources

- **Documentation**: Use `search_docs` for indexed documentation
- **Examples**: Use `find_examples` for working code
- **Community**: Senzing community forums
- **Support**: https://senzing.zendesk.com/hc/en-us/requests/new
