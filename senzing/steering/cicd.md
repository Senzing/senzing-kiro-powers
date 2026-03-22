# Senzing — CI/CD Integration

This guide covers integrating Senzing into continuous integration and deployment pipelines.

## GitHub Actions

### Basic Test Workflow

```yaml
name: Senzing Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:12
        env:
          POSTGRES_PASSWORD: senzing
          POSTGRES_USER: senzing
          POSTGRES_DB: senzing
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install Senzing SDK
        run: |
          wget https://senzing-production-apt.s3.amazonaws.com/senzingrepo_1.0.0-1_amd64.deb
          sudo apt-get install ./senzingrepo_1.0.0-1_amd64.deb
          sudo apt-get update
          sudo apt-get install senzingapi
      
      - name: Install Python dependencies
        run: |
          pip install senzing pytest
      
      - name: Run tests
        env:
          SENZING_ENGINE_CONFIGURATION_JSON: |
            {
              "PIPELINE": {
                "CONFIGPATH": "/opt/senzing/data",
                "RESOURCEPATH": "/opt/senzing/resources",
                "SUPPORTPATH": "/opt/senzing/data"
              },
              "SQL": {
                "CONNECTION": "postgresql://senzing:senzing@localhost:5432/senzing"
              }
            }
        run: |
          pytest tests/
```

### Data Mapping Validation

```yaml
name: Validate Data Mapping

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Download linter
        run: |
          curl -O https://mcp.senzing.com/resources/sz_json_linter.py
      
      - name: Validate mapped data
        run: |
          python sz_json_linter.py data/mapped/*.jsonl
      
      - name: Analyze data quality
        run: |
          curl -O https://mcp.senzing.com/resources/sz_json_analyzer.py
          python sz_json_analyzer.py data/mapped/*.jsonl
```

## GitLab CI

### Basic Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - test
  - deploy

variables:
  POSTGRES_DB: senzing
  POSTGRES_USER: senzing
  POSTGRES_PASSWORD: senzing

test:
  stage: test
  image: python:3.9
  services:
    - postgres:12
  before_script:
    - apt-get update
    - apt-get install -y wget
    - wget https://senzing-production-apt.s3.amazonaws.com/senzingrepo_1.0.0-1_amd64.deb
    - apt-get install -y ./senzingrepo_1.0.0-1_amd64.deb
    - apt-get update
    - apt-get install -y senzingapi
    - pip install senzing pytest
  script:
    - export SENZING_ENGINE_CONFIGURATION_JSON='{"PIPELINE":{"CONFIGPATH":"/opt/senzing/data","RESOURCEPATH":"/opt/senzing/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"postgresql://senzing:senzing@postgres:5432/senzing"}}'
    - pytest tests/
  only:
    - merge_requests
    - main

deploy:
  stage: deploy
  script:
    - echo "Deploying to production"
    - ./deploy.sh
  only:
    - main
