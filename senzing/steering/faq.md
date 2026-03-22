# Senzing — Frequently Asked Questions

## General Questions

### What is Senzing?
Senzing is an entity resolution engine that identifies and links records referring to the same real-world entity across multiple data sources. It uses AI-powered matching to resolve identities even when data is incomplete, inconsistent, or contains errors.

### How does Senzing differ from traditional deduplication?
Traditional deduplication typically uses exact or fuzzy matching on specific fields. Senzing uses probabilistic matching across multiple features, considers relationships between entities, and continuously learns from new data to improve accuracy.

### What is entity resolution?
Entity resolution is the process of determining which records in one or more datasets refer to the same real-world entity (person, organization, or thing), even when the records don't match exactly.

### Do I need to be a data scientist to use Senzing?
No. Senzing is designed to work out-of-the-box without requiring data science expertise. The MCP tools guide you through data mapping, and the SDK provides simple APIs for loading and querying data.

## Licensing and Pricing

### How is Senzing priced?
Senzing uses a DSR (Data Source Record) pricing model. One DSR = one record from one data source. For example, loading 1 million customer records from a CRM = 1 million DSRs.

### What is the evaluation limit?
The free evaluation license allows loading up to 500 records. This is sufficient for proof-of-concept testing and learning.

### Can I use Senzing for free?
Yes, for evaluation purposes (up to 500 records). For production use, contact Senzing sales for licensing.

### How do I get a production license?
Contact Senzing sales at https://senzing.com/contact or use `search_docs(query="licensing", category="pricing", version="current")`.

### What happens if I exceed the evaluation limit?
Loading will fail with error code SENZ0040 (License Limit Exceeded). You'll need to either delete records to stay under the limit or obtain a production license.

## Technical Questions

### What databases does Senzing support?
- **SQLite**: For evaluation and POC (< 100K records)
- **PostgreSQL**: Recommended for production (100K+ records)
- **MS SQL Server**: Supported for Windows environments
- **Oracle**: Contact Senzing for support
- **MySQL/MariaDB**: Not officially supported

### Can I use SQLite for production?
No. SQLite is single-threaded and doesn't scale beyond ~100K records. Always use PostgreSQL or MS SQL Server for production.

### What programming languages are supported?
- Python (best documentation, most examples)
- Java (enterprise environments)
- C# (.NET environments)
- Rust (high-performance applications)

### Does Senzing work with cloud databases?
Yes. Senzing works with cloud-hosted PostgreSQL (AWS RDS, Azure Database, Google Cloud SQL) and cloud-hosted MS SQL Server.

### Can I run Senzing in Docker?
Yes. Use `sdk_guide(topic="install", platform="docker", version="current")` for Docker setup instructions.

### Can I run Senzing in Kubernetes?
Yes. Senzing can be deployed in Kubernetes. Contact Senzing support for deployment guidance.

## Data Mapping Questions

### What is data mapping?
Data mapping is the process of transforming your source data fields into Senzing's standardized attribute format (e.g., mapping "full_name" to "NAME_FULL").

### Do I have to map data manually?
No. Use `mapping_workflow` which provides an interactive 7-step process to map your data with validation.

### What if my attribute names are wrong?
Wrong attribute names are the most common error. Always use `mapping_workflow` instead of guessing attribute names. Common mistakes: "BUSINESS_NAME_ORG" (wrong) vs "NAME_ORG" (correct).

### Can I map multiple files at once?
Yes. `mapping_workflow` accepts multiple file paths: `file_paths=["file1.csv", "file2.json"]`.

### What file formats are supported?
CSV, JSON, and JSONL are supported by `mapping_workflow`. For other formats, convert to one of these first.

### How do I handle missing data?
Senzing handles missing data gracefully. Include only the fields you have - don't create fake or placeholder values.

### What are DATA_SOURCE and RECORD_ID?
- **DATA_SOURCE**: Identifies which system the record came from (e.g., "CUSTOMERS", "VENDORS")
- **RECORD_ID**: Unique identifier for the record within that data source

Both are required for every record.

## Performance Questions

### How fast can Senzing load data?
- Small datasets (< 10K): 100-500 records/second
- Medium datasets (10K-1M): 500-2000 records/second
- Large datasets (> 1M): 2000-5000+ records/second (optimized, multi-threaded)

### How can I improve loading performance?
1. Use PostgreSQL instead of SQLite
2. Use multi-threading (4-8 threads)
3. Use larger batch sizes (1000-5000 records)
4. Disable redo processing during initial load
5. Tune database configuration
6. Use SSD storage

