# Senzing Power - Offline Mode Documentation

This guide explains what works offline vs requires internet connectivity, and provides guidance for air-gapped and restricted network environments.

## Overview

The Senzing Kiro Power has two main components:
1. **Local Documentation** - Steering guides and reference materials (works offline)
2. **MCP Server Tools** - Remote tools for data mapping, code generation, etc. (requires internet)

## What Works Offline

### ✅ Full Offline Access

These resources are available without internet connection:

#### Documentation Files
- All 16 steering guides
- POWER.md
- METADATA.md
- CHANGELOG.md
- IMPROVEMENTS_SUMMARY.md
- SMOKE_TEST.md
- TEST_EXAMPLES.md
- FAQ.md
- All reference materials

#### Validation Tools
- `validate_power.py` - Power structure validation
- File structure checks
- Metadata validation
- Internal link validation
- Configuration validation

#### Reference Materials
- Quick reference commands
- Code examples (Python, Java, C#, Rust)
- Best practices documentation
- Troubleshooting guides
- Glossary (50+ terms)
- Checklists (4 interactive checklists)
- Use case walkthroughs
- Integration patterns
- Security guidelines

#### Local Resources
- ASCII workflow diagrams
- Configuration examples
- Test examples
- Smoke test procedures

### ✅ Partial Offline Access

These work offline with limitations:

#### Senzing SDK
- **Offline**: SDK installation, configuration, loading, querying
- **Online**: Initial SDK download, updates, license validation
- **Workaround**: Download SDK packages in advance

#### Code Examples
- **Offline**: All code examples in steering guides
- **Online**: `find_examples` MCP tool for searching GitHub
- **Workaround**: Save examples locally from steering/examples.md

#### Documentation
- **Offline**: All steering guides and reference materials
- **Online**: `search_docs` MCP tool for indexed search
- **Workaround**: Use local file search or grep

## What Requires Internet

### ❌ Internet Required

These features require active internet connection:

#### MCP Server Tools
All MCP tools require connection to https://mcp.senzing.com/mcp:

1. **get_capabilities** - Discover available tools
2. **mapping_workflow** - Interactive data mapping
3. **lint_record** - Validate mapped records
4. **analyze_record** - Analyze data quality
5. **generate_scaffold** - Generate SDK code
6. **sdk_guide** - Platform-specific setup instructions
7. **get_sample_data** - Download sample datasets
8. **find_examples** - Search GitHub repositories
9. **search_docs** - Search indexed documentation
10. **explain_error_code** - Diagnose error codes
11. **get_sdk_reference** - SDK method signatures
12. **download_resource** - Download SDK packages
13. **submit_feedback** - Submit feedback

#### External Resources
- Senzing SDK downloads
- Sample data downloads
- GitHub repository access
- Official documentation website
- Support portal

## Offline Workflows

### Scenario 1: Complete Offline Development

**Preparation (while online)**:
1. Download Senzing SDK packages
2. Save sample data locally
3. Generate code scaffolds for common workflows
4. Download all steering guides (already included)
5. Save code examples from GitHub
6. Print or save error code reference

**Offline Development**:
1. Use local SDK installation
2. Load data from local files
3. Query local database
4. Reference local steering guides
5. Use saved code examples
6. Validate with local tools

**Example Offline Workflow**:
```bash
# 1. Validate power structure (offline)
python validate_power.py

# 2. Reference local documentation
cat steering/getting-started.md
cat steering/quick-reference.md

# 3. Use pre-generated code
# (Generated while online, saved locally)
python my_loader.py

# 4. Load data (offline)
# Senzing SDK works offline once installed
```

### Scenario 2: Air-Gapped Environment

**Setup Process**:

1. **On Internet-Connected System**:
   ```bash
   # Download Senzing SDK
   wget https://senzing-production-apt.s3.amazonaws.com/senzingapi_X.X.X_amd64.deb
   
   # Download sample data
   curl -O https://example.com/sample_data.jsonl
   
   # Generate code scaffolds
   generate_scaffold(language="python", workflow="full_pipeline", version="current")
   # Save output to files
   
   # Download documentation (if not included)
   # All steering guides are already in the power
   
   # Package everything
   tar -czf senzing-offline-bundle.tar.gz senzing/ sdk/ data/ code/
   ```

2. **Transfer to Air-Gapped System**:
   ```bash
   # Copy bundle via approved transfer method
   # (USB drive, secure file transfer, etc.)
   ```

3. **On Air-Gapped System**:
   ```bash
   # Extract bundle
   tar -xzf senzing-offline-bundle.tar.gz
   
   # Install SDK
   sudo dpkg -i senzingapi_X.X.X_amd64.deb
   
   # Use local resources
   cd senzing
   python validate_power.py
   
   # Reference documentation
   cat steering/getting-started.md
   
   # Run pre-generated code
   python code/loader.py
   ```

### Scenario 3: Restricted Network

**Configuration for Proxy/Firewall**:

If you have restricted internet access:

1. **Configure Proxy** (if applicable):
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ```

2. **Whitelist MCP Server**:
   - Domain: mcp.senzing.com
   - Port: 443 (HTTPS)
   - Protocol: HTTPS

3. **Test Connectivity**:
   ```bash
   curl -I https://mcp.senzing.com/status
   ```

4. **Adjust Timeout** (if slow connection):
   ```json
   // mcp.json
   {
     "mcpServers": {
       "senzing-mcp-server": {
         "url": "https://mcp.senzing.com/mcp",
         "timeout": 60000  // 60 seconds for slow connections
       }
     }
   }
   ```

## Offline Alternatives

### Alternative 1: Pre-Generated Code

**While Online**:
```python
# Generate all common workflows
workflows = [
    "initialize",
    "configure", 
    "add_records",
    "query",
    "full_pipeline"
]

for workflow in workflows:
    code = generate_scaffold(
        language="python",
        workflow=workflow,
        version="current"
    )
    
    # Save to file
    with open(f"offline_code/{workflow}.py", "w") as f:
        f.write(code)
```

**While Offline**:
```python
# Use pre-generated code
with open("offline_code/full_pipeline.py") as f:
    code = f.read()
    # Adapt as needed
```

### Alternative 2: Local Documentation Search

**Instead of `search_docs`**:
```bash
# Use grep to search local steering guides
grep -r "entity resolution" senzing/steering/

# Or use find
find senzing/steering -name "*.md" -exec grep -l "performance" {} \;
```

### Alternative 3: Local Code Examples

**Instead of `find_examples`**:
```bash
# All examples are in steering/examples.md
cat senzing/steering/examples.md | grep -A 20 "Load Single Record"
```

### Alternative 4: Manual Data Mapping

**Instead of `mapping_workflow`**:
```python
# Use reference guide for attribute names
# See steering/reference.md for complete list

# Manual mapping
record = {
    "DATA_SOURCE": "CUSTOMERS",
    "RECORD_ID": "CUST001",
    "NAME_FULL": "John Smith",  # Not "FULL_NAME"
    "EMAIL_ADDRESS": "john@example.com",  # Not "EMAIL"
    "PHONE_NUMBER": "555-1234",  # Not "PHONE"
    "ADDR_FULL": "123 Main St"  # Not "ADDRESS"
}

# Validate with local linter (if available)
# Or reference steering/best-practices.md
```

### Alternative 5: Cached Resources

**Create Local Cache**:
```bash
# While online, cache commonly used resources
mkdir -p offline_cache

# Save error code reference
explain_error_code(error_code="SENZ0001", version="current") > offline_cache/error_codes.txt
explain_error_code(error_code="SENZ0002", version="current") >> offline_cache/error_codes.txt
# ... repeat for common errors

# Save SDK reference
get_sdk_reference(topic="all", version="current") > offline_cache/sdk_reference.json

# Save sample data
get_sample_data(dataset="las-vegas", limit=1000) > offline_cache/sample_data.jsonl
```

## Offline Checklist

### Pre-Offline Preparation

- [ ] Download Senzing SDK packages
- [ ] Download sample data
- [ ] Generate code scaffolds for all workflows
- [ ] Save error code reference
- [ ] Save SDK reference documentation
- [ ] Cache commonly used MCP tool outputs
- [ ] Test offline workflows
- [ ] Document any custom procedures
- [ ] Package everything for transfer

### Offline Development Setup

- [ ] Install Senzing SDK from local packages
- [ ] Verify all steering guides are accessible
- [ ] Test validation script works
- [ ] Confirm local database is configured
- [ ] Verify pre-generated code is available
- [ ] Test sample workflow end-to-end
- [ ] Document any issues or workarounds

### Offline Operations

- [ ] Use local steering guides for reference
- [ ] Use pre-generated code templates
- [ ] Use local validation tools
- [ ] Reference local error code cache
- [ ] Use local sample data
- [ ] Document any limitations encountered

## Network Requirements

### Minimum Requirements (Online Mode)

- **Bandwidth**: 1 Mbps (for MCP tools)
- **Latency**: < 500ms to mcp.senzing.com
- **Ports**: 443 (HTTPS)
- **Protocols**: HTTPS/TLS 1.2+

### Recommended Requirements

- **Bandwidth**: 10 Mbps
- **Latency**: < 100ms
- **Reliability**: 99%+ uptime
- **Firewall**: Whitelist mcp.senzing.com

## Troubleshooting Offline Issues

### Issue: MCP Tools Not Working

**Symptom**: All MCP tools fail with connection errors

**Solution**:
1. Check if you're offline (expected behavior)
2. Use offline alternatives documented above
3. Reference local steering guides
4. Use pre-generated code and cached resources

### Issue: SDK Installation Fails

**Symptom**: Cannot install Senzing SDK

**Solution**:
1. Download SDK packages while online
2. Transfer to offline system
3. Install from local packages
4. See steering/getting-started.md for installation steps

### Issue: Missing Documentation

**Symptom**: Cannot access certain documentation

**Solution**:
1. All steering guides are included in the power
2. Use local file search: `grep -r "topic" senzing/steering/`
3. Reference POWER.md for overview
4. Check FAQ.md for common questions

### Issue: Cannot Validate Data Mapping

**Symptom**: `lint_record` requires internet

**Solution**:
1. Use manual validation against reference guide
2. Check steering/best-practices.md for common mistakes
3. Reference steering/reference.md for attribute names
4. Test with small batch in Senzing SDK

## Best Practices for Offline Use

1. **Plan Ahead**: Download everything you need while online
2. **Cache Aggressively**: Save all MCP tool outputs you might need
3. **Document Procedures**: Write down your offline workflows
4. **Test Offline**: Verify everything works before going offline
5. **Use Local Tools**: Leverage validation script and local docs
6. **Keep Backups**: Maintain copies of SDK packages and data
7. **Version Control**: Track your code and configurations
8. **Update Regularly**: Refresh cached resources periodically

## Hybrid Approach

For best results, use a hybrid approach:

**Online Activities**:
- Data mapping with `mapping_workflow`
- Code generation with `generate_scaffold`
- Documentation search with `search_docs`
- Error diagnosis with `explain_error_code`
- Finding examples with `find_examples`

**Offline Activities**:
- SDK development and testing
- Data loading and querying
- Reference documentation review
- Code validation
- Performance testing

## Support for Offline Users

For offline/air-gapped deployment support:
- Contact Senzing sales for on-premises options
- Request offline documentation packages
- Inquire about local MCP server deployment
- Discuss custom licensing for restricted environments

**Contact**: https://senzing.com/contact

## Resources

### Local Resources (Always Available)
- All steering guides in `senzing/steering/`
- POWER.md for overview
- METADATA.md for power information
- CHANGELOG.md for version history
- FAQ.md for common questions
- Quick reference in `steering/quick-reference.md`

### Online Resources (Internet Required)
- MCP server tools
- Official documentation: https://senzing.com/documentation
- Support portal: https://senzing.zendesk.com
- GitHub repositories: https://github.com/senzing

### Cached Resources (Prepare While Online)
- SDK packages
- Sample data
- Generated code
- Error code reference
- SDK reference documentation

---

**Note**: This power is designed for online use with MCP server access. For production air-gapped deployments, contact Senzing for enterprise solutions and on-premises options.
