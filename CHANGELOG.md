# Changelog

All notable changes to this project will be documented in this file.

The changelog format is based on [Keep a Changelog] and [CommonMark].
This project adheres to [Semantic Versioning].

## [1.0.1] - 2026-06-09

### Changed in 1.0.1

- Synced POWER.md with the public Senzing MCP server (v1.24.0): 13 tools (was 14)
- Removed the retired `lint_record` tool; its validation now lives in `analyze_record`
- Updated `find_examples` repo count to 37, `sdk_guide`/`generate_scaffold` to 5 languages
- Clarified official (Python, Java, C#) vs community (Rust, TypeScript/Node.js) SDKs
- Added the `evaluation` topic to `reporting_guide`
- Documented the required `workspace_dir` parameter for `mapping_workflow` and `analyze_record`
- Noted the platform-layer access caveat for `get_sample_data` record retrieval

## [1.0.0] - 2026-03-23

### Added to 1.0.0

- Comprehensive README with installation instructions and quick start examples
- Enhanced POWER.md with detailed tool reference organized by category
- 9 key workflows with step-by-step instructions
- Best practices section for optimal MCP server usage
- Version and license metadata in power frontmatter
- Compatibility information for MCP server requirements

### Changed in 1.0.0

- Upgraded from initial release (0.0.0) to production-ready 1.0.0
- Improved documentation structure based on senzing-mcp-skill reference
- Enhanced workflow descriptions with tips and anti-pattern checks
- Updated examples to reflect 8-step mapping workflow
- Added language specifications to code blocks for better rendering

## [0.0.0] - 2026-03-21

### Added to 0.0.0

- Initial Release

[CommonMark]: https://commonmark.org/
[Keep a Changelog]: https://keepachangelog.com/
[Semantic Versioning]: https://semver.org/