See [performance.md](performance.md) for detailed guidance.

### Why is my loading slow?
Common causes:
- Using SQLite (switch to PostgreSQL)
- Single-threaded loading (use multi-threading)
- Small batch sizes (increase to 1000+)
- Database not tuned (tune PostgreSQL)
- Slow disk (use SSD)
- Insufficient resources (add CPU/RAM)

### How long does it take to load 1 million records?
With optimized setup (PostgreSQL, multi-threading, tuned database):
- Initial load: 10-30 minutes
- With redo processing: 30-60 minutes

### Why are my queries slow?
Common causes:
- Database not tuned
- Insufficient indexes
- Complex search criteria
- Large result sets
- Database needs VACUUM/ANALYZE

## Matching Questions

### How does Senzing decide if records match?
Senzing uses probabilistic matching across multiple features (name, address, phone, email, etc.). It considers:
- Feature similarity scores
- Feature frequency (rare features weighted higher)
- Combinations of matching features
- Relationship networks

### Can I control matching strictness?
Basic matching rules are built-in and work well for most use cases. Custom threshold tuning requires Senzing support - contact them for advanced configuration.

### Why aren't my records matching?
Common causes:
- Insufficient matching data (need at least name + one other identifier)
- Data quality issues (typos, inconsistent formats)
- Wrong attribute types in mapping
- Data too generic (e.g., all records have same phone number)

Use `why_record_not_in_entity` to understand why specific records didn't match.

### Why are too many records matching?
Common causes:
- Generic or placeholder data (000-000-0000, test@test.com)
- Missing data (all records have same default value)
- Data quality issues

Use `why_entities` to understand why records matched, then improve data quality.

### What is a "match key"?
A match key describes which features caused records to match. Example: "+NAME+ADDRESS" means records matched on both name and address.

### What are match levels?
- **Level 1 (Resolved)**: High confidence, same entity
- **Level 2 (Possibly Same)**: Moderate confidence
- **Level 3 (Possibly Related)**: Low confidence, may be related
- **Level 4 (Name Only)**: Only name matches

## Error Questions

### How do I diagnose errors?
Use `explain_error_code(error_code="SENZ0005", version="current")` with your error code. Accepts formats: "SENZ0005", "0005", or "5".

### What is error SENZ0001?
Configuration error. Verify `SENZING_ENGINE_CONFIGURATION_JSON` is set correctly. Use `sdk_guide` to generate correct configuration.

### What is error SENZ0002?
Database connection error. Check:
- Database is running
- Connection string is correct
- Credentials are valid
- Firewall allows connection

### What is error SENZ0005?
Invalid record format. Common causes:
- Missing DATA_SOURCE or RECORD_ID
- Invalid JSON syntax
- Wrong attribute names

Use `lint_record` to validate records before loading.

### What is error SENZ0037?
Data source not registered. Use `sdk_guide(topic="configure", data_sources=["YOUR_SOURCE"])` to register it.

### What is error SENZ0040?
License limit exceeded (500 records for evaluation). Either delete records or obtain production license.

## Deployment Questions

### Can I deploy Senzing on-premises?
Yes. Senzing can be deployed on-premises on Linux, Windows, or macOS.

### Can I deploy Senzing in the cloud?
Yes. Senzing works on AWS, Azure, Google Cloud, and other cloud providers.

### Do I need internet access to use Senzing?
The Senzing SDK works offline once installed. The MCP server (mcp.senzing.com) requires internet access for tools like `mapping_workflow` and `search_docs`.

### How do I handle sensitive data?
See [security-compliance.md](security-compliance.md) for:
- Data encryption (at rest and in transit)
- Access control
- Audit logging
- GDPR/CCPA compliance
- PII handling best practices

### What are the system requirements?
**Minimum (evaluation)**:
- 4 CPU cores
- 8GB RAM
- 20GB disk space
- Linux, Windows, or macOS

**Recommended (production)**:
- 8+ CPU cores
- 16GB+ RAM
- 100GB+ SSD storage
- Linux (Ubuntu, RHEL, CentOS)
- PostgreSQL database

### Can I use Senzing with microservices?
Yes. See [use-cases.md](use-cases.md) for microservices architecture patterns.

## Integration Questions

### Can I integrate Senzing with Kafka?
Yes. See [examples.md](examples.md) for Kafka consumer example.

