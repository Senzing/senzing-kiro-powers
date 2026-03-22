# Senzing — Code Examples

This guide provides practical code examples and patterns for common Senzing operations.

**Note**: These are simplified examples for illustration. Always use `generate_scaffold` for production-ready code with proper error handling, configuration, and resource management.

## Basic Record Loading

### Python

```python
import json
from senzing import SzEngine, SzConfig

# Initialize engine
engine = SzEngine()
config_json = '{"PIPELINE": {"CONFIGPATH": "/opt/senzing/data", "RESOURCEPATH": "/opt/senzing/resources", "SUPPORTPATH": "/opt/senzing/data"}}'
engine.initialize("MyApp", config_json)

try:
    # Load a single record
    record = {
        "DATA_SOURCE": "CUSTOMERS",
        "RECORD_ID": "CUST001",
        "NAME_FULL": "John Smith",
        "EMAIL_ADDRESS": "john.smith@example.com",
        "PHONE_NUMBER": "555-1234",
        "ADDR_FULL": "123 Main St, Anytown, ST 12345"
    }
    
    engine.add_record(
        data_source_code="CUSTOMERS",
        record_id="CUST001",
        record_definition=json.dumps(record)
    )
    
    print("Record loaded successfully")
    
finally:
    engine.destroy()
```

### Java

```java
import com.senzing.sdk.SzEngine;
import com.senzing.sdk.SzException;

public class LoadRecord {
    public static void main(String[] args) {
        SzEngine engine = new SzEngine();
        String config = "{\"PIPELINE\": {...}}";
        
        try {
            engine.initialize("MyApp", config);
            
            String record = "{" +
                "\"DATA_SOURCE\": \"CUSTOMERS\"," +
                "\"RECORD_ID\": \"CUST001\"," +
                "\"NAME_FULL\": \"John Smith\"," +
                "\"EMAIL_ADDRESS\": \"john.smith@example.com\"" +
                "}";
            
            engine.addRecord("CUSTOMERS", "CUST001", record);
            System.out.println("Record loaded successfully");
            
        } catch (SzException e) {
            e.printStackTrace();
        } finally {
            engine.destroy();
        }
    }
}
```

### C#

```csharp
using Senzing.Sdk;
using System;

class LoadRecord
{
    static void Main()
    {
        var engine = new SzEngine();
        string config = "{\"PIPELINE\": {...}}";
        
        try
        {
            engine.Initialize("MyApp", config);
            
            string record = @"{
                ""DATA_SOURCE"": ""CUSTOMERS"",
                ""RECORD_ID"": ""CUST001"",
                ""NAME_FULL"": ""John Smith"",
                ""EMAIL_ADDRESS"": ""john.smith@example.com""
            }";
            
            engine.AddRecord("CUSTOMERS", "CUST001", record);
            Console.WriteLine("Record loaded successfully");
        }
        finally
        {
            engine.Destroy();
        }
    }
}
```

## Batch Loading

### Python - Multi-threaded Loader

```python
import json
import threading
from queue import Queue
from senzing import SzEngine

class BatchLoader:
    def __init__(self, config_json, num_threads=4):
        self.config_json = config_json
        self.num_threads = num_threads
        self.queue = Queue()
        self.engines = []
        
    def worker(self, thread_id):
        engine = SzEngine()
        engine.initialize(f"Loader-{thread_id}", self.config_json)
        self.engines.append(engine)
        
        while True:
            item = self.queue.get()
            if item is None:
                break
                
            data_source, record_id, record = item
            try:
                engine.add_record(data_source, record_id, json.dumps(record))
            except Exception as e:
                print(f"Error loading {record_id}: {e}")
            finally:
                self.queue.task_done()
        
        engine.destroy()
    
    def load_records(self, records):
        # Start worker threads
        threads = []
        for i in range(self.num_threads):
            t = threading.Thread(target=self.worker, args=(i,))
            t.start()
            threads.append(t)
        
        # Queue records
        for record in records:
            self.queue.put((
                record["DATA_SOURCE"],
                record["RECORD_ID"],
                record
            ))
        
        # Wait for completion
        self.queue.join()
        
        # Stop workers
        for _ in range(self.num_threads):
            self.queue.put(None)
        for t in threads:
            t.join()

# Usage
loader = BatchLoader(config_json, num_threads=4)
loader.load_records(my_records)
```

## Entity Search

### Python - Search by Attributes

```python
import json
from senzing import SzEngine

engine = SzEngine()
engine.initialize("SearchApp", config_json)

try:
    # Search for entities matching criteria
    search_criteria = {
        "NAME_FULL": "John Smith",
        "DATE_OF_BIRTH": "1980-01-15"
    }
    
    result = engine.search_by_attributes(
        attributes=json.dumps(search_criteria)
    )
    
    entities = json.loads(result)
    
    print(f"Found {len(entities.get('RESOLVED_ENTITIES', []))} entities")
    
    for entity in entities.get('RESOLVED_ENTITIES', []):
        print(f"Entity ID: {entity['ENTITY_ID']}")
        print(f"Match Score: {entity.get('MATCH_SCORE', 'N/A')}")
        
finally:
    engine.destroy()
```

