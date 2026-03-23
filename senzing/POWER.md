---
name: "senzing"
displayName: "Senzing"
description: "Resolve entities, deduplicate records, and match identities with Senzing -- includes data mapping, SDK scaffolding, and deployment guidance."
keywords:
  [
    "senzing",
    "entity-resolution",
    "identity-resolution",
    "deduplication",
    "mdm",
    "record-linkage",
    "fuzzy-matching",
  ]
author: "Senzing"
---

# Senzing

This power connects to the Senzing MCP server. All Senzing domain knowledge is served by the MCP tools -- never hand-code Senzing JSON, attribute names, or SDK calls from training data.

Call `get_capabilities(version="current")` first to discover available tools and suggested workflows.

## Workflows

These show how to chain MCP tools for common goals. Tool names come from `get_capabilities`; if a tool listed here is not found, re-check capabilities for renames or replacements.

**Evaluate**: `get_capabilities` -> `get_sample_data` -> `sdk_guide(topic="full_pipeline")` -> `generate_scaffold(workflow="full_pipeline")` (supports Python, Java, C#, Rust, TypeScript/Node.js) -> load -> query

**Map data**: `mapping_workflow(action="start")` -> advance steps -> `lint_record` -> `analyze_record` -> `generate_scaffold(workflow="add_records")`

**Deploy**: `search_docs(category="deployment")` -> `sdk_guide(topic="install")` (includes direct package downloads for firewalled environments) -> `generate_scaffold(workflow="full_pipeline")` -> `search_docs(category="database")`

**Troubleshoot**: `explain_error_code` -> `search_docs` -> `find_examples` -> `get_sdk_reference`

**Migrate V3->V4**: `get_sdk_reference(topic="migration")` -> `get_sdk_reference(topic="flags")` -> `search_docs(query="migration")`

**Report**: `reporting_guide(topic="export")` -> `reporting_guide(topic="reports")` -> `reporting_guide(topic="data_mart")` -> `reporting_guide(topic="dashboard")` -> `reporting_guide(topic="graph")`

**Check pitfalls**: `search_docs(category="anti_patterns")` -> review results -> `sdk_guide` also returns anti-patterns inline

## Critical Rules

1. **Never hand-code Senzing JSON** -- use `mapping_workflow`. Training data produces wrong attribute names (e.g., `BUSINESS_NAME` vs correct `NAME_ORG`).
2. **Never guess SDK methods** -- use `generate_scaffold` or `get_sdk_reference`. Methods changed between V3 and V4.
3. **Check anti-patterns** -- before recommending installation or deployment: `search_docs(query="topic", category="anti_patterns")`.
4. **MCP first for all Senzing questions** -- `search_docs` covers pricing, architecture, deployment, SDK, database tuning, globalization, and more. It reflects current releases.
5. **Discover tools dynamically** -- call `get_capabilities` rather than assuming tool names from this file or training data.

## Entity Resolution Concepts

- **Entity** — A real-world person, organization, or object represented by one or more records across data sources.
- **Feature** — An attribute used for matching: NAME, ADDRESS, PHONE, DOB, SSN, PASSPORT, etc. Senzing supports 100+ features across 30+ feature types.
- **Data Source** — A labeled origin for records (e.g., "CUSTOMERS", "WATCHLIST"). Every record must have a DATA_SOURCE and RECORD_ID.
- **Entity Type** — PERSON or ORGANIZATION (default: PERSON).
- **Matched** — Records confirmed as the same entity.
- **Possible Match** — Records that might be the same entity but need review.
- **Relationship** — A declared or discovered connection between entities.
- **DSR (Disclosed, Sized, Resolved)** — Senzing's pricing unit. One DSR equals one record loaded into the engine.

## Examples

### Example 1: Map a CSV file

```
User: "I have a customer CSV at /data/customers.csv I need to load into Senzing"
→ Call mapping_workflow(action='start', file_paths=['/data/customers.csv'])
→ Walk through all 5 steps, passing state each time
→ Run lint_record on the output JSONL
→ Run analyze_record to check quality
```

### Example 2: Set up Senzing SDK on Linux

```
User: "Help me install and set up the Senzing SDK on Ubuntu"
→ Call sdk_guide(topic='install', platform='linux_apt', version='current')
→ Present install commands and engine config
→ If user has firewall issues, use the direct_download URLs from the response
→ Call sdk_guide(topic='configure', platform='linux_apt', language='python', version='current')
→ Present configuration code
```

### Example 3: Generate Python loader code

```
User: "Write me Python code to initialize Senzing and load records"
→ Call generate_scaffold(language='python', version='current', workflow='initialize')
→ Call generate_scaffold(language='python', version='current', workflow='add_records')
→ Combine and present the code
```

### Example 4: Debug an error

```
User: "I'm getting SENZ7234 when loading records"
→ Call explain_error_code(error_code='7234', version='current')
→ Present causes and resolution steps
→ Use search_docs if additional context is needed
```
