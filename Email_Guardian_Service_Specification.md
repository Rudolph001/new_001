
# Email Guardian - Service Specification

## Executive Summary

Email Guardian is a comprehensive email security analysis platform designed to process Tessian email export data and identify security threats, data exfiltration attempts, and anomalous communication patterns using AI-powered analytics and rule-based filtering.

## Core Platform Services

### 1. Data Processing Engine
**Service:** CSV File Processing and Ingestion
- **Functionality:** Chunked processing of large Tessian email export files (1,000 records per chunk in fast mode)
- **Input:** CSV files with email communication data
- **Output:** Structured database records with normalized field mapping
- **Performance:** Optimized for files up to 500MB with automatic session management
- **Technology:** Python pandas with SQLite persistence

### 2. Machine Learning Analytics Service
**Service:** AI-Powered Risk Assessment and Anomaly Detection
- **Core ML Engine:** Isolation Forest algorithm for pattern recognition
- **Risk Scoring:** Multi-dimensional assessment (0-1 scale) with configurable thresholds
- **Features:** 
  - Anomaly detection with configurable contamination rate
  - Text analysis using TF-IDF vectorization
  - Behavioral pattern clustering
  - Fast mode optimization (25 estimators, 200 TF-IDF features)
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
- **Whitelist Management:** Manual domain addition with bulk operations
- **Pattern Recognition:** BAU (Business As Usual) communication identification

### 5. Case Management System
**Service:** Security Incident Tracking and Investigation
- **Case Lifecycle:** Active → Escalated → Cleared
- **Investigation Tools:** Detailed record analysis with risk explanations
- **Filtering:** Advanced search by risk level, status, and content
- **Manual Actions:** Mark cases as cleared or escalated

### 6. Analytics Dashboard Suite
**Service:** Real-time Visualization and Reporting
- **Main Dashboard:** Processing statistics and ML insights
- **Sender Analysis:** Individual behavior pattern assessment
- **Time Analysis:** Temporal pattern detection (business hours vs. after-hours)
- **Advanced ML Dashboard:** Network analysis and correlation detection
- **Whitelist Analysis:** Domain trust assessment and recommendations

## Technical Architecture

### Database Layer
- **Primary Database:** SQLite with SQLAlchemy ORM
- **Models:** 
  - ProcessingSession: File upload and processing state management
  - EmailRecord: Individual email communication data
  - Rule: Security and exclusion rule definitions
  - WhitelistDomain: Trusted domain registry

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
- **Processing Speed:** Fast mode with configurable chunking (1000-2000 records per chunk)
- **Concurrent Sessions:** Multiple file processing support
- **Real-time Updates:** AJAX-based progress monitoring

### Security Features
- **Data Privacy:** Local processing with no external data transmission
- **Risk Assessment:** Comprehensive scoring with explainable AI
- **Threat Detection:** Pattern-based anomaly and risk indicators
- **Data Analysis:** Communication pattern and timing analysis

### Administrative Capabilities
- **Rule Management:** Create, modify, and test security rules
- **Domain Management:** Whitelist administration with manual operations
- **Session Management:** Processing history and data cleanup
- **System Monitoring:** Performance metrics and error tracking

## Deployment Specifications

### System Requirements
- **Platform:** Cross-platform (Windows, macOS, Linux)
- **Python Version:** 3.8 or higher
- **Memory:** 4GB minimum, 8GB recommended
- **Storage:** 1GB for application, additional space for data files
- **Network:** Web-based interface (0.0.0.0:5000)

### Configuration Options
- **Fast Mode:** Reduced processing for speed optimization
- **ML Parameters:** Configurable estimators and feature limits
- **Chunk Size:** Adjustable processing batch sizes (1000-2000 records)
- **Progress Reporting:** Configurable update intervals

## API Specifications

### Core Endpoints
- `POST /upload` - File upload and session creation
- `GET /api/processing-status/{session_id}` - Real-time processing updates
- `GET /api/dashboard-stats/{session_id}` - Dashboard analytics
- `GET /api/ml_insights/{session_id}` - Machine learning analysis results
- `POST /api/rules` - Security rule creation and management
- `GET/POST /api/whitelist-domains` - Domain whitelist management
- `GET /cases/{session_id}` - Case management interface

### Data Formats
- **Input:** CSV files with flexible column mapping
- **Output:** JSON responses with structured data
- **Storage:** JSON-based session persistence with gzip compression

## Service Level Characteristics

### Reliability
- **Error Handling:** Comprehensive exception management with user feedback
- **Data Integrity:** Transaction-based database operations
- **Recovery:** Session state persistence with resume capability

### Scalability
- **Processing Optimization:** Fast mode with configurable performance parameters
- **Memory Management:** Chunked processing for large files
- **Database Operations:** Optimized batch processing

### Maintainability
- **Modular Design:** Separate engines for ML, rules, and domain management
- **Configuration Management:** Environment variable based settings
- **Logging:** Comprehensive debug and audit logging

## Current Build Status

✅ **Implemented Services:**
- Complete data processing pipeline with chunked CSV processing
- Machine learning risk assessment with Isolation Forest
- Rule engine with complex AND/OR logic support
- Domain classification and manual whitelisting
- Case management system with investigation tools
- Multi-dashboard analytics suite (Main, Sender, Time, Advanced ML, Whitelist)
- Administrative interface for rules and domain management
- RESTful API endpoints for all major functions
- Performance optimization with fast mode
- Session-based file processing with progress tracking

🔧 **Operational Status:**
- Fully functional web application on Flask
- Production-ready codebase with error handling
- Real-time processing monitoring with AJAX updates
- Professional Bootstrap 5 UI/UX implementation
- SQLite database with full ORM support
- Gunicorn-based production deployment ready

📋 **Available Features:**
- CSV file upload and validation
- Automated email record processing
- AI-powered anomaly detection
- Business rule filtering
- Domain trust analysis
- Security case generation
- Interactive dashboards with Chart.js visualizations
- Administrative tools for system management
