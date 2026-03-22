# Senzing Power - Configuration Examples

This guide provides example configurations for different scenarios and environments.

## Table of Contents

1. [Basic Configuration](#basic-configuration)
2. [Development Configuration](#development-configuration)
3. [Production Configuration](#production-configuration)
4. [Performance-Tuned Configuration](#performance-tuned-configuration)
5. [Security-Hardened Configuration](#security-hardened-configuration)
6. [Multi-Environment Setup](#multi-environment-setup)
7. [Proxy Configuration](#proxy-configuration)
8. [Troubleshooting Configuration](#troubleshooting-configuration)

## Basic Configuration

### Minimal Setup

The simplest configuration for getting started:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false
    }
  }
}
```

**Use Case**: First-time users, quick evaluation

**Features**:
- Default timeout (30 seconds)
- No custom environment variables
- No auto-approval

## Development Configuration

### Local Development

Optimized for development with verbose logging:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 60000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "DEBUG"
      },
      "autoApprove": []
    }
  }
}
```

**Use Case**: Active development, debugging

**Features**:
- Extended timeout (60 seconds) for debugging
- DEBUG logging for troubleshooting
- No auto-approval for safety

### Development with Auto-Approval

For faster development workflow:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 45000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "INFO"
      },
      "autoApprove": [
        "get_capabilities",
        "search_docs",
        "get_sample_data",
        "explain_error_code",
        "get_sdk_reference"
      ]
    }
  }
}
```

**Use Case**: Rapid prototyping, frequent tool use

**Features**:
- Auto-approve read-only tools
- INFO logging (less verbose)
- Moderate timeout

**Warning**: Only auto-approve tools you trust and understand.

## Production Configuration

### Standard Production

Balanced configuration for production use:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 30000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "WARN"
      },
      "autoApprove": []
    }
  }
}
```

**Use Case**: Production deployments, stable operations

**Features**:
- Standard timeout (30 seconds)
- WARN logging (errors and warnings only)
- No auto-approval (manual review required)

### High-Availability Production

For mission-critical deployments:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 20000,
      "retries": 3,
      "retryDelay": 1000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "ERROR"
      },
      "autoApprove": []
    }
  }
}
```

**Use Case**: Critical systems, high uptime requirements

**Features**:
- Shorter timeout (20 seconds) for faster failure detection
- Retry logic (3 attempts)
- ERROR logging only (minimal noise)
- No auto-approval

**Note**: `retries` and `retryDelay` may not be supported by all MCP implementations. Check your Kiro version.

## Performance-Tuned Configuration

### High-Performance Setup

Optimized for speed and throughput:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 15000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "ERROR",
        "SENZING_MCP_CACHE_ENABLED": "true",
        "SENZING_MCP_CACHE_TTL": "3600"
      },
      "autoApprove": [
        "get_capabilities",
        "search_docs",
        "get_sdk_reference",
        "explain_error_code"
      ]
    }
  }
}
```

**Use Case**: High-volume operations, performance-critical

**Features**:
- Short timeout (15 seconds)
- Caching enabled (if supported)
- Auto-approve frequently used tools
- Minimal logging

**Trade-offs**: Less safety, more speed

### Batch Processing

For large-scale batch operations:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 120000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "WARN",
        "SENZING_MCP_BATCH_MODE": "true"
      },
      "autoApprove": [
        "mapping_workflow",
        "lint_record",
        "analyze_record"
      ]
    }
  }
}
```

**Use Case**: Batch data mapping, bulk operations

**Features**:
- Extended timeout (120 seconds) for large files
- Batch mode optimization (if supported)
- Auto-approve data processing tools

## Security-Hardened Configuration

### Maximum Security

Strictest security settings:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 30000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "INFO",
        "SENZING_MCP_AUDIT_LOG": "true",
        "SENZING_MCP_AUDIT_LOG_PATH": "/var/log/senzing/mcp-audit.log"
      },
      "autoApprove": [],
      "requireConfirmation": true
    }
  }
}
```

