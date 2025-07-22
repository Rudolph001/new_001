
# Email Guardian - Process Flow Documentation

## Overview
This document outlines the complete process flow for Email Guardian's email security analysis platform, from initial file upload through final case resolution.

## 1. File Upload and Session Initialization

```
User Action: File Upload
    ↓
CSV File Validation
    ├── File Type Check (.csv required)
    ├── File Size Validation (≤ 500MB)
    └── Format Verification
    ↓
Session Creation
    ├── Generate Unique Session ID (UUID)
    ├── Create ProcessingSession Record
    ├── Store File in uploads/ Directory
    └── Initialize Processing Status
    ↓
Background Processing Thread Launch
```

## 2. Data Processing Pipeline

### Phase 1: Data Ingestion
```
CSV File Processing
    ↓
Column Mapping Engine
    ├── Case-Insensitive Field Matching
    ├── Flexible Header Recognition
    └── Data Type Validation
    ↓
Chunked Processing (2,500 records/chunk)
    ├── Memory Optimization
    ├── Progress Tracking
    └── Error Isolation
    ↓
Database Record Creation
    ├── EmailRecord Entry per Row
    ├── Data Normalization
    └── Relationship Establishment
```

### Phase 2: Business Logic Application
```
Exclusion Rule Engine
    ↓
Rule Evaluation Process
    ├── Load Active Exclusion Rules
    ├── Apply Complex AND/OR Logic
    ├── Pattern Matching (Regex Support)
    └── Record Marking (excluded_by_rule)
    ↓
Whitelist Domain Filtering
    ├── Load Active Whitelist Domains
    ├── Domain Matching Logic
    ├── Trust Score Application
    └── Record Marking (whitelisted=True)
```

### Phase 3: Security Analysis
```
Security Rule Processing
    ↓
Threat Detection Engine
    ├── Load Active Security Rules
    ├── Pattern Recognition
    ├── Risk Factor Assessment
    └── Rule Match Recording
    ↓
Machine Learning Analysis
    ├── Feature Engineering
        ├── Text Analysis (Subject/Attachments)
        ├── Domain Classification
        ├── Temporal Patterns
        └── Behavioral Indicators
    ├── Anomaly Detection (Isolation Forest)
    ├── Risk Score Calculation (0-1 Scale)
    └── Risk Level Assignment
```

## 3. Analysis Engine Workflow

### ML Risk Assessment Process
```
Data Preparation
    ├── Feature Vector Creation
    ├── Text Vectorization (TF-IDF)
    ├── Numerical Normalization
    └── Pattern Extraction
    ↓
Anomaly Detection Algorithm
    ├── Isolation Forest Training
    ├── Contamination Rate: 10%
    ├── Estimators: Configurable (25-100)
    └── Decision Function Scoring
    ↓
Risk Score Computation
    ├── Anomaly Contribution (40%)
    ├── Rule-Based Factors (60%)
        ├── Leaver Status (30%)
        ├── External Domain (20%)
        ├── Attachment Risk (30%)
        ├── Keyword Matches (20%)
        ├── Time-based Risk (10%)
        └── Justification Analysis (10%)
    └── Final Score Normalization
```

### Domain Classification Process
```
Domain Analysis
    ├── Pattern Recognition
        ├── Corporate Domains
        ├── Public Email Providers
        ├── Suspicious TLDs
        └── Custom Classifications
    ├── Trust Score Calculation
        ├── Communication Frequency (30%)
        ├── Average Risk Score (40%)
        ├── Business Context (20%)
        └── Domain Reputation (10%)
    └── Whitelist Recommendations
```

## 4. Case Management Workflow

### Case Generation Process
```
Risk Assessment Results
    ↓
Case Creation Logic
    ├── Exclude Whitelisted Records
    ├── Filter by Risk Threshold
    ├── Apply Security Rule Matches
    └── Generate Case Records
    ↓
Case Classification
    ├── Critical Cases (Risk ≥ 0.8)
    ├── High Risk Cases (Risk ≥ 0.6)
    ├── Medium Risk Cases (Risk ≥ 0.4)
    └── Low Risk Cases (Risk < 0.4)
```

### Investigation Workflow
```
Case Review Process
    ├── Case Details Analysis
        ├── Email Content Review
        ├── Sender Behavior Analysis
        ├── Attachment Risk Assessment
        └── ML Explanation Review
    ├── Investigation Actions
        ├── Risk Level Adjustment
        ├── Case Status Updates
        ├── Notes and Documentation
        └── Evidence Collection
    └── Case Resolution
        ├── Escalation to Security Team
        ├── Case Clearance
        └── Final Documentation
```

