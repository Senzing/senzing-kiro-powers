# Senzing Power - Smoke Test Guide

This guide provides a quick smoke test to verify the Senzing power is correctly installed and functional.

## Prerequisites

- Kiro IDE installed
- Senzing power installed
- Internet connection (for MCP server access)

## Quick Smoke Test (5 minutes)

### 1. Verify Power Installation

Check that the power is installed:

```bash
# List installed powers
# Look for "senzing" in the output
```

Expected: Senzing power appears in the list

### 2. Verify File Structure

Run the validation script:

```bash
cd senzing
python validate_power.py
```

Expected output:
```
✅ File structure validation passed
✅ Metadata validation passed
✅ mcp.json validation passed
✅ Internal link validation passed
✅ Steering file completeness validation passed
✅ File size check complete

🎉 All validations passed! Power is ready for production.
```

### 3. Test MCP Server Connectivity

Test basic MCP tool access:

```python
# Test get_capabilities
get_capabilities(version="current")
```

Expected: Returns server capabilities without errors

### 4. Test Documentation Access

Verify steering files are accessible:

```bash
# Check that steering files exist
ls -la senzing/steering/

# Should show 16 .md files
```

Expected: All 16 steering files present

### 5. Test Sample Workflow

Run a minimal workflow:

```python
# 1. Get capabilities
response = get_capabilities(version="current")
print("✅ get_capabilities works")

# 2. List sample datasets
response = get_sample_data(dataset="list")
print("✅ get_sample_data works")

# 3. Search documentation
response = search_docs(query="entity resolution", version="current")
print("✅ search_docs works")
```

Expected: All three commands execute without errors

## Detailed Smoke Test (15 minutes)

### Test 1: Metadata Validation

```bash
cd senzing
python validate_power.py --verbose
```

Verify:
- ✅ All required metadata fields present
- ✅ Version follows semantic versioning
- ✅ All URLs are valid
- ✅ License fields are present

### Test 2: Internal Links

```bash
cd senzing
python validate_power.py
```

Verify:
- ✅ No broken internal links
- ✅ All steering file cross-references work
- ✅ All relative paths resolve correctly

### Test 3: MCP Tools

Test each major MCP tool category:

```python
# Documentation tools
get_capabilities(version="current")
search_docs(query="test", version="current")
explain_error_code(error_code="SENZ0005", version="current")

# Data tools
get_sample_data(dataset="list")
# Note: mapping_workflow requires files, skip for smoke test

# Code generation
generate_scaffold(language="python", workflow="initialize", version="current")

# Examples
find_examples(query="load records", language="python")

# SDK reference
get_sdk_reference(topic="flags", version="current")
```

Expected: All tools return valid responses

### Test 4: Steering File Navigation

Open and verify key steering files:

1. **steering/steering.md** - Navigation hub
   - ✅ Contains links to all other guides
   - ✅ Quick navigation section present
   - ✅ Document structure diagram present

2. **steering/getting-started.md** - Quick start
   - ✅ MCP tool catalog present
   - ✅ Decision trees present
   - ✅ Workflow diagrams present

3. **steering/quick-reference.md** - Commands
   - ✅ Copy-paste ready commands present
   - ✅ Common workflows present

4. **steering/faq.md** - FAQ
   - ✅ 100+ questions present
   - ✅ Organized by category

### Test 5: Configuration

Verify mcp.json:

```bash
cat senzing/mcp.json
```

Verify:
- ✅ Valid JSON syntax
- ✅ senzing-mcp-server configured
- ✅ URL points to https://mcp.senzing.com/mcp
- ✅ Timeout configured
- ✅ Environment variables present

### Test 6: Documentation Completeness

Check that all major topics are covered:

```bash
cd senzing/steering
grep -l "Quick Start" *.md
grep -l "Best Practices" *.md
grep -l "Performance" *.md
grep -l "Security" *.md
grep -l "Troubleshooting" *.md
```

Expected: Each topic found in appropriate files

## Automated Test Suite

### Run All Tests

```bash
cd senzing
python validate_power.py --verbose
```

### Test Categories

1. **Structure Tests**
   - File existence
   - Directory structure
   - Required files present