### Python - Get Entity by Record ID

```python
import json
from senzing import SzEngine

engine = SzEngine()
engine.initialize("QueryApp", config_json)

try:
    # Get entity containing a specific record
    result = engine.get_entity_by_record_id(
        data_source_code="CUSTOMERS",
        record_id="CUST001"
    )
    
    entity = json.loads(result)
    
    print(f"Entity ID: {entity['RESOLVED_ENTITY']['ENTITY_ID']}")
    print(f"Records in entity: {len(entity['RESOLVED_ENTITY']['RECORDS'])}")
    
    # List all records in the entity
    for record in entity['RESOLVED_ENTITY']['RECORDS']:
        print(f"  - {record['DATA_SOURCE']}: {record['RECORD_ID']}")
        
finally:
    engine.destroy()
```

## Why Analysis

### Python - Understanding Why Records Matched

```python
import json
from senzing import SzEngine

engine = SzEngine()
engine.initialize("WhyApp", config_json)

try:
    # Understand why two entities matched
    result = engine.why_entities(
        entity_id_1=1001,
        entity_id_2=1002
    )
    
    why_result = json.loads(result)
    
    print("Match Analysis:")
    print(f"Match Level: {why_result.get('MATCH_INFO', {}).get('MATCH_LEVEL_CODE')}")
    print(f"Match Key: {why_result.get('MATCH_INFO', {}).get('MATCH_KEY')}")
    
    # Show matching features
    for feature in why_result.get('MATCH_INFO', {}).get('FEATURE_SCORES', []):
        print(f"  {feature['FEATURE_TYPE']}: {feature['SCORE']}")
        
finally:
    engine.destroy()
```

### Python - Why Record Not in Entity

```python
import json
from senzing import SzEngine

engine = SzEngine()
engine.initialize("WhyApp", config_json)

try:
    # Understand why a record didn't match an entity
    result = engine.why_record_not_in_entity(
        data_source_code="CUSTOMERS",
        record_id="CUST001",
        entity_id=1001
    )
    
    why_result = json.loads(result)
    
    print("Non-Match Analysis:")
    print(f"Reason: {why_result.get('INFO', {}).get('INTERNAL_ID')}")
    
finally:
    engine.destroy()
```

## Configuration Management

### Python - Register Data Sources

```python
import json
from senzing import SzConfig, SzConfigManager, SzEngine

config_mgr = SzConfigManager()
config_mgr.initialize("ConfigApp", config_json)

sz_config = SzConfig()
sz_config.initialize("ConfigApp", config_json)

try:
    # Get current config
    config_id = config_mgr.get_default_config_id()
    config_handle = sz_config.import_config(
        config_mgr.get_config(config_id)
    )
    
    # Add data source
    data_source_def = {
        "DSRC_CODE": "NEW_SOURCE"
    }
    sz_config.add_data_source(config_handle, json.dumps(data_source_def))
    
    # Export and save new config
    new_config = sz_config.export_config(config_handle)
    new_config_id = config_mgr.add_config(new_config, "Added NEW_SOURCE")
    config_mgr.set_default_config_id(new_config_id)
    
    print(f"Data source registered. New config ID: {new_config_id}")
    
finally:
    sz_config.close_config(config_handle)
    sz_config.destroy()
    config_mgr.destroy()
```

## Error Handling

### Python - Robust Error Handling

```python
import json
import logging
from senzing import SzEngine, SzException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustLoader:
    def __init__(self, config_json):
        self.engine = SzEngine()
        self.engine.initialize("RobustLoader", config_json)
    
    def load_record_with_retry(self, data_source, record_id, record, max_retries=3):
        for attempt in range(max_retries):
            try:
                self.engine.add_record(
                    data_source_code=data_source,
                    record_id=record_id,
                    record_definition=json.dumps(record)
                )
                logger.info(f"Loaded {data_source}:{record_id}")
                return True
                
            except SzException as e:
                error_code = e.error_code
                
                # Handle specific error codes
                if error_code == "SENZ0037":  # Data source not registered
                    logger.error(f"Data source {data_source} not registered")
                    return False
                    
                elif error_code == "SENZ0005":  # Invalid record format
                    logger.error(f"Invalid record format: {record_id}")
                    return False
                    
                elif error_code == "SENZ0002":  # Database connection error
                    if attempt < max_retries - 1:
                        logger.warning(f"Database error, retrying... ({attempt + 1}/{max_retries})")
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    else:
                        logger.error(f"Database error after {max_retries} attempts")
                        return False
                        
                else:
                    logger.error(f"Unexpected error: {e}")
                    return False
        
        return False
    
    def __del__(self):
        if hasattr(self, 'engine'):
            self.engine.destroy()

# Usage
loader = RobustLoader(config_json)
success = loader.load_record_with_retry("CUSTOMERS", "CUST001", record)
```

## Testing Patterns

### Python - Unit Testing with Mock Data