**Use Case**: Regulated industries, sensitive data

**Features**:
- No auto-approval
- Audit logging enabled
- Explicit confirmation required
- INFO logging for audit trail

**Note**: Audit logging features depend on Kiro version support.

### Compliance Mode

For GDPR/CCPA compliance:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 30000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "INFO",
        "SENZING_MCP_DATA_RETENTION": "session",
        "SENZING_MCP_PII_HANDLING": "strict"
      },
      "autoApprove": [],
      "dataHandling": {
        "logRequests": true,
        "logResponses": false,
        "retainData": false
      }
    }
  }
}
```

**Use Case**: GDPR, CCPA, data privacy compliance

**Features**:
- Session-only data retention
- Strict PII handling
- Request logging (not responses)
- No data retention

## Multi-Environment Setup

### Development, Staging, Production

Use environment variables to switch configurations:

**config.dev.json**:
```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 60000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "DEBUG",
        "ENVIRONMENT": "development"
      },
      "autoApprove": [
        "get_capabilities",
        "search_docs",
        "get_sample_data"
      ]
    }
  }
}
```

**config.staging.json**:
```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 45000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "INFO",
        "ENVIRONMENT": "staging"
      },
      "autoApprove": []
    }
  }
}
```

**config.prod.json**:
```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 30000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "WARN",
        "ENVIRONMENT": "production"
      },
      "autoApprove": []
    }
  }
}
```

**Usage**:
```bash
# Switch environments
cp config.dev.json mcp.json    # Development
cp config.staging.json mcp.json # Staging
cp config.prod.json mcp.json   # Production
```

### Environment-Specific URLs

For organizations with multiple MCP servers:

```json
{
  "mcpServers": {
    "senzing-mcp-dev": {
      "url": "https://mcp-dev.senzing.com/mcp",
      "disabled": false,
      "timeout": 60000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "DEBUG"
      }
    },
    "senzing-mcp-prod": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": true,
      "timeout": 30000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "WARN"
      }
    }
  }
}
```

**Note**: Enable only one server at a time by setting `disabled: true` for others.

## Proxy Configuration

### Corporate Proxy

For environments behind corporate proxy:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 45000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "INFO",
        "HTTP_PROXY": "http://proxy.company.com:8080",
        "HTTPS_PROXY": "http://proxy.company.com:8080",
        "NO_PROXY": "localhost,127.0.0.1"
      },
      "autoApprove": []
    }
  }
}
```

**Use Case**: Corporate networks, proxy servers

**Features**:
- HTTP/HTTPS proxy configuration
- NO_PROXY for local addresses
- Extended timeout for proxy latency

### Authenticated Proxy

With proxy authentication:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 45000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "INFO",
        "HTTP_PROXY": "http://username:password@proxy.company.com:8080",
        "HTTPS_PROXY": "http://username:password@proxy.company.com:8080"
      },
      "autoApprove": []
    }
  }
}
```

**Security Note**: Store credentials securely, not in plain text. Use environment variables or secret management.

## Troubleshooting Configuration

### Debug Mode

Maximum verbosity for troubleshooting:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 120000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "DEBUG",
        "SENZING_MCP_TRACE": "true",
        "SENZING_MCP_VERBOSE": "true"
      },
      "autoApprove": []
    }
  }
}
```

**Use Case**: Debugging connection issues, investigating errors

**Features**:
- DEBUG logging
- Request/response tracing
- Verbose output
- Extended timeout

### Connection Testing

Minimal config for testing connectivity:

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 10000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

**Test with**:
```python
# Simple connectivity test
get_capabilities(version="current")
```

## Configuration Best Practices

### 1. Environment-Specific Configs

Don't use the same configuration for all environments:
- Development: Verbose logging, longer timeouts
- Staging: Moderate logging, standard timeouts
- Production: Minimal logging, optimized timeouts

