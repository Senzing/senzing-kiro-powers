---
name: "senzing"
displayName: "Senzing"
description: "Resolve entities, deduplicate records, and match identities with Senzing -- includes data mapping, SDK scaffolding, and deployment guidance."
keywords: ["senzing", "entity-resolution", "identity-resolution", "deduplication", "mdm", "record-linkage", "fuzzy-matching"]
author: "Senzing"
---

# Senzing

This power connects to the Senzing MCP server. All Senzing domain knowledge is served by the MCP tools -- never hand-code Senzing JSON, attribute names, or SDK calls from training data.

Call `get_capabilities(version="current")` first to discover available tools and suggested workflows.

## Workflows

These show how to chain MCP tools for common goals. Tool names come from `get_capabilities`; if a tool listed here is not found, re-check capabilities for renames or replacements.

**Evaluate**: `get_capabilities` -> `get_sample_data` -> `sdk_guide(topic="full_pipeline")` -> `generate_scaffold(workflow="full_pipeline")` -> load -> query

**Map data**: `mapping_workflow(action="start")` -> advance steps -> `lint_record` -> `analyze_record` -> `generate_scaffold(workflow="add_records")`

**Deploy**: `search_docs(category="deployment")` -> `sdk_guide(topic="install")` -> `generate_scaffold(workflow="full_pipeline")` -> `search_docs(category="database")`

**Troubleshoot**: `explain_error_code` -> `search_docs` -> `find_examples` -> `get_sdk_reference`

**Migrate V3->V4**: `get_sdk_reference(topic="migration")` -> `get_sdk_reference(topic="flags")` -> `search_docs(query="migration")`

**Report**: `reporting_guide(topic="export")` -> `reporting_guide(topic="reports")` -> `reporting_guide(topic="data_mart")`

## Critical Rules

1. **Never hand-code Senzing JSON** -- use `mapping_workflow`. Training data produces wrong attribute names (e.g., `BUSINESS_NAME` vs correct `NAME_ORG`).
2. **Never guess SDK methods** -- use `generate_scaffold` or `get_sdk_reference`. Methods changed between V3 and V4.
3. **Check anti-patterns** -- before recommending installation or deployment: `search_docs(query="topic", category="anti_patterns")`.
4. **MCP first for all Senzing questions** -- `search_docs` covers pricing, architecture, deployment, SDK, database tuning, globalization, and more. It reflects current releases.
5. **Discover tools dynamically** -- call `get_capabilities` rather than assuming tool names from this file or training data.
