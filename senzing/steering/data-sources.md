# Senzing — Data Source Integration Examples

This guide provides specific guidance for integrating common data sources with Senzing.

## CRM Systems

### Salesforce

**Common Fields**:
- Account ID → RECORD_ID
- Account Name → NAME_ORG (for companies) or NAME_FULL (for contacts)
- Email → EMAIL_ADDRESS
- Phone → PHONE_NUMBER
- Billing Address → ADDR_FULL
- Website → WEBSITE_ADDRESS

**Mapping Example**:
```python
salesforce_record = {
    "DATA_SOURCE": "SALESFORCE",
    "RECORD_ID": account["Id"],
    "NAME_ORG": account["Name"],
    "PHONE_NUMBER": account["Phone"],
    "EMAIL_ADDRESS": account["Email"],
    "ADDR_FULL": f"{account['BillingStreet']}, {account['BillingCity']}, {account['BillingState']} {account['BillingPostalCode']}",
    "WEBSITE_ADDRESS": account["Website"]
}
```

**Export from Salesforce**:
```python
# Using simple-salesforce library
from simple_salesforce import Salesforce

sf = Salesforce(username='user@example.com', password='password', security_token='token')

# Query accounts
accounts = sf.query("SELECT Id, Name, Phone, Email, BillingStreet, BillingCity, BillingState, BillingPostalCode, Website FROM Account")

# Map and load
for account in accounts['records']:
    senzing_record = map_salesforce_record(account)
    engine.add_record("SALESFORCE", senzing_record["RECORD_ID"], json.dumps(senzing_record))
```

### HubSpot

**Common Fields**:
- Contact ID → RECORD_ID
- First Name + Last Name → NAME_FULL
- Email → EMAIL_ADDRESS
- Phone → PHONE_NUMBER
- Company → NAME_ORG (if linking to companies)

**Mapping Example**:
```python
hubspot_record = {
    "DATA_SOURCE": "HUBSPOT",
    "RECORD_ID": contact["vid"],
    "NAME_FULL": f"{contact['properties']['firstname']['value']} {contact['properties']['lastname']['value']}",
    "EMAIL_ADDRESS": contact['properties']['email']['value'],
    "PHONE_NUMBER": contact['properties']['phone']['value']
}
```

### Microsoft Dynamics

**Common Fields**:
- Contact ID → RECORD_ID
- Full Name → NAME_FULL
- Email Address → EMAIL_ADDRESS
- Business Phone → PHONE_NUMBER
- Address → ADDR_FULL

## ERP Systems

### SAP

**Common Fields**:
- Customer Number → RECORD_ID
- Name → NAME_ORG or NAME_FULL
- Tax ID → TAX_ID_NUMBER
- Street, City, Postal Code → ADDR_FULL
- Telephone → PHONE_NUMBER

**Mapping Example**:
```python
sap_record = {
    "DATA_SOURCE": "SAP",
    "RECORD_ID": customer["KUNNR"],  # Customer number
    "NAME_ORG": customer["NAME1"],
    "TAX_ID_NUMBER": customer["STCD1"],  # Tax number
    "ADDR_FULL": f"{customer['STRAS']}, {customer['ORT01']}, {customer['PSTLZ']}",
    "PHONE_NUMBER": customer["TELF1"]
}
```

### Oracle ERP

**Common Fields**:
- Party ID → RECORD_ID
- Party Name → NAME_ORG or NAME_FULL
- Tax Reference → TAX_ID_NUMBER
- Address → ADDR_FULL

## E-Commerce Platforms

### Shopify

**Common Fields**:
- Customer ID → RECORD_ID
- First Name + Last Name → NAME_FULL
- Email → EMAIL_ADDRESS
- Phone → PHONE_NUMBER
- Default Address → ADDR_FULL

**Mapping Example**:
```python
shopify_record = {
    "DATA_SOURCE": "SHOPIFY",
    "RECORD_ID": str(customer["id"]),
    "NAME_FULL": f"{customer['first_name']} {customer['last_name']}",
    "EMAIL_ADDRESS": customer["email"],
    "PHONE_NUMBER": customer["phone"],
    "ADDR_FULL": format_shopify_address(customer["default_address"])
}

def format_shopify_address(addr):
    if not addr:
        return None
    return f"{addr['address1']}, {addr['city']}, {addr['province']} {addr['zip']}, {addr['country']}"
```

### WooCommerce

**Common Fields**:
- Customer ID → RECORD_ID
- Billing First Name + Last Name → NAME_FULL
- Billing Email → EMAIL_ADDRESS
- Billing Phone → PHONE_NUMBER
- Billing Address → ADDR_FULL

## Marketing Platforms

### Mailchimp

**Common Fields**:
- Email Address → RECORD_ID (use email as ID)
- First Name + Last Name → NAME_FULL
- Email → EMAIL_ADDRESS

