# Contributing to Senzing Kiro Power

Thank you for your interest in contributing to the Senzing Kiro Power!

## How to Contribute

### Reporting Issues

If you encounter any issues with the power:

1. Check existing issues to avoid duplicates
2. Provide clear reproduction steps
3. Include your Kiro version and operating system
4. Share relevant error messages or logs

### Suggesting Enhancements

We welcome suggestions for improvements:

1. Describe the enhancement clearly
2. Explain the use case and benefits
3. Consider backward compatibility

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run validation: `python3 validate_power.py`
5. Update CHANGELOG.md with your changes
6. Commit with clear messages
7. Push to your fork
8. Open a pull request

## Development Guidelines

### Repository Structure

- `senzing/` - The Kiro Power (production files only)
  - `POWER.md` - Power manifest and documentation
  - `mcp.json` - MCP server configuration
- `senzing-power-development/` - Development tools
  - `validate_power.py` - Validation script
  - `README.md` - Development documentation
  - `QUICKSTART.md` - User quick start guide
- Repository root - Project documentation
  - `CHANGELOG.md` - Version history
  - `CONTRIBUTING.md` - This file
  - `CODE_OF_CONDUCT.md` - Community standards
  - `.github/` - GitHub workflows and templates

### Documentation Standards

- Use clear, concise language
- Include examples for complex workflows
- Keep tool references up to date
- Follow markdown best practices

### Testing

Before submitting changes:

1. Run the validation script from repository root: `python3 senzing-power-development/validate_power.py --dir senzing`
2. Test workflows with the MCP server
3. Verify documentation renders correctly
4. Check for broken links

## Questions?

For questions about Senzing entity resolution or the MCP server, use the
`submit_feedback` tool through the power or visit [senzing.com](https://senzing.com).

## License

By contributing, you agree that your contributions will be licensed under the
Apache License 2.0.
