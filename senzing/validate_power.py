#!/usr/bin/env python3
"""
Senzing Power Validation Script

This script validates the Senzing Kiro Power structure, including:
- File existence checks
- Internal link validation
- Metadata validation
- Frontmatter parsing
- Steering file completeness

Usage:
    python validate_power.py
    python validate_power.py --verbose
    python validate_power.py --fix-links
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Set

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
        
        required_steering_files = [
            "steering/steering.md",
            "steering/getting-started.md",
            "steering/quick-reference.md",
            "steering/best-practices.md",
            "steering/performance.md",
            "steering/troubleshooting.md",
            "steering/examples.md",
            "steering/use-cases.md",
            "steering/security-compliance.md",
            "steering/advanced-topics.md",
            "steering/monitoring.md",
            "steering/data-sources.md",
            "steering/cicd.md",
            "steering/faq.md",
            "steering/community.md",
            "steering/reference.md",
            "steering/config-examples.md",
            "steering/smoke-test.md",
            "steering/offline-mode.md"
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
        
        # Required fields
        required_fields = [
            "name",
            "displayName",
            "version",
            "description",
            "author"
        ]
        
        # Recommended fields
        recommended_fields = [
            "keywords",
            "homepage",
            "license",
            "category",
            "maturity",
            "support_url",
            "last_updated"
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
        
        # Check recommended fields
        for field in recommended_fields:
            pattern = f'^{field}:'
            if not re.search(pattern, frontmatter, re.MULTILINE):
                self.log("WARNING", f"Recommended metadata field missing: {field}")
            else:
                self.log("INFO", f"Found recommended field: {field}")
        
        # Validate version format (semantic versioning)
        version_match = re.search(r'^version:\s*"?([^"\n]+)"?', frontmatter, re.MULTILINE)
        if version_match:
            version = version_match.group(1)
            if not re.match(r'^\d+\.\d+\.\d+', version):
                self.log("WARNING", f"Version '{version}' doesn't follow semantic versioning (MAJOR.MINOR.PATCH)")
        
        # Validate maturity value
        maturity_match = re.search(r'^maturity:\s*"?([^"\n]+)"?', frontmatter, re.MULTILINE)
        if maturity_match:
            maturity = maturity_match.group(1)
            valid_maturity = ["alpha", "beta", "stable"]
            if maturity not in valid_maturity:
                self.log("WARNING", f"Maturity '{maturity}' not in {valid_maturity}")
        
        # Validate URLs
        url_fields = ["homepage", "repository", "support_url", "documentation_url", "mcp_server_url"]
        for field in url_fields:
            url_match = re.search(f'^{field}:\\s*"?([^"\n]+)"?', frontmatter, re.MULTILINE)
            if url_match:
                url = url_match.group(1)
                if not url.startswith(("http://", "https://")):
                    self.log("WARNING", f"{field} '{url}' should be a valid HTTP(S) URL")
        
        if all_valid:
            self.log("SUCCESS", "Metadata validation passed")
        
        return all_valid
    
    def validate_internal_links(self, fix: bool = False) -> bool:
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
                self.log("WARNING", "mcp.json missing 'senzing-mcp-server' configuration")
            else:
                server_config = servers["senzing-mcp-server"]
                
                # Check required fields
                if "url" not in server_config:
                    self.log("ERROR", "senzing-mcp-server missing 'url' field")
                    all_valid = False
                
                # Check optional but recommended fields
                if "disabled" not in server_config:
                    self.log("INFO", "senzing-mcp-server missing 'disabled' field (optional)")
                
                if "timeout" not in server_config:
                    self.log("INFO", "senzing-mcp-server missing 'timeout' field (optional)")
        
        if all_valid:
            self.log("SUCCESS", "mcp.json validation passed")
        
        return all_valid
    
    def validate_steering_completeness(self) -> bool:
        """Validate that steering files are complete and cross-referenced"""
        self.log("INFO", "Validating steering file completeness...")
        
        steering_md = self.power_dir / "steering" / "steering.md"
        if not steering_md.exists():
            self.log("ERROR", "steering/steering.md not found")
            return False
        
        content = steering_md.read_text()
        
        # Expected steering files
        expected_files = [
            "getting-started.md",
            "quick-reference.md",
            "best-practices.md",
            "performance.md",
            "troubleshooting.md",
            "examples.md",
            "use-cases.md",
            "security-compliance.md",
            "advanced-topics.md",
            "monitoring.md",
            "data-sources.md",
            "cicd.md",
            "faq.md",
            "community.md",
            "reference.md",
            "config-examples.md",
            "smoke-test.md",
            "offline-mode.md"
        ]
        
        all_valid = True
        
        # Check that each file is referenced in steering.md
        for file in expected_files:
            if file not in content:
                self.log("WARNING", f"steering.md doesn't reference {file}")
                all_valid = False
        
        if all_valid:
            self.log("SUCCESS", "Steering file completeness validation passed")
        
        return all_valid
    
    def check_file_sizes(self) -> bool:
        """Check for unusually large files"""
        self.log("INFO", "Checking file sizes...")
        
        max_size_kb = 500  # 500 KB warning threshold
        
        md_files = list(self.power_dir.glob("**/*.md"))
        
        for md_file in md_files:
            size_kb = md_file.stat().st_size / 1024
            if size_kb > max_size_kb:
                self.log("WARNING", f"Large file: {md_file.relative_to(self.power_dir)} ({size_kb:.1f} KB)")
        
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
    
    def run_all_validations(self, fix_links: bool = False) -> bool:
        """Run all validation checks"""
        print("\n" + "="*60)
        print("Senzing Power Validation")
        print("="*60 + "\n")
        
        results = []
        
        results.append(self.validate_file_structure())
        results.append(self.validate_metadata())
        results.append(self.validate_mcp_config())
        results.append(self.validate_internal_links(fix=fix_links))
        results.append(self.validate_steering_completeness())
        results.append(self.check_file_sizes())
        
        print("\n" + "="*60)
        print("Validation Summary")
        print("="*60)
        
        report = self.generate_report()
        
        print(f"\n❌ Errors: {report['errors']}")
        print(f"⚠️  Warnings: {report['warnings']}")
        print(f"ℹ️  Info: {report['info']}")
        
        if report['errors'] == 0 and report['warnings'] == 0:
            print("\n🎉 All validations passed! Power is ready for production.")
            return True
        elif report['errors'] == 0:
            print(f"\n✅ No errors found, but {report['warnings']} warnings to review.")
            return True
        else:
            print(f"\n❌ Validation failed with {report['errors']} errors.")
            return False

def main():
    parser = argparse.ArgumentParser(description="Validate Senzing Kiro Power")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--fix-links", action="store_true", help="Attempt to fix broken links")
    parser.add_argument("--dir", default=".", help="Power directory (default: current directory)")
    
    args = parser.parse_args()
    
    validator = PowerValidator(power_dir=args.dir, verbose=args.verbose)
    success = validator.run_all_validations(fix_links=args.fix_links)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
