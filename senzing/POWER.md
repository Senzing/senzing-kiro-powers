---
name: "senzing"
displayName: "Senzing"
description: "Entity resolution and identity matching. Map data, generate SDK code, search documentation, troubleshoot errors, and access sample datasets."
keywords: ["senzing", "entity-resolution", "identity-resolution", "deduplication", "mdm", "record-linkage", "fuzzy-matching"]
author: "Senzing"
---

# Senzing Entity Resolution

AI-powered entity resolution for deduplication, identity matching, and master data management.

## What is Senzing?

Senzing provides real-time entity resolution that identifies when different records refer to the same person, organization, or entity. Use it for:

- Customer 360 and unified customer views
- Fraud detection and network analysis
- Data deduplication and cleansing
- Compliance screening and watchlist matching
- Master data management (MDM)

## Quick Start

The Senzing MCP server provides 14 specialized tools for entity resolution workflows. Start here:

```
Call get_capabilities with version="current" to see all available tools and workflows
```

This returns:
- Complete tool catalog with descriptions and examples
- Suggested workflows for common tasks
- Getting started guidance
- Coverage areas (data mapping, SDK, documentation, troubleshooting, etc.)

## Common Tasks

**Map your data to Senzing format:**
```
Use mapping_workflow - Interactive 7-step guided workflow
```

**Generate SDK code:**
```
Use generate_scaffold - Python, Java, C#, Rust, TypeScript
```

**Search documentation:**
```
Use search_docs - Covers pricing, architecture, deployment, SDK, database tuning
```

**Troubleshoot errors:**
```
Use explain_error_code - 456 error codes with solutions
```

**Get sample data:**
```
Use get_sample_data - Las Vegas, London, Moscow datasets
```

**Find code examples:**
```
Use find_examples - 27+ GitHub repos with working code
```

## Why Use This Power?

The Senzing MCP server provides:

- **No guessing**: Tools generate validated attribute names, method signatures, and configurations
- **Current documentation**: Indexed from official Senzing sources
- **Working code**: Real examples from GitHub repositories with provenance
- **Guided workflows**: Step-by-step assistance for complex tasks
- **Comprehensive coverage**: Entity specification, SDK docs, quickstart guides, database tuning, error codes, release notes

## Prerequisites

- Internet connection to https://mcp.senzing.com
- Firewall allows HTTPS traffic (port 443)

For SDK usage (optional):
- Python 3.8+, Java 11+, C# .NET 6+, or Rust 1.70+
- Database: SQLite (included) or PostgreSQL for production

## Getting Help

All documentation and guidance is provided by the MCP server tools:

1. **Start with capabilities**: `get_capabilities(version="current")`
2. **Search for topics**: `search_docs(query="your question", version="current")`
3. **Find examples**: `find_examples(query="your use case")`
4. **Get SDK help**: `sdk_guide(topic="install", platform="linux_apt", version="current")`
5. **Report issues**: `submit_feedback(message="your feedback", category="bug")`

## Data Privacy

- The MCP server processes requests remotely at https://mcp.senzing.com
- `mapping_workflow` sends source data for analysis (not stored beyond session)
- `get_sample_data` returns publicly available datasets
- All communication uses HTTPS encryption
- For sensitive data, consult your organization's data handling policies

## Additional Resources

- [Senzing Homepage](https://senzing.com)
- [Official Documentation](https://senzing.com/documentation)
- [Support Portal](https://senzing.zendesk.com/hc/en-us/requests/new)
- [GitHub](https://github.com/senzing)

## License

This power integrates with senzing-mcp-server (Apache-2.0).

**MCP Server**: https://mcp.senzing.com/mcp  
**Server Version**: 0.24.2  
**Senzing SDK**: 4.0+
