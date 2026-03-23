---
inclusion: auto
---

# Working with Senzing MCP Server

This guide helps you effectively use the Senzing MCP server for entity resolution tasks.

## Critical First Step

**ALWAYS call `get_capabilities` first** when starting any Senzing-related work:

```
get_capabilities(version="current")
```

This returns:
- All 14 available tools with descriptions and examples
- Suggested workflows for common tasks
- Getting started guidance
- What the server can do

## Key Principle: Don't Duplicate, Delegate

The Senzing MCP server contains comprehensive documentation, code examples, and guidance. When a user asks about Senzing:

1. **Don't guess** - Use the MCP tools
2. **Don't hand-code** - Use `generate_scaffold` or `mapping_workflow`
3. **Don't search the web** - Use `search_docs` first
4. **Don't write documentation** - Reference the MCP server's responses

## Tool Selection Guide

**User wants to...**

- Understand what's available → `get_capabilities`
- Map source data → `mapping_workflow` (interactive 7-step workflow)
- Validate mapped data → `lint_record` or `analyze_record`
- Generate code → `generate_scaffold` (Python, Java, C#, Rust, TypeScript)
- Install Senzing → `sdk_guide` with platform and language
- Search documentation → `search_docs` with query and optional category
- Troubleshoot errors → `explain_error_code` with error code
- Get sample data → `get_sample_data` with dataset name
- Find code examples → `find_examples` with query
- Check SDK methods → `get_sdk_reference` with topic
- Build reports/dashboards → `reporting_guide` with topic
- Report issues → `submit_feedback` with message

## Common Workflows

The MCP server provides 9 suggested workflows via `get_capabilities`:

1. Map a Data Source
2. Get Started with the SDK
3. Troubleshoot an Error
4. Evaluate Senzing
5. Migrate V3 to V4
6. SDK Setup Guide
7. Build ER Reporting
8. Check for Common Pitfalls
9. Deploy Senzing

**Get workflow details**: Call `get_capabilities` and review the `suggested_workflows` section.

## Anti-Patterns to Avoid

❌ **Don't hand-code Senzing JSON mappings**
- Attribute names are specific (e.g., `NAME_ORG` not `BUSINESS_NAME`)
- Use `mapping_workflow` instead

❌ **Don't guess SDK method names**
- Method names changed between V3 and V4
- Use `generate_scaffold` or `get_sdk_reference` instead

❌ **Don't search the web for Senzing documentation**
- The MCP server has indexed official documentation
- Use `search_docs` first

❌ **Don't write installation instructions**
- Use `sdk_guide` which provides platform-specific commands

❌ **Don't create example code from memory**
- Use `find_examples` to get real working code from GitHub

## Response Pattern

When a user asks about Senzing:

1. **Identify the task** (mapping, coding, troubleshooting, etc.)
2. **Call the appropriate MCP tool** (don't guess or use training data)
3. **Present the MCP server's response** (it's authoritative)
4. **Offer to drill deeper** if needed (call additional tools)

## Example Interactions

**User**: "How do I map my customer data to Senzing?"

**Response**: Call `mapping_workflow(action="start", file_paths=["customers.csv"], version="current")` and guide them through the interactive workflow.

**User**: "What does error SENZ0005 mean?"

**Response**: Call `explain_error_code(error_code="SENZ0005", version="current")` and present the explanation.

**User**: "Show me Python code to load records"

**Response**: Call `generate_scaffold(language="python", workflow="add_records", version="current")` and present the generated code.

**User**: "How much does Senzing cost?"

**Response**: Call `search_docs(query="pricing", category="pricing", version="current")` and present the pricing information.

## State Management

Some tools maintain state (e.g., `mapping_workflow`):

- The server returns a `state` object in responses
- **Always pass this state back** in the next request
- Don't modify or reconstruct the state
- State is opaque and managed by the server

Example:
```
response1 = mapping_workflow(action="start", file_paths=["data.csv"], version="current")
state = response1["state"]

response2 = mapping_workflow(action="advance", state=state, data={...}, version="current")
state = response2["state"]
```

## Version Parameter

Most tools accept a `version` parameter:
- Use `"current"` for the latest Senzing SDK version (4.0+)
- Use `"3.x"` for legacy V3 support (limited to Python and Java)

## Categories for search_docs

When calling `search_docs`, use these categories for better results:

- `general` - Basic concepts and overview
- `sdk` - SDK usage and API reference
- `data_mapping` - Attribute names and mapping guidance
- `troubleshooting` - Error handling and debugging
- `pricing` - Pricing and licensing
- `deployment` - Installation and deployment
- `quickstart` - Getting started guides
- `configuration` - Engine configuration
- `database` - Database setup and tuning
- `performance` - Optimization and scaling
- `anti_patterns` - Common mistakes to avoid

## Data Privacy Note

- `mapping_workflow` sends source data to the server for analysis
- Data is not stored beyond the session
- For highly sensitive data, consult your organization's policies
- All communication uses HTTPS encryption

## When to Use Web Search

Only use web search for Senzing topics if:
1. You've already tried the relevant MCP tools
2. The MCP server doesn't have the information
3. You need information about third-party integrations not covered by Senzing

**Always try MCP tools first** - they have current, authoritative information.
