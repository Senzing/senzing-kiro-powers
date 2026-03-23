#!/usr/bin/env python3
"""
Senzing Power Validation Script

Validates the Senzing Kiro Power structure:
- Required files (POWER.md, mcp.json)
- POWER.md frontmatter (name, displayName, description, keywords, author)
- mcp.json structure and URL
- Internal link integrity

Usage:
    python validate_power.py
    python validate_power.py --verbose
"""

import json
import re
import sys
import argparse
from pathlib import Path


class PowerValidator:
    """Validate Senzing Power structure and content."""

    REQUIRED_FILES = [
        "POWER.md",
        "mcp.json",
    ]

    REQUIRED_FRONTMATTER_FIELDS = [
        "name",
        "displayName",
        "description",
        "keywords",
        "author",
    ]

    def __init__(self, power_dir: str = "senzing", verbose: bool = False):
        self.power_dir = Path(power_dir)
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def log(self, level: str, message: str):
        match level:
            case "ERROR":
                self.errors.append(message)
                print(f"  ERROR: {message}")
            case "WARNING":
                self.warnings.append(message)
                print(f"  WARNING: {message}")
            case "INFO":
                self.info.append(message)
                if self.verbose:
                    print(f"  INFO: {message}")
            case "SUCCESS":
                print(f"  PASS: {message}")

    def validate_file_structure(self) -> bool:
        """Validate that all required files exist."""
        all_valid = True
        for file in self.REQUIRED_FILES:
            if not (self.power_dir / file).exists():
                self.log("ERROR", f"Required file missing: {file}")
                all_valid = False
            else:
                self.log("INFO", f"Found: {file}")
        if all_valid:
            self.log("SUCCESS", "File structure validation passed")
        return all_valid

    def validate_metadata(self) -> bool:
        """Validate POWER.md frontmatter metadata."""
        power_md = self.power_dir / "POWER.md"
        if not power_md.exists():
            self.log("ERROR", "POWER.md not found")
            return False

        content = power_md.read_text()
        frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not frontmatter_match:
            self.log("ERROR", "No frontmatter found in POWER.md")
            return False

        frontmatter = frontmatter_match.group(1)
        all_valid = True

        for field in self.REQUIRED_FRONTMATTER_FIELDS:
            if not re.search(rf"^{field}:", frontmatter, re.MULTILINE):
                self.log("ERROR", f"Required metadata field missing: {field}")
                all_valid = False
            else:
                self.log("INFO", f"Found field: {field}")

        if all_valid:
            self.log("SUCCESS", "Metadata validation passed")
        return all_valid

    def validate_internal_links(self) -> bool:
        """Validate internal links in markdown files."""
        all_valid = True
        broken_count = 0

        for md_file in self.power_dir.glob("**/*.md"):
            content = md_file.read_text()
            links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", content)
            for link_text, link_path in links:
                if link_path.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                link_file = (md_file.parent / link_path).resolve()
                if not link_file.exists():
                    rel_path = md_file.relative_to(self.power_dir)
                    self.log("ERROR", f"Broken link in {rel_path}: [{link_text}]({link_path})")
                    broken_count += 1
                    all_valid = False

        if all_valid:
            self.log("SUCCESS", "Internal link validation passed")
        else:
            self.log("ERROR", f"Found {broken_count} broken internal links")
        return all_valid

    def validate_mcp_config(self) -> bool:
        """Validate mcp.json configuration."""
        mcp_json = self.power_dir / "mcp.json"
        if not mcp_json.exists():
            self.log("ERROR", "mcp.json not found")
            return False

        try:
            config = json.loads(mcp_json.read_text())
        except json.JSONDecodeError as e:
            self.log("ERROR", f"Invalid JSON in mcp.json: {e}")
            return False

        all_valid = True

        if "mcpServers" not in config:
            self.log("ERROR", "mcp.json missing 'mcpServers' key")
            all_valid = False
        else:
            servers = config["mcpServers"]
            if not servers:
                self.log("ERROR", "No servers defined in mcpServers")
                all_valid = False
            else:
                for name, server_config in servers.items():
                    if "url" not in server_config:
                        self.log("ERROR", f"Server '{name}' missing 'url' field")
                        all_valid = False
                    elif not server_config["url"].startswith("https://"):
                        self.log("WARNING", f"Server '{name}' URL should use HTTPS")

        if all_valid:
            self.log("SUCCESS", "mcp.json validation passed")
        return all_valid

    def run_all_validations(self) -> bool:
        print()
        print("=" * 50)
        print("Senzing Power Validation")
        print("=" * 50)
        print()

        results = [
            self.validate_file_structure(),
            self.validate_metadata(),
            self.validate_mcp_config(),
            self.validate_internal_links(),
        ]

        print()
        print("=" * 50)
        print(f"  Errors:   {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")

        if len(self.errors) == 0:
            print("\n  All validations passed.")
            return True
        else:
            print(f"\n  Validation failed with {len(self.errors)} errors.")
            return False


def main():
    parser = argparse.ArgumentParser(description="Validate Senzing Kiro Power")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--dir", default="senzing", help="Power directory (default: senzing)")
    args = parser.parse_args()

    validator = PowerValidator(power_dir=args.dir, verbose=args.verbose)
    success = validator.run_all_validations()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
