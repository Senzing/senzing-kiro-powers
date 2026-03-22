# Senzing — Steering Guide

This document provides navigation to detailed guidance for the Senzing power. The agent loads these on-demand when users engage with Senzing activities.

## Quick Navigation

### For New Users
Start with [getting-started.md](getting-started.md) for:
- MCP tool catalog
- Decision trees for choosing the right tool
- Common workflows
- Data flow diagrams
- Entity resolution design patterns

### For Quick Commands
See [quick-reference.md](quick-reference.md) for:
- Copy-paste ready commands
- Common parameter combinations
- One-liners for frequent tasks
- Bash shortcuts
- Quick workflows

### For Best Practices
See [best-practices.md](best-practices.md) for:
- What to always do and never do
- Common pitfalls and how to avoid them
- Data quality considerations
- Configuration best practices

### For Performance
See [performance.md](performance.md) for:
- Database selection guidance
- Loading and query optimization
- PostgreSQL tuning
- Monitoring metrics
- Scaling strategies

### For Troubleshooting
See [troubleshooting.md](troubleshooting.md) for:
- Quick troubleshooting reference
- Error handling strategies
- Common error codes
- Typical troubleshooting sessions
- Network and connectivity issues

### For Code Examples
See [examples.md](examples.md) for:
- Basic record loading (Python, Java, C#)
- Batch loading patterns
- Entity search examples
- Why analysis examples
- Error handling patterns
- Integration patterns (Kafka, REST API)
- Testing examples

### For Real-World Use Cases
See [use-cases.md](use-cases.md) for:
- Customer 360 implementation
- Fraud detection network
- KYC/compliance screening
- Data migration and deduplication
- Vendor master data management

### For Security and Compliance
See [security-compliance.md](security-compliance.md) for:
- PII handling best practices
- GDPR and CCPA compliance
- Access control and RBAC
- Audit logging
- Data encryption

### For Advanced Topics
See [advanced-topics.md](advanced-topics.md) for:
- Custom configuration tuning
- Advanced matching rules
- Network analysis techniques
- Graph traversal patterns
- Advanced export patterns

### For Monitoring
See [monitoring.md](monitoring.md) for:
- Key metrics to track
- Prometheus integration
- Grafana dashboards
- Alerting rules
- Health checks

### For Data Source Integration
See [data-sources.md](data-sources.md) for:
- CRM systems (Salesforce, HubSpot)
- ERP systems (SAP, Oracle)
- E-commerce platforms (Shopify, WooCommerce)
- Marketing platforms (Mailchimp, Marketo)
- Public records and watchlists

### For CI/CD Integration
See [cicd.md](cicd.md) for:
- GitHub Actions workflows
- GitLab CI pipelines
- Jenkins configuration
- Automated testing
- Deployment automation

### For FAQ
See [faq.md](faq.md) for:
- General questions
- Licensing and pricing
- Technical questions
- Performance questions
- Troubleshooting questions

### For Community Resources
See [community.md](community.md) for:
- Official resources
- Learning materials
- Support channels
- Community projects
- Contributing guidelines

### For Reference
See [reference.md](reference.md) for:
- MCP tool parameter quick reference
- Interactive checklists (pre-deployment, data mapping, production readiness)
- Cost and licensing guidance
- Integration patterns
- Testing strategy
- Glossary of Senzing terms

### For Configuration
See [config-examples.md](config-examples.md) for:
- Configuration examples for all scenarios
- Development, staging, and production configs
- Performance-tuned configurations
- Security-hardened configurations
- Proxy configurations
- Multi-environment setup

### For Testing
See [smoke-test.md](smoke-test.md) for:
- Quick 5-minute smoke test
- Detailed 15-minute test suite
- Automated validation procedures
- Common issues and solutions

### For Offline Usage
See [offline-mode.md](offline-mode.md) for:
- What works offline vs requires internet
- Air-gapped environment setup
- Offline alternatives and workarounds
- Pre-offline preparation checklist

## Key Principles

1. **Always use the tools**: Tools like `mapping_workflow`, `generate_scaffold`, and `sdk_guide` produce validated, version-correct output. Never hand-code Senzing JSON or SDK calls.

2. **Start with capabilities**: Call `get_capabilities` at the start of any Senzing session to discover available tools and workflows.

3. **Validate everything**: Use `lint_record` and `analyze_record` before loading data to catch issues early.

4. **Test with small batches**: Always test with 100-1000 records before loading millions.

5. **Choose the right database**: SQLite for evaluation (< 100K records), PostgreSQL for production.

6. **Monitor and optimize**: Track loading throughput, query performance, and resource utilization.

## Quick Links by Task

| Task | Primary Guide | Supporting Guides |
| --- | --- | --- |
| First-time setup | [getting-started.md](getting-started.md) | [quick-reference.md](quick-reference.md), [reference.md](reference.md) |
| Quick commands | [quick-reference.md](quick-reference.md) | [getting-started.md](getting-started.md) |
| Map new data source | [getting-started.md](getting-started.md) | [best-practices.md](best-practices.md), [data-sources.md](data-sources.md) |
| Write loader code | [examples.md](examples.md) | [best-practices.md](best-practices.md), [quick-reference.md](quick-reference.md) |
| Optimize performance | [performance.md](performance.md) | [monitoring.md](monitoring.md), [reference.md](reference.md) |
| Debug issues | [troubleshooting.md](troubleshooting.md) | [examples.md](examples.md), [faq.md](faq.md) |
| Production deployment | [reference.md](reference.md) | [performance.md](performance.md), [security-compliance.md](security-compliance.md), [cicd.md](cicd.md) |
| Security/compliance | [security-compliance.md](security-compliance.md) | [reference.md](reference.md) |
| Real-world examples | [use-cases.md](use-cases.md) | [examples.md](examples.md), [data-sources.md](data-sources.md) |
| Advanced techniques | [advanced-topics.md](advanced-topics.md) | [performance.md](performance.md) |
| Set up monitoring | [monitoring.md](monitoring.md) | [performance.md](performance.md) |
| Integrate data source | [data-sources.md](data-sources.md) | [getting-started.md](getting-started.md) |
| CI/CD setup | [cicd.md](cicd.md) | [reference.md](reference.md) |
| Find answers | [faq.md](faq.md) | [troubleshooting.md](troubleshooting.md) |
| Get help | [community.md](community.md) | [faq.md](faq.md) |
| Understand concepts | [reference.md](reference.md) | [getting-started.md](getting-started.md) |
| Configure power | [config-examples.md](config-examples.md) | [reference.md](reference.md) |
| Test power | [smoke-test.md](smoke-test.md) | [getting-started.md](getting-started.md) |
| Work offline | [offline-mode.md](offline-mode.md) | [getting-started.md](getting-started.md) |

## Document Structure

```
steering/
├── steering.md (this file) - Navigation hub
├── getting-started.md - Quick start, workflows, decision trees, diagrams
├── quick-reference.md - Command cheat sheet, one-liners, copy-paste commands
├── best-practices.md - Do's, don'ts, common pitfalls
├── performance.md - Optimization, tuning, scaling
├── troubleshooting.md - Error handling, debugging, typical sessions
├── examples.md - Code examples and patterns (Python, Java, C#)
├── use-cases.md - Real-world implementation walkthroughs
├── security-compliance.md - Security, GDPR, CCPA, access control
├── advanced-topics.md - Custom config, network analysis, graph traversal
├── monitoring.md - Metrics, alerting, dashboards, health checks
├── data-sources.md - CRM, ERP, e-commerce, public records integration
├── cicd.md - GitHub Actions, GitLab CI, Jenkins, deployment automation
├── faq.md - Comprehensive frequently asked questions
├── community.md - Resources, support, learning materials
├── reference.md - Tool parameters, checklists, glossary
├── config-examples.md - Configuration examples for all scenarios
├── smoke-test.md - Quick validation and testing procedures
└── offline-mode.md - Offline usage and air-gapped deployments
```

## How to Use These Guides

1. **New to Senzing?** Start with [getting-started.md](getting-started.md)
2. **Need quick commands?** Check [quick-reference.md](quick-reference.md)
3. **Building something?** Check [examples.md](examples.md) for code patterns
4. **Hitting issues?** Go to [troubleshooting.md](troubleshooting.md) or [faq.md](faq.md)
5. **Optimizing?** See [performance.md](performance.md) and [monitoring.md](monitoring.md)
6. **Need a checklist?** Use [reference.md](reference.md)
7. **Want best practices?** Read [best-practices.md](best-practices.md)
8. **Real-world examples?** See [use-cases.md](use-cases.md)
9. **Security/compliance?** Check [security-compliance.md](security-compliance.md)
10. **Advanced techniques?** Explore [advanced-topics.md](advanced-topics.md)
11. **Integrating data?** See [data-sources.md](data-sources.md)
12. **Setting up CI/CD?** Check [cicd.md](cicd.md)
13. **Need help?** Visit [community.md](community.md)
14. **Configuring power?** See [config-examples.md](config-examples.md)
15. **Testing power?** Check [smoke-test.md](smoke-test.md)
16. **Working offline?** See [offline-mode.md](offline-mode.md)

## Getting Help

- **Documentation**: Use `search_docs` for indexed Senzing documentation
- **Examples**: Use `find_examples` to search 27 Senzing GitHub repositories
- **Errors**: Use `explain_error_code` for specific error diagnosis
- **Feedback**: Use `submit_feedback` to report issues or suggestions
- **Support**: https://senzing.zendesk.com/hc/en-us/requests/new
