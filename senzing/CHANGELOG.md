# Changelog

All notable changes to the Senzing Kiro Power will be documented in this file.

## [1.1.0] - 2026-03-23

### Changed

**Redesigned as lightweight MCP activation layer**: Transformed from documentation repository to a focused power that delegates to the MCP server.

- **POWER.md**: Streamlined to 120 lines (from 429 lines)
  - Removed duplicate documentation that exists in MCP server
  - Focuses on quick start and directing users to MCP tools
  - Clear "call get_capabilities first" guidance
  - Essential information only: what Senzing does, common tasks, prerequisites

- **Steering files**: Consolidated to 1 focused guide (from 19 files)
  - Single guide: `using-senzing-mcp.md` - How to work with the MCP server effectively
  - Teaches tool selection, workflows, anti-patterns, and response patterns
  - Removed 18 redundant guides that duplicated MCP server content

- **Validation**: Updated `validate_power.py` to v1.1 standards
  - Validates lightweight activation layer design
  - Checks file sizes to prevent documentation bloat
  - Ensures power philosophy compliance

### Design Philosophy

This power follows the correct pattern for MCP integration:

- **Thin activation layer**: Configures MCP connection and provides quick start
- **Delegates to MCP server**: All documentation, examples, and guidance come from authoritative source
- **Single source of truth**: MCP server is always current and authoritative
- **Minimal maintenance**: No documentation synchronization needed

### Benefits

- 98% reduction in documentation size (~10,000 lines → ~200 lines)
- Always current information (from MCP server)
- No sync issues between power and MCP server
- Clearer purpose and easier maintenance
- Better user experience with authoritative responses

### User Guide

Start with the MCP server tools:

1. **Discover capabilities**: `get_capabilities(version="current")`
2. **Search documentation**: `search_docs(query="your question", version="current")`
3. **Find code examples**: `find_examples(query="your use case")`
4. **Generate SDK code**: `generate_scaffold(language="python", workflow="full_pipeline", version="current")`
5. **Map data**: `mapping_workflow(action="start", file_paths=["data.csv"], version="current")`

All 14 MCP tools provide comprehensive, up-to-date guidance.

### Migration from 1.0.0

The extensive steering files from v1.0.0 are no longer needed:
- All content is available via MCP tools
- Call `get_capabilities` to see what's available
- Use `search_docs` to find specific topics
- Use `find_examples` for working code samples

## [1.0.0] - 2026-03-22

### Added

Initial release with comprehensive documentation (now superseded by 1.1.0 redesign).

- POWER.md with 429 lines of documentation
- 19 steering guides with 10,000+ lines of content
- mcp.json configuration
- validate_power.py validation script

**Note**: This approach was redesigned in 1.1.0 to avoid duplicating MCP server content.

## Version Philosophy

**1.1.0+**: Lightweight activation layer - delegates to MCP server
**1.0.0**: Documentation repository - duplicated MCP server content (deprecated approach)

## Links

- [Senzing Homepage](https://senzing.com)
- [MCP Server](https://mcp.senzing.com/mcp)
- [Documentation](https://senzing.com/documentation)
- [Support](https://senzing.zendesk.com/hc/en-us/requests/new)
