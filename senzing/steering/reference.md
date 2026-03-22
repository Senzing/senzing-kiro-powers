# Senzing — Reference Guide

This guide provides quick reference materials including tool parameters, checklists, cost guidance, integration patterns, testing strategies, and a glossary.

## MCP Tool Parameter Quick Reference

### get_capabilities
- **Required**: `version` (string) - e.g., "current", "4.0"
- **Returns**: Server info, available tools, workflows, getting started guidance

### mapping_workflow
- **Required**: `action` (string) - "start", "advance", "back", "status", "reset"
- **Optional**: 
  - `file_paths` (array) - Required for "start" action
  - `state` (object) - Required for all actions except "start"
  - `data` (object) - Required for "advance" action
  - `version` (string) - Default: "current"
- **Returns**: Workflow state, instructions, mapped data

### lint_record
- **Optional**: 
  - `file_paths` (array) - Senzing JSON/JSONL files to validate
  - `version` (string) - Default: "current"
- **Returns**: Python linter script and commands

### analyze_record
- **Optional**: 
  - `file_paths` (array) - Senzing JSON/JSONL files to analyze
  - `version` (string) - Default: "current"
- **Returns**: Python analyzer script and commands

### generate_scaffold
- **Required**: 
  - `language` (string) - "python", "java", "csharp", "rust"
  - `workflow` (string) - "initialize", "configure", "add_records", "delete", "query", "redo", "stewardship", "information", "full_pipeline"
  - `version` (string) - "4.0" or "current"
- **Returns**: Working code with source URLs

### sdk_guide
- **Required**: `topic` (string) - "install", "configure", "load", "export", "full_pipeline"
- **Optional**: 
  - `platform` (string) - "linux_apt", "linux_yum", "macos_arm", "windows", "docker"
  - `language` (string) - "python", "java", "csharp", "rust"
  - `data_sources` (array) - For "configure" topic
  - `input_file` (string) - For "load" topic
  - `record_count` (number) - For "load" topic
  - `version` (string) - Default: "current"
- **Returns**: Platform-specific setup instructions

### get_sample_data
- **Required**: `dataset` (string) - "las-vegas", "london", "moscow", or "list"
- **Optional**: 
  - `source` (string) - Filter by vendor, or "list"
  - `limit` (number) - Number of records
  - `offset` (number or "random") - Starting position
- **Returns**: Sample records with download URL

### find_examples
- **Optional**: 
  - `query` (string) - Search query (required for search mode)
  - `repo` (string) - Specific repository
  - `language` (string) - "python", "java", "csharp", "rust"
  - `file_path` (string) - Specific file in repo
  - `list_files` (boolean) - List files in repo
  - `max_lines` (number) - Limit file content
- **Returns**: Code examples with GitHub URLs

### search_docs
- **Required**: 
  - `query` (string) - Search query
  - `version` (string) - Senzing version
- **Optional**: 
  - `category` (string) - "general", "sdk", "data_mapping", "troubleshooting", "pricing", "deployment", etc.
  - `max_results` (number) - Limit results
- **Returns**: Relevant documentation excerpts

### explain_error_code
- **Required**: 
  - `error_code` (string) - e.g., "SENZ0005", "0005", "5"
  - `version` (string) - Senzing version
- **Returns**: Error explanation, causes, resolution steps

### get_sdk_reference
- **Required**: `topic` (string) - "migration", "flags", "response_schemas", "all"
- **Optional**: 
  - `filter` (string) - Method name, module name, or flag name
  - `version` (string) - Default: "current"
- **Returns**: SDK reference data

### download_resource
- **Required**: `filename` (string) - Resource filename
- **Optional**: `version` (string) - Default: "current"
- **Returns**: Resource content

### submit_feedback
- **Required**: `message` (string) - Feedback message
- **Optional**: `category` (string) - "bug", "feature", "question", "general"
- **Returns**: Submission confirmation

## Interactive Checklists

### Pre-Deployment Checklist

- [ ] **Environment Setup**
  - [ ] Senzing SDK installed and verified
  - [ ] Database selected and configured (PostgreSQL for production)
  - [ ] Database schema initialized
  - [ ] Required data sources registered in configuration
  - [ ] Environment variables set (SENZING_ENGINE_CONFIGURATION_JSON)

- [ ] **Data Preparation**
  - [ ] Source data profiled and understood
  - [ ] Data mapping completed using `mapping_workflow`
  - [ ] Mapped data validated with `lint_record`
  - [ ] Data quality analyzed with `analyze_record`
  - [ ] Test batch loaded successfully (100-1000 records)

