
# Email Guardian - Step-by-Step Rebuild Guide

This guide provides clear, sequential steps to rebuild Email Guardian from scratch. Each step should be requested separately from Replit Assistant to ensure proper implementation and testing.

## Prerequisites & Important Notes

- **Local Development**: App will run locally on Replit
- **External Email Focus**: All imported emails are external communications (no internal emails)
- **CSV Fields**: Use existing field structure from current implementation
- **Database**: SQLite for simplicity and local development

## Phase 1: Foundation Setup

### Step 1: Basic Flask Application Structure
**Request to Replit Assistant:**
```
Create a basic Flask web application with the following structure:
- main.py as the entry point
- app.py for Flask app configuration
- A simple index page template
- Basic CSS framework (Bootstrap 5)
- SQLite database configuration using SQLAlchemy
- Basic logging setup
- Port 5000 configuration for local development
```

### Step 2: Database Models Setup
**Request to Replit Assistant:**
```
Create SQLAlchemy database models for Email Guardian with these tables:
1. ProcessingSession - to track CSV upload sessions
2. EmailRecord - to store individual email records with these fields:
   - session_id, record_id, time, sender, subject, attachments
   - recipients, recipients_email_domain, leaver, termination_date
   - wordlist_attachment, wordlist_subject, bunit, department
   - status, user_response, final_outcome, justification, policy_name
   - ML fields: ml_risk_score, risk_level, ml_explanation
   - Processing flags: excluded_by_rule, whitelisted, rule_matches
3. Rule - for security and exclusion rules
4. WhitelistDomain - for trusted domains
5. AttachmentKeyword - for ML keyword analysis

Include database initialization and migration functions.
```

## Phase 2: Core Data Processing

### Step 3: CSV Upload and Processing
**Request to Replit Assistant:**
```
Create a CSV file upload system that:
1. Accepts CSV files through a web form
2. Validates CSV structure against expected columns (case-insensitive matching)
3. Processes files in chunks (1000 records per chunk) for performance
4. Creates unique session IDs for each upload
5. Stores processed records in EmailRecord table
6. Shows upload progress to user
7. Handles errors gracefully and logs them
8. Maps these CSV columns: _time, sender, subject, attachments, recipients, recipients_email_domain, leaver, termination_date, wordlist_attachment, wordlist_subject, bunit, department, status, user_response, final_outcome, justification, policy_name
```

### Step 4: Session Management Dashboard
**Request to Replit Assistant:**
```
Create a dashboard system that:
1. Shows list of uploaded sessions with basic statistics
2. Displays session status (uploading, processing, completed, error)
3. Shows progress bars for active processing
4. Provides links to detailed analysis for completed sessions
5. Includes session management (view, delete sessions)
6. Real-time updates using JavaScript for processing status
```

## Phase 3: Business Logic Implementation

### Step 5: Rule Engine Foundation
**Request to Replit Assistant:**
```
Create a flexible rule engine system that:
1. Supports two types of rules: "exclusion" and "security"
2. Uses JSON-based conditions with AND/OR logic support
3. Supports field matching, regex patterns, keyword detection
4. Has a web interface for creating/editing rules
5. Can be applied to email records in batch
6. Logs rule matches and exclusions
7. Provides rule testing functionality
8. Include sample rules for common patterns
```

### Step 6: Domain Management System
**Request to Replit Assistant:**
```
Create a domain whitelist management system that:
1. Manages trusted domains with categories (Corporate, Public, Suspicious, etc.)
2. Supports domain pattern matching (exact, subdomain, wildcard)
3. Applies whitelist filtering to email records
4. Web interface for adding/removing domains
5. Bulk import functionality for domain lists
6. Analytics on domain usage and trust scores
7. Remember: ALL emails are external, so focus on domain risk classification rather than internal/external distinction
```

## Phase 4: Machine Learning & Risk Analysis

### Step 7: Basic ML Risk Scoring
**Request to Replit Assistant:**
```
Create a machine learning risk scoring system that:
1. Analyzes email records for risk factors optimized for external-only emails
2. Uses these risk factors:
   - Leaver status (high risk for data exfiltration)
   - Suspicious/temporary domains (disposable email services)
   - Public domains (Gmail, Yahoo - low risk since common for external)
   - Business domains (legitimate companies - lowest risk)
   - Attachment analysis (file types, suspicious patterns)
   - Keyword matching (sensitive terms)
   - Time-based patterns (weekend/after-hours activity)
3. Assigns risk levels: Critical, High, Medium, Low
4. Provides explanations for risk scores
5. Uses scikit-learn for anomaly detection
6. Optimized for performance with large datasets
```

