# Changelog

All notable changes to the Senzing Kiro Power will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Additional language examples (TypeScript, Go)
- Video tutorial references
- Interactive tutorials
- Community-contributed content

## [1.0.0] - 2026-03-22

### Added

#### Core Power Structure

- **POWER.md** - Main documentation with Power-Builder compliant frontmatter
  - Valid frontmatter fields: name, displayName, description, keywords, author
  - 7 optimized keywords for entity resolution domain
  - Comprehensive documentation (429 lines)
- **mcp.json** - Remote MCP server configuration
  - Server URL: <https://mcp.senzing.com/mcp>
  - Timeout: 30 seconds
  - Environment variables for logging control
- **CHANGELOG.md** - Version history and release notes
- **validate_power.py** - Automated validation script (400+ lines)

#### User Experience Enhancements

- **Table of Contents** in POWER.md for easier navigation (12 sections)
- **Prerequisites section** with clear requirements checklist
- **5-Minute Quick Start** for rapid onboarding with 5 practical steps
- **Code Examples section** with 4 copy-paste ready examples:
  - Map and validate data
  - Generate and use SDK code
  - Search for help
  - Get sample data for testing
- **Troubleshooting Quick Reference** with top 5 common issues:
  - Cannot connect to MCP server (with symptoms, quick fixes, solutions)
  - Wrong attribute names in mapped data (with common mistakes)
  - SDK method not found / wrong signature
  - Error codes (SENZ0000)
  - Slow performance / timeouts

#### Steering Guides (19 files)