- [ ] **Code Development**
  - [ ] Loader code generated with `generate_scaffold`
  - [ ] Error handling implemented
  - [ ] Logging configured
  - [ ] Connection pooling configured
  - [ ] Multi-threading tested (if applicable)

- [ ] **Testing**
  - [ ] Unit tests written and passing
  - [ ] Integration tests with sample data passing
  - [ ] Performance testing completed
  - [ ] Match quality validated
  - [ ] Error scenarios tested

- [ ] **Infrastructure**
  - [ ] Database tuned for production workload
  - [ ] Backup strategy implemented
  - [ ] Monitoring configured
  - [ ] Resource limits set (CPU, memory, disk)
  - [ ] Network connectivity verified

- [ ] **Documentation**
  - [ ] Data mapping documented
  - [ ] Deployment procedures documented
  - [ ] Troubleshooting guide created
  - [ ] Runbook prepared

### Data Mapping Quality Checklist

- [ ] **Required Fields**
  - [ ] All records have DATA_SOURCE
  - [ ] All records have RECORD_ID
  - [ ] RECORD_ID is unique within each DATA_SOURCE

- [ ] **Attribute Mapping**
  - [ ] Attribute names validated (not guessed)
  - [ ] Name fields mapped correctly (NAME_FULL, NAME_FIRST, NAME_LAST, NAME_ORG)
  - [ ] Address fields mapped correctly (ADDR_FULL or components)
  - [ ] Phone numbers mapped to PHONE_NUMBER
  - [ ] Email addresses mapped to EMAIL_ADDRESS
  - [ ] Dates formatted correctly (YYYY-MM-DD)

- [ ] **Data Quality**
  - [ ] Feature coverage analyzed (% of records with each attribute)
  - [ ] No placeholder values (000-000-0000, test@test.com)
  - [ ] Data standardized (consistent formats)
  - [ ] Special characters handled correctly
  - [ ] Null/empty values handled appropriately

- [ ] **Validation**
  - [ ] `lint_record` passes with no errors
  - [ ] `analyze_record` shows acceptable coverage
  - [ ] Sample records manually reviewed
  - [ ] Test load completes successfully

### Production Readiness Checklist

- [ ] **Performance**
  - [ ] Database tuned for expected workload
  - [ ] Loading throughput meets requirements
  - [ ] Query response times acceptable
  - [ ] Resource utilization within limits

- [ ] **Reliability**
  - [ ] Error handling tested
  - [ ] Retry logic implemented
  - [ ] Database connection pooling configured
  - [ ] Failover tested (if applicable)

- [ ] **Monitoring**
  - [ ] Loading metrics tracked
  - [ ] Database metrics monitored
  - [ ] Error rates monitored
  - [ ] Alerts configured

- [ ] **Security**
  - [ ] Database credentials secured
  - [ ] Network access restricted
  - [ ] Audit logging enabled
  - [ ] Data encryption configured (if required)

- [ ] **Operations**
  - [ ] Backup and restore tested
  - [ ] Disaster recovery plan documented
  - [ ] On-call procedures defined
  - [ ] Escalation paths established

### Performance Optimization Checklist

- [ ] **Database**
  - [ ] PostgreSQL configuration tuned (shared_buffers, work_mem, etc.)
  - [ ] Indexes healthy and optimized
  - [ ] Statistics up to date (ANALYZE run)
  - [ ] Vacuum performed regularly
  - [ ] Connection pooling configured

- [ ] **Loading**
  - [ ] Batch size optimized (1000-5000 records)
  - [ ] Thread count optimized (4-8 threads typical)
  - [ ] Redo processing disabled during initial load
  - [ ] Transaction size appropriate

- [ ] **System**
  - [ ] SSD storage used
  - [ ] Sufficient RAM allocated (8GB+ for production)
  - [ ] CPU cores available for threading
  - [ ] Network latency minimized

- [ ] **Application**
  - [ ] Connection pooling implemented
  - [ ] Resource cleanup (close connections, destroy engines)
  - [ ] Memory leaks checked
  - [ ] Logging not excessive

## Cost and Licensing Guidance

### DSR (Data Source Record) Pricing Model

Senzing uses a DSR-based pricing model:

- **DSR Definition**: One record from one data source
- **Example**: If you load 1 million customer records from a CRM system, that's 1 million DSRs
- **Multiple Sources**: Loading the same entity from 3 different sources = 3 DSRs

### Evaluation Limits