2. **Metadata Tests**
   - Frontmatter parsing
   - Required fields present
   - Version format valid
   - URLs valid

3. **Link Tests**
   - Internal links resolve
   - No broken references
   - Cross-references valid

4. **Configuration Tests**
   - mcp.json valid JSON
   - Required fields present
   - Server configuration correct

5. **Completeness Tests**
   - All steering files referenced
   - All topics covered
   - No orphaned files

## Common Issues and Solutions

### Issue: Validation Script Fails

**Symptom**: `python validate_power.py` returns errors

**Solutions**:
1. Check Python version (3.7+ required)
2. Verify you're in the senzing directory
3. Check file permissions
4. Review error messages for specific issues

### Issue: Broken Internal Links

**Symptom**: Link validation fails

**Solutions**:
1. Check that all steering files exist
2. Verify relative paths are correct
3. Ensure no typos in filenames
4. Run with `--fix-links` flag (if implemented)

### Issue: MCP Server Unreachable

**Symptom**: MCP tools fail with connection errors

**Solutions**:
1. Check internet connectivity
2. Verify firewall allows HTTPS to mcp.senzing.com
3. Check mcp.json configuration
4. Try accessing https://mcp.senzing.com/status in browser

### Issue: Missing Steering Files

**Symptom**: File structure validation fails

**Solutions**:
1. Verify power installation completed
2. Check that all files were extracted
3. Re-install power if necessary
4. Check file permissions

## Success Criteria

The power passes smoke testing if:

✅ All validation checks pass
✅ No broken internal links
✅ MCP server connectivity works
✅ All steering files present and accessible
✅ Metadata is complete and valid
✅ Configuration is correct
✅ Sample MCP tools execute successfully

## Regression Testing

When updating the power, re-run smoke tests to ensure:

1. **No Breaking Changes**
   - All existing links still work
   - All files still present
   - Metadata still valid

2. **New Features Work**
   - New steering files added to navigation
   - New links resolve correctly
   - New metadata fields valid

3. **Documentation Updated**
   - Version number incremented
   - Last updated date current
   - Changelog updated

## Continuous Validation

### Pre-Commit Checks

Before committing changes:

```bash
cd senzing
python validate_power.py
```

Fix any errors before committing.

### Pre-Release Checks

Before releasing a new version:

1. Run full validation: `python validate_power.py --verbose`
2. Test all MCP tools manually
3. Review all steering files for accuracy
4. Update version number
5. Update last_updated date
6. Update IMPROVEMENTS_SUMMARY.md

### Post-Installation Checks

After installing in a new environment:

1. Run smoke test
2. Test MCP connectivity
3. Verify steering files accessible
4. Test sample workflow

## Reporting Issues

If smoke tests fail:

1. **Collect Information**:
   - Validation script output
   - Error messages
   - Environment details (OS, Kiro version)
   - Steps to reproduce

2. **Submit Feedback**:
   ```python
   submit_feedback(
       message="Smoke test failure: [describe issue]",
       category="bug"
   )
   ```

3. **Include**:
   - Validation report
   - Expected vs actual behavior
   - Any error logs

## Test Automation

### GitHub Actions Example

```yaml
name: Validate Senzing Power

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Run validation
        run: |
          cd senzing
          python validate_power.py --verbose
```

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

cd senzing
python validate_power.py

if [ $? -ne 0 ]; then
    echo "❌ Power validation failed. Commit aborted."
    exit 1
fi

echo "✅ Power validation passed."
exit 0
```

## Next Steps

After successful smoke testing:

1. ✅ Power is validated and ready to use
2. ✅ Proceed with actual Senzing workflows
3. ✅ Refer to steering guides for detailed guidance
4. ✅ Use quick-reference.md for common commands

## Resources

- **Validation Script**: `senzing/validate_power.py`
- **Power Metadata**: `senzing/METADATA.md`
- **Improvements Summary**: `senzing/IMPROVEMENTS_SUMMARY.md`
- **Steering Hub**: `senzing/steering/steering.md`

## Support

For smoke test issues:
- Review error messages carefully
- Check prerequisites are met
- Consult troubleshooting section
- Submit feedback via MCP tool
- Contact Senzing support
