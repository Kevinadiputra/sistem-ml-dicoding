import json

# Define the Grafana dashboard JSON schema with correct Python values
dashboard = {
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": True,
        "hide": True,
        "name": "Annotations & Alerts",
        "target": {
          "limit": 100,
          "matchAny": False,
          "tags": [],
          "type": "dashboard"
        },
        "type": "dashboard"
      }
    ]
  },
  "editable": True,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": None,
  "links": [],
  "liveNow": False,
  "panels": [
    # --- ROW 1: SYSTEM HEALTH ---
    {
      "collapsed": False,
      "gridPos": {"h": 1, "w": 24, "x": 0, "y": 0},
      "id": 1,
      "title": "System Resource Monitoring",
      "type": "row"
    },
    {
      "datasource": {"type": "prometheus", "uid": "prometheus"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "thresholds"},
          "mappings": [],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "green", "value": None},
              {"color": "yellow", "value": 70},
              {"color": "red", "value": 80}
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {"h": 5, "w": 8, "x": 0, "y": 1},
      "id": 2,
      "options": {"orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "showThresholdLabels": False, "showThresholdMarkers": True, "textMode": "auto"},
      "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "editorMode": "code", "expr": "cpu_usage_percent", "legendFormat": "CPU Usage", "range": True, "refId": "A"}],
      "title": "5. CPU Usage",
      "type": "gauge"
    },
    {
      "datasource": {"type": "prometheus", "uid": "prometheus"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "thresholds"},
          "mappings": [],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "green", "value": None},
              {"color": "yellow", "value": 75},
              {"color": "red", "value": 90}
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {"h": 5, "w": 8, "x": 8, "y": 1},
      "id": 3,
      "options": {"orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "showThresholdLabels": False, "showThresholdMarkers": True, "textMode": "auto"},
      "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "editorMode": "code", "expr": "memory_usage_percent", "legendFormat": "Memory Usage", "range": True, "refId": "A"}],
      "title": "6. Memory Usage",
      "type": "gauge"
    },
    {
      "datasource": {"type": "prometheus", "uid": "prometheus"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "thresholds"},
          "mappings": [],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "green", "value": None},
              {"color": "yellow", "value": 80},
              {"color": "red", "value": 90}
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {"h": 5, "w": 8, "x": 16, "y": 1},
      "id": 4,
      "options": {"orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "showThresholdLabels": False, "showThresholdMarkers": True, "textMode": "auto"},
      "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "editorMode": "code", "expr": "disk_usage_percent", "legendFormat": "Disk Usage", "range": True, "refId": "A"}],
      "title": "7. Disk Usage",
      "type": "gauge"
    },
    # --- ROW 2: API TRAFFIC & MONITORING ---
    {
      "collapsed": False,
      "gridPos": {"h": 1, "w": 24, "x": 0, "y": 6},
      "id": 5,
      "title": "API Traffic & Performance",
      "type": "row"
    },
    {
      "datasource": {"type": "prometheus", "uid": "prometheus"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "custom": {"axisBorderShow": False, "axisCenteredZero": False, "axisColorMode": "text", "axisLabel": "Requests / Sec", "axisPlacement": "auto", "barAlignment": 0, "drawStyle": "line", "fillOpacity": 10, "gradientMode": "none", "hideFrom": {"legend": False, "tooltip": False, "viz": False}, "lineInterpolation": "smooth", "lineWidth": 2, "pointSize": 5, "scaleDistribution": {"type": "linear"}, "showPoints": "auto", "spanNulls": False, "stacking": {"group": "A", "mode": "none"}, "thresholdsStyle": {"mode": "off"}},
          "mappings": [],
          "min": 0
        },
        "overrides": []
      },
      "gridPos": {"h": 6, "w": 8, "x": 0, "y": 7},
      "id": 6,
      "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "editorMode": "code", "expr": "rate(request_count_total[1m])", "legendFormat": "Requests Rate", "range": True, "refId": "A"}],
      "title": "3. Request Count (Rate/min)",
      "type": "timeseries"
    },
    {
      "datasource": {"type": "prometheus", "uid": "prometheus"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "fixed", "fixedColor": "red"},
          "custom": {"axisBorderShow": False, "axisCenteredZero": False, "axisColorMode": "text", "axisPlacement": "auto", "barAlignment": 0, "drawStyle": "line", "fillOpacity": 10, "gradientMode": "none", "lineInterpolation": "smooth", "lineWidth": 2, "pointSize": 5, "scaleDistribution": {"type": "linear"}, "showPoints": "auto", "spanNulls": False, "stacking": {"group": "A", "mode": "none"}, "thresholdsStyle": {"mode": "off"}},
          "mappings": [],
          "min": 0
        },
        "overrides": []
      },
      "gridPos": {"h": 6, "w": 8, "x": 8, "y": 7},
      "id": 7,
      "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "editorMode": "code", "expr": "rate(error_count_total[1m])", "legendFormat": "Errors Rate", "range": True, "refId": "A"}],
      "title": "4. Error Count (Rate/min)",
      "type": "timeseries"
    },
    {
      "datasource": {"type": "prometheus", "uid": "prometheus"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "mappings": [],
          "min": 0,
          "unit": "reqps"
        },
        "overrides": []
      },
      "gridPos": {"h": 6, "w": 8, "x": 16, "y": 7},
      "id": 8,
      "options": {"colorMode": "value", "graphMode": "area", "justifyMode": "auto", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
      "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "editorMode": "code", "expr": "api_throughput_requests_per_second", "legendFormat": "Throughput", "range": True, "refId": "A"}],
      "title": "9. Throughput",
      "type": "stat"
    },
    # --- ROW 3: ML MODEL METRICS ---
    {
      "collapsed": False,
      "gridPos": {"h": 1, "w": 24, "x": 0, "y": 13},
      "id": 9,
      "title": "Model Inference Indicators",
      "type": "row"
    },
    {
      "datasource": {"type": "prometheus", "uid": "prometheus"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "mappings": [],
          "min": 0
        },
        "overrides": []
      },
      "gridPos": {"h": 6, "w": 6, "x": 0, "y": 14},
      "id": 10,
      "options": {"colorMode": "value", "graphMode": "area", "justifyMode": "auto", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
      "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "editorMode": "code", "expr": "prediction_count_total", "legendFormat": "Predictions", "range": True, "refId": "A"}],
      "title": "1. Prediction Count",
      "type": "stat"
    },
    {
      "datasource": {"type": "prometheus", "uid": "prometheus"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "thresholds"},
          "mappings": [],
          "max": 1,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "red", "value": None},
              {"color": "yellow", "value": 0.75},
              {"color": "green", "value": 0.85}
            ]
          },
          "unit": "percentunit"
        },
        "overrides": []
      },
      "gridPos": {"h": 6, "w": 6, "x": 6, "y": 14},
      "id": 11,
      "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "auto", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
      "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "editorMode": "code", "expr": "model_accuracy_ratio", "legendFormat": "Accuracy", "range": True, "refId": "A"}],
      "title": "8. Model Accuracy",
      "type": "stat"
    },
    {
      "datasource": {"type": "prometheus", "uid": "prometheus"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "custom": {"axisLabel": "Latency (Seconds)", "drawStyle": "line", "fillOpacity": 10, "lineInterpolation": "smooth", "lineWidth": 2, "pointSize": 5, "showPoints": "auto"},
          "mappings": [],
          "min": 0,
          "unit": "s"
        },
        "overrides": []
      },
      "gridPos": {"h": 6, "w": 6, "x": 12, "y": 14},
      "id": 12,
      "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "editorMode": "code", "expr": "prediction_latency_seconds_sum / (prediction_latency_seconds_count + 1e-5)", "legendFormat": "Inference Latency", "range": True, "refId": "A"}],
      "title": "2. Prediction Latency",
      "type": "timeseries"
    },
    {
      "datasource": {"type": "prometheus", "uid": "prometheus"},
      "fieldConfig": {
        "defaults": {
          "color": {"mode": "palette-classic"},
          "custom": {"axisLabel": "Response Time (Seconds)", "drawStyle": "line", "fillOpacity": 10, "lineInterpolation": "smooth", "lineWidth": 2, "pointSize": 5, "showPoints": "auto"},
          "mappings": [],
          "min": 0,
          "unit": "s"
        },
        "overrides": []
      },
      "gridPos": {"h": 6, "w": 6, "x": 18, "y": 14},
      "id": 13,
      "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "editorMode": "code", "expr": "api_response_time_seconds_sum / (api_response_time_seconds_count + 1e-5)", "legendFormat": "Response Time", "range": True, "refId": "A"}],
      "title": "10. Response Time",
      "type": "timeseries"
    }
  ],
  "schemaVersion": 36,
  "style": "dark",
  "tags": ["mlops", "dicoding"],
  "templating": {"list": []},
  "time": {"from": "now-15m", "to": "now"},
  "timepicker": {},
  "timezone": "",
  "title": "[NAMA USERNAME DICODING]",
  "uid": "dicoding_mlops_heart_disease",
  "version": 1,
  "weekStart": ""
}

with open("grafana_dashboard.json", "w") as f:
    json.dump(dashboard, f, indent=2)

print("grafana_dashboard.json generated successfully!")
