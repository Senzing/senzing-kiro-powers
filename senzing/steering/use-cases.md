# Senzing — Real-World Use Cases

This guide provides detailed walkthroughs of common Senzing implementations with real-world scenarios.

## Table of Contents

- [Use Case 1: Customer 360 Implementation](#use-case-1-customer-360-implementation)
- [Use Case 2: Fraud Detection Network](#use-case-2-fraud-detection-network)
- [Use Case 3: KYC/Compliance Screening](#use-case-3-kyccompliance-screening)
- [Use Case 4: Data Migration and Deduplication](#use-case-4-data-migration-and-deduplication)
- [Use Case 5: Vendor Master Data Management](#use-case-5-vendor-master-data-management)

---

## Use Case 1: Customer 360 Implementation

### Business Problem
A retail company has customer data scattered across 5 systems:
- E-commerce platform (online orders)
- Point-of-sale system (in-store purchases)
- Loyalty program database
- Customer service CRM
- Email marketing platform

They need a unified view of each customer to:
- Eliminate duplicate marketing sends
- Provide consistent customer service
- Understand complete purchase history
- Identify high-value customers

### Data Sources

**E-commerce** (50K records):
- Customer ID, name, email, shipping address, phone

**POS** (200K records):
- Transaction ID, loyalty card number, name, phone

**Loyalty Program** (75K records):
- Member ID, name, email, phone, address, birthdate

**CRM** (30K records):
- Contact ID, name, email, phone, company

**Email Marketing** (100K records):
- Subscriber ID, email, name, preferences

### Implementation Steps

#### Step 1: Data Mapping (2-3 hours)

```python
# Map e-commerce data
mapping_workflow(
    action="start",
    file_paths=["ecommerce_customers.csv"],
    version="current"
)

# Follow interactive prompts to map:
# - customer_id → RECORD_ID
# - full_name → NAME_FULL
# - email → EMAIL_ADDRESS
# - phone → PHONE_NUMBER
# - shipping_address → ADDR_FULL

# Repeat for each data source with appropriate DATA_SOURCE codes:
# - "ECOMMERCE"
# - "POS"
# - "LOYALTY"
# - "CRM"
# - "EMAIL_MARKETING"
```

#### Step 2: Data Quality Analysis (30 minutes)

```python
# Analyze each mapped file
analyze_record(file_paths=["ecommerce_mapped.jsonl"], version="current")
analyze_record(file_paths=["pos_mapped.jsonl"], version="current")
analyze_record(file_paths=["loyalty_mapped.jsonl"], version="current")
analyze_record(file_paths=["crm_mapped.jsonl"], version="current")
analyze_record(file_paths=["email_mapped.jsonl"], version="current")

# Expected coverage:
# - NAME: 95%+ across all sources
# - EMAIL: 80%+ (POS may be lower)
# - PHONE: 70%+ (Email marketing may be lower)
# - ADDRESS: 60%+ (varies by source)
```

#### Step 3: Database Setup (1 hour)

```bash
# Install PostgreSQL
sudo apt-get install postgresql-12

# Create database
sudo -u postgres createdb senzing
sudo -u postgres createuser senzing -P

# Configure Senzing
sdk_guide(
    topic="configure",
    platform="linux_apt",
    language="python",
    data_sources=["ECOMMERCE", "POS", "LOYALTY", "CRM", "EMAIL_MARKETING"],
    version="current"
)
```

#### Step 4: Initial Load (2-4 hours)

```python
# Generate multi-threaded loader
generate_scaffold(
    language="python",
    workflow="add_records",
    version="current"
)

# Load each source (customize generated code):
# - Use 4-8 threads
# - Batch size: 1000 records
# - Disable redo during initial load
# - Monitor throughput (target: 1000+ records/sec)

# Expected results:
# - Total records loaded: ~455K
# - Resolved entities: ~150K (67% reduction)
# - Average records per entity: 3
```

#### Step 5: Match Quality Validation (1 hour)

```python
# Sample entity analysis
engine = SzEngine()
engine.initialize("Customer360", config_json)

# Get sample entity
result = engine.get_entity_by_record_id("ECOMMERCE", "CUST12345")
entity = json.loads(result)

# Verify entity contains records from multiple sources
sources = set(r["DATA_SOURCE"] for r in entity["RESOLVED_ENTITY"]["RECORDS"])
print(f"Entity spans {len(sources)} data sources: {sources}")

# Analyze why records matched
for i, record1 in enumerate(entity["RESOLVED_ENTITY"]["RECORDS"]):
    for record2 in entity["RESOLVED_ENTITY"]["RECORDS"][i+1:]:
        why = engine.why_records(
            record1["DATA_SOURCE"], record1["RECORD_ID"],
            record2["DATA_SOURCE"], record2["RECORD_ID"]
        )
        print(f"Match: {record1['DATA_SOURCE']} + {record2['DATA_SOURCE']}")
        print(f"  Key: {json.loads(why)['MATCH_INFO']['MATCH_KEY']}")
```

### Results

**Before Senzing**:
- 455,000 customer records across 5 systems
- No way to link records across systems
- Duplicate marketing sends
- Incomplete customer history

**After Senzing**:
- 150,000 unique customers identified
- 67% reduction in duplicates
- Unified customer profiles
- Complete cross-channel history

**Business Impact**:
- 40% reduction in marketing costs (fewer duplicate sends)
- 25% increase in customer satisfaction (consistent service)
- 15% increase in cross-sell opportunities (complete purchase history)

---

## Use Case 2: Fraud Detection Network

### Business Problem
An insurance company needs to detect fraud rings where multiple people stage accidents and file false claims. Fraudsters use:
- Fake identities
- Shared addresses
- Shared phone numbers
- Shared vehicles
- Shared medical providers

### Data Sources

**Claims** (500K records):
- Claim ID, claimant name, address, phone, SSN, vehicle VIN

**Providers** (50K records):
- Provider ID, name, address, phone, tax ID

**Vehicles** (300K records):
- VIN, owner name, address, registration

**Watchlist** (10K records):
- Known fraudsters, aliases, addresses

### Implementation Steps

#### Step 1: Entity Type Planning

```python
# Define entity types:
# 1. PERSON entities (claimants, providers)
# 2. ORGANIZATION entities (medical providers, body shops)
# 3. VEHICLE entities (cars involved in claims)

# Map data with appropriate entity types
mapping_workflow(
    action="start",
    file_paths=["claims.csv", "providers.csv", "vehicles.csv", "watchlist.csv"],
    version="current"
)

# Key mappings:
# - Claimant → PERSON entity (NAME_FULL, ADDR_FULL, PHONE_NUMBER, SSN_NUMBER)
# - Provider → ORGANIZATION entity (NAME_ORG, ADDR_FULL, PHONE_NUMBER, TAX_ID_NUMBER)
# - Vehicle → Custom attributes (VIN, OWNER_NAME)
```

#### Step 2: Network Analysis Setup

```python
# Load all data
generate_scaffold(language="python", workflow="full_pipeline", version="current")

# After loading, identify suspicious networks
engine = SzEngine()
engine.initialize("FraudDetection", config_json)

# Find entities with many records (potential fraud rings)
# Custom query to find entities with 5+ records from different claims
```

#### Step 3: Fraud Ring Detection

```python
# Example: Detect shared addresses
def find_shared_addresses():
    # Query entities with same address but different names
    # This indicates potential fraud ring
    
    suspicious_entities = []
    
    # Search for entities at known fraud addresses
    for address in known_fraud_addresses:
        result = engine.search_by_attributes(
            json.dumps({"ADDR_FULL": address})
        )
        entities = json.loads(result)
        
        if len(entities.get("RESOLVED_ENTITIES", [])) > 3:
            suspicious_entities.append({
                "address": address,
                "entity_count": len(entities["RESOLVED_ENTITIES"]),
                "entities": entities["RESOLVED_ENTITIES"]
            })
    
    return suspicious_entities

# Example: Detect shared phones
def find_shared_phones():
    # Similar logic for phone numbers
    pass

# Example: Network traversal
def analyze_fraud_network(entity_id):
    # Get entity details
    entity = json.loads(engine.get_entity_by_entity_id(entity_id))
    
    # Extract all related identifiers
    addresses = set()
    phones = set()
    vehicles = set()
    
    for record in entity["RESOLVED_ENTITY"]["RECORDS"]:
        # Extract features
        for feature in record.get("FEATURES", []):
            if feature["FEATURE_TYPE"] == "ADDRESS":
                addresses.add(feature["FEATURE_VALUE"])
            elif feature["FEATURE_TYPE"] == "PHONE":
                phones.add(feature["FEATURE_VALUE"])
    
    # Find other entities sharing these identifiers
    network = {"entities": [entity_id], "connections": []}
    
    for address in addresses:
        result = engine.search_by_attributes(
            json.dumps({"ADDR_FULL": address})
        )
        # Add connected entities to network
    
    return network
```

### Results

**Fraud Ring Example**:
- 15 people identified in fraud ring
- Shared 3 addresses, 5 phone numbers, 8 vehicles
- 47 fraudulent claims totaling $2.3M
- Network visualization shows clear connections

**Business Impact**:
- $2.3M in fraudulent claims prevented
- 15 criminal referrals made
- Fraud detection time reduced from weeks to hours
- Proactive identification of new fraud patterns

---

## Use Case 3: KYC/Compliance Screening

### Business Problem
A financial institution must screen new customers against:
- OFAC sanctions lists
- PEP (Politically Exposed Persons) lists
- Internal watchlists
- Adverse media

They need to:
- Screen during account opening (real-time)
- Re-screen existing customers (batch)
- Handle name variations and aliases
- Minimize false positives

### Data Sources

**Customer Applications** (streaming):
- Name, DOB, address, nationality, ID numbers

**OFAC SDN List** (updated daily):
- Names, aliases, DOB, nationalities, IDs

**PEP Lists** (updated weekly):
- Names, positions, countries, DOB

**Internal Watchlist** (updated continuously):
- Previous fraud cases, closed accounts

### Implementation Steps

#### Step 1: Watchlist Loading

```python
# Map watchlist data
mapping_workflow(
    action="start",
    file_paths=["ofac_sdn.csv", "pep_list.csv", "internal_watchlist.csv"],
    version="current"
)

# Key considerations:
# - Map all name variations (NAME_FULL, NAME_FIRST, NAME_LAST)
# - Include all aliases
# - Map DOB, nationalities, ID numbers
# - Use appropriate DATA_SOURCE codes: "OFAC", "PEP", "WATCHLIST"

# Load watchlists
generate_scaffold(language="python", workflow="add_records", version="current")
```

#### Step 2: Real-Time Screening API

```python
from flask import Flask, request, jsonify
from senzing import SzEngine
import json

app = Flask(__name__)
engine = SzEngine()
engine.initialize("KYC_Screening", config_json)

@app.route('/screen', methods=['POST'])
def screen_customer():
    """Screen a customer application against watchlists"""
    
    customer = request.json
    
    # Search for matches
    search_criteria = {
        "NAME_FULL": customer["name"],
        "DATE_OF_BIRTH": customer["dob"],
        "NATIONALITY": customer["nationality"]
    }
    
    result = engine.search_by_attributes(json.dumps(search_criteria))
    matches = json.loads(result)
    
    # Analyze matches
    risk_level = "LOW"
    matched_lists = []
    
    for entity in matches.get("RESOLVED_ENTITIES", []):
        match_score = entity.get("MATCH_SCORE", 0)
        
        # Check which watchlists matched
        for record in entity.get("RECORDS", []):
            if record["DATA_SOURCE"] in ["OFAC", "PEP", "WATCHLIST"]:
                if match_score > 90:
                    risk_level = "HIGH"
                    matched_lists.append({
                        "list": record["DATA_SOURCE"],
                        "record_id": record["RECORD_ID"],
                        "score": match_score
                    })
                elif match_score > 70:
                    risk_level = max(risk_level, "MEDIUM")
    
    return jsonify({
        "customer_id": customer["id"],
        "risk_level": risk_level,
        "matches": matched_lists,
        "requires_review": risk_level in ["HIGH", "MEDIUM"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### Step 3: Batch Re-Screening

```python
def rescreen_existing_customers():
    """Re-screen all existing customers against updated watchlists"""
    
    engine = SzEngine()
    engine.initialize("Batch_Rescreen", config_json)
    
    # Get all customer records
    customers = load_customers_from_database()
    
    flagged_customers = []
    
    for customer in customers:
        # Search for matches
        result = engine.search_by_attributes(
            json.dumps({
                "NAME_FULL": customer["name"],
                "DATE_OF_BIRTH": customer["dob"]
            })
        )
        
        matches = json.loads(result)
        
        # Check for watchlist matches
        for entity in matches.get("RESOLVED_ENTITIES", []):
            for record in entity.get("RECORDS", []):
                if record["DATA_SOURCE"] in ["OFAC", "PEP", "WATCHLIST"]:
                    flagged_customers.append({
                        "customer_id": customer["id"],
                        "matched_list": record["DATA_SOURCE"],
                        "match_score": entity.get("MATCH_SCORE", 0)
                    })
    
    # Generate report
    generate_compliance_report(flagged_customers)
    
    engine.destroy()
```

### Results

**Screening Performance**:
- Real-time screening: < 200ms per application
- Batch re-screening: 10,000 customers/hour
- False positive rate: < 5% (down from 30% with previous system)
- True positive detection: 99.8%

**Business Impact**:
- Regulatory compliance maintained
- Customer onboarding time reduced by 60%
- Manual review workload reduced by 75%
- Zero regulatory fines for missed matches

---

## Use Case 4: Data Migration and Deduplication

### Business Problem
A company is migrating from 3 legacy systems to a new ERP. They need to:
- Merge customer data from all 3 systems
- Eliminate duplicates
- Create clean master records
- Maintain audit trail

### Data Sources

**Legacy System A** (100K records):
- Old CRM, poor data quality, many duplicates

**Legacy System B** (75K records):
- Accounting system, high quality financial data

**Legacy System C** (50K records):
- Support ticketing, contact information

### Implementation Steps

#### Step 1: Data Profiling

```python
# Profile each source
analyze_record(file_paths=["system_a.jsonl"], version="current")
analyze_record(file_paths=["system_b.jsonl"], version="current")
analyze_record(file_paths=["system_c.jsonl"], version="current")

# Expected findings:
# System A: 60% name coverage, 40% email, many typos
# System B: 95% name coverage, 90% address, clean data
# System C: 85% name coverage, 95% email, 70% phone
```

#### Step 2: Deduplication Strategy

```python
# Load all data with source tracking
generate_scaffold(language="python", workflow="add_records", version="current")

# After loading:
# - Total records: 225K
# - Unique entities: ~80K (64% reduction)
# - Duplicates eliminated: 145K

# Analyze deduplication results
engine = SzEngine()
engine.initialize("Migration", config_json)

# Find entities with records from multiple systems
multi_system_entities = []

# Sample query (would need to iterate through entities)
# This is conceptual - actual implementation would use export
for entity_id in range(1, 1000):  # Sample
    try:
        result = engine.get_entity_by_entity_id(entity_id)
        entity = json.loads(result)
        
        sources = set(r["DATA_SOURCE"] for r in entity["RESOLVED_ENTITY"]["RECORDS"])
        
        if len(sources) > 1:
            multi_system_entities.append({
                "entity_id": entity_id,
                "sources": list(sources),
                "record_count": len(entity["RESOLVED_ENTITY"]["RECORDS"])
            })
    except:
        pass

print(f"Entities spanning multiple systems: {len(multi_system_entities)}")
```

#### Step 3: Master Record Creation

```python
def create_master_record(entity_id):
    """Create a master record from resolved entity"""
    
    engine = SzEngine()
    engine.initialize("MasterData", config_json)
    
    # Get entity
    result = engine.get_entity_by_entity_id(entity_id)
    entity = json.loads(result)
    
    # Build master record with best data from each source
    master = {
        "master_id": f"MASTER_{entity_id}",
        "source_records": []
    }
    
    # Collect all features
    names = []
    emails = []
    phones = []
    addresses = []
    
    for record in entity["RESOLVED_ENTITY"]["RECORDS"]:
        master["source_records"].append({
            "source": record["DATA_SOURCE"],
            "id": record["RECORD_ID"]
        })
        
        # Extract features (simplified)
        if "NAME_FULL" in record:
            names.append(record["NAME_FULL"])
        if "EMAIL_ADDRESS" in record:
            emails.append(record["EMAIL_ADDRESS"])
    
    # Select best values (most complete, most recent, etc.)
    master["name"] = select_best_name(names)
    master["email"] = select_best_email(emails)
    master["phone"] = select_best_phone(phones)
    master["address"] = select_best_address(addresses)
    
    return master

# Export all master records
export_master_data_to_new_erp()
```

### Results

**Data Quality Improvement**:
- Before: 225K records, ~40% duplicates, inconsistent data
- After: 80K master records, 0% duplicates, standardized data
- Data completeness: +35% (combining data from multiple sources)

**Migration Success**:
- Clean cutover to new ERP
- Complete audit trail maintained
- Zero data loss
- 64% reduction in record count

**Business Impact**:
- $500K annual savings (reduced storage, licensing)
- Improved data quality enables better analytics
- Faster system performance (fewer records)
- Single source of truth established

---

## Use Case 5: Vendor Master Data Management

### Business Problem
A large enterprise has vendor data scattered across divisions:
- Each division maintains own vendor list
- Same vendor has different IDs in each system
- Duplicate payments
- Missed volume discounts
- Compliance risks

### Data Sources

**Division A Vendors** (5K records):
- Vendor ID, company name, tax ID, address

**Division B Vendors** (3K records):
- Supplier ID, business name, EIN, location

**Division C Vendors** (4K records):
- Partner ID, organization name, tax number, address

**Dun & Bradstreet** (external enrichment):
- DUNS number, legal name, address, corporate hierarchy

### Implementation Steps

#### Step 1: Vendor Data Mapping

```python
# Map vendor data (organization entities)
mapping_workflow(
    action="start",
    file_paths=["division_a_vendors.csv", "division_b_vendors.csv", "division_c_vendors.csv"],
    version="current"
)

# Key mappings:
# - company_name/business_name/organization_name → NAME_ORG
# - tax_id/EIN/tax_number → TAX_ID_NUMBER
# - address/location → ADDR_FULL
# - phone → PHONE_NUMBER
# - website → WEBSITE_ADDRESS
```

#### Step 2: Vendor Consolidation

```python
# Load all vendor data
generate_scaffold(language="python", workflow="add_records", version="current")

# Results:
# - Total vendor records: 12K
# - Unique vendors: 4.5K (62% reduction)
# - Duplicates identified: 7.5K

# Analyze consolidation
engine = SzEngine()
engine.initialize("VendorMDM", config_json)

# Find vendors used by multiple divisions
cross_division_vendors = []

# Export and analyze (conceptual)
# Identify vendors with records from 2+ divisions
# These represent consolidation opportunities
```

#### Step 3: Volume Discount Analysis

```python
def analyze_spending_consolidation():
    """Identify volume discount opportunities"""
    
    # For each consolidated vendor entity
    # Sum spending across all divisions
    
    opportunities = []
    
    for entity in consolidated_vendors:
        total_spend = 0
        divisions = set()
        
        for record in entity["RESOLVED_ENTITY"]["RECORDS"]:
            division = record["DATA_SOURCE"]
            divisions.add(division)
            
            # Get spending from financial system
            spend = get_division_spending(division, record["RECORD_ID"])
            total_spend += spend
        
        if len(divisions) > 1 and total_spend > 100000:
            opportunities.append({
                "vendor": entity["RESOLVED_ENTITY"]["ENTITY_NAME"],
                "divisions": list(divisions),
                "total_spend": total_spend,
                "potential_discount": total_spend * 0.05  # Assume 5% volume discount
            })
    
    return opportunities

# Generate report
opportunities = analyze_spending_consolidation()
print(f"Total potential savings: ${sum(o['potential_discount'] for o in opportunities):,.2f}")
```

### Results

**Vendor Consolidation**:
- 12,000 vendor records → 4,500 unique vendors
- 62% reduction in duplicates
- 847 vendors used by multiple divisions

**Financial Impact**:
- $2.3M in duplicate payments prevented
- $1.8M in volume discounts negotiated
- $400K annual savings in vendor management costs

**Compliance Impact**:
- Single vendor screening process
- Consistent contract terms
- Improved audit trail
- Reduced compliance risk

---

## Common Patterns Across Use Cases

### Pattern 1: Multi-Source Integration
All use cases involve integrating data from multiple sources with different formats and quality levels.

**Key Success Factors**:
- Use `mapping_workflow` for each source
- Validate with `lint_record` and `analyze_record`
- Test with small batches first
- Monitor match quality

### Pattern 2: Data Quality Improvement
Entity resolution improves data quality by combining partial information from multiple sources.

**Key Success Factors**:
- Profile data before loading
- Standardize formats where possible
- Handle missing data gracefully
- Create master records from best available data

### Pattern 3: Network Analysis
Many use cases require understanding relationships between entities.

**Key Success Factors**:
- Use `why_entities` to understand connections
- Implement graph traversal for network analysis
- Visualize networks for human review
- Set appropriate match thresholds

### Pattern 4: Real-Time + Batch Processing
Most implementations need both real-time queries and batch processing.

**Key Success Factors**:
- Use connection pooling for real-time APIs
- Disable redo for batch loads
- Monitor performance separately
- Implement appropriate caching

### Pattern 5: Continuous Improvement
Entity resolution quality improves over time with tuning and feedback.

**Key Success Factors**:
- Monitor match quality metrics
- Review false positives/negatives
- Tune configuration as needed
- Maintain audit trail for compliance
