---
name: "senzing"
displayName: "Senzing"
description: "Add entity resolution to your project with Senzing. This power connects the Senzing MCP server for data mapping, SDK setup, code generation, and deployment guidance."
keywords:
  [
    "senzing",
    "entity-resolution",
    "identity-resolution",
    "identity-graph",
    "identity-matching",
    "deduplication",
    "dedupe",
    "mdm",
    "master-data-management",
    "record-linkage",
    "record-linking",
    "record-matching",
    "fuzzy-matching",
    "kyc",
    "aml",
    "sanctions-screening",
    "watchlist-screening",
    "watchlist-matching",
    "patient-matching",
    "mpi",
    "continuous-vetting",
    "customer-360",
    "vendor-risk",
    "third-party-risk",
  ]
author: "Senzing"
---

# Senzing Entity Resolution — Kiro Power

Use this power whenever a task involves entity resolution, record linkage,
deduplication, or any interaction with the Senzing platform.

## What Is Senzing

Senzing provides real-time AI-powered entity resolution as an embeddable SDK.
It determines when two records refer to the same real-world entity (person,
organization, etc.) by analyzing names, addresses, identifiers, and other
attributes across data sources — without training data or manual rules.

## MCP Server Setup

The Senzing MCP server is configured in `mcp.json` and connects to:
`https://mcp.senzing.com/mcp`

The server works from pre-fetched documentation — it never connects to live
Senzing instances and never handles PII. It also hosts official Senzing SDK
packages for direct download in firewalled environments — `sdk_guide` returns
download URLs and install commands automatically.

## Getting Started

**Always call `get_capabilities(version="current")` first** to discover available
tools and suggested workflows. This ensures you're using current tool names and
methods rather than outdated patterns from training data.

## Tool Reference

The Senzing MCP server provides 14 tools across 6 categories. Start any Senzing
session by calling `get_capabilities` for an up-to-date tool listing.

### Data Mapping (4 tools)

- **mapping_workflow** — Interactive 8-step workflow: profile source data → plan entities → map fields → generate code → detect SDK → load test → validate → evaluate. State is client-side — always pass state back verbatim.
- **lint_record** — Returns a Python linter script to validate mapped Senzing JSON/JSONL files locally. No data leaves the client.
- **analyze_record** — Returns a Python analyzer script to examine feature distribution, attribute coverage, and data quality locally.
- **download_resource** — Fallback for fetching workflow resources (linter, analyzer, entity spec, mapping examples) when network restrictions block direct download.

### Documentation & Reference (3 tools)

