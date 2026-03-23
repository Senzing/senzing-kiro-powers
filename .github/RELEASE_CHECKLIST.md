# Release Checklist

Use this checklist when preparing a new release of the Senzing Kiro Power.

## Pre-Release

- [ ] All tests pass (`python3 senzing-power-development/validate_power.py --dir senzing`)
- [ ] Documentation is up to date
- [ ] `CHANGELOG.md` updated with new version
- [ ] Version number updated in `senzing/POWER.md` frontmatter
- [ ] All examples tested with current MCP server
- [ ] Breaking changes documented (if any)
- [ ] Migration guide provided (if needed)

## Documentation Review

- [ ] README.md reflects current features
- [ ] POWER.md workflows are accurate
- [ ] Tool descriptions match MCP server capabilities
- [ ] Examples use correct tool names and parameters
- [ ] Links are not broken
- [ ] Code blocks have language specifications

## Testing

- [ ] Test with fresh Kiro installation
- [ ] Verify MCP server connection
- [ ] Test each major workflow:
  - [ ] Data mapping workflow
  - [ ] SDK installation guide
  - [ ] Code generation
  - [ ] Error troubleshooting
  - [ ] Sample data access
  - [ ] Documentation search
- [ ] Test on multiple platforms (if applicable)

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **Major (X.0.0)**: Breaking changes, incompatible API changes
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes, backward compatible

## Release Process

1. Update version in `senzing/POWER.md` frontmatter
2. Update `CHANGELOG.md` with release date
3. Commit changes: `git commit -m "Release vX.Y.Z"`
4. Create git tag: `git tag -a vX.Y.Z -m "Version X.Y.Z"`
5. Push changes: `git push && git push --tags`
6. Create GitHub release with changelog excerpt
7. Announce release (if applicable)

## Post-Release

- [ ] Verify installation from release
- [ ] Monitor for issues
- [ ] Update documentation site (if applicable)
- [ ] Respond to user feedback

## Rollback Plan

If critical issues are discovered:

1. Document the issue
2. Revert to previous version if necessary
3. Fix the issue
4. Release patch version
5. Update `CHANGELOG.md` with fix details
