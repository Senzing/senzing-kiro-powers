# Senzing Power Quick Start

Get started with Senzing entity resolution in Kiro in minutes.

## Installation

1. Place the `senzing` folder in your Kiro powers directory
2. The MCP server connection is configured automatically
3. Start using Senzing in your Kiro chat

## First Steps

### 1. Verify Connection

Ask Kiro:

```
Check if the Senzing power is working
```

Kiro will call `get_capabilities` to verify the MCP server connection.

### 2. Learn About Senzing

Ask Kiro:

```
What is Senzing and how does entity resolution work?
```

### 3. Try a Sample Workflow

Ask Kiro:

```
Show me sample data from the las-vegas CORD dataset
```

## Common Tasks

### Map Your Data

```
I have a CSV file at /path/to/customers.csv that I need to map to Senzing format
```

Kiro will guide you through the interactive mapping workflow.

### Install Senzing SDK

```
Help me install the Senzing SDK on [your platform]
```

Replace `[your platform]` with: Ubuntu, CentOS, macOS, Windows, or Docker.

### Generate Code

```
Generate Python code to load records into Senzing
```

Kiro will create working SDK code from real examples.

### Troubleshoot Errors

```
I'm getting error SENZ1234 when loading records
```

Kiro will explain the error and provide resolution steps.

### Build Reports

```
How do I export entity resolution results and build analytics reports?
```

Kiro will provide SQL queries, data mart schemas, and visualization guidance.

## Key Concepts

- **Entity** - A real-world person or organization
- **Data Source** - Where records come from (e.g., "CUSTOMERS")
- **Record ID** - Unique identifier within a data source
- **Feature** - Attributes used for matching (NAME, ADDRESS, PHONE, etc.)
- **Matched** - Records confirmed as the same entity
- **Possible Match** - Records that might be the same entity

## Tips

- The power always uses the latest Senzing documentation
- Data mapping and analysis happen locally - no data is sent to the server
- Use `search_docs` for any Senzing question before web search
- Check for anti-patterns before deploying to production

## Next Steps

- Read [senzing/POWER.md](senzing/POWER.md) for detailed workflows
- Explore the 14 MCP tools available
- Try the CORD sample datasets
- Generate SDK code in your preferred language

## Need Help?

Ask Kiro to search the documentation:

```
Search Senzing docs for [your topic]
```

Or submit feedback through the power:

```
Submit feedback about the Senzing MCP server
```