### Can I build a REST API with Senzing?
Yes. See [examples.md](examples.md) for Flask REST API example.

### Can I use Senzing with Spark?
Yes. Contact Senzing support for Spark integration guidance.

### Can I use Senzing with Airflow?
Yes. Senzing SDK can be called from Airflow tasks.

### Does Senzing have a web UI?
Senzing offers separate web UI products. Contact Senzing for details.

## Data Questions

### Can I delete records?
Yes. Use `engine.delete_record(data_source, record_id)`. This is required for GDPR/CCPA compliance.

### Can I update records?
Yes. Load the record again with the same DATA_SOURCE and RECORD_ID. Senzing will update it.

### Can I export resolved entities?
Yes. Use `sdk_guide(topic="export")` for export patterns.

### How do I back up my data?
Back up the PostgreSQL database using standard PostgreSQL backup tools (pg_dump, pg_basebackup).

### Can I migrate data between environments?
Yes. Export from source environment, load into target environment. Ensure both use same Senzing version.

### What happens to deleted records?
Deleted records are removed from the entity repository. Entities are re-evaluated and may split if the deleted record was the only link.

## Troubleshooting Questions

### Where can I find examples?
Use `find_examples(query="your search", language="python")` to search 27 Senzing GitHub repositories.

### Where is the documentation?
Use `search_docs(query="your question", version="current")` to search indexed Senzing documentation.

### How do I get help?
1. Use `search_docs` for documentation
2. Use `find_examples` for code examples
3. Use `explain_error_code` for error diagnosis
4. Contact Senzing support: https://senzing.zendesk.com
5. Use `submit_feedback` to report issues

### Can I see working code?
Yes. Use `generate_scaffold(language="python", workflow="full_pipeline", version="current")` for complete working code.

### How do I report bugs?
Use `submit_feedback(message="your bug report", category="bug")` or contact Senzing support.

## Comparison Questions

### Senzing vs. traditional MDM?
- **Senzing**: AI-powered, real-time, no rules to maintain
- **Traditional MDM**: Rule-based, batch processing, requires ongoing rule maintenance

### Senzing vs. fuzzy matching libraries?
- **Senzing**: Complete entity resolution with probabilistic matching, relationship analysis, and continuous learning
- **Fuzzy matching**: Simple string similarity, no entity resolution, no relationship analysis

### Senzing vs. building custom solution?
- **Senzing**: Production-ready, proven algorithms, ongoing support
- **Custom**: Requires data science expertise, ongoing maintenance, unproven accuracy

## Advanced Questions

### Can I customize matching rules?
Custom configuration requires Senzing support. Contact them for advanced tuning.

### Can I add custom entity types?
Custom entity types require configuration changes. Contact Senzing support.

### Can I use Senzing for graph analysis?
Yes. See [advanced-topics.md](advanced-topics.md) for network analysis and graph traversal patterns.

### Can I integrate with my ML pipeline?
Yes. Senzing SDK can be called from Python ML pipelines (scikit-learn, TensorFlow, PyTorch).

### Does Senzing support real-time streaming?
Yes. See [use-cases.md](use-cases.md) for Kafka streaming example.

## Getting Started

### I'm new to Senzing. Where do I start?
1. Call `get_capabilities(version="current")` to see available tools
2. Get sample data: `get_sample_data(dataset="las-vegas", limit=100)`
3. Follow [getting-started.md](getting-started.md) for complete walkthrough
4. Try the quick start in [quick-reference.md](quick-reference.md)

### What's the fastest way to see Senzing in action?
```python
# 30-minute quick start
get_capabilities(version="current")
get_sample_data(dataset="las-vegas", limit=100)
sdk_guide(topic="full_pipeline", platform="linux_apt", language="python", version="current")
# Follow the generated instructions
```

### Where can I find more resources?
- **Documentation**: `search_docs(query="topic", version="current")`
- **Examples**: `find_examples(query="topic", language="python")`
- **Guides**: See all steering files in senzing/steering/
- **Support**: https://senzing.zendesk.com
- **Website**: https://senzing.com

## Still Have Questions?

Use these tools to find answers:
```python
# Search documentation
search_docs(query="your question", version="current")

# Find code examples
find_examples(query="your topic", language="python")

# Get error help
explain_error_code(error_code="SENZ0005", version="current")

# Submit feedback
submit_feedback(message="your question", category="question")
```

Or contact Senzing support: https://senzing.zendesk.com/hc/en-us/requests/new
