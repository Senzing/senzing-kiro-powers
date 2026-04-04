# Senzing Entity Resolution — Development Guide

Development documentation for the Senzing Kiro Power.

## Repository Structure

- `../senzing/` - The Kiro Power (production files only)
  - `POWER.md` - Power manifest and documentation
  - `mcp.json` - MCP server configuration
- `senzing-power-development/` - Development tools (this directory)
  - `validate_power.py` - Validation script
  - `README.md` - This file
  - `QUICKSTART.md` - User quick start guide
- Repository root - Project documentation
  - `CHANGELOG.md` - Version history
  - `CONTRIBUTING.md` - Contribution guidelines
  - `CODE_OF_CONDUCT.md` - Community standards
  - `.github/` - GitHub workflows and templates

## Development

### Validation

Run the validation script from the repository root:

```bash
python3 senzing-power-development/validate_power.py --dir senzing
```

Or with verbose output:

```bash
python3 senzing-power-development/validate_power.py --dir senzing --verbose
```

### Making Changes

1. Edit files in `../senzing/` directory
2. Run validation to ensure compliance
3. Update `../CHANGELOG.md` with changes
4. Test with the MCP server
5. Submit pull request

## User Documentation

See [QUICKSTART.md](QUICKSTART.md) for user-facing quick start guide.

## Privacy

The Senzing MCP server works from pre-fetched documentation. It never connects
to live Senzing instances and never handles PII. Data mapping and analysis
scripts run locally on the client.

## What Is Senzing

Senzing provides real-time AI-powered entity resolution as an embeddable SDK.
It determines when two records refer to the same real-world entity (person,
organization, etc.) by analyzing names, addresses, identifiers, and other
attributes across data sources — without training data or manual rules.

## Quick Start Examples

### Map a CSV file

```text
"I have a customer CSV at /data/customers.csv I need to load into Senzing"
```

The agent will guide you through the interactive mapping workflow, validate the output, and analyze data quality.

### Set up Senzing SDK

```text
"Help me install and set up the Senzing SDK on Ubuntu"
```

The agent will provide platform-specific install commands and configuration code.

### Generate integration code

```text
"Write me Python code to initialize Senzing and load records"
```

The agent will generate working SDK code from real GitHub examples.

### Debug an error

```text
"I'm getting SENZ7234 when loading records"
```

The agent will explain the error and provide resolution steps.

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

## Additional Resources

- [Quick Start Guide](QUICKSTART.md) - Get started in minutes
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Version history and updates
- [Senzing Website](https://senzing.com) - Official Senzing documentation
- [Senzing MCP Server](https://mcp.senzing.com/mcp) - MCP server endpoint

## Related Projects

- [senzing-mcp-skill](https://github.com/Senzing/senzing-mcp-skill) - Claude skill version
- [Senzing SDK](https://senzing.com/senzing-api/) - Official SDK documentation
