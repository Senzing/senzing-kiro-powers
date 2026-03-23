# Senzing Kiro Powers

This repository contains the Senzing entity resolution power for Kiro.

## Repository Structure

- **`senzing/`** - The Kiro Power (install this directory)
  - `POWER.md` - Power manifest and documentation
  - `mcp.json` - MCP server configuration

- **`senzing-power-development/`** - Development tools
  - `validate_power.py` - Validation script
  - `README.md` - Development documentation
  - `QUICKSTART.md` - User quick start guide

- **Repository files** (root level)
  - `CHANGELOG.md` - Version history
  - `CONTRIBUTING.md` - Contribution guidelines
  - `CODE_OF_CONDUCT.md` - Community standards
  - `.github/` - GitHub workflows and templates

## Installation

Copy the `senzing` directory to your Kiro powers location. The power will automatically connect to the Senzing MCP server.

See [senzing-power-development/QUICKSTART.md](senzing-power-development/QUICKSTART.md) for detailed setup instructions.

## Documentation

- [Quick Start Guide](senzing-power-development/QUICKSTART.md)
- [Power Documentation](senzing/POWER.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.
