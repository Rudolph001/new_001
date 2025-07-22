
# Email Guardian - Service Specification

## Executive Summary

Email Guardian is a comprehensive email security analysis platform designed to process Tessian email export data and identify security threats, data exfiltration attempts, and anomalous communication patterns using AI-powered analytics and rule-based filtering.

## Core Platform Services

### 1. Data Processing Engine
**Service:** CSV File Processing and Ingestion
- **Functionality:** Chunked processing of large Tessian email export files (2,500 records per chunk)
- **Input:** CSV files with email communication data
- **Output:** Structured database records with normalized field mapping
- **Performance:** Optimized for files up to 500MB with automatic compression
- **Technology:** Python pandas with SQLite persistence

### 2. Machine Learning Analytics Service
**Service:** AI-Powered Risk Assessment and Anomaly Detection
- **Core ML Engine:** Isolation Forest algorithm for pattern recognition
- **Risk Scoring:** Multi-dimensional assessment (0-1 scale) with configurable thresholds
- **Features:** 
  - Anomaly detection with 10% contamination rate
  - Text analysis using TF-IDF vectorization
  - Behavioral pattern clustering
  - Temporal pattern analysis
- **Outputs:** Risk levels (Critical/High/Medium/Low) with explanations

### 3. Rule Engine System
**Service:** Business Logic and Security Policy Enforcement
- **Exclusion Rules:** Pre-processing filters for known-good communications
- **Security Rules:** Threat detection with complex AND/OR logic
- **Operators Supported:** equals, contains, regex, range comparisons, list membership
- **Configuration:** JSON-based rule definitions with priority ordering

### 4. Domain Classification Service
**Service:** Automated Domain Analysis and Trust Scoring
- **Domain Categories:** Corporate, Personal, Public, Suspicious
- **Trust Scoring:** 0-100 scale based on communication patterns and risk factors
- **Whitelist Management:** Automated recommendations with confidence levels
- **Pattern Recognition:** BAU (Business As Usual) communication identification

### 5. Case Management System
**Service:** Security Incident Tracking and Investigation
- **Case Lifecycle:** Active → Escalated → Cleared
- **Escalation Workflow:** Automated email generation for critical cases
- **Investigation Tools:** Detailed record analysis with risk explanations
- **Filtering:** Advanced search by risk level, status, and content

### 6. Analytics Dashboard Suite
**Service:** Real-time Visualization and Reporting
- **Main Dashboard:** Processing statistics and ML insights
- **Sender Analysis:** Individual behavior pattern assessment
- **Time Analysis:** Temporal pattern detection (business hours vs. after-hours)
- **Attachment Intelligence:** File type risk assessment and malware indicators
- **Advanced ML Dashboard:** Network analysis and correlation detection

## Technical Architecture

### Database Layer
- **Primary Database:** SQLite (development/local deployment)
- **Models:** 
  - ProcessingSession: File upload and processing state management
  - EmailRecord: Individual email communication data
  - Rule: Security and exclusion rule definitions
  - WhitelistDomain: Trusted domain registry
  - AttachmentKeyword: ML keyword scoring database

### Web Application Layer
- **Framework:** Flask with SQLAlchemy ORM
- **Frontend:** Bootstrap 5 with responsive design
- **Authentication:** Session-based with configurable secret keys
- **API Endpoints:** RESTful design for dashboard updates and management

### Processing Pipeline
1. **File Upload** → Session creation and validation
2. **Data Ingestion** → Chunked CSV processing with field mapping
3. **Exclusion Filtering** → Apply business exclusion rules
4. **Domain Whitelisting** → Filter trusted communications
5. **Security Rules** → Apply threat detection rules
6. **ML Analysis** → Risk scoring and anomaly detection
7. **Case Generation** → Create investigatable security cases

## Service Capabilities

### Performance Specifications
- **File Size Limit:** 500MB maximum upload
- **Processing Speed:** Optimized chunking with configurable batch sizes
- **Concurrent Sessions:** Multiple file processing support
- **Real-time Updates:** AJAX-based progress monitoring

### Security Features
- **Data Privacy:** Local processing with no external data transmission
- **Risk Assessment:** Comprehensive scoring with explainable AI
- **Threat Detection:** Pattern-based malware and phishing indicators
- **Data Exfiltration Detection:** Bulk transfer and suspicious timing analysis

### Administrative Capabilities
- **Rule Management:** Create, modify, and test security rules
- **Domain Management:** Whitelist administration with bulk operations
- **Session Management:** Processing history and cleanup utilities
- **System Monitoring:** Performance metrics and error tracking

## Deployment Specifications

### System Requirements
- **Platform:** Cross-platform (Windows, macOS, Linux)
- **Python Version:** 3.8 or higher
- **Memory:** 4GB minimum, 8GB recommended
- **Storage:** 1GB for application, additional space for data files
- **Network:** Local deployment (127.0.0.1:5000)

### Configuration Options
- **Fast Mode:** Reduced processing for speed optimization
- **ML Parameters:** Configurable estimators and feature limits
- **Chunk Size:** Adjustable processing batch sizes
- **Progress Reporting:** Configurable update intervals

## API Specifications

### Core Endpoints
- `POST /upload` - File upload and session creation
- `GET /api/processing-status/{session_id}` - Real-time processing updates
- `GET /api/dashboard-stats/{session_id}` - Dashboard analytics
- `GET /api/ml_insights/{session_id}` - Machine learning analysis results
- `POST /api/rules` - Security rule creation and management
- `GET/POST /api/whitelist-domains` - Domain whitelist management

### Data Formats
- **Input:** CSV files with flexible column mapping
- **Output:** JSON responses with structured data
- **Storage:** Compressed JSON for large datasets

## Service Level Characteristics

### Reliability
- **Error Handling:** Comprehensive exception management with user feedback
- **Data Integrity:** Transaction-based database operations
- **Recovery:** Session state persistence with resume capability

### Scalability
- **Processing Optimization:** Configurable performance parameters
- **Memory Management:** Chunked processing for large files
- **Database Scaling:** SQLite to PostgreSQL migration path

### Maintainability
- **Modular Design:** Separate engines for ML, rules, and domain management
- **Configuration Management:** Environment variable based settings
- **Logging:** Comprehensive debug and audit logging

## Current Build Status

✅ **Implemented Services:**
- Complete data processing pipeline
- Machine learning risk assessment
- Rule engine with complex logic support
- Domain classification and whitelisting
- Case management system
- Multi-dashboard analytics suite
- Administrative interface
- RESTful API endpoints

🔧 **Operational Status:**
- Fully functional local deployment
- Production-ready codebase
- Comprehensive error handling
- Real-time processing monitoring
- Professional UI/UX implementation