### 2. Timeout Tuning

Adjust timeouts based on your network:
- Fast network: 15-30 seconds
- Average network: 30-45 seconds
- Slow network: 45-60 seconds
- Batch operations: 60-120 seconds

### 3. Logging Levels

Choose appropriate logging:
- **DEBUG**: Development, troubleshooting
- **INFO**: Normal operations, audit trail
- **WARN**: Production (errors and warnings only)
- **ERROR**: High-performance (errors only)

### 4. Auto-Approval

Only auto-approve tools you trust:
- ✅ Safe: `get_capabilities`, `search_docs`, `get_sdk_reference`
- ⚠️ Caution: `mapping_workflow`, `generate_scaffold`
- ❌ Never: Tools that modify data or configurations

### 5. Security

- Don't commit credentials to version control
- Use environment variables for sensitive data
- Enable audit logging in production
- Review auto-approved tools regularly
- Use HTTPS only (never HTTP)

### 6. Performance

- Use shorter timeouts for faster failure detection
- Enable caching if available
- Auto-approve frequently used read-only tools
- Minimize logging in production

### 7. Monitoring

- Log all configuration changes
- Monitor timeout rates
- Track tool usage patterns
- Alert on configuration errors

## Configuration Validation

### Validate Your Configuration

```bash
# Check JSON syntax
python -m json.tool mcp.json

# Validate with power script
python validate_power.py

# Test connectivity
# Use get_capabilities to verify connection
```

### Common Configuration Errors

**Invalid JSON**:
```json
// ❌ Wrong: Trailing comma
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
    }
  }
}

// ✅ Correct: No trailing comma
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp"
    }
  }
}
```

**Wrong URL**:
```json
// ❌ Wrong: HTTP instead of HTTPS
"url": "http://mcp.senzing.com/mcp"

// ✅ Correct: HTTPS
"url": "https://mcp.senzing.com/mcp"
```

**Invalid Timeout**:
```json
// ❌ Wrong: String instead of number
"timeout": "30000"

// ✅ Correct: Number
"timeout": 30000
```

## Configuration Templates

### Quick Start Template

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 30000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "INFO"
      },
      "autoApprove": []
    }
  }
}
```

### Full-Featured Template

```json
{
  "mcpServers": {
    "senzing-mcp-server": {
      "url": "https://mcp.senzing.com/mcp",
      "disabled": false,
      "timeout": 30000,
      "env": {
        "SENZING_MCP_LOG_LEVEL": "INFO",
        "HTTP_PROXY": "",
        "HTTPS_PROXY": "",
        "NO_PROXY": "localhost,127.0.0.1"
      },
      "autoApprove": [],
      "metadata": {
        "environment": "production",
        "version": "0.1.0",
        "owner": "team-name"
      }
    }
  }
}
```

## Migrating Configurations

### From Default to Custom

1. **Backup current config**:
   ```bash
   cp mcp.json mcp.json.backup
   ```

2. **Choose template** from examples above

3. **Customize** for your environment

4. **Validate**:
   ```bash
   python validate_power.py
   ```

5. **Test**:
   ```python
   get_capabilities(version="current")
   ```

### Version Control

Store configurations in version control:

```bash
# .gitignore
mcp.json          # Don't commit active config
*.backup          # Don't commit backups

# Commit templates
git add config.*.json
git commit -m "Add environment-specific configs"
```

## Support

For configuration help:
- Review this guide
- Check SMOKE_TEST.md for testing
- Use `submit_feedback` MCP tool
- Contact Senzing support

## Resources

- **Power Validation**: `validate_power.py`
- **Smoke Testing**: `SMOKE_TEST.md`
- **Offline Mode**: `OFFLINE_MODE.md`
- **Metadata**: `METADATA.md`
- **Troubleshooting**: `steering/troubleshooting.md`

---

**Note**: Configuration options may vary by Kiro version. Check your Kiro documentation for supported fields and features.