**Mapping Example**:
```python
mailchimp_record = {
    "DATA_SOURCE": "MAILCHIMP",
    "RECORD_ID": member["email_address"],  # Use email as ID
    "NAME_FULL": f"{member['merge_fields']['FNAME']} {member['merge_fields']['LNAME']}",
    "EMAIL_ADDRESS": member["email_address"]
}
```

### Marketo

**Common Fields**:
- Lead ID → RECORD_ID
- First Name + Last Name → NAME_FULL
- Email → EMAIL_ADDRESS
- Phone → PHONE_NUMBER
- Company → NAME_ORG

## Financial Systems

### Stripe

**Common Fields**:
- Customer ID → RECORD_ID
- Name → NAME_FULL
- Email → EMAIL_ADDRESS
- Phone → PHONE_NUMBER
- Address → ADDR_FULL

**Mapping Example**:
```python
stripe_record = {
    "DATA_SOURCE": "STRIPE",
    "RECORD_ID": customer["id"],
    "NAME_FULL": customer["name"],
    "EMAIL_ADDRESS": customer["email"],
    "PHONE_NUMBER": customer["phone"],
    "ADDR_FULL": format_stripe_address(customer["address"])
}
```

### PayPal

**Common Fields**:
- Payer ID → RECORD_ID
- Payer Name → NAME_FULL
- Payer Email → EMAIL_ADDRESS
- Shipping Address → ADDR_FULL

## Public Records

### Business Registrations

**Common Fields**:
- Registration Number → RECORD_ID
- Business Name → NAME_ORG
- Tax ID / EIN → TAX_ID_NUMBER
- Registered Address → ADDR_FULL
- Registration Date → DATE_OF_REGISTRATION (custom field)

**Mapping Example**:
```python
business_record = {
    "DATA_SOURCE": "BUSINESS_REGISTRY",
    "RECORD_ID": registration["registration_number"],
    "NAME_ORG": registration["business_name"],
    "TAX_ID_NUMBER": registration["ein"],
    "ADDR_FULL": registration["registered_address"]
}
```

### Property Records

**Common Fields**:
- Parcel ID → RECORD_ID
- Owner Name → NAME_FULL or NAME_ORG
- Property Address → ADDR_FULL
- Owner Address → ADDR_FULL (separate field)

## Watchlists and Screening

### OFAC SDN List

**Common Fields**:
- UID → RECORD_ID
- Name → NAME_FULL or NAME_ORG
- Aliases → Multiple NAME_FULL entries
- Date of Birth → DATE_OF_BIRTH
- Nationality → NATIONALITY
- Passport → PASSPORT_NUMBER

**Mapping Example**:
```python
ofac_record = {
    "DATA_SOURCE": "OFAC",
    "RECORD_ID": entry["uid"],
    "NAME_FULL": entry["name"],
    "DATE_OF_BIRTH": entry["dob"],
    "NATIONALITY": entry["nationality"],
    "PASSPORT_NUMBER": entry["passport"]
}

# Handle aliases
for alias in entry.get("aliases", []):
    alias_record = ofac_record.copy()
    alias_record["RECORD_ID"] = f"{entry['uid']}_ALIAS_{alias['id']}"
    alias_record["NAME_FULL"] = alias["name"]
    # Load alias record
```

### PEP Lists

**Common Fields**:
- ID → RECORD_ID
- Name → NAME_FULL
- Position → POSITION (custom field)
- Country → NATIONALITY
- Date of Birth → DATE_OF_BIRTH

## Healthcare Systems

### HL7 Messages

**Common Fields**:
- Patient ID → RECORD_ID
- Patient Name → NAME_FULL
- Date of Birth → DATE_OF_BIRTH
- SSN → SSN_NUMBER
- Address → ADDR_FULL
- Phone → PHONE_NUMBER

**Mapping Example**:
```python
# Parse HL7 message
import hl7

message = hl7.parse(hl7_string)
pid_segment = message.segment('PID')

hl7_record = {
    "DATA_SOURCE": "EMR",
    "RECORD_ID": str(pid_segment[3]),  # Patient ID
    "NAME_FULL": f"{pid_segment[5][1]} {pid_segment[5][0]}",  # First Last
    "DATE_OF_BIRTH": pid_segment[7],
    "SSN_NUMBER": pid_segment[19],
    "ADDR_FULL": format_hl7_address(pid_segment[11]),
    "PHONE_NUMBER": pid_segment[13]
}
```

### FHIR Resources

**Common Fields**:
- Patient ID → RECORD_ID
- Name → NAME_FULL
- Birth Date → DATE_OF_BIRTH
- Identifier (SSN, MRN) → SSN_NUMBER or custom field
- Address → ADDR_FULL
- Telecom → PHONE_NUMBER, EMAIL_ADDRESS

## Social Media (Public Data Only)

### LinkedIn (Public Profiles)