## 5. Dashboard and Reporting Flow

### Real-time Analytics Process
```
Dashboard Data Pipeline
    ↓
Statistics Aggregation
    ├── Session Processing Stats
    ├── Risk Distribution Analysis
    ├── ML Insights Generation
    └── Workflow Metrics
    ↓
Visualization Data Preparation
    ├── Chart Data Formatting
    ├── Trend Analysis
    ├── Comparative Metrics
    └── Real-time Updates
    ↓
Dashboard Rendering
    ├── Animated Counters
    ├── Interactive Charts
    ├── Progress Indicators
    └── Status Updates
```

### Advanced Analytics Flow
```
Deep Analysis Engines
    ├── Sender Behavior Analysis
        ├── Communication Pattern Detection
        ├── Risk Profile Generation
        ├── Behavioral Anomaly Identification
        └── Network Relationship Mapping
    ├── Temporal Pattern Analysis
        ├── Time-based Risk Detection
        ├── Business Hours Analysis
        ├── Weekend Activity Monitoring
        └── Anomalous Timing Identification
    ├── Attachment Intelligence
        ├── File Type Risk Assessment
        ├── Malware Indicator Detection
        ├── Data Exfiltration Pattern Recognition
        └── Bulk Transfer Analysis
    └── BAU Pattern Recognition
        ├── Business Communication Identification
        ├── Whitelist Recommendation Generation
        ├── Trust Score Optimization
        └── False Positive Reduction
```

## 6. Administrative Process Flow

### Rule Management Process
```
Rule Configuration
    ├── Rule Creation Interface
        ├── Condition Builder (AND/OR Logic)
        ├── Field Selection
        ├── Operator Configuration
        └── Action Definition
    ├── Rule Validation
        ├── Syntax Checking
        ├── Logic Verification
        └── Test Case Execution
    ├── Rule Deployment
        ├── Activation Control
        ├── Priority Management
        └── Impact Assessment
    └── Rule Monitoring
        ├── Performance Tracking
        ├── Match Rate Analysis
        └── Effectiveness Measurement
```

### System Maintenance Flow
```
Administrative Tasks
    ├── Session Management
        ├── Processing History Review
        ├── Data Cleanup Operations
        ├── Performance Monitoring
        └── Error Log Analysis
    ├── Domain Management
        ├── Whitelist Administration
        ├── Trust Score Calibration
        ├── Bulk Domain Operations
        └── Recommendation Review
    ├── System Configuration
        ├── Performance Tuning
        ├── Security Parameter Adjustment
        ├── ML Model Optimization
        └── Resource Management
    └── Reporting and Audit
        ├── Processing Statistics
        ├── Security Metrics
        ├── System Health Monitoring
        └── Compliance Reporting
```

## 7. Error Handling and Recovery

### Error Management Process
```
Error Detection
    ├── Processing Exceptions
    ├── Data Validation Failures
    ├── Resource Constraints
    └── System Errors
    ↓
Error Classification
    ├── Critical System Errors
    ├── Data Processing Issues
    ├── User Input Errors
    └── Resource Limitations
    ↓
Recovery Actions
    ├── Automatic Retry Logic
    ├── Graceful Degradation
    ├── User Notification
    └── Session State Preservation
    ↓
Logging and Monitoring
    ├── Error Log Generation
    ├── Performance Impact Assessment
    ├── Recovery Tracking
    └── Root Cause Analysis
```

## 8. Performance Optimization Flow

### Speed Optimization Process
```
Performance Configuration
    ├── Fast Mode Activation
        ├── Reduced ML Processing
        ├── Limited Feature Sets
        ├── Larger Chunk Sizes
        └── Optimized Algorithms
    ├── Resource Management
        ├── Memory Usage Optimization
        ├── CPU Utilization Control
        ├── I/O Operation Batching
        └── Database Query Optimization
    └── Real-time Monitoring
        ├── Processing Speed Tracking
        ├── Resource Usage Monitoring
        ├── Bottleneck Identification
        └── Performance Tuning
```

This process flow represents the complete operational workflow of the Email Guardian platform as currently implemented, providing a comprehensive view of all system processes from data ingestion through case resolution and system administration.