- **Free Evaluation**: 500 DSRs (records) for testing
- **Purpose**: Proof of concept, evaluation, learning
- **Limitation**: Cannot be used for production workloads

### When to Contact Sales

Contact Senzing sales when:
- You need to load > 500 records
- You're ready for production deployment
- You need enterprise support
- You require custom configuration or tuning
- You have questions about pricing for your use case

### When to Self-Serve

You can self-serve for:
- Initial evaluation (< 500 records)
- Learning and training
- Development and testing with sample data
- Proof of concept demonstrations

### Cost Optimization Tips

1. **Deduplicate before loading**: Remove duplicates in source data
2. **Load only necessary fields**: Don't load attributes you won't use for matching
3. **Consolidate data sources**: Fewer sources = lower DSR count
4. **Archive old records**: Remove records no longer needed for matching

### Licensing Resources

- **Pricing information**: Use `search_docs` with category "pricing"
- **Sales contact**: https://senzing.com/contact
- **Support**: https://senzing.zendesk.com

## Integration Patterns

### Pattern 1: Batch Processing Pipeline

```
Source System → Extract → Transform → Map (mapping_workflow) → 
Validate (lint_record) → Load (Senzing) → Export Results
```

**Use cases**: Nightly data loads, data migration, periodic deduplication

**Key considerations**:
- Schedule during off-peak hours
- Use multi-threading for large volumes
- Disable redo during initial load
- Monitor for failures and retry

### Pattern 2: Real-Time Streaming

```
Event Stream (Kafka/Kinesis) → Consumer → Map → 
Load (Senzing) → Publish Results → Downstream Systems
```

**Use cases**: Real-time fraud detection, live customer 360, KYC onboarding

**Key considerations**:
- Handle backpressure
- Implement error queues (dead letter queue)
- Monitor lag and throughput
- Use connection pooling

### Pattern 3: REST API Integration

```
Client Application → REST API → Senzing SDK → 
Database → Response → Client
```

**Use cases**: Interactive applications, search interfaces, data stewardship

**Key considerations**:
- Implement rate limiting
- Cache frequently accessed entities
- Use async processing for loads
- Return appropriate HTTP status codes

### Pattern 4: Database Triggers

```
Source Database → Trigger (INSERT/UPDATE/DELETE) → 
Queue/Message Bus → Senzing Loader → Entity Repository
```

**Use cases**: Change data capture, real-time synchronization

**Key considerations**:
- Keep triggers lightweight
- Use async processing
- Handle trigger failures gracefully
- Monitor trigger performance

### Pattern 5: Microservices Architecture

```
Multiple Services → Message Bus → Senzing Service → 
Entity Repository → Query Service → Consumers
```

**Use cases**: Large-scale distributed systems, cloud-native applications

**Key considerations**:
- Service discovery and registration
- Health checks and monitoring
- Distributed tracing
- Circuit breakers for resilience

## Testing Strategy

### Unit Testing

**What to test**:
- Data mapping logic
- Record validation
- Error handling
- Configuration management