**Common Fields**:
- Profile URL → RECORD_ID
- Name → NAME_FULL
- Company → NAME_ORG (current employer)
- Location → ADDR_CITY, ADDR_STATE

**Note**: Only use publicly available data. Respect terms of service and privacy policies.

## Database Systems

### MySQL/PostgreSQL

**Direct Query Example**:
```python
import psycopg2

conn = psycopg2.connect("postgresql://user:pass@localhost/db")
cursor = conn.cursor()

cursor.execute("SELECT id, first_name, last_name, email, phone, address FROM customers")

for row in cursor.fetchall():
    record = {
        "DATA_SOURCE": "CUSTOMER_DB",
        "RECORD_ID": str(row[0]),
        "NAME_FULL": f"{row[1]} {row[2]}",
        "EMAIL_ADDRESS": row[3],
        "PHONE_NUMBER": row[4],
        "ADDR_FULL": row[5]
    }
    engine.add_record("CUSTOMER_DB", record["RECORD_ID"], json.dumps(record))

cursor.close()
conn.close()
```

### MongoDB

**Query Example**:
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["customers"]

for doc in collection.find():
    record = {
        "DATA_SOURCE": "MONGODB",
        "RECORD_ID": str(doc["_id"]),
        "NAME_FULL": doc["name"],
        "EMAIL_ADDRESS": doc["email"],
        "PHONE_NUMBER": doc["phone"]
    }
    engine.add_record("MONGODB", record["RECORD_ID"], json.dumps(record))
```

## File Formats

### CSV Files

```python
import csv

with open("customers.csv", "r") as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        record = {
            "DATA_SOURCE": "CSV_IMPORT",
            "RECORD_ID": row["customer_id"],
            "NAME_FULL": row["full_name"],
            "EMAIL_ADDRESS": row["email"],
            "PHONE_NUMBER": row["phone"]
        }
        engine.add_record("CSV_IMPORT", record["RECORD_ID"], json.dumps(record))
```

### JSON Files

```python
import json

with open("customers.json", "r") as f:
    data = json.load(f)
    
    for customer in data:
        record = {
            "DATA_SOURCE": "JSON_IMPORT",
            "RECORD_ID": customer["id"],
            "NAME_FULL": customer["name"],
            "EMAIL_ADDRESS": customer["email"]
        }
        engine.add_record("JSON_IMPORT", record["RECORD_ID"], json.dumps(record))
```

### Excel Files

```python
import pandas as pd

df = pd.read_excel("customers.xlsx")

for _, row in df.iterrows():
    record = {
        "DATA_SOURCE": "EXCEL_IMPORT",
        "RECORD_ID": str(row["ID"]),
        "NAME_FULL": row["Name"],
        "EMAIL_ADDRESS": row["Email"]
    }
    engine.add_record("EXCEL_IMPORT", record["RECORD_ID"], json.dumps(record))
```

## Best Practices for Data Source Integration

### 1. Use Descriptive DATA_SOURCE Names
```python
# Good
"SALESFORCE_ACCOUNTS"
"HUBSPOT_CONTACTS"
"SAP_CUSTOMERS"

# Bad
"SOURCE1"
"DATA"
"IMPORT"
```

### 2. Ensure RECORD_ID Uniqueness
```python
# If source doesn't have unique ID, create one
record_id = f"{source_system}_{original_id}"
```

### 3. Handle Missing Data
```python
# Don't create fake data
record = {
    "DATA_SOURCE": "CUSTOMERS",
    "RECORD_ID": "CUST001",
    "NAME_FULL": customer.get("name"),  # May be None
    "EMAIL_ADDRESS": customer.get("email")  # May be None
}

# Remove None values
record = {k: v for k, v in record.items() if v is not None}
```

### 4. Standardize Formats
```python
# Phone numbers
phone = re.sub(r'[^0-9]', '', raw_phone)  # Remove formatting

# Dates
date = datetime.strptime(raw_date, "%m/%d/%Y").strftime("%Y-%m-%d")

# Addresses
address = address.upper().strip()  # Standardize case
```

### 5. Use mapping_workflow
```python
# Always use mapping_workflow for new data sources
mapping_workflow(
    action="start",
    file_paths=["new_source.csv"],
    version="current"
)
```

## Data Source Registration

Before loading data, register your data sources:

```python
sdk_guide(
    topic="configure",
    data_sources=["SALESFORCE", "HUBSPOT", "SAP", "SHOPIFY"],
    version="current"
)
```

## Testing with Sample Data

Always test with a small sample first:

```python
# Test with 100 records
test_records = all_records[:100]

for record in test_records:
    engine.add_record(record["DATA_SOURCE"], record["RECORD_ID"], json.dumps(record))

# Verify results
# Check entity count, match quality, etc.
```

For more data source integration guidance, use:
```python
search_docs(query="data source integration", category="data_mapping", version="current")
find_examples(query="data source", language="python")
```
