# Changelog

All notable changes to the Senzing Kiro Power will be documented in this file.

## [2.0.0] - 2026-03-23

### Changed - BREAKING

**Complete redesign**: Transformed from documentation repository to lightweight MCP activation layer.

**Philosophy shift**: The power now delegates to the MCP server instead of duplicating its content.

- **POWER.md**: Reduced from 429 lines to ~100 lines
  - Removed duplicate documentation that exists in MCP server
  - Now focuses on quick start and directing users to MCP tools
  - Added clear "call get_capabilities first" guidance
  - Simplified to essential information only

- **Steering files**: Reduced from 19 files to 1 focused guide
  - Removed: 18 redundant guides (getting-started, quick-reference, best-practices, performance, troubleshooting, examples, use-cases, security-compliance, advanced-topics, monitoring, data-sources, cicd, faq, community, reference, config-examples, smoke-test, offline-mode, steering)
  - Added: `using-senzing-mcp.md` - Single guide on how to work with the MCP server effectively
  - New guide teaches tool selection, workflows, anti-patterns, and response patterns

### Why This Change?

**Problem**: The original power duplicated 10,000+ lines of documentation that already exists in the MCP server, creating:
- Maintenance burden (two sources of truth)
- Sync issues (power docs could become stale)
- Confusion (which source is authoritative?)
- Bloat (unnecessary duplication)

**Solution**: A Kiro power should be a thin activation layer that:
- Configures MCP server connection
- Provides quick start guidance
- Teaches users how to use MCP tools effectively
- Delegates all documentation/examples/guidance to the MCP server

**Result**: 
- Power is now ~95% smaller
- Single source of truth (MCP server)
- Always current (MCP server is authoritative)
- Easier to maintain
- Clearer purpose

### What Users Should Do

Instead of reading power documentation, users should:

1. **Start with**: `get_capabilities(version="current")`
2. **Search docs**: `search_docs(query="your question", version="current")`
3. **Find examples**: `find_examples(query="your use case")`
4. **Generate code**: `generate_scaffold(language="python", workflow="full_pipeline", version="current")`
5. **Get help**: All 14 MCP tools provide comprehensive guidance

### Migration from 1.0.0

If you were using the steering files for reference:
- All that content is available via MCP tools
- Call `get_capabilities` to see what's available
- Use `search_docs` to find specific topics
- Use `find_examples` for code samples

## [1.0.0] - 2026-03-22

### Added

Initial release with comprehensive documentation (now superseded by 2.0.0 redesign).

- POWER.md with 429 lines of documentation
- 19 steering guides with 10,000+ lines of content
- mcp.json configuration
- validate_power.py validation script

**Note**: This approach was redesigned in 2.0.0 to avoid duplicating MCP server content.

## Version Philosophy

**2.0.0+**: Lightweight activation layer - delegates to MCP server
**1.0.0**: Documentation repository - duplicated MCP server content (deprecated approach)

## Links

- [Senzing Homepage](https://senzing.com)
- [MCP Server](https://mcp.senzing.com/mcp)
- [Documentation](https://senzing.com/documentation)
- [Support](https://senzing.zendesk.com/hc/en-us/requests/new)