```

## Jenkins

### Jenkinsfile

```groovy
pipeline {
    agent any
    
    environment {
        SENZING_ENGINE_CONFIGURATION_JSON = credentials('senzing-config')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install senzing pytest
                '''
            }
        }
        
        stage('Validate Data') {
            steps {
                sh '''
                    . venv/bin/activate
                    curl -O https://mcp.senzing.com/resources/sz_json_linter.py
                    python sz_json_linter.py data/mapped/*.jsonl
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ --junitxml=test-results.xml
                '''
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh'
            }
        }
    }
    
    post {
        always {
            junit 'test-results.xml'
        }
    }
}
```

## CircleCI

### Configuration

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  test:
    docker:
      - image: python:3.9
      - image: postgres:12
        environment:
          POSTGRES_USER: senzing
          POSTGRES_PASSWORD: senzing
          POSTGRES_DB: senzing
    
    steps:
      - checkout
      
      - run:
          name: Install Senzing
          command: |
            apt-get update
            apt-get install -y wget
            wget https://senzing-production-apt.s3.amazonaws.com/senzingrepo_1.0.0-1_amd64.deb
            apt-get install -y ./senzingrepo_1.0.0-1_amd64.deb
            apt-get update
            apt-get install -y senzingapi
      
      - run:
          name: Install dependencies
          command: pip install senzing pytest
      
      - run:
          name: Run tests
          command: pytest tests/
          environment:
            SENZING_ENGINE_CONFIGURATION_JSON: '{"PIPELINE":{"CONFIGPATH":"/opt/senzing/data","RESOURCEPATH":"/opt/senzing/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"postgresql://senzing:senzing@localhost:5432/senzing"}}'

workflows:
  version: 2
  test-and-deploy:
    jobs:
      - test
```

## Automated Testing

### Unit Tests

```python
# tests/test_senzing.py
import pytest
import json
from senzing import SzEngine

@pytest.fixture
def engine():
    """Create Senzing engine for testing"""
    engine = SzEngine()
    engine.initialize("TestEngine", config_json)
    yield engine
    engine.destroy()

def test_load_record(engine):
    """Test loading a record"""
    record = {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "TEST001",
        "NAME_FULL": "Test Person"
    }
    
    engine.add_record("TEST", "TEST001", json.dumps(record))
    
    # Verify record was loaded
    result = engine.get_entity_by_record_id("TEST", "TEST001")
    entity = json.loads(result)
    
    assert entity["RESOLVED_ENTITY"]["RECORDS"][0]["RECORD_ID"] == "TEST001"

def test_entity_resolution(engine):
    """Test that similar records resolve"""
    record1 = {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "TEST002",
        "NAME_FULL": "John Smith",
        "EMAIL_ADDRESS": "john@example.com"
    }
    
    record2 = {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "TEST003",
        "NAME_FULL": "John Smith",
        "EMAIL_ADDRESS": "john@example.com"
    }
    
    engine.add_record("TEST", "TEST002", json.dumps(record1))
    engine.add_record("TEST", "TEST003", json.dumps(record2))
    
    # Verify they resolved to same entity
    entity1 = json.loads(engine.get_entity_by_record_id("TEST", "TEST002"))
    entity2 = json.loads(engine.get_entity_by_record_id("TEST", "TEST003"))
    
    assert entity1["RESOLVED_ENTITY"]["ENTITY_ID"] == entity2["RESOLVED_ENTITY"]["ENTITY_ID"]

def test_data_quality(engine):
    """Test data quality validation"""
    # Load test data
    with open("tests/data/test_records.jsonl") as f:
        for line in f:
            record = json.loads(line)
            engine.add_record(record["DATA_SOURCE"], record["RECORD_ID"], line)
    
    # Verify expected entity count
    # This would require export functionality
    pass
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
import json
from senzing import SzEngine

@pytest.fixture(scope="module")
def loaded_engine():
    """Create engine and load test dataset"""
    engine = SzEngine()
    engine.initialize("IntegrationTest", config_json)
    
    # Load test dataset
    with open("tests/data/integration_test.jsonl") as f:
        for line in f:
            record = json.loads(line)
            engine.add_record(record["DATA_SOURCE"], record["RECORD_ID"], line)
    
    yield engine
    engine.destroy()

def test_search_performance(loaded_engine):
    """Test search performance"""
    import time
    
    start = time.time()
    result = loaded_engine.search_by_attributes(
        json.dumps({"NAME_FULL": "John Smith"})
    )
    duration = time.time() - start
    
    assert duration < 1.0, f"Search took {duration}s, expected < 1s"

def test_match_quality(loaded_engine):
    """Test match quality against golden dataset"""
    # Load golden matches
    with open("tests/data/golden_matches.json") as f:
        golden = json.load(f)
    
    # Verify matches
    for expected_match in golden:
        entity1 = json.loads(loaded_engine.get_entity_by_record_id(
            expected_match["source1"], expected_match["id1"]
        ))
        entity2 = json.loads(loaded_engine.get_entity_by_record_id(
            expected_match["source2"], expected_match["id2"]
        ))
        
        assert entity1["RESOLVED_ENTITY"]["ENTITY_ID"] == entity2["RESOLVED_ENTITY"]["ENTITY_ID"], \
            f"Expected {expected_match['id1']} and {expected_match['id2']} to match"
```

## Deployment Automation

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Install Senzing
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://senzing-production-apt.s3.amazonaws.com/senzingrepo_1.0.0-1_amd64.deb && \
    apt-get install -y ./senzingrepo_1.0.0-1_amd64.deb && \
    apt-get update && \
    apt-get install -y senzingapi && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:12
    environment:
      POSTGRES_USER: senzing
      POSTGRES_PASSWORD: senzing
      POSTGRES_DB: senzing
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  senzing-app:
    build: .
    environment:
      SENZING_ENGINE_CONFIGURATION_JSON: |
        {
          "PIPELINE": {
            "CONFIGPATH": "/opt/senzing/data",
            "RESOURCEPATH": "/opt/senzing/resources",
            "SUPPORTPATH": "/opt/senzing/data"
          },
          "SQL": {
            "CONNECTION": "postgresql://senzing:senzing@postgres:5432/senzing"
          }
        }
    depends_on:
      - postgres
    ports:
      - "8080:8080"

volumes:
  postgres_data:
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: senzing-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: senzing-app
  template:
    metadata:
      labels:
        app: senzing-app
    spec:
      containers:
      - name: senzing-app
        image: myregistry/senzing-app:latest
        env:
        - name: SENZING_ENGINE_CONFIGURATION_JSON
          valueFrom:
            secretKeyRef:
              name: senzing-config
              key: config.json
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
---
apiVersion: v1
kind: Service
metadata:
  name: senzing-app
spec:
  selector:
    app: senzing-app
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

## Configuration Management

### Environment-Specific Configs

```python
# config.py
import os
import json

def get_config(environment):
    """Get environment-specific configuration"""
    
    configs = {
        "development": {
            "PIPELINE": {
                "CONFIGPATH": "/opt/senzing/data",
                "RESOURCEPATH": "/opt/senzing/resources",
                "SUPPORTPATH": "/opt/senzing/data"
            },
            "SQL": {
                "CONNECTION": "postgresql://senzing:senzing@localhost:5432/senzing_dev"
            }
        },
        "staging": {
            "PIPELINE": {
                "CONFIGPATH": "/opt/senzing/data",
                "RESOURCEPATH": "/opt/senzing/resources",
                "SUPPORTPATH": "/opt/senzing/data"
            },
            "SQL": {
                "CONNECTION": os.environ.get("STAGING_DB_CONNECTION")
            }
        },
        "production": {
            "PIPELINE": {
                "CONFIGPATH": "/opt/senzing/data",
                "RESOURCEPATH": "/opt/senzing/resources",
                "SUPPORTPATH": "/opt/senzing/data"
            },
            "SQL": {
                "CONNECTION": os.environ.get("PRODUCTION_DB_CONNECTION")
            }
        }
    }
    
    return json.dumps(configs[environment])

# Usage
environment = os.environ.get("ENVIRONMENT", "development")
config_json = get_config(environment)
```

### Secrets Management

```python
# Using AWS Secrets Manager
import boto3
import json

def get_senzing_config_from_secrets():
    """Retrieve Senzing configuration from AWS Secrets Manager"""
    
    client = boto3.client('secretsmanager')
    
    response = client.get_secret_value(SecretId='senzing/config')
    secret = json.loads(response['SecretString'])
    
    config = {
        "PIPELINE": {
            "CONFIGPATH": "/opt/senzing/data",
            "RESOURCEPATH": "/opt/senzing/resources",
            "SUPPORTPATH": "/opt/senzing/data"
        },
        "SQL": {
            "CONNECTION": secret['database_connection']
        }
    }
    
    return json.dumps(config)
```

## Version Control

### Managing Data Mappings

```bash
# Store mapping configurations in version control
git add data/mappings/customers_mapping.json
git add data/mappings/vendors_mapping.json
git commit -m "Update customer mapping to include phone numbers"
git push
```

### Database Schema Versioning

```python
# migrations/001_initial_setup.py
def upgrade(engine):
    """Initialize Senzing database schema"""
    # Senzing handles schema automatically
    # This is for custom tables/indexes
    pass

def downgrade(engine):
    """Rollback changes"""
    pass
```

## Monitoring in CI/CD

### Performance Benchmarks

```python
# tests/test_performance.py
import pytest
import time
import json
from senzing import SzEngine

def test_loading_throughput(engine):
    """Ensure loading throughput meets requirements"""
    
    records = generate_test_records(1000)
    
    start = time.time()
    for record in records:
        engine.add_record(record["DATA_SOURCE"], record["RECORD_ID"], json.dumps(record))
    duration = time.time() - start
    
    throughput = len(records) / duration
    
    assert throughput > 100, f"Throughput {throughput:.0f} rec/sec below threshold of 100"

def test_query_performance(engine):
    """Ensure query performance meets requirements"""
    
    start = time.time()
    result = engine.search_by_attributes(json.dumps({"NAME_FULL": "John Smith"}))
    duration = time.time() - start
    
    assert duration < 0.5, f"Query took {duration}s, expected < 0.5s"
```

## Blue-Green Deployment

```bash
#!/bin/bash
# deploy.sh

# Deploy to green environment
kubectl apply -f k8s/deployment-green.yaml

# Wait for green to be ready
kubectl wait --for=condition=available --timeout=300s deployment/senzing-app-green

# Run smoke tests
pytest tests/smoke/

# Switch traffic to green
kubectl patch service senzing-app -p '{"spec":{"selector":{"version":"green"}}}'

# Monitor for issues
sleep 60

# If successful, remove blue
kubectl delete deployment senzing-app-blue
```

For more CI/CD integration guidance, use:
```python
search_docs(query="deployment automation", category="deployment", version="current")
find_examples(query="ci cd", language="python")
```