- **search_docs** — Full-text search across entity specification, SDK guides, quickstarts, database tuning, pricing, architecture, globalization, EDA/data analysis, engine configuration, error codes, release notes, and PoC methodology. **Prefer this over web search for any Senzing question.** Use `category='anti_patterns'` to check for known pitfalls.
- **get_sdk_reference** — Authoritative SDK reference: method signatures, flags, response schemas, V3→V4 migration mappings. Topics: `migration`, `flags`, `response_schemas`, `functions`/`methods`/`classes`/`api`, `all`.
- **find_examples** — Search 27+ indexed GitHub repos for working code (Python, Java, C#, Rust, TypeScript/Node.js). Three modes: search by query, list files in a repo, or retrieve a specific file.

### SDK Setup & Code Generation (2 tools)

- **sdk_guide** — Guided SDK setup across 5 platforms (Linux apt/yum, macOS, Windows, Docker) and 4 languages. Covers install, configure, load, export, full_pipeline with decision trees, anti-patterns, and direct package download links for firewalled environments.
- **generate_scaffold** — Generates SDK scaffold code from real indexed GitHub snippets with source URLs for provenance. 10 workflows (initialize, configure, add_records, delete, query, redo, stewardship, information, error_handling, full_pipeline) in Python, Java, C#, Rust, or TypeScript/Node.js.

### Sample Data (1 tool)

- **get_sample_data** — Real data from CORD (Collections Of Relatable Data): las-vegas (US, 11 sources), london (international, 5 sources), moscow (Cyrillic, 6 sources). Use `dataset='list'` to discover available sets. Always present the `download_url` to the user.

### Reporting & Visualization (1 tool)

- **reporting_guide** — Guided reporting and visualization for entity resolution results. Provides SDK patterns for data extraction (5 languages), SQL analytics queries for aggregate reports, data mart schema (SQLite/PostgreSQL), visualization concepts, and anti-patterns. Topics: `export`, `reports`, `entity_views`, `data_mart`, `dashboard`, `graph`, `quality`.

### Troubleshooting (1 tool)

- **explain_error_code** — Explains any of 456 Senzing error codes with causes and resolution steps. Accepts SENZ0005, SENZ-0005, 0005, or just 5.

### Meta & Utility (2 tools)

- **get_capabilities** — Server version, capabilities overview, available tools, suggested workflows, and getting started guidance. **Call this first in any Senzing session.**
- **submit_feedback** — Send feedback to the MCP server maintainer. **Always preview the message with the user and get explicit confirmation before sending.** Never include PII unless the user approves.

## Key Workflows

These show how to chain MCP tools for common goals. Tool names come from `get_capabilities`; if a tool listed here is not found, re-check capabilities for renames or replacements.

### 1. Map Source Data to Senzing Format

This is the most common workflow:

1. Call `mapping_workflow` with `action='start'` and the source file paths
2. Walk through each step: Profile → Plan → Map → Codegen → Detect SDK → Load Test → Validate → Evaluate
3. At each step, pass the `state` object from the previous response verbatim
4. After codegen, use `lint_record` to validate the output JSON
5. Use `analyze_record` to check feature distribution and coverage
6. If scripts fail to download, use `download_resource`

**Tips:**

- The workflow generates a mapper script — run it locally to produce JSONL
- Profile step: read the source data yourself or run the profiler script
- Plan step: identify master entities vs. child records vs. relationships
- Map step: map every source field to a Senzing feature with a confidence score
- QA step: evaluate whether the output meets quality thresholds

### 2. Set Up the Senzing SDK

1. Call `sdk_guide` with `topic='install'` — it returns a platform decision tree
2. Call again with the chosen platform (e.g., `topic='install', platform='linux_apt'`)
   - For firewalled environments, the response includes `direct_download` with package URLs
3. Call `sdk_guide` with `topic='configure'` for engine configuration code
4. Call `sdk_guide` with `topic='load'` for record loading code
5. Or use `topic='full_pipeline'` for install + configure + load + export in one call

### 3. Generate SDK Integration Code

1. Call `generate_scaffold` with the target language and workflow
   - Start with `workflow='initialize'` for engine setup
   - Then `workflow='add_records'` for record loading
   - Use `workflow='full_pipeline'` for an end-to-end example
2. Call `find_examples` to find real-world usage patterns
3. Use `search_docs` for API details and deployment guidance

### 4. Troubleshoot Errors

1. Call `explain_error_code` with the code from the user's logs
2. Follow the resolution steps in the response
3. Call `search_docs` for additional context on the error class

### 5. Evaluate Senzing

1. `search_docs` — learn about architecture (embedded SDK, air-gapped deployment)
2. `search_docs` with query "pricing" — DSR pricing model
3. `get_sample_data` — get real test data from CORD datasets
4. `generate_scaffold` with `workflow='full_pipeline'` — end-to-end example

### 6. Migrate V3 to V4

1. `get_sdk_reference` with `topic='migration'` — all breaking changes
2. Filter by module: `topic='migration', filter='SzEngine'`
3. `get_sdk_reference` with `topic='flags'` — new flag system

### 7. Build ER Reporting

1. Call `reporting_guide` with `topic='export'` and your language to get data extraction code
2. Call `reporting_guide` with `topic='reports'` to get SQL for the 4 core aggregate reports
3. Call `reporting_guide` with `topic='data_mart'` to get the analytical schema
4. Call `reporting_guide` with `topic='dashboard'` for visualization concepts
5. Call `reporting_guide` with `topic='graph'` for network graph export patterns

### 8. Check for Common Pitfalls

Before recommending installation, architecture, or deployment approaches:

1. Call `search_docs` with `category='anti_patterns'` and a query describing what you plan to recommend
2. Review any matching anti-patterns before proceeding
3. Note: `sdk_guide` also returns topic-specific anti-patterns inline

### 9. Deploy Senzing

1. `search_docs` with your platform (e.g., "docker quickstart", "AWS deployment")
2. `search_docs` for database setup (PostgreSQL, MySQL, MSSQL)
3. `search_docs` for engine configuration and tuning guidance
4. `generate_scaffold` with `workflow='initialize'` for your language

## Workflow Shortcuts

**Evaluate**: `get_capabilities` → `get_sample_data` → `sdk_guide(topic="full_pipeline")` → `generate_scaffold(workflow="full_pipeline")` → load → query

**Map data**: `mapping_workflow(action="start")` → advance steps → `lint_record` → `analyze_record` → `generate_scaffold(workflow="add_records")`

**Deploy**: `search_docs(category="deployment")` → `sdk_guide(topic="install")` → `generate_scaffold(workflow="full_pipeline")` → `search_docs(category="database")`

**Troubleshoot**: `explain_error_code` → `search_docs` → `find_examples` → `get_sdk_reference`

**Migrate V3→V4**: `get_sdk_reference(topic="migration")` → `get_sdk_reference(topic="flags")` → `search_docs(query="migration")`

**Report**: `reporting_guide(topic="export")` → `reporting_guide(topic="reports")` → `reporting_guide(topic="data_mart")` → `reporting_guide(topic="dashboard")` → `reporting_guide(topic="graph")`

## Critical Rules

These rules are non-negotiable. Violating them produces incorrect output.

1. **Never hand-code Senzing JSON** — use `mapping_workflow`. Training data produces wrong attribute names (e.g., `BUSINESS_NAME` vs correct `NAME_ORG`).
2. **Never guess SDK methods** — use `generate_scaffold` or `get_sdk_reference`. Methods changed between V3 and V4.
3. **Check anti-patterns first** — before recommending installation or deployment: `search_docs(query="topic", category="anti_patterns")`.
4. **MCP first for all Senzing questions** — `search_docs` covers pricing, architecture, deployment, SDK, database tuning, globalization, and more. It reflects current releases — prefer it over training knowledge.
5. **Discover tools dynamically** — call `get_capabilities` rather than assuming tool names from this file or training data.

## Best Practices

- **Always call `get_capabilities` first** to get current tool count and workflows
- **Prefer `search_docs` over web search** for any Senzing-related question. The MCP server indexes authoritative content that may not rank well on the web
- **Pass state faithfully** in `mapping_workflow` — the server is stateless, all workflow state lives in the client
- **Never send source data to the server** — The `lint_record` and `analyze_record` tools return scripts that run locally. The mapping workflow sends field names and schema — not row-level data
- **Present `download_url`** from `get_sample_data` results directly to the user. Do not dump raw CORD records into the conversation — they are a preview only
- **Version parameter:** Most tools accept `version`. Use `"current"` for the latest Senzing version unless the user specifies V3 (use `"3.x"`)

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

```text
User: "I have a customer CSV at /data/customers.csv I need to load into Senzing"
→ Call mapping_workflow(action='start', file_paths=['/data/customers.csv'])
→ Walk through all 8 steps, passing state each time
→ Run lint_record on the output JSONL
→ Run analyze_record to check quality
```

### Example 2: Set up Senzing SDK on Linux

```text
User: "Help me install and set up the Senzing SDK on Ubuntu"
→ Call sdk_guide(topic='install', platform='linux_apt', version='current')
→ Present install commands and engine config
→ If user has firewall issues, use the direct_download URLs from the response
→ Call sdk_guide(topic='configure', platform='linux_apt', language='python', version='current')
→ Present configuration code
```

### Example 3: Generate Python loader code

```text
User: "Write me Python code to initialize Senzing and load records"
→ Call generate_scaffold(language='python', version='current', workflow='initialize')
→ Call generate_scaffold(language='python', version='current', workflow='add_records')
→ Combine and present the code
```

### Example 4: Debug an error

```text
User: "I'm getting SENZ7234 when loading records"
→ Call explain_error_code(error_code='7234', version='current')
→ Present causes and resolution steps
→ Use search_docs if additional context is needed
```

---

## Privacy & Support

### Privacy Policies

- Senzing [Privacy Notice](https://senzing.com/privacy-notice/)
- Senzing MCP server [Privacy Policy](https://mcp.senzing.com/privacy)

### Support

For technical support, questions, or to report issues with this power,
please [contact our support team](https://senzing.zendesk.com/hc/en-us/requests/new).
Support from Senzing is always free.

For API-related questions and developer resources, visit our [Developer Documentation](https://www.senzing.com/docs/).

### License

- Kiro Power licensed as Apache-2.0
- Senzing SDK [End User License Agreement (EULA)](https://senzing.com/end-user-license-agreement/)
- Request [Non-Production License](https://senzing.com/request-non-prod-license/)

### Service Information

This power connects to the [Senzing MCP service](https://mcp.senzing.com/),
which provides access to Senzing's SDK documentation and developer resources.
The service is hosted and maintained by senzing.com.
