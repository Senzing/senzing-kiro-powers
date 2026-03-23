# Senzing MCP Server -- Content Gap Report

**Date**: 2026-03-23
**Context**: Analysis from senzing-kiro-powers restructure to eliminate content duplication with the MCP server.

## Summary

During restructuring of the Kiro power to delegate to the MCP server rather than duplicate its content, we removed 15 steering files that overlapped with MCP tools. The MCP server covers the vast majority of what users need. We identified two areas where MCP coverage could be expanded -- both are Senzing-specific (not generic DevOps/infrastructure).

## Current MCP Coverage (Excellent)

The MCP server (v0.24.2, 14 tools) covers:

- Data mapping workflow (`mapping_workflow`, `lint_record`, `analyze_record`)
- SDK code generation across 5 languages (`generate_scaffold`)
- SDK installation and setup across 5 platforms (`sdk_guide`)
- Documentation search covering architecture, pricing, deployment, DB tuning, globalization, PoC methodology, anti-patterns (`search_docs`)
- Error diagnosis for 456 error codes (`explain_error_code`)
- Working code from 27+ GitHub repos (`find_examples`)
- SDK method signatures, flags, and V3-to-V4 migration (`get_sdk_reference`)
- Sample data from 3 CORD datasets (`get_sample_data`)
- Reporting and visualization patterns (`reporting_guide`)

## Potential Gap: Data Source Mapping Recipes

**What**: Pre-built field mapping templates for common source systems (e.g., "Salesforce Contact -> Senzing JSON"). The `mapping_workflow` tool handles the mechanics of mapping, but a user starting with Salesforce data doesn't know which Salesforce fields map to which Senzing features without domain knowledge of both systems.

**Scope check**: This is Senzing-specific -- it's about mapping external fields to Senzing's entity specification attributes.

**Suggested approach**: Could be an extension to `mapping_workflow` (e.g., `mapping_workflow(action="start", source_system="salesforce")` that pre-populates a suggested mapping) or a `search_docs` category for "source_recipes".

**Priority**: Medium. The mapping_workflow already guides users through profiling, so this is a convenience improvement.

## Potential Gap: Business Use Case Context

**What**: High-level descriptions of how entity resolution applies to specific business domains (Customer 360, fraud detection, KYC/compliance, data migration, vendor MDM). Not implementation details (covered by existing tools) but the "why" and "what to expect" context that helps users evaluate whether Senzing fits their needs and set realistic expectations.

**Scope check**: This is about entity resolution concepts and Senzing's applicability -- squarely in Senzing's domain.

**Suggested approach**: Could be a `search_docs` category for "use_cases" or a small set of indexed documents.

**Priority**: Low. Users evaluating Senzing likely get this from sales/marketing materials. The MCP server's `search_docs` may already cover some of this under architecture or PoC methodology.

## Out of Scope (Not Recommended for MCP)

The following topics were in the original Kiro power steering files but are generic infrastructure concerns, not Senzing-specific. They do not belong in the MCP server:

- **Operational monitoring** (Prometheus, Grafana, alerting) -- generic observability
- **CI/CD integration** (GitHub Actions, GitLab CI, Jenkins, K8s) -- generic DevOps
- **Security/compliance implementation** (GDPR deletion code, RBAC, audit logging) -- generic security patterns
- **Community resources** (learning materials, support channels) -- better served by website

## Files Removed from Kiro Power (Covered by MCP)

| Removed File | MCP Tool(s) That Cover It |
|---|---|
| examples.md | `generate_scaffold`, `find_examples` |
| quick-reference.md | `get_capabilities` |
| faq.md | `search_docs` |
| troubleshooting.md | `explain_error_code`, `search_docs` |
| best-practices.md | `search_docs` (anti_patterns category) |
| performance.md | `search_docs` (performance/database) |
| reference.md | `get_capabilities`, `get_sdk_reference` |
| advanced-topics.md | `search_docs`, `get_sdk_reference` |
| getting-started.md | `get_capabilities` (suggested_workflows) |
| community.md | `search_docs` |
| use-cases.md | `search_docs` (partially) |
| security-compliance.md | Out of scope |
| monitoring.md | Out of scope |
| cicd.md | Out of scope |
| data-sources.md | `mapping_workflow` (partially) |
