# Senzing — Security and Compliance Guide

This guide covers security best practices, compliance considerations, and data protection strategies for Senzing deployments.

## Table of Contents

- [PII Handling Best Practices](#pii-handling-best-practices)
- [GDPR Compliance](#gdpr-compliance)
- [CCPA Compliance](#ccpa-compliance)
- [Audit Logging](#audit-logging)
- [Access Control](#access-control)
- [Data Encryption](#data-encryption)
- [Security Checklist](#security-checklist)

---

## PII Handling Best Practices

### Data Classification

**Highly Sensitive PII** (requires encryption at rest and in transit):
- Social Security Numbers (SSN_NUMBER)
- Government ID numbers (PASSPORT_NUMBER, DRIVERS_LICENSE_NUMBER)
- Financial account numbers
- Health information
- Biometric data

**Moderate Sensitivity PII**:
- Full names (NAME_FULL)
- Email addresses (EMAIL_ADDRESS)
- Phone numbers (PHONE_NUMBER)
- Physical addresses (ADDR_FULL)
- Date of birth (DATE_OF_BIRTH)

**Low Sensitivity**:
- Company names (NAME_ORG)
- Business addresses
- Business phone numbers
- Public identifiers

### Data Minimization

**Principle**: Only load data necessary for entity resolution.

```python
# Bad: Loading unnecessary sensitive data
record = {
    "DATA_SOURCE": "CUSTOMERS",
    "RECORD_ID": "CUST001",
    "NAME_FULL": "John Smith",
    "SSN_NUMBER": "123-45-6789",  # Not needed for matching
    "CREDIT_CARD": "4111-1111-1111-1111",  # Never load payment data
    "PASSWORD_HASH": "abc123"  # Never load credentials
}

# Good: Only load matching attributes
record = {
    "DATA_SOURCE": "CUSTOMERS",
    "RECORD_ID": "CUST001",
    "NAME_FULL": "John Smith",
    "EMAIL_ADDRESS": "john.smith@example.com",
    "PHONE_NUMBER": "555-1234",
    "ADDR_FULL": "123 Main St, Anytown, ST 12345"
}
```

### Data Masking

**For non-production environments**:

```python
def mask_sensitive_data(record):
    """Mask sensitive data for testing/development"""
    
    masked = record.copy()
    
    # Mask SSN (keep last 4 digits)
    if "SSN_NUMBER" in masked:
        ssn = masked["SSN_NUMBER"]
        masked["SSN_NUMBER"] = f"XXX-XX-{ssn[-4:]}"
    
    # Mask email (keep domain)
    if "EMAIL_ADDRESS" in masked:
        email = masked["EMAIL_ADDRESS"]
        username, domain = email.split("@")
        masked["EMAIL_ADDRESS"] = f"user{hash(username) % 10000}@{domain}"
    
    # Mask phone (keep area code)
    if "PHONE_NUMBER" in masked:
        phone = masked["PHONE_NUMBER"]
        masked["PHONE_NUMBER"] = f"{phone[:3]}-XXX-XXXX"
    
    # Mask address (keep city/state)
    if "ADDR_FULL" in masked:
        # Keep only city and state
        masked["ADDR_FULL"] = "XXXX, City, ST XXXXX"
    
    return masked

# Use for test data generation
test_records = [mask_sensitive_data(r) for r in production_records[:1000]]
```

### Tokenization

**For highly sensitive data**:

```python
import hashlib
import hmac

class TokenizationService:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def tokenize(self, value):
        """Create a consistent token for a value"""
        return hmac.new(
            self.secret_key.encode(),
            value.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def tokenize_record(self, record):
        """Tokenize sensitive fields"""
        tokenized = record.copy()
        
        # Tokenize SSN
        if "SSN_NUMBER" in tokenized:
            tokenized["SSN_TOKEN"] = self.tokenize(tokenized["SSN_NUMBER"])
            del tokenized["SSN_NUMBER"]
        
        # Tokenize other sensitive fields
        # Keep name, email, phone for matching
        
        return tokenized

# Usage
tokenizer = TokenizationService(secret_key="your-secret-key")
tokenized_record = tokenizer.tokenize_record(original_record)
```

## GDPR Compliance

### Right to Access (Article 15)

**Requirement**: Individuals can request all data held about them.

```python
def export_individual_data(person_identifier):
    """Export all data for a specific individual"""
    
    engine = SzEngine()
    engine.initialize("GDPR_Access", config_json)
    
    # Search for the individual
    result = engine.search_by_attributes(
        json.dumps({"EMAIL_ADDRESS": person_identifier})
    )
    
    entities = json.loads(result)
    
    # Export all records for matched entities
    individual_data = []
    
    for entity in entities.get("RESOLVED_ENTITIES", []):
        entity_detail = engine.get_entity_by_entity_id(entity["ENTITY_ID"])
        entity_json = json.loads(entity_detail)
        
        # Extract all records
        for record in entity_json["RESOLVED_ENTITY"]["RECORDS"]:
            individual_data.append({
                "source": record["DATA_SOURCE"],
                "record_id": record["RECORD_ID"],
                "data": record
            })
    
    engine.destroy()
    
    return individual_data
```

### Right to Erasure (Article 17)

**Requirement**: Individuals can request deletion of their data.

```python
def delete_individual_data(person_identifier):
    """Delete all records for a specific individual"""
    
    engine = SzEngine()
    engine.initialize("GDPR_Erasure", config_json)
    
    # Find all records for the individual
    result = engine.search_by_attributes(
        json.dumps({"EMAIL_ADDRESS": person_identifier})
    )
    
    entities = json.loads(result)
    
    deleted_records = []
    
    for entity in entities.get("RESOLVED_ENTITIES", []):
        entity_detail = engine.get_entity_by_entity_id(entity["ENTITY_ID"])
        entity_json = json.loads(entity_detail)
        
        # Delete each record
        for record in entity_json["RESOLVED_ENTITY"]["RECORDS"]:
            engine.delete_record(
                data_source_code=record["DATA_SOURCE"],
                record_id=record["RECORD_ID"]
            )
            
            deleted_records.append({
                "source": record["DATA_SOURCE"],
                "record_id": record["RECORD_ID"]
            })
    
    engine.destroy()
    
    # Log deletion for audit trail
    log_gdpr_deletion(person_identifier, deleted_records)
    
    return deleted_records
```

### Data Retention Policies

```python
def implement_retention_policy(retention_days=2555):  # 7 years
    """Delete records older than retention period"""
    
    engine = SzEngine()
    engine.initialize("Retention", config_json)
    
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    
    # Query records older than cutoff
    # This is conceptual - actual implementation depends on your metadata
    old_records = query_records_before_date(cutoff_date)
    
    for record in old_records:
        # Delete record
        engine.delete_record(
            data_source_code=record["DATA_SOURCE"],
            record_id=record["RECORD_ID"]
        )
        
        # Log deletion
        log_retention_deletion(record)
    
    engine.destroy()
```

### Consent Management

```python
class ConsentManager:
    """Track and enforce data processing consent"""
    
    def __init__(self):
        self.consent_db = {}  # In practice, use a real database
    
    def record_consent(self, individual_id, purpose, granted=True):
        """Record consent for data processing"""
        self.consent_db[individual_id] = {
            "purpose": purpose,
            "granted": granted,
            "timestamp": datetime.now(),
            "version": "1.0"
        }
    
    def check_consent(self, individual_id, purpose):
        """Check if consent exists for a purpose"""
        consent = self.consent_db.get(individual_id)
        
        if not consent:
            return False
        
        return consent["granted"] and consent["purpose"] == purpose
    
    def withdraw_consent(self, individual_id):
        """Withdraw consent and trigger deletion"""
        self.consent_db[individual_id]["granted"] = False
        
        # Trigger data deletion
        delete_individual_data(individual_id)

# Usage
consent_mgr = ConsentManager()
consent_mgr.record_consent("user@example.com", "entity_resolution", granted=True)

# Before processing
if consent_mgr.check_consent("user@example.com", "entity_resolution"):
    # Process data
    pass
else:
    # Cannot process without consent
    raise ConsentError("No consent for entity resolution")
```

## CCPA Compliance

### Right to Know

**Requirement**: California residents can request information about data collection and use.

```python
def generate_ccpa_disclosure(person_identifier):
    """Generate CCPA disclosure for an individual"""
    
    engine = SzEngine()
    engine.initialize("CCPA_Disclosure", config_json)
    
    # Find individual's data
    result = engine.search_by_attributes(
        json.dumps({"EMAIL_ADDRESS": person_identifier})
    )
    
    entities = json.loads(result)
    
    disclosure = {
        "categories_collected": set(),
        "sources": set(),
        "business_purposes": ["Entity Resolution", "Fraud Detection"],
        "third_parties": [],
        "data_sold": False  # Senzing doesn't sell data
    }
    
    for entity in entities.get("RESOLVED_ENTITIES", []):
        entity_detail = engine.get_entity_by_entity_id(entity["ENTITY_ID"])
        entity_json = json.loads(entity_detail)
        
        for record in entity_json["RESOLVED_ENTITY"]["RECORDS"]:
            # Track data categories
            if "NAME_FULL" in record:
                disclosure["categories_collected"].add("Identifiers")
            if "EMAIL_ADDRESS" in record:
                disclosure["categories_collected"].add("Contact Information")
            if "ADDR_FULL" in record:
                disclosure["categories_collected"].add("Address Information")
            
            # Track sources
            disclosure["sources"].add(record["DATA_SOURCE"])
    
    engine.destroy()
    
    return disclosure
```

### Right to Delete

**Requirement**: California residents can request deletion (similar to GDPR).

```python
# Use the same delete_individual_data function from GDPR section
# Add CCPA-specific logging

def ccpa_delete_request(person_identifier):
    """Handle CCPA deletion request"""
    
    # Verify identity (required by CCPA)
    if not verify_identity(person_identifier):
        raise IdentityVerificationError("Cannot verify identity")
    
    # Check for exceptions (legal obligations, etc.)
    if has_legal_hold(person_identifier):
        return {
            "status": "denied",
            "reason": "Legal obligation to retain data"
        }
    
    # Perform deletion
    deleted = delete_individual_data(person_identifier)
    
    # Log for CCPA compliance
    log_ccpa_deletion(person_identifier, deleted)
    
    return {
        "status": "completed",
        "records_deleted": len(deleted)
    }
```

## Audit Logging

### Comprehensive Audit Trail

```python
import logging
import json
from datetime import datetime

class SenzingAuditLogger:
    """Audit logger for Senzing operations"""
    
    def __init__(self, log_file="senzing_audit.log"):
        self.logger = logging.getLogger("SenzingAudit")
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_record_load(self, user, data_source, record_id, success=True):
        """Log record loading operation"""
        self.logger.info(json.dumps({
            "operation": "LOAD_RECORD",
            "user": user,
            "data_source": data_source,
            "record_id": record_id,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }))
    
    def log_record_delete(self, user, data_source, record_id, reason):
        """Log record deletion operation"""
        self.logger.info(json.dumps({
            "operation": "DELETE_RECORD",
            "user": user,
            "data_source": data_source,
            "record_id": record_id,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }))
    
    def log_entity_query(self, user, query_type, criteria, result_count):
        """Log entity query operation"""
        self.logger.info(json.dumps({
            "operation": "QUERY_ENTITY",
            "user": user,
            "query_type": query_type,
            "criteria": criteria,
            "result_count": result_count,
            "timestamp": datetime.now().isoformat()
        }))
    
    def log_access(self, user, entity_id, purpose):
        """Log entity access for compliance"""
        self.logger.info(json.dumps({
            "operation": "ACCESS_ENTITY",
            "user": user,
            "entity_id": entity_id,
            "purpose": purpose,
            "timestamp": datetime.now().isoformat()
        }))

# Usage
audit_logger = SenzingAuditLogger()

# Log operations
audit_logger.log_record_load("user@example.com", "CUSTOMERS", "CUST001")
audit_logger.log_entity_query("user@example.com", "search", {"name": "John Smith"}, 5)
audit_logger.log_access("user@example.com", 12345, "Customer service inquiry")
```

### Audit Report Generation

```python
def generate_audit_report(start_date, end_date):
    """Generate audit report for compliance"""
    
    report = {
        "period": {"start": start_date, "end": end_date},
        "operations": {
            "loads": 0,
            "deletes": 0,
            "queries": 0,
            "accesses": 0
        },
        "users": set(),
        "data_sources": set()
    }
    
    # Parse audit log
    with open("senzing_audit.log", "r") as f:
        for line in f:
            try:
                entry = json.loads(line.split(" - ")[-1])
                entry_date = datetime.fromisoformat(entry["timestamp"])
                
                if start_date <= entry_date <= end_date:
                    # Count operations
                    op = entry["operation"]
                    if op == "LOAD_RECORD":
                        report["operations"]["loads"] += 1
                    elif op == "DELETE_RECORD":
                        report["operations"]["deletes"] += 1
                    elif op == "QUERY_ENTITY":
                        report["operations"]["queries"] += 1
                    elif op == "ACCESS_ENTITY":
                        report["operations"]["accesses"] += 1
                    
                    # Track users and sources
                    report["users"].add(entry["user"])
                    if "data_source" in entry:
                        report["data_sources"].add(entry["data_source"])
            except:
                pass
    
    report["users"] = list(report["users"])
    report["data_sources"] = list(report["data_sources"])
    
    return report
```

## Access Control

### Role-Based Access Control (RBAC)

```python
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"
    DATA_STEWARD = "data_steward"

class Permission(Enum):
    LOAD_DATA = "load_data"
    DELETE_DATA = "delete_data"
    QUERY_DATA = "query_data"
    VIEW_ENTITY = "view_entity"
    EXPORT_DATA = "export_data"
    CONFIGURE = "configure"

ROLE_PERMISSIONS = {
    Role.ADMIN: [
        Permission.LOAD_DATA,
        Permission.DELETE_DATA,
        Permission.QUERY_DATA,
        Permission.VIEW_ENTITY,
        Permission.EXPORT_DATA,
        Permission.CONFIGURE
    ],
    Role.ANALYST: [
        Permission.QUERY_DATA,
        Permission.VIEW_ENTITY,
        Permission.EXPORT_DATA
    ],
    Role.VIEWER: [
        Permission.QUERY_DATA,
        Permission.VIEW_ENTITY
    ],
    Role.DATA_STEWARD: [
        Permission.LOAD_DATA,
        Permission.DELETE_DATA,
        Permission.QUERY_DATA,
        Permission.VIEW_ENTITY
    ]
}

class AccessControl:
    def __init__(self):
        self.user_roles = {}  # user_id -> Role
    
    def assign_role(self, user_id, role):
        """Assign a role to a user"""
        self.user_roles[user_id] = role
    
    def check_permission(self, user_id, permission):
        """Check if user has permission"""
        role = self.user_roles.get(user_id)
        if not role:
            return False
        
        return permission in ROLE_PERMISSIONS.get(role, [])
    
    def require_permission(self, user_id, permission):
        """Decorator to enforce permission"""
        if not self.check_permission(user_id, permission):
            raise PermissionError(f"User {user_id} lacks {permission.value} permission")

# Usage
ac = AccessControl()
ac.assign_role("analyst@example.com", Role.ANALYST)

# Check before operation
if ac.check_permission("analyst@example.com", Permission.QUERY_DATA):
    # Perform query
    pass
else:
    raise PermissionError("Cannot query data")
```

### API Key Management

```python
import secrets
import hashlib
from datetime import datetime, timedelta

class APIKeyManager:
    def __init__(self):
        self.keys = {}  # hashed_key -> {user, role, expires, created}
    
    def generate_key(self, user_id, role, expires_days=90):
        """Generate a new API key"""
        # Generate random key
        key = secrets.token_urlsafe(32)
        
        # Hash for storage
        hashed = hashlib.sha256(key.encode()).hexdigest()
        
        # Store metadata
        self.keys[hashed] = {
            "user": user_id,
            "role": role,
            "expires": datetime.now() + timedelta(days=expires_days),
            "created": datetime.now()
        }
        
        # Return key once (never stored in plain text)
        return key
    
    def validate_key(self, key):
        """Validate an API key"""
        hashed = hashlib.sha256(key.encode()).hexdigest()
        
        if hashed not in self.keys:
            return None
        
        key_data = self.keys[hashed]
        
        # Check expiration
        if datetime.now() > key_data["expires"]:
            return None
        
        return key_data
    
    def revoke_key(self, key):
        """Revoke an API key"""
        hashed = hashlib.sha256(key.encode()).hexdigest()
        if hashed in self.keys:
            del self.keys[hashed]

# Usage
key_mgr = APIKeyManager()
api_key = key_mgr.generate_key("user@example.com", Role.ANALYST, expires_days=90)

# Validate on each request
key_data = key_mgr.validate_key(api_key)
if key_data:
    # Process request with user's role
    pass
else:
    # Invalid or expired key
    raise AuthenticationError("Invalid API key")
```

## Data Encryption

### Encryption at Rest

```python
# PostgreSQL encryption configuration
postgresql_conf = """
# Enable SSL
ssl = on
ssl_cert_file = '/path/to/server.crt'
ssl_key_file = '/path/to/server.key'
ssl_ca_file = '/path/to/root.crt'

# Require SSL for connections
ssl_min_protocol_version = 'TLSv1.2'
"""

# Senzing configuration with encrypted database
config_json = {
    "PIPELINE": {
        "CONFIGPATH": "/opt/senzing/data",
        "RESOURCEPATH": "/opt/senzing/resources",
        "SUPPORTPATH": "/opt/senzing/data"
    },
    "SQL": {
        "CONNECTION": "postgresql://senzing:password@localhost:5432/senzing?sslmode=require"
    }
}
```

### Encryption in Transit

```python
# Always use SSL/TLS for database connections
# PostgreSQL connection with SSL
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="senzing",
    user="senzing",
    password="password",
    sslmode="require",
    sslcert="/path/to/client.crt",
    sslkey="/path/to/client.key",
    sslrootcert="/path/to/root.crt"
)
```

### Field-Level Encryption

```python
from cryptography.fernet import Fernet

class FieldEncryption:
    def __init__(self, key):
        self.cipher = Fernet(key)
    
    def encrypt_field(self, value):
        """Encrypt a field value"""
        return self.cipher.encrypt(value.encode()).decode()
    
    def decrypt_field(self, encrypted_value):
        """Decrypt a field value"""
        return self.cipher.decrypt(encrypted_value.encode()).decode()
    
    def encrypt_record(self, record, sensitive_fields):
        """Encrypt sensitive fields in a record"""
        encrypted = record.copy()
        
        for field in sensitive_fields:
            if field in encrypted:
                encrypted[field] = self.encrypt_field(encrypted[field])
        
        return encrypted

# Usage
key = Fernet.generate_key()
encryptor = FieldEncryption(key)

# Encrypt before loading
record = {
    "DATA_SOURCE": "CUSTOMERS",
    "RECORD_ID": "CUST001",
    "NAME_FULL": "John Smith",
    "SSN_NUMBER": "123-45-6789"
}

encrypted_record = encryptor.encrypt_record(
    record,
    sensitive_fields=["SSN_NUMBER"]
)

# Load encrypted record
engine.add_record("CUSTOMERS", "CUST001", json.dumps(encrypted_record))
```

## Security Checklist

### Pre-Deployment Security Review

- [ ] **Data Classification**
  - [ ] All data classified by sensitivity level
  - [ ] Data minimization applied
  - [ ] Unnecessary sensitive data excluded

- [ ] **Access Control**
  - [ ] RBAC implemented
  - [ ] API keys generated and distributed
  - [ ] Principle of least privilege applied
  - [ ] Regular access reviews scheduled

- [ ] **Encryption**
  - [ ] Database encryption at rest enabled
  - [ ] SSL/TLS for all connections
  - [ ] Field-level encryption for highly sensitive data
  - [ ] Key management process defined

- [ ] **Audit Logging**
  - [ ] Comprehensive audit logging enabled
  - [ ] Log retention policy defined
  - [ ] Log review process established
  - [ ] Audit reports automated

- [ ] **Compliance**
  - [ ] GDPR requirements addressed (if applicable)
  - [ ] CCPA requirements addressed (if applicable)
  - [ ] Industry-specific regulations reviewed
  - [ ] Data retention policies implemented
  - [ ] Consent management in place

- [ ] **Network Security**
  - [ ] Firewall rules configured
  - [ ] Database not exposed to internet
  - [ ] VPN required for remote access
  - [ ] Network segmentation implemented

- [ ] **Application Security**
  - [ ] Input validation implemented
  - [ ] SQL injection prevention
  - [ ] API rate limiting
  - [ ] Error messages don't leak sensitive info

- [ ] **Incident Response**
  - [ ] Incident response plan documented
  - [ ] Breach notification procedures defined
  - [ ] Contact information current
  - [ ] Regular drills scheduled

## Compliance Resources

- **GDPR**: https://gdpr.eu/
- **CCPA**: https://oag.ca.gov/privacy/ccpa
- **HIPAA**: https://www.hhs.gov/hipaa/
- **PCI DSS**: https://www.pcisecuritystandards.org/
- **SOC 2**: https://www.aicpa.org/soc

For Senzing-specific security guidance, use:
```python
search_docs(query="security best practices", category="general", version="current")
```
