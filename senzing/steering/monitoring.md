# Senzing — Monitoring and Observability

This guide covers monitoring strategies, metrics, alerting, and observability for Senzing deployments.

## Table of Contents

- [Key Metrics to Track](#key-metrics-to-track)
- [Metrics Collection Implementation](#metrics-collection-implementation)
- [Prometheus Integration](#prometheus-integration)
- [Grafana Dashboards](#grafana-dashboards)
- [Alert Rules](#alert-rules)
- [Alert Notifications](#alert-notifications)
- [Health Checks](#health-checks)
- [Log Analysis](#log-analysis)
- [Dashboard Examples](#dashboard-examples)

---

## Key Metrics to Track

### Loading Metrics

**Throughput**:
- Records loaded per second
- Records loaded per minute
- Records loaded per hour
- Total records loaded

**Performance**:
- Average load time per record
- 95th percentile load time
- 99th percentile load time
- Maximum load time

**Quality**:
- Load success rate
- Load error rate
- Error types distribution
- Retry count

**Resource Utilization**:
- CPU usage during loading
- Memory usage during loading
- Disk I/O during loading
- Network I/O during loading

### Query Metrics

**Response Times**:
- Average query response time
- 95th percentile response time
- 99th percentile response time
- Maximum response time

**Query Types**:
- get_entity_by_record_id count
- get_entity_by_entity_id count
- search_by_attributes count
- why_entities count

**Query Performance**:
- Queries per second
- Concurrent query count
- Query queue depth
- Query timeout rate

### Entity Metrics

**Entity Counts**:
- Total entity count
- Entities per data source
- New entities per day
- Deleted entities per day

**Entity Characteristics**:
- Average records per entity
- Maximum records per entity
- Single-record entities count
- Multi-source entities count

**Resolution Quality**:
- Match level distribution
- Average match score
- Ambiguous resolution count
- Possibly related count

### Database Metrics

**Size**:
- Total database size
- Table sizes
- Index sizes
- Growth rate per day

**Performance**:
- Query execution time
- Index hit rate
- Cache hit rate
- Connection count

**Health**:
- Active connections
- Idle connections
- Long-running queries
- Deadlock count

### System Metrics

**CPU**:
- Overall CPU utilization
- Per-core utilization
- CPU wait time
- Load average

**Memory**:
- Total memory usage
- Available memory
- Swap usage
- Memory pressure

**Disk**:
- Disk utilization
- Disk I/O rate
- Disk queue depth
- Disk latency

**Network**:
- Network throughput
- Network errors
- Connection count
- Packet loss

## Monitoring Implementation

### Python Metrics Collection

```python
import time
import psutil
from datetime import datetime
from collections import defaultdict

class SenzingMetricsCollector:
    """Collect and track Senzing metrics"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_time = time.time()
    
    def record_load(self, data_source, record_id, duration, success=True):
        """Record a load operation"""
        self.metrics["loads"].append({
            "timestamp": datetime.now(),
            "data_source": data_source,
            "record_id": record_id,
            "duration": duration,
            "success": success
        })
    
    def record_query(self, query_type, duration, result_count):
        """Record a query operation"""
        self.metrics["queries"].append({
            "timestamp": datetime.now(),
            "query_type": query_type,
            "duration": duration,
            "result_count": result_count
        })
    
    def record_error(self, operation, error_code, error_message):
        """Record an error"""
        self.metrics["errors"].append({
            "timestamp": datetime.now(),
            "operation": operation,
            "error_code": error_code,
            "error_message": error_message
        })
    
    def get_throughput(self, window_seconds=60):
        """Calculate current throughput"""
        cutoff = time.time() - window_seconds
        recent_loads = [
            m for m in self.metrics["loads"]
            if m["timestamp"].timestamp() > cutoff and m["success"]
        ]
        return len(recent_loads) / window_seconds
    
    def get_error_rate(self, window_seconds=60):
        """Calculate current error rate"""
        cutoff = time.time() - window_seconds
        recent_loads = [
            m for m in self.metrics["loads"]
            if m["timestamp"].timestamp() > cutoff
        ]
        if not recent_loads:
            return 0.0
        
        errors = sum(1 for m in recent_loads if not m["success"])
        return errors / len(recent_loads)
    
    def get_avg_response_time(self, query_type=None, window_seconds=60):
        """Calculate average response time"""
        cutoff = time.time() - window_seconds
        recent_queries = [
            m for m in self.metrics["queries"]
            if m["timestamp"].timestamp() > cutoff
            and (query_type is None or m["query_type"] == query_type)
        ]
        
        if not recent_queries:
            return 0.0
        
        return sum(m["duration"] for m in recent_queries) / len(recent_queries)
    
    def get_system_metrics(self):
        """Get current system metrics"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "network_io": psutil.net_io_counters()._asdict()
        }
    
    def export_metrics(self, output_file="metrics.json"):
        """Export metrics to file"""
        import json
        
        summary = {
            "collection_period": time.time() - self.start_time,
            "total_loads": len(self.metrics["loads"]),
            "successful_loads": sum(1 for m in self.metrics["loads"] if m["success"]),
            "total_queries": len(self.metrics["queries"]),
            "total_errors": len(self.metrics["errors"]),
            "current_throughput": self.get_throughput(),
            "current_error_rate": self.get_error_rate(),
            "avg_response_time": self.get_avg_response_time(),
            "system_metrics": self.get_system_metrics()
        }
        
        with open(output_file, "w") as f:
            json.dump(summary, f, indent=2, default=str)
        
        return summary

# Usage
metrics = SenzingMetricsCollector()

# Record operations
start = time.time()
try:
    engine.add_record("CUSTOMERS", "CUST001", json.dumps(record))
    metrics.record_load("CUSTOMERS", "CUST001", time.time() - start, success=True)
except Exception as e:
    metrics.record_load("CUSTOMERS", "CUST001", time.time() - start, success=False)
    metrics.record_error("add_record", "SENZ0005", str(e))

# Export metrics
summary = metrics.export_metrics()
print(f"Throughput: {summary['current_throughput']:.2f} records/sec")
```

### Prometheus Integration

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
records_loaded = Counter('senzing_records_loaded_total', 'Total records loaded', ['data_source'])
records_failed = Counter('senzing_records_failed_total', 'Total records failed', ['data_source', 'error_code'])
load_duration = Histogram('senzing_load_duration_seconds', 'Record load duration')
query_duration = Histogram('senzing_query_duration_seconds', 'Query duration', ['query_type'])
entity_count = Gauge('senzing_entity_count', 'Total entity count')
database_size = Gauge('senzing_database_size_bytes', 'Database size in bytes')

class PrometheusMonitor:
    """Monitor Senzing with Prometheus metrics"""
    
    def __init__(self, port=8000):
        # Start Prometheus HTTP server
        start_http_server(port)
    
    def record_load(self, data_source, record_id, duration, success=True, error_code=None):
        """Record a load operation"""
        if success:
            records_loaded.labels(data_source=data_source).inc()
        else:
            records_failed.labels(data_source=data_source, error_code=error_code).inc()
        
        load_duration.observe(duration)
    
    def record_query(self, query_type, duration):
        """Record a query operation"""
        query_duration.labels(query_type=query_type).observe(duration)
    
    def update_entity_count(self, count):
        """Update entity count gauge"""
        entity_count.set(count)
    
    def update_database_size(self, size_bytes):
        """Update database size gauge"""
        database_size.set(size_bytes)

# Usage
monitor = PrometheusMonitor(port=8000)

# Record operations
start = time.time()
try:
    engine.add_record("CUSTOMERS", "CUST001", json.dumps(record))
    monitor.record_load("CUSTOMERS", "CUST001", time.time() - start, success=True)
except Exception as e:
    monitor.record_load("CUSTOMERS", "CUST001", time.time() - start, success=False, error_code="SENZ0005")

# Metrics available at http://localhost:8000/metrics
```

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "Senzing Monitoring",
    "panels": [
      {
        "title": "Loading Throughput",
        "targets": [
          {
            "expr": "rate(senzing_records_loaded_total[5m])",
            "legendFormat": "{{data_source}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(senzing_records_failed_total[5m]) / rate(senzing_records_loaded_total[5m])",
            "legendFormat": "Error Rate"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Query Response Time (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(senzing_query_duration_seconds_bucket[5m]))",
            "legendFormat": "{{query_type}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Entity Count",
        "targets": [
          {
            "expr": "senzing_entity_count",
            "legendFormat": "Total Entities"
          }
        ],
        "type": "stat"
      },
      {
        "title": "Database Size",
        "targets": [
          {
            "expr": "senzing_database_size_bytes",
            "legendFormat": "Database Size"
          }
        ],
        "type": "stat"
      }
    ]
  }
}
```

## Alerting

### Alert Rules

```yaml
# Prometheus alert rules
groups:
  - name: senzing_alerts
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(senzing_records_failed_total[5m]) / rate(senzing_records_loaded_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} over the last 5 minutes"
      
      # Low throughput
      - alert: LowThroughput
        expr: rate(senzing_records_loaded_total[5m]) < 100
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Low loading throughput"
          description: "Throughput is {{ $value }} records/sec, below threshold of 100"
      
      # Slow queries
      - alert: SlowQueries
        expr: histogram_quantile(0.95, rate(senzing_query_duration_seconds_bucket[5m])) > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Slow query performance"
          description: "95th percentile query time is {{ $value }}s, above threshold of 1s"
      
      # Database size growth
      - alert: RapidDatabaseGrowth
        expr: rate(senzing_database_size_bytes[1h]) > 1073741824  # 1GB/hour
        for: 1h
        labels:
          severity: info
        annotations:
          summary: "Rapid database growth"
          description: "Database growing at {{ $value | humanize }}B/hour"
      
      # High CPU usage
      - alert: HighCPUUsage
        expr: avg(rate(process_cpu_seconds_total[5m])) > 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is {{ $value | humanizePercentage }}"
      
      # High memory usage
      - alert: HighMemoryUsage
        expr: process_resident_memory_bytes / node_memory_MemTotal_bytes > 0.9
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value | humanizePercentage }}"
```

### Alert Notification

```python
import requests
import json

class AlertManager:
    """Send alerts to various channels"""
    
    def __init__(self, slack_webhook=None, email_config=None):
        self.slack_webhook = slack_webhook
        self.email_config = email_config
    
    def send_slack_alert(self, title, message, severity="warning"):
        """Send alert to Slack"""
        if not self.slack_webhook:
            return
        
        color = {
            "info": "#36a64f",
            "warning": "#ff9900",
            "critical": "#ff0000"
        }.get(severity, "#808080")
        
        payload = {
            "attachments": [{
                "color": color,
                "title": title,
                "text": message,
                "footer": "Senzing Monitoring",
                "ts": int(time.time())
            }]
        }
        
        requests.post(self.slack_webhook, json=payload)
    
    def send_email_alert(self, subject, body):
        """Send alert via email"""
        if not self.email_config:
            return
        
        import smtplib
        from email.mime.text import MIMEText
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_config['from']
        msg['To'] = self.email_config['to']
        
        with smtplib.SMTP(self.email_config['smtp_server']) as server:
            server.send_message(msg)
    
    def check_and_alert(self, metrics):
        """Check metrics and send alerts if needed"""
        
        # High error rate
        if metrics.get_error_rate() > 0.05:
            self.send_slack_alert(
                "High Error Rate",
                f"Error rate is {metrics.get_error_rate():.2%}",
                severity="warning"
            )
        
        # Low throughput
        if metrics.get_throughput() < 100:
            self.send_slack_alert(
                "Low Throughput",
                f"Throughput is {metrics.get_throughput():.0f} records/sec",
                severity="warning"
            )
        
        # Slow queries
        avg_response = metrics.get_avg_response_time()
        if avg_response > 1.0:
            self.send_slack_alert(
                "Slow Queries",
                f"Average response time is {avg_response:.2f}s",
                severity="warning"
            )

# Usage
alert_mgr = AlertManager(slack_webhook="https://hooks.slack.com/services/YOUR/WEBHOOK/URL")
alert_mgr.check_and_alert(metrics)
```

## Health Checks

### Application Health Check

```python
from flask import Flask, jsonify
from senzing import SzEngine

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    
    health = {
        "status": "healthy",
        "checks": {}
    }
    
    # Check Senzing engine
    try:
        engine = SzEngine()
        engine.initialize("HealthCheck", config_json)
        engine.destroy()
        health["checks"]["senzing_engine"] = "ok"
    except Exception as e:
        health["status"] = "unhealthy"
        health["checks"]["senzing_engine"] = f"error: {str(e)}"
    
    # Check database
    try:
        import psycopg2
        conn = psycopg2.connect(database_connection_string)
        conn.close()
        health["checks"]["database"] = "ok"
    except Exception as e:
        health["status"] = "unhealthy"
        health["checks"]["database"] = f"error: {str(e)}"
    
    # Check disk space
    import shutil
    disk = shutil.disk_usage('/')
    disk_percent = (disk.used / disk.total) * 100
    if disk_percent > 90:
        health["status"] = "degraded"
        health["checks"]["disk_space"] = f"warning: {disk_percent:.1f}% used"
    else:
        health["checks"]["disk_space"] = "ok"
    
    status_code = 200 if health["status"] == "healthy" else 503
    return jsonify(health), status_code

@app.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness check for Kubernetes"""
    
    # Check if application is ready to serve traffic
    try:
        engine = SzEngine()
        engine.initialize("ReadinessCheck", config_json)
        engine.destroy()
        return jsonify({"status": "ready"}), 200
    except:
        return jsonify({"status": "not ready"}), 503

@app.route('/live', methods=['GET'])
def liveness_check():
    """Liveness check for Kubernetes"""
    
    # Simple check that application is running
    return jsonify({"status": "alive"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### Database Health Monitoring

```python
import psycopg2

def check_database_health(connection_string):
    """Check PostgreSQL database health"""
    
    health = {
        "status": "healthy",
        "metrics": {}
    }
    
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        
        # Check connection count
        cursor.execute("SELECT count(*) FROM pg_stat_activity;")
        connection_count = cursor.fetchone()[0]
        health["metrics"]["connection_count"] = connection_count
        
        # Check database size
        cursor.execute("SELECT pg_database_size(current_database());")
        db_size = cursor.fetchone()[0]
        health["metrics"]["database_size_bytes"] = db_size
        
        # Check for long-running queries
        cursor.execute("""
            SELECT count(*) 
            FROM pg_stat_activity 
            WHERE state = 'active' 
            AND now() - query_start > interval '5 minutes';
        """)
        long_queries = cursor.fetchone()[0]
        health["metrics"]["long_running_queries"] = long_queries
        
        if long_queries > 0:
            health["status"] = "degraded"
        
        # Check for deadlocks
        cursor.execute("SELECT deadlocks FROM pg_stat_database WHERE datname = current_database();")
        deadlocks = cursor.fetchone()[0]
        health["metrics"]["deadlocks"] = deadlocks
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        health["status"] = "unhealthy"
        health["error"] = str(e)
    
    return health

# Usage
db_health = check_database_health("postgresql://senzing:password@localhost:5432/senzing")
print(f"Database status: {db_health['status']}")
```

## Log Analysis

### Structured Logging

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    """Structured logging for Senzing operations"""
    
    def __init__(self, log_file="senzing.log"):
        self.logger = logging.getLogger("Senzing")
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
    
    def log(self, event_type, **kwargs):
        """Log a structured event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            **kwargs
        }
        self.logger.info(json.dumps(event))
    
    def log_load(self, data_source, record_id, duration, success=True, error=None):
        """Log a load operation"""
        self.log(
            "record_load",
            data_source=data_source,
            record_id=record_id,
            duration=duration,
            success=success,
            error=error
        )
    
    def log_query(self, query_type, duration, result_count):
        """Log a query operation"""
        self.log(
            "query",
            query_type=query_type,
            duration=duration,
            result_count=result_count
        )

# Usage
logger = StructuredLogger()
logger.log_load("CUSTOMERS", "CUST001", 0.123, success=True)
logger.log_query("search_by_attributes", 0.456, 5)
```

### Log Aggregation

```python
def analyze_logs(log_file="senzing.log", time_window_minutes=60):
    """Analyze logs for patterns and issues"""
    
    from datetime import datetime, timedelta
    import json
    
    cutoff = datetime.now() - timedelta(minutes=time_window_minutes)
    
    analysis = {
        "total_events": 0,
        "loads": {"success": 0, "failed": 0},
        "queries": {"count": 0, "total_duration": 0},
        "errors": [],
        "slow_operations": []
    }
    
    with open(log_file, "r") as f:
        for line in f:
            try:
                event = json.loads(line)
                event_time = datetime.fromisoformat(event["timestamp"])
                
                if event_time < cutoff:
                    continue
                
                analysis["total_events"] += 1
                
                if event["event_type"] == "record_load":
                    if event["success"]:
                        analysis["loads"]["success"] += 1
                    else:
                        analysis["loads"]["failed"] += 1
                        analysis["errors"].append(event)
                    
                    if event["duration"] > 1.0:
                        analysis["slow_operations"].append(event)
                
                elif event["event_type"] == "query":
                    analysis["queries"]["count"] += 1
                    analysis["queries"]["total_duration"] += event["duration"]
                    
                    if event["duration"] > 1.0:
                        analysis["slow_operations"].append(event)
            
            except:
                pass
    
    # Calculate averages
    if analysis["queries"]["count"] > 0:
        analysis["queries"]["avg_duration"] = (
            analysis["queries"]["total_duration"] / analysis["queries"]["count"]
        )
    
    return analysis

# Usage
analysis = analyze_logs(time_window_minutes=60)
print(f"Success rate: {analysis['loads']['success'] / (analysis['loads']['success'] + analysis['loads']['failed']):.2%}")
print(f"Average query time: {analysis['queries'].get('avg_duration', 0):.3f}s")
print(f"Slow operations: {len(analysis['slow_operations'])}")
```

## Dashboard Examples

### Real-Time Dashboard (Terminal)

```python
import curses
import time

def realtime_dashboard(metrics):
    """Display real-time metrics in terminal"""
    
    def draw_dashboard(stdscr):
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(1)   # Non-blocking input
        
        while True:
            stdscr.clear()
            
            # Title
            stdscr.addstr(0, 0, "=== Senzing Real-Time Dashboard ===", curses.A_BOLD)
            
            # Loading metrics
            stdscr.addstr(2, 0, "Loading Metrics:", curses.A_BOLD)
            stdscr.addstr(3, 2, f"Throughput: {metrics.get_throughput():.0f} records/sec")
            stdscr.addstr(4, 2, f"Error Rate: {metrics.get_error_rate():.2%}")
            stdscr.addstr(5, 2, f"Total Loaded: {len(metrics.metrics['loads'])}")
            
            # Query metrics
            stdscr.addstr(7, 0, "Query Metrics:", curses.A_BOLD)
            stdscr.addstr(8, 2, f"Avg Response: {metrics.get_avg_response_time():.3f}s")
            stdscr.addstr(9, 2, f"Total Queries: {len(metrics.metrics['queries'])}")
            
            # System metrics
            system = metrics.get_system_metrics()
            stdscr.addstr(11, 0, "System Metrics:", curses.A_BOLD)
            stdscr.addstr(12, 2, f"CPU: {system['cpu_percent']:.1f}%")
            stdscr.addstr(13, 2, f"Memory: {system['memory_percent']:.1f}%")
            stdscr.addstr(14, 2, f"Disk: {system['disk_percent']:.1f}%")
            
            stdscr.addstr(16, 0, "Press 'q' to quit")
            
            stdscr.refresh()
            
            # Check for quit
            key = stdscr.getch()
            if key == ord('q'):
                break
            
            time.sleep(1)
    
    curses.wrapper(draw_dashboard)

# Usage
# realtime_dashboard(metrics)
```

For more monitoring and observability guidance, use:
```python
search_docs(query="monitoring", category="general", version="current")
```
