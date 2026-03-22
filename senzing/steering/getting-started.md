# Senzing — Getting Started

This guide helps you get started with Senzing entity resolution quickly.

## MCP Tool Catalog

Always call `get_capabilities` first to discover available tools and workflows.

| Tool | Purpose | When to Use |
| --- | --- | --- |
| `get_capabilities` | Discover all tools and workflows | First call in any Senzing session |
| `mapping_workflow` | 7-step interactive data mapping to Senzing JSON | Mapping source data to Senzing format |
| `lint_record` | Validate mapped records | After creating or editing mapped JSON |
| `analyze_record` | Analyze mapped data quality | After mapping, before loading |
| `generate_scaffold` | Generate SDK code (Python, Java, C#, Rust) | Creating loader, query, or pipeline code |
| `sdk_guide` | Platform-specific SDK installation and setup | Installing Senzing, setting up pipelines |
| `get_sample_data` | Sample datasets (Las Vegas, London, Moscow) | Testing and learning |
| `find_examples` | Working code from 27 Senzing GitHub repos | Looking for real-world patterns |
| `search_docs` | Search indexed Senzing documentation | Any Senzing question |
| `explain_error_code` | Diagnose Senzing errors (456 codes) | When errors occur |
| `get_sdk_reference` | SDK method signatures and flags | Checking method names, parameters, flags |
| `download_resource` | Download SDK packages and resources | Installing SDK components |
| `submit_feedback` | Submit feedback about the MCP server | Reporting issues or suggestions |

**Key principle**: Tools like `mapping_workflow`, `generate_scaffold`, and `sdk_guide` produce validated, version-correct output. Always prefer them over hand-coding.

## Decision Tree: Choosing the Right Tool

**"I need to..."**

- **...understand what's available** → `get_capabilities`
- **...map source data to Senzing format** → `mapping_workflow`
- **...validate my mapped data** → `lint_record` (validation) or `analyze_record` (quality analysis)
- **...write code to load/query data** → `generate_scaffold` (for code) or `sdk_guide` (for setup)
- **...get sample data for testing** → `get_sample_data`
- **...find working code examples** → `find_examples`
- **...understand a Senzing concept** → `search_docs`
- **...diagnose an error** → `explain_error_code`
- **...check method signatures** → `get_sdk_reference`
- **...install Senzing** → `sdk_guide` with your platform
- **...report an issue** → `submit_feedback`

**"What database should I use?"**

- **Evaluation/POC** (< 100K records) → SQLite (included with SDK)
- **Production** (> 100K records) → PostgreSQL (recommended) or MS SQL Server
- **Never use** → SQLite for production workloads

**"What language should I use?"**

- **Python** → Best documentation, most examples, fastest to prototype
- **Java** → Enterprise environments, Spring integration
- **C#** → .NET environments, Windows deployments
- **Rust** → High-performance, systems programming

## Common Workflows

### Workflow 1: Evaluate Senzing (First Time)
```
get_capabilities → get_sample_data → sdk_guide (install) → 
generate_scaffold (full_pipeline) → load sample data → query results
```

### Workflow 2: Map New Data Source
```
mapping_workflow (start) → mapping_workflow (advance through steps) → 
lint_record → analyze_record → generate_scaffold (add_records)
```

### Workflow 3: Production Deployment
```
search_docs (category: "deployment") → sdk_guide (platform-specific) → 
generate_scaffold (full_pipeline) → search_docs (category: "database") → 
deploy and monitor
```

### Workflow 4: Troubleshoot Issues
```
explain_error_code → search_docs (category: "troubleshooting") → 
find_examples → get_sdk_reference
```

## Data Flow Diagram

```
┌─────────────┐
│ Source Data │ (CSV, JSON, Database)
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ mapping_workflow│ Transform to Senzing JSON
└──────┬──────────┘
       │
       ▼
┌─────────────┐
│ lint_record │ Validate format
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Senzing Engine   │ Load & Resolve
│ (add_record)     │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Entity Repository│ Resolved entities stored
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Query & Export   │ search_by_attributes, get_entity, why_entities
└──────────────────┘
```

## Mapping Workflow State Transitions

```
START
  │
  ▼
┌──────────────┐
│ File Upload  │ Provide source files
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Profiling    │ Analyze data structure
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Entity Plan  │ Define entity types
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Field Mapping│ Map fields to Senzing attributes
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Review       │ Validate mappings
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Generate     │ Create mapped JSON
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Complete     │ Download mapped data
└──────────────┘
```

## Database Selection Decision Tree

```
How many records?
│
├─ < 100K records
│  └─ Use SQLite (included, no setup)
│
├─ 100K - 10M records
│  └─ Use PostgreSQL (recommended)
│     ├─ Single server: Standard PostgreSQL
│     └─ High availability: PostgreSQL with replication
│
└─ > 10M records
   └─ Use PostgreSQL with clustering
      ├─ Partitioning for very large datasets
      └─ Consider Senzing support for architecture review
```

## Entity Resolution Design Patterns

Common business problems that Senzing entity resolution addresses:

| Pattern | Use Case | Key Matching Criteria |
| --- | --- | --- |
| Customer 360 | Unified customer view across systems | Names, emails, phones, addresses |
| Fraud Detection | Identify fraud rings and suspicious networks | Names, addresses, devices, IPs |
| Data Migration | Merge and deduplicate during system consolidation | All available identifiers |
| Compliance Screening | Watchlist and sanctions matching | Names, DOB, nationalities, IDs |
| Marketing Dedup | Eliminate duplicate contacts | Names, addresses, emails |
| Patient Matching | Unified medical records across providers | Names, DOB, SSN, MRNs |
| Vendor MDM | Clean vendor/supplier master data | Company names, tax IDs, addresses |
| Claims Fraud | Detect staged accidents and fraud rings | Names, vehicles, providers |
| KYC/Onboarding | Verify identity during account opening | Names, DOB, SSN, government IDs |
| Supply Chain | Unified supplier view across divisions | Company names, GLNs, tax IDs |

When a user describes their problem, help them identify which pattern best fits their situation. This sets realistic expectations for matching criteria, data sources, and outcomes.