**Tools**:
- pytest (Python)
- JUnit (Java)
- NUnit (C#)
- cargo test (Rust)

**Example test cases**:
```python
def test_record_has_required_fields():
    record = create_test_record()
    assert "DATA_SOURCE" in record
    assert "RECORD_ID" in record

def test_attribute_mapping():
    source_record = {"full_name": "John Smith"}
    mapped = map_record(source_record)
    assert mapped["NAME_FULL"] == "John Smith"
```

### Integration Testing

**What to test**:
- End-to-end data flow
- SDK initialization and configuration
- Database connectivity
- Record loading and retrieval
- Entity resolution accuracy

**Approach**:
1. Set up test database (SQLite for speed)
2. Load known test data
3. Verify expected entity resolution
4. Clean up after tests

**Example test cases**:
```python
def test_entity_resolution():
    # Load two records that should match
    load_record(record1)
    load_record(record2)
    
    # Verify they resolved to same entity
    entity1 = get_entity_by_record_id(record1)
    entity2 = get_entity_by_record_id(record2)
    
    assert entity1.entity_id == entity2.entity_id
```

### Performance Testing

**What to test**:
- Loading throughput (records/second)
- Query response times
- Resource utilization (CPU, memory, disk)
- Scalability (how performance changes with data volume)

**Approach**:
1. Define performance requirements
2. Create representative test data
3. Measure baseline performance
4. Test with increasing load
5. Identify bottlenecks

**Metrics to track**:
- Records loaded per second
- Average query response time
- 95th percentile query response time
- CPU utilization
- Memory usage
- Database size growth

### Data Quality Testing

**What to test**:
- Feature coverage (% records with each attribute)
- Data completeness
- Data consistency
- Match quality (precision and recall)

**Tools**:
- `analyze_record` for coverage analysis
- `why_entities` for match analysis
- Custom scripts for quality metrics

**Example checks**:
```python
def test_data_quality():
    analysis = analyze_records(test_file)
    
    # Check feature coverage
    assert analysis["NAME_FULL_coverage"] > 0.95  # 95%+ have names
    assert analysis["EMAIL_ADDRESS_coverage"] > 0.80  # 80%+ have emails
    
    # Check for placeholder values
    assert analysis["placeholder_count"] == 0
```

### Match Quality Validation

**What to test**:
- True positives (records that should match do match)
- False positives (records that shouldn't match but do)
- False negatives (records that should match but don't)

**Approach**:
1. Create golden dataset with known matches
2. Load data into Senzing
3. Compare Senzing results to golden dataset
4. Calculate precision and recall

**Metrics**:
- **Precision**: % of Senzing matches that are correct
- **Recall**: % of true matches that Senzing found
- **F1 Score**: Harmonic mean of precision and recall

## Glossary

### Core Concepts

**Entity**: A real-world person, organization, or thing. Senzing resolves multiple records into entities.

**Record**: A single data entry from a data source. Multiple records can resolve to one entity.

**Data Source**: A system or dataset that provides records (e.g., "CUSTOMERS", "VENDORS").

**Record ID**: Unique identifier for a record within a data source.

**Entity ID**: Senzing-assigned unique identifier for a resolved entity.

**Resolution**: The process of determining which records refer to the same real-world entity.

### Matching Concepts

**Feature**: An attribute used for matching (e.g., name, address, phone).

**Principle**: A matching rule (e.g., "same name and same address").

**Candidate**: A potential match that Senzing evaluates.

**Match Level**: The strength of a match (e.g., resolved, possibly related, possibly same).

**Match Key**: The specific features that caused records to match.

**Match Score**: Numeric confidence in a match (0-100).

### Data Mapping

**Attribute**: A Senzing field name (e.g., NAME_FULL, PHONE_NUMBER).

**Feature Type**: Category of attribute (e.g., NAME, ADDRESS, PHONE).

**Mapping**: The process of transforming source data to Senzing JSON format.

**Validation**: Checking that mapped data conforms to Senzing requirements.

### Operations

**Loading**: Adding records to Senzing for resolution.

**Redo Processing**: Re-evaluating entities when new data arrives.

**Why Analysis**: Understanding why records matched or didn't match.

**Search**: Finding entities by attributes.

**Export**: Extracting resolved entities from Senzing.

### Configuration

**Configuration JSON**: JSON structure defining Senzing engine settings.

**Data Source Registration**: Adding a data source to Senzing configuration.

**Resource Path**: Directory containing Senzing matching rules and resources.

**Config Path**: Directory containing Senzing configuration database.

**Support Path**: Directory containing Senzing support files.

### Performance

**Throughput**: Records processed per unit time (e.g., records/second).

**Latency**: Time to complete an operation (e.g., query response time).

**Batch Size**: Number of records processed together.

**Thread Count**: Number of parallel processing threads.

**Connection Pool**: Reusable database connections for efficiency.

### Database

**SQLite**: Embedded database, good for evaluation (< 100K records).

**PostgreSQL**: Production database, recommended for scale (100K+ records).

**Schema**: Database structure for storing Senzing data.

**Index**: Database structure for fast lookups.

**Vacuum**: Database maintenance operation to reclaim space.

### SDK

**SzEngine**: Main SDK interface for loading and querying.

**SzConfig**: SDK interface for configuration management.

**SzConfigManager**: SDK interface for managing configuration versions.

**Initialize**: Set up SDK instance with configuration.

**Destroy**: Clean up SDK instance and release resources.

### Error Handling

**Error Code**: Senzing error identifier (e.g., SENZ0005).

**Exception**: Programming language error object.

**Retry Logic**: Automatically retrying failed operations.

**Dead Letter Queue**: Storage for records that failed to process.

### Deployment

**POC (Proof of Concept)**: Small-scale test deployment.

**Production**: Live deployment serving real workloads.

**Staging**: Pre-production environment for testing.

**High Availability**: System design for minimal downtime.

**Disaster Recovery**: Plan for recovering from system failures.