### Step 8: Advanced Analytics Dashboard
**Request to Replit Assistant:**
```
Create comprehensive analytics dashboards that show:
1. Risk distribution charts and statistics
2. Sender behavior analysis (volume, patterns, anomalies)
3. Domain communication patterns and trends
4. Temporal analysis (time-based patterns)
5. Attachment risk intelligence
6. Case management statistics (active, cleared, escalated)
7. Interactive charts using Chart.js
8. Export functionality for reports
9. Real-time data updates
```

## Phase 5: Case Management & Workflow

### Step 9: Case Management System
**Request to Replit Assistant:**
```
Create a case management system for security analysts that:
1. Shows active cases (non-whitelisted, non-excluded emails)
2. Provides filtering by risk level, status, sender, domain
3. Allows case status updates (Active, Cleared, Escalated)
4. Supports bulk operations on multiple cases
5. Case details view with full email information
6. Escalation workflow with email generation
7. Notes and comments on cases
8. Search functionality across all fields
9. Pagination for large datasets
```

### Step 10: Reporting & Export System
**Request to Replit Assistant:**
```
Create comprehensive reporting system that:
1. Generates executive summary reports
2. Detailed case analysis reports
3. Monthly/quarterly trend reports
4. Export to CSV/Excel formats
5. Scheduled report generation
6. Email delivery of reports
7. Custom report builder
8. Performance metrics and KPIs
9. Compliance reporting templates
```

## Phase 6: Advanced Features

### Step 11: Network Analysis & Visualization
**Request to Replit Assistant:**
```
Create network analysis features that:
1. Visualizes communication networks (sender -> domain relationships)
2. Interactive network graphs using D3.js or similar
3. Identifies unusual communication patterns
4. Supports multiple relationship types (sender-recipient, domain-domain)
5. Network metrics and statistics
6. Anomaly detection in communication patterns
7. Export network data for external analysis
```

### Step 12: Administration & Configuration
**Request to Replit Assistant:**
```
Create administration interface that:
1. System performance monitoring
2. User management (if multi-user needed later)
3. Configuration management for ML parameters
4. Database optimization tools
5. Backup and restore functionality
6. Audit logging for all actions
7. System health checks
8. Performance tuning options
9. Security configuration
```

## Phase 7: Polish & Production Readiness

### Step 13: User Experience Improvements
**Request to Replit Assistant:**
```
Enhance user experience with:
1. Responsive design for mobile/tablet
2. Loading indicators and progress bars
3. Error handling and user-friendly messages
4. Keyboard shortcuts for power users
5. Context help and tooltips
6. Data table enhancements (sorting, filtering, search)
7. Theme support (light/dark mode)
8. Accessibility improvements
```

### Step 14: Performance Optimization
**Request to Replit Assistant:**
```
Optimize application performance:
1. Database indexing for common queries
2. Caching for frequently accessed data
3. Pagination for large datasets
4. Background processing for heavy operations
5. Memory usage optimization
6. Query optimization
7. Asset compression and minification
8. API response optimization
```

### Step 15: Testing & Documentation
**Request to Replit Assistant:**
```
Add testing and documentation:
1. Unit tests for core functions
2. Integration tests for workflows
3. API documentation
4. User manual and help system
5. Installation and setup guide
6. Troubleshooting guide
7. Code documentation
8. Performance benchmarks
```

## Implementation Tips

1. **Test Each Step**: After each phase, test thoroughly before moving to the next
2. **Sample Data**: Keep your existing CSV file for testing throughout development
3. **Incremental**: Each step builds on the previous ones
4. **Backup**: Regular backups of your database during development
5. **Performance**: Monitor performance with your 9000-record dataset

## Key Reminders for Each Request

When making requests to Replit Assistant, always mention:
- "This is for Email Guardian running locally on Replit"
- "All imported emails are external communications only"
- "Use SQLite database"
- "Optimize for 9000+ record datasets"
- "Include error handling and logging"
- "Use Bootstrap 5 for styling"
- "Port 5000 for local development"

This guide ensures you build a robust, scalable Email Guardian step by step!
