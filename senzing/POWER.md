---
name: "senzing"
displayName: "Senzing"
description: "Senzing entity resolution. Covers data mapping, SDK setup, loading, performance testing, security hardening, monitoring, and production deployment."
keywords: ["senzing", "entity-resolution", "identity-resolution", "deduplication", "mdm", "record-linkage", "fuzzy-matching"]
author: "Senzing"
---

# Senzing

> **Entity Resolution and Identity Matching** - Comprehensive Senzing integration covering data mapping, SDK setup, performance optimization, security, and production deployment.

**Quick Links**: [Homepage](https://senzing.com) | [Documentation](https://senzing.com/documentation) | [Support](https://senzing.zendesk.com/hc/en-us/requests/new) | [GitHub](https://github.com/senzing)

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [5-Minute Quick Start](#5-minute-quick-start)
- [Quick Start](#quick-start)
- [Available Steering Files](#available-steering-files)
- [Code Examples](#code-examples)
- [Available MCP Tools](#available-mcp-tools)
- [Common Workflows](#common-workflows)
- [Version Compatibility](#version-compatibility)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
  - [Quick Reference: Top 5 Issues](#quick-reference-top-5-issues)
- [Data Privacy and Security](#data-privacy-and-security)
- [Detailed Guidance](#detailed-guidance)
- [Additional Resources](#additional-resources)

---

## Prerequisites

Before using this power, ensure you have:

- ✅ **Kiro IDE** installed and running
- ✅ **Internet connection** for MCP server access (see [offline-mode.md](steering/offline-mode.md) for alternatives)
- ✅ **Senzing power** installed in Kiro
- ✅ **Basic understanding** of entity resolution concepts (optional but helpful)

**Optional for SDK usage**:

- Python 3.8+, Java 11+, C# .NET 6+, or Rust 1.70+ (depending on your language choice)
- Database: SQLite (included) or PostgreSQL for production

**Network requirements**:

- HTTPS access to `mcp.senzing.com` (port 443)
- Firewall rules allowing outbound HTTPS traffic

Ready? Let's get started! 👇

---

## 5-Minute Quick Start

Get up and running with Senzing in 5 minutes:

### Step 1: Verify Connection (30 seconds)

```python
# Check that the MCP server is accessible
get_capabilities(version="current")
```

✅ You should see server information and available tools.

### Step 2: Get Sample Data (1 minute)

```python
# Download 10 sample records from Las Vegas dataset
get_sample_data(dataset="las-vegas", limit=10)
```

✅ You should see sample customer records in Senzing JSON format.

### Step 3: Try a Quick Search (1 minute)

```python
# Search documentation for a topic
search_docs(query="getting started", version="current")
```

✅ You should see relevant documentation snippets.

### Step 4: Generate Your First Code (2 minutes)

```python
# Generate a complete Python loader script
generate_scaffold(
    language="python",
    workflow="full_pipeline",
    version="current"
)
```

✅ You should see working Python code with imports, initialization, and loading logic.

### Step 5: Explore More (30 seconds)

```python
# Find real code examples
find_examples(query="load records", language="python")
```

✅ You should see actual code from Senzing GitHub repositories.

**🎉 Success!** You've just used 5 different Senzing MCP tools. Ready for more? Continue to the [Quick Start](#quick-start) section below.

---

## Quick Start

New to Senzing? Follow this sequence:

1. **Discover capabilities**: `get_capabilities` with `version: "current"`
2. **Get sample data**: `get_sample_data` with `dataset: "las-vegas"` and `limit: 100`
3. **Map your data**: `mapping_workflow` with `action: "start"` and your file paths
4. **Validate mapping**: `lint_record` with your mapped file paths
5. **Generate loader code**: `generate_scaffold` with `language: "python"`, `workflow: "full_pipeline"`, `version: "current"`

Typical workflow: Map data → Validate → Generate loader → Load → Query results

## Available Steering Files

This power includes 19 comprehensive steering guides for detailed workflows and advanced topics:

**Core Guides**:

- **getting-started.md** - Quick start, decision trees, common workflows
- **quick-reference.md** - Copy-paste ready commands and one-liners
- **examples.md** - Code examples (Python, Java, C#, Rust)

**Best Practices & Optimization**:

- **best-practices.md** - Do's, don'ts, common pitfalls
- **performance.md** - Optimization, tuning, scaling strategies
- **troubleshooting.md** - Error handling, debugging, typical sessions

**Advanced Topics**:

- **advanced-topics.md** - Custom config, network analysis, graph traversal
- **use-cases.md** - 5 real-world implementation walkthroughs with metrics
- **security-compliance.md** - GDPR, CCPA, PII handling, access control
- **monitoring.md** - Metrics, Prometheus, Grafana, alerting, dashboards

**Integration & Deployment**:

- **data-sources.md** - 20+ system integrations (CRM, ERP, e-commerce)
- **cicd.md** - GitHub Actions, GitLab CI, Jenkins, deployment automation
- **config-examples.md** - Configuration examples for 8+ scenarios
- **offline-mode.md** - Offline usage and air-gapped deployment guidance

**Reference & Support**:

- **reference.md** - Tool parameters, checklists, glossary (50+ terms)
- **faq.md** - 100+ questions covering all topics
- **community.md** - Resources, support, learning materials
- **smoke-test.md** - Quick and detailed validation procedures
- **steering.md** - Navigation hub with quick links and task-based index

## Code Examples

Here are practical examples to get you started:

### Example 1: Map and Validate Data

```python
# Start mapping workflow with your CSV file
response = mapping_workflow(
    action="start",
    file_paths=["customers.csv"],
    version="current"
)

# Follow the interactive prompts to map fields
# Then validate the mapped data
lint_record(
    file_paths=["customers_mapped.jsonl"],
    version="current"
)
```

### Example 2: Generate and Use SDK Code

```python
# Generate a complete Python loader
code = generate_scaffold(
    language="python",
    workflow="full_pipeline",
    version="current"
)

# Save the generated code
with open("senzing_loader.py", "w") as f:
    f.write(code)

# The generated code includes:
# - Senzing SDK initialization
# - Database configuration
# - Record loading with error handling
# - Entity querying examples
```

### Example 3: Search for Help

```python
# Get help with error codes
explain_error_code(
    error_code="SENZ0005",
    version="current"
)

# Search documentation
search_docs(
    query="performance tuning",
    category="performance",
    version="current"
)

# Find working examples
find_examples(
    query="batch loading",
    language="python"
)
```

### Example 4: Get Sample Data for Testing

```python
# List available datasets
datasets = get_sample_data(dataset="list")

# Get 100 records from Las Vegas dataset
data = get_sample_data(
    dataset="las-vegas",
    limit=100
)

# The data is ready to load into Senzing
# Each record has proper Senzing JSON format
```

**💡 Tip**: All these examples work immediately - no setup required! For more examples, see [steering/examples.md](steering/examples.md).

## Available MCP Tools

The Senzing MCP server provides 12 tools for entity resolution workflows:

**Most Commonly Used**:

- `get_capabilities` — Discover all tools and workflows (call this first)
- `mapping_workflow` — 7-step interactive data mapping to Senzing JSON
- `generate_scaffold` — Generate SDK code (Python, Java, C#, Rust)
- `search_docs` — Search indexed Senzing documentation

**Data Validation & Quality**:

- `lint_record` — Validate mapped data format and structure
- `analyze_record` — Analyze mapped data quality and coverage

**SDK & Installation**:

- `sdk_guide` — Platform-specific SDK installation and setup
- `get_sdk_reference` — SDK method signatures and flags
- `download_resource` — Download SDK packages

**Examples & Learning**:

- `get_sample_data` — Sample datasets for testing (CORD collections)
- `find_examples` — Working code from 27 Senzing GitHub repos

**Support & Troubleshooting**:

- `explain_error_code` — Diagnose Senzing errors (456 codes)
- `submit_feedback` — Report issues or suggestions

## Common Workflows

### Evaluate Senzing (First Time)

```text
get_capabilities → get_sample_data → sdk_guide (install) → 
generate_scaffold (full_pipeline) → load sample data → query results
```

### Map New Data Source

```text
mapping_workflow (start) → mapping_workflow (advance through steps) → 
lint_record → analyze_record → generate_scaffold (add_records)
```

### Production Deployment

```text
search_docs (category: "deployment") → sdk_guide (platform-specific) → 
generate_scaffold (full_pipeline) → search_docs (category: "database") → 
deploy and monitor
```

### Troubleshoot Issues

```text
explain_error_code → search_docs (category: "troubleshooting") → 
find_examples → get_sdk_reference
```

## Version Compatibility

- **Senzing SDK**: 4.0+ (current version)
- **MCP Server**: Latest version at mcp.senzing.com
- **Python SDK**: 4.0+
- **Java SDK**: 4.0+
- **C# SDK**: 4.0+
- **Rust SDK**: 4.0+

## Best Practices

- Always call `get_capabilities` first when starting a Senzing session
- Never hand-code Senzing JSON mappings — use `mapping_workflow` for validated attribute names
- Never guess SDK method signatures — use `generate_scaffold` or `sdk_guide`
- Check `search_docs` with category `anti_patterns` before recommending installation or deployment approaches
- Start with SQLite for evaluation; recommend PostgreSQL for production

## Troubleshooting

### Quick Reference: Top 5 Issues

#### 1. 🔌 Cannot Connect to MCP Server

**Symptoms**: All MCP tools fail with connection errors  
**Quick Fix**:

```python
# Test connectivity
get_capabilities(version="current")
```

**Solutions**:

- Check internet connection
- Verify firewall allows HTTPS to `mcp.senzing.com` (port 443)
- Check `mcp.json` timeout setting (increase if needed)
- Try: `curl -I https://mcp.senzing.com/status`

#### 2. ❌ Wrong Attribute Names in Mapped Data

**Symptoms**: Records fail validation, attribute names rejected  
**Quick Fix**: Never hand-code attribute names - always use `mapping_workflow`

```python
# Use mapping workflow instead of guessing
mapping_workflow(
    action="start",
    file_paths=["your_data.csv"],
    version="current"
)
```

**Common Mistakes**:

- ❌ `BUSINESS_NAME` → ✅ `NAME_ORG`
- ❌ `FULL_NAME` → ✅ `NAME_FULL`
- ❌ `EMAIL` → ✅ `EMAIL_ADDRESS`
- ❌ `PHONE` → ✅ `PHONE_NUMBER`

#### 3. 🐛 SDK Method Not Found / Wrong Signature

**Symptoms**: `AttributeError`, method doesn't exist, wrong parameters  
**Quick Fix**: Generate code instead of guessing

```python
# Generate correct SDK code
generate_scaffold(
    language="python",
    workflow="full_pipeline",
    version="current"
)
```

**Why**: Method names changed between V3 and V4. Always use code generation.

#### 4. 🔢 Error Code: SENZ0000

**Symptoms**: Senzing returns error code like `SENZ0005`  
**Quick Fix**:

```python
# Get detailed explanation
explain_error_code(
    error_code="SENZ0005",  # or just "5" or "0005"
    version="current"
)
```

**Common Codes**:

- `SENZ0001`: Configuration error
- `SENZ0005`: Database connection issue
- `SENZ0025`: Invalid JSON format

#### 5. 🐌 Slow Performance / Timeouts

**Symptoms**: Operations take too long, timeout errors  
**Quick Fixes**:

- Increase timeout in `mcp.json`: `"timeout": 60000` (60 seconds)
- Check network latency to `mcp.senzing.com`
- For large files, process in smaller batches
- See [steering/performance.md](steering/performance.md) for optimization

**Still Having Issues?**

- 📖 Full troubleshooting guide: [steering/troubleshooting.md](steering/troubleshooting.md)
- 🔍 Search docs: `search_docs(query="your issue", version="current")`
- 💬 Submit feedback: `submit_feedback(message="describe issue", category="bug")`

---

### Detailed Troubleshooting

- **Wrong attribute names**: Never guess Senzing attribute names (e.g., `NAME_ORG` not `BUSINESS_NAME_ORG`). Use `mapping_workflow`.
- **Wrong method signatures**: Never guess SDK methods. Use `generate_scaffold` or `get_sdk_reference`.
- **Error codes**: Use `explain_error_code` with the code (accepts `SENZ0005`, `0005`, or `5`).
- **Configuration issues**: Use `search_docs` with category `configuration` or `database`.
- **Network/connectivity issues**: Check that <https://mcp.senzing.com> is reachable. Verify firewall rules allow HTTPS traffic. Check timeout settings in `mcp.json`.
- **MCP server unavailable**: If the remote server is down, check status at <https://mcp.senzing.com/status> or contact support.
- **Tool failures**: If an MCP tool returns unexpected results, use `submit_feedback` to report the issue with details.
- **Rate limits**: The MCP server has no hard rate limits, but excessive concurrent requests may be throttled. Space out bulk operations.

## Data Privacy and Security

- **Remote MCP server**: The Senzing MCP server at mcp.senzing.com processes tool requests remotely
- **Data transmission**: When using `mapping_workflow`, source data is sent to the server for analysis and mapping
- **No data retention**: The MCP server does not store your source data or mapped records beyond the session
- **Sample data**: `get_sample_data` returns publicly available datasets (CORD collections)
- **Sensitive data**: For highly sensitive data, consider running mapping workflows locally or using on-premises Senzing installations
- **Network security**: All communication uses HTTPS encryption
- **Compliance**: Review your organization's data handling policies before using cloud-based mapping tools

For on-premises or air-gapped deployments, contact Senzing support for alternative deployment options.

## Detailed Guidance

See steering files for detailed workflows. Use the agent's `readSteering` action or navigate directly to these files:

- [steering/getting-started.md](steering/getting-started.md) - Quick start, decision trees, common workflows
- [steering/best-practices.md](steering/best-practices.md) - Best practices, anti-patterns, common pitfalls
- [steering/performance.md](steering/performance.md) - Performance tuning, database selection, optimization
- [steering/troubleshooting.md](steering/troubleshooting.md) - Error handling, debugging strategies, typical sessions
- [steering/examples.md](steering/examples.md) - Code examples and patterns
- [steering/reference.md](steering/reference.md) - Tool parameters, checklists, glossary

See the [Available Steering Files](#available-steering-files) section above for the complete list of 19 guides.

## Additional Resources

### Power Infrastructure

- [CHANGELOG.md](CHANGELOG.md) - Version history and release notes
- [validate_power.py](validate_power.py) - Automated validation script

### User Guides

- [steering/offline-mode.md](steering/offline-mode.md) - Offline usage and air-gapped deployments
- [steering/config-examples.md](steering/config-examples.md) - Configuration examples for all scenarios
- [steering/smoke-test.md](steering/smoke-test.md) - Quick validation and testing procedures

### License and Support

This power integrates with senzing-mcp-server (Apache-2.0).

- [Privacy Policy](https://mcp.senzing.com/privacy)
- [Support](https://senzing.zendesk.com/hc/en-us/requests/new)

---

**Package**: senzing-mcp-server  
**MCP Server**: <https://mcp.senzing.com/mcp>  
**License**: Apache-2.0