- **steering.md** - Navigation hub with quick links and task-based index
- **getting-started.md** - Quick start, workflows, decision trees, ASCII diagrams
- **quick-reference.md** - Copy-paste ready commands and one-liners
- **best-practices.md** - Do's, don'ts, common pitfalls
- **performance.md** - Optimization, tuning, scaling strategies
- **troubleshooting.md** - Error handling, debugging, typical sessions
- **examples.md** - Code examples (Python, Java, C#, Rust)
- **use-cases.md** - 5 real-world implementation walkthroughs with metrics
- **security-compliance.md** - GDPR, CCPA, PII handling, access control
- **advanced-topics.md** - Custom config, network analysis, graph traversal
- **monitoring.md** - Metrics, Prometheus, Grafana, alerting, dashboards
- **data-sources.md** - 20+ system integrations (CRM, ERP, e-commerce)
- **cicd.md** - GitHub Actions, GitLab CI, Jenkins, deployment automation
- **faq.md** - 100+ questions covering all topics
- **community.md** - Resources, support, learning materials
- **reference.md** - Tool parameters, checklists, glossary (50+ terms)
- **config-examples.md** - Configuration examples for 8+ scenarios
- **smoke-test.md** - Quick and detailed validation procedures
- **offline-mode.md** - Offline usage and air-gapped deployment guidance

#### Documentation Content

- 12 MCP tools documented with usage examples
- 4 common workflow sequences
- Version compatibility information (Senzing SDK 4.0+)
- Best practices for entity resolution
- Data privacy and security guidance
- Links to all steering files for detailed guidance

#### Features and Content

- 50+ code examples across multiple languages (Python, Java, C#, Rust)
- 100+ FAQ items
- 50+ glossary terms
- 20+ data source integration examples
- 5 CI/CD platform configurations
- 5 real-world use cases with business metrics
- 4 interactive checklists (100+ items total)
- 3 ASCII workflow diagrams

### Changed

- **Power-Builder Compliance**: Updated to meet all Power-Builder standards
  - Removed 13 invalid frontmatter fields
  - Reduced keywords from 22 to 7 specific terms
  - Fixed all markdown linting warnings
  - Achieved 100% compliance score
- **Markdown Formatting**: Fixed 80+ markdown linting warnings
  - Added blank lines around code blocks and lists
  - Wrapped bare URLs in angle brackets
  - Fixed heading spacing issues
  - Changed bold text to proper headings in workflow sections
- **Keywords Optimization**: Refined to domain-specific terms only
  - Removed generic keywords (SDK, Performance, Security, Monitoring, Deployment)
  - Kept specific keywords (senzing, entity-resolution, identity-resolution, deduplication, mdm, record-linkage, fuzzy-matching)

### Removed

- **Invalid Frontmatter Fields**: Removed 13 non-existent fields per Power-Builder spec
  - version, homepage, repository, license, category, tags, maturity
  - senzing_compatibility, mcp_server_url, mcp_server_license
  - support_url, documentation_url, last_updated
- **Metadata Reference Section**: Removed documentation of invalid fields
- **Badge Images**: Removed version/maturity/license badges referencing invalid fields

### Documentation Coverage

- Getting started and quick reference
- Best practices and common pitfalls
- Performance optimization and tuning
- Troubleshooting and error handling
- Security and compliance (GDPR, CCPA)
- Advanced techniques and network analysis
- Monitoring and observability
- Data source integration (20+ systems)
- CI/CD integration (5 platforms)
- Community resources and support
- Offline and air-gapped deployment

### Quality Assurance

- Power-Builder standards compliance: 100%
- Automated validation script with 6 validation categories
- File structure validation
- Metadata validation (5 valid fields only)
- Internal link validation
- MCP configuration validation
- Steering file completeness validation
- Markdown linting: 0 warnings
- All validations pass: 0 errors, 0 warnings

### Statistics

- **Total files**: 23 (4 core + 19 steering guides)
- **POWER.md size**: 429 lines (under 500-line threshold)
- **Documentation**: 10,000+ lines across all files
- **Steering guides**: 19 comprehensive guides
- **FAQ items**: 100+
- **Code examples**: 50+
- **Glossary terms**: 50+
- **Data source integrations**: 20+
- **CI/CD examples**: 5 platforms
- **Use cases**: 5 detailed walkthroughs
- **Checklists**: 4 interactive (100+ items)
- **Diagrams**: 3 ASCII workflows

## Version History

### Version Numbering

This power follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version: Incompatible API changes or breaking changes
- **MINOR** version: New functionality in a backward compatible manner
- **PATCH** version: Backward compatible bug fixes

### Release Process

1. Document changes in CHANGELOG.md under [Unreleased]
2. Run validation: `python validate_power.py`
3. Run smoke tests
4. Move [Unreleased] changes to new version section
5. Tag release in version control

## Migration Guides

### Migrating to 1.0.0

**From pre-release versions**: This is the first stable release.

**Power-Builder Compliance Changes**:

1. **Frontmatter Simplified**: Only 5 valid fields remain
   - Kept: name, displayName, description, keywords, author
   - Removed: 13 invalid fields (version, homepage, repository, license, etc.)
   - No action required for users - changes are internal to power structure

2. **Keywords Optimized**: Reduced from 22 to 7 specific terms
   - Improved discoverability with domain-specific keywords
   - Reduced false positive activations

3. **Markdown Formatting**: All linting warnings resolved
   - Improved readability and consistency
   - No functional changes

## Breaking Changes

None - This is the initial stable release.

## Deprecations

None - This is the initial stable release.

## Known Issues

None reported.

## Contributors

### Version 1.0.0

- Complete power development and documentation
- 19 comprehensive steering guides
- Validation and testing infrastructure
- User experience enhancements (TOCs, quick start, examples, troubleshooting)
- Power-Builder standards compliance
- Quality assurance and production readiness

## Support

For questions about specific versions:

- Check the version's section in this changelog
- Use `submit_feedback` MCP tool
- Contact Senzing support: <https://senzing.zendesk.com/hc/en-us/requests/new>

## Links

- [Homepage](https://senzing.com)
- [Documentation](https://senzing.com/documentation)
- [Support](https://senzing.zendesk.com/hc/en-us/requests/new)
- [GitHub](https://github.com/senzing)

## Changelog Maintenance

This changelog is manually maintained. When making changes:

1. **Add entries under [Unreleased]** for work in progress
2. **Move to versioned section** when releasing
3. **Use categories**: Added, Changed, Deprecated, Removed, Fixed, Security
4. **Be specific**: Include file names, feature names, and impacts
5. **Link issues**: Reference issue numbers when applicable
6. **Date releases**: Use ISO 8601 format (YYYY-MM-DD)

### Categories

- **Added**: New features, files, or capabilities
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed in future versions
- **Removed**: Features that have been removed
- **Fixed**: Bug fixes
- **Security**: Security-related changes

## Notes

- This power integrates with Senzing MCP server (Apache-2.0)
- Compatible with Senzing SDK 4.0+
- Requires internet connection for MCP server access (see steering/offline-mode.md for alternatives)
- Production ready and Power-Builder compliant (100% compliance score)
- All documentation follows Power-Builder standards

---

**Note**: This changelog tracks changes to the Senzing Kiro Power itself, not changes to the Senzing SDK or MCP server. For Senzing product changes, see official Senzing release notes.
