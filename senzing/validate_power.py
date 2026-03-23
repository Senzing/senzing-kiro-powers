#!/usr/bin/env python3
"""
Senzing Power Validation Script

Validates the Senzing Kiro Power structure for the lightweight MCP activation layer design.

Usage:
    python validate_power.py
    python validate_power.py --verbose
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict

class PowerValidator:
    """Validate Senzing Power structure and content"""
    
    def __init__(self, power_dir: str = ".", verbose: bool = False):
        self.power_dir = Path(power_dir)
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.info = []
        
    def log(self, level: str, message: str):
        """Log a message"""
        if level == "ERROR":
            self.errors.append(message)
            print(f"❌ ERROR: {message}")
        elif level == "WARNING":
            self.warnings.append(message)
            print(f"⚠️  WARNING: {message}")
        elif level == "INFO":
            self.info.append(message)
            if self.verbose:
                print(f"ℹ️  INFO: {message}")
        elif level == "SUCCESS":
            print(f"✅ {message}")
    
    def validate_file_structure(self) -> bool:
        """Validate that all required files exist"""
        self.log("INFO", "Validating file structure...")
        
        required_files = [
            "POWER.md",
            "mcp.json",
            "CHANGELOG.md",
            "validate_power.py"
        ]
        
        required_dirs = [
            "steering"
        ]
        
        # Minimal steering structure - just one guide on using the MCP server
        required_steering_files = [
            "steering/using-senzing-mcp.md"
        ]
        
        all_valid = True
        
        # Check required files
        for file in required_files:
            file_path = self.power_dir / file
            if not file_path.exists():
                self.log("ERROR", f"Required file missing: {file}")
                all_valid = False
            else:
                self.log("INFO", f"Found: {file}")
        
        # Check required directories
        for dir_name in required_dirs:
            dir_path = self.power_dir / dir_name
            if not dir_path.is_dir():
                self.log("ERROR", f"Required directory missing: {dir_name}")
                all_valid = False
            else:
                self.log("INFO", f"Found directory: {dir_name}")
        
        # Check steering files
        for file in required_steering_files:
            file_path = self.power_dir / file
            if not file_path.exists():
                self.log("ERROR", f"Required steering file missing: {file}")
                all_valid = False
            else:
                self.log("INFO", f"Found: {file}")
        
        if all_valid:
            self.log("SUCCESS", "File structure validation passed")
        
        return all_valid
    
    def validate_metadata(self) -> bool:
        """Validate POWER.md frontmatter metadata"""
        self.log("INFO", "Validating metadata...")
        
        power_md = self.power_dir / "POWER.md"
        if not power_md.exists():
            self.log("ERROR", "POWER.md not found")
            return False
        
        content = power_md.read_text()
        
        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            self.log("ERROR", "No frontmatter found in POWER.md")
            return False
        
        frontmatter = frontmatter_match.group(1)
        
        # Valid Power-Builder fields (as of 2.0.0)
        valid_fields = [
            "name",
            "displayName",
            "description",
            "keywords",
            "author"
        ]
        
        # Required fields
        required_fields = [
            "name",
            "displayName",
            "description",
            "author"
        ]
        
        all_valid = True
        
        # Check required fields
        for field in required_fields:
            pattern = f'^{field}:'
            if not re.search(pattern, frontmatter, re.MULTILINE):
                self.log("ERROR", f"Required metadata field missing: {field}")
                all_valid = False
            else:
                self.log("INFO", f"Found required field: {field}")
        
        # Check for invalid fields (fields not in valid_fields list)
        for line in frontmatter.split('\n'):
            if ':' in line:
                field = line.split(':')[0].strip()
                if field and field not in valid_fields:
                    self.log("WARNING", f"Invalid metadata field (not in Power-Builder spec): {field}")
        
        # Validate keywords (should be array)
        keywords_match = re.search(r'^keywords:\s*\[(.*?)\]', frontmatter, re.MULTILINE)
        if keywords_match:
            keywords_str = keywords_match.group(1)
            keywords = [k.strip().strip('"') for k in keywords_str.split(',')]
            self.log("INFO", f"Found {len(keywords)} keywords")
            
            if len(keywords) > 10:
                self.log("WARNING", f"Too many keywords ({len(keywords)}). Recommend 5-7 specific terms.")
        
        if all_valid:
            self.log("SUCCESS", "Metadata validation passed")
        
        return all_valid
    
    def validate_internal_links(self) -> bool:
        """Validate internal links in markdown files"""
        self.log("INFO", "Validating internal links...")
        
        all_valid = True
        broken_links = []
        
        # Find all markdown files
        md_files = list(self.power_dir.glob("**/*.md"))
        
        for md_file in md_files:
            content = md_file.read_text()
            
            # Find all markdown links [text](path)
            links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
            
            for link_text, link_path in links:
                # Skip external links
                if link_path.startswith(("http://", "https://", "#")):
                    continue
                
                # Skip mailto links
                if link_path.startswith("mailto:"):
                    continue
                
                # Resolve relative path
                link_file = (md_file.parent / link_path).resolve()
                
                # Check if file exists
                if not link_file.exists():
                    self.log("ERROR", f"Broken link in {md_file.relative_to(self.power_dir)}: [{link_text}]({link_path})")
                    broken_links.append((md_file, link_path))
                    all_valid = False
                else:
                    self.log("INFO", f"Valid link: {link_path}")
        
        if all_valid:
            self.log("SUCCESS", "Internal link validation passed")
        else:
            self.log("ERROR", f"Found {len(broken_links)} broken internal links")
        
        return all_valid
    
    def validate_mcp_config(self) -> bool:
        """Validate mcp.json configuration"""
        self.log("INFO", "Validating mcp.json...")
        
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
        
        # Check structure
        if "mcpServers" not in config:
            self.log("ERROR", "mcp.json missing 'mcpServers' key")
            all_valid = False
        else:
            servers = config["mcpServers"]
            
            if "senzing-mcp-server" not in servers:
                self.log("ERROR", "mcp.json missing 'senzing-mcp-server' configuration")
                all_valid = False
            else:
                server_config = servers["senzing-mcp-server"]
                
                # Check required fields
                if "url" not in server_config:
                    self.log("ERROR", "senzing-mcp-server missing 'url' field")
                    all_valid = False
                else:
                    url = server_config["url"]
                    if not url.startswith("https://"):
                        self.log("WARNING", f"MCP server URL should use HTTPS: {url}")
                    self.log("INFO", f"MCP server URL: {url}")
                
                # Check disabled field
                if "disabled" in server_config:
                    if server_config["disabled"]:
                        self.log("WARNING", "MCP server is disabled")
                
                # Check timeout
                if "timeout" in server_config:
                    timeout = server_config["timeout"]
                    if timeout < 30000:
                        self.log("WARNING", f"Timeout ({timeout}ms) may be too short for MCP operations")
        
        if all_valid:
            self.log("SUCCESS", "mcp.json validation passed")
        
        return all_valid
    
    def validate_power_philosophy(self) -> bool:
        """Validate that the power follows the lightweight activation layer philosophy"""
        self.log("INFO", "Validating power philosophy (lightweight design)...")
        
        power_md = self.power_dir / "POWER.md"
        if not power_md.exists():
            return False
        
        content = power_md.read_text()
        lines = len(content.split('\n'))
        
        all_valid = True
        
        # POWER.md should be concise (< 200 lines for activation layer)
        if lines > 200:
            self.log("WARNING", f"POWER.md is {lines} lines. Consider if content should be in MCP server instead.")
        else:
            self.log("INFO", f"POWER.md is {lines} lines (good for activation layer)")
        
        # Should mention get_capabilities
        if "get_capabilities" not in content:
            self.log("WARNING", "POWER.md should mention calling get_capabilities first")
            all_valid = False
        
        # Should reference MCP server
        if "MCP" not in content and "mcp" not in content:
            self.log("WARNING", "POWER.md should reference the MCP server")
            all_valid = False
        
        # Check steering directory
        steering_dir = self.power_dir / "steering"
        if steering_dir.exists():
            steering_files = list(steering_dir.glob("*.md"))
            if len(steering_files) > 3:
                self.log("WARNING", f"Found {len(steering_files)} steering files. Consider if content should be in MCP server instead.")
            else:
                self.log("INFO", f"Found {len(steering_files)} steering files (minimal design)")
        
        if all_valid:
            self.log("SUCCESS", "Power philosophy validation passed")
        
        return all_valid
    
    def check_file_sizes(self) -> bool:
        """Check for unusually large files"""
        self.log("INFO", "Checking file sizes...")
        
        max_size_kb = 100  # 100 KB warning threshold for activation layer
        
        md_files = list(self.power_dir.glob("**/*.md"))
        
        for md_file in md_files:
            size_kb = md_file.stat().st_size / 1024
            if size_kb > max_size_kb:
                self.log("WARNING", f"Large file: {md_file.relative_to(self.power_dir)} ({size_kb:.1f} KB) - consider if content belongs in MCP server")
            else:
                self.log("INFO", f"{md_file.relative_to(self.power_dir)}: {size_kb:.1f} KB")
        
        self.log("SUCCESS", "File size check complete")
        return True
    
    def generate_report(self) -> Dict:
        """Generate validation report"""
        return {
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "info": len(self.info),
            "error_details": self.errors,
            "warning_details": self.warnings,
            "info_details": self.info if self.verbose else []
        }
    
    def run_all_validations(self) -> bool:
        """Run all validation checks"""
        print("\n" + "="*60)
        print("Senzing Power Validation (v2.0 - Lightweight Design)")
        print("="*60 + "\n")
        
        results = []
        
        results.append(self.validate_file_structure())
        results.append(self.validate_metadata())
        results.append(self.validate_mcp_config())
        results.append(self.validate_internal_links())
        results.append(self.validate_power_philosophy())
        results.append(self.check_file_sizes())
        
        print("\n" + "="*60)
        print("Validation Summary")
        print("="*60)
        
        report = self.generate_report()
        
        print(f"\n❌ Errors: {report['errors']}")
        print(f"⚠️  Warnings: {report['warnings']}")
        print(f"ℹ️  Info: {report['info']}")
        
        if report['errors'] == 0 and report['warnings'] == 0:
            print("\n🎉 All validations passed! Power follows lightweight activation layer design.")
            return True
        elif report['errors'] == 0:
            print(f"\n✅ No errors found, but {report['warnings']} warnings to review.")
            return True
        else:
            print(f"\n❌ Validation failed with {report['errors']} errors.")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Validate Senzing Kiro Power (v2.0 - Lightweight Activation Layer)"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--dir", default=".", help="Power directory (default: current directory)")
    
    args = parser.parse_args()
    
    validator = PowerValidator(power_dir=args.dir, verbose=args.verbose)
    success = validator.run_all_validations()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