```python
import unittest
import json
from senzing import SzEngine

class TestEntityResolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = SzEngine()
        cls.engine.initialize("TestApp", config_json)
    
    @classmethod
    def tearDownClass(cls):
        cls.engine.destroy()
    
    def test_load_and_retrieve(self):
        # Load test record
        record = {
            "DATA_SOURCE": "TEST",
            "RECORD_ID": "TEST001",
            "NAME_FULL": "Test Person"
        }
        
        self.engine.add_record("TEST", "TEST001", json.dumps(record))
        
        # Retrieve and verify
        result = self.engine.get_entity_by_record_id("TEST", "TEST001")
        entity = json.loads(result)
        
        self.assertIn("RESOLVED_ENTITY", entity)
        self.assertEqual(
            entity["RESOLVED_ENTITY"]["RECORDS"][0]["RECORD_ID"],
            "TEST001"
        )
    
    def test_entity_matching(self):
        # Load two similar records
        record1 = {
            "DATA_SOURCE": "TEST",
            "RECORD_ID": "TEST002",
            "NAME_FULL": "Jane Doe",
            "EMAIL_ADDRESS": "jane@example.com"
        }
        
        record2 = {
            "DATA_SOURCE": "TEST",
            "RECORD_ID": "TEST003",
            "NAME_FULL": "Jane Doe",
            "EMAIL_ADDRESS": "jane@example.com"
        }
        
        self.engine.add_record("TEST", "TEST002", json.dumps(record1))
        self.engine.add_record("TEST", "TEST003", json.dumps(record2))
        
        # Verify they resolved to same entity
        entity1 = json.loads(self.engine.get_entity_by_record_id("TEST", "TEST002"))
        entity2 = json.loads(self.engine.get_entity_by_record_id("TEST", "TEST003"))
        
        self.assertEqual(
            entity1["RESOLVED_ENTITY"]["ENTITY_ID"],
            entity2["RESOLVED_ENTITY"]["ENTITY_ID"]
        )

if __name__ == "__main__":
    unittest.main()
```

## Integration Patterns

### Python - Kafka Consumer

```python
from kafka import KafkaConsumer
import json
from senzing import SzEngine

class SenzingKafkaConsumer:
    def __init__(self, config_json, kafka_config):
        self.engine = SzEngine()
        self.engine.initialize("KafkaConsumer", config_json)
        
        self.consumer = KafkaConsumer(
            kafka_config['topic'],
            bootstrap_servers=kafka_config['bootstrap_servers'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    
    def process_messages(self):
        for message in self.consumer:
            record = message.value
            
            try:
                self.engine.add_record(
                    data_source_code=record["DATA_SOURCE"],
                    record_id=record["RECORD_ID"],
                    record_definition=json.dumps(record)
                )
                print(f"Processed: {record['RECORD_ID']}")
                
            except Exception as e:
                print(f"Error processing {record.get('RECORD_ID')}: {e}")
    
    def close(self):
        self.consumer.close()
        self.engine.destroy()

# Usage
kafka_config = {
    'topic': 'senzing-records',
    'bootstrap_servers': ['localhost:9092']
}

consumer = SenzingKafkaConsumer(config_json, kafka_config)
consumer.process_messages()
```

### Python - REST API Wrapper

```python
from flask import Flask, request, jsonify
from senzing import SzEngine
import json

app = Flask(__name__)

# Initialize Senzing engine
engine = SzEngine()
engine.initialize("APIServer", config_json)

@app.route('/entity/<int:entity_id>', methods=['GET'])
def get_entity(entity_id):
    try:
        result = engine.get_entity_by_entity_id(entity_id)
        return jsonify(json.loads(result))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['POST'])
def search_entities():
    try:
        search_criteria = request.json
        result = engine.search_by_attributes(json.dumps(search_criteria))
        return jsonify(json.loads(result))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/record', methods=['POST'])
def add_record():
    try:
        record = request.json
        engine.add_record(
            record["DATA_SOURCE"],
            record["RECORD_ID"],
            json.dumps(record)
        )
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Performance Optimization Examples

### Python - Batch Processing with Transaction Control

```python
import json
from senzing import SzEngine

def load_in_batches(engine, records, batch_size=1000):
    total = len(records)
    loaded = 0
    
    for i in range(0, total, batch_size):
        batch = records[i:i + batch_size]
        
        for record in batch:
            try:
                engine.add_record(
                    record["DATA_SOURCE"],
                    record["RECORD_ID"],
                    json.dumps(record)
                )
                loaded += 1
            except Exception as e:
                print(f"Error: {e}")
        
        print(f"Progress: {loaded}/{total} ({100*loaded/total:.1f}%)")
    
    return loaded

# Usage
engine = SzEngine()
engine.initialize("BatchLoader", config_json)

try:
    loaded_count = load_in_batches(engine, my_records, batch_size=1000)
    print(f"Loaded {loaded_count} records")
finally:
    engine.destroy()
```

For more examples, use `find_examples` to search 27 Senzing GitHub repositories for working code patterns.
