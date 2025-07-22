
# Email Guardian - Visual Process Flow

## System Architecture Flow Diagram

```
                            Email Guardian - Process Flow
    
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ CSV Upload  │───▶│ Data Valid. │───▶│ Chunked Proc│───▶│ Dashboard   │
    │ Tessian     │    │ Column Map  │    │ 1000 Records│    │ Analytics   │
    │ Large Files │    │ Format Check│    │ Memory Eff. │    │ Visualize   │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
           │                                       │                   ▲
           ▼                                       ▼                   │
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Rule Engine │───▶│ Whitelist   │───▶│ ML Analysis │───▶│ Case Gen.   │───▶│ Case Mgmt   │
    │ Exclusion   │    │ Filter      │    │ Isolation   │    │ Risk Assess │    │ Review      │
    │ AND/OR Logic│    │ Domain Trust│    │ Forest      │    │ Priority    │    │ Queue       │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
           │                   │                   │                   │                   │
           ▼                   ▼                   ▼                   ▼                   ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Clear Case  │    │ Escalate    │    │ Investigate │    │ Data Store  │    │ Reporting   │
    │ Mark Safe   │    │ Generate    │    │ Deep        │    │ Session     │    │ Statistics  │
    │ Close Invest│    │ Email Alert │    │ Analysis    │    │ Audit Trail │    │ Compliance  │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

Key Features:                                      Performance:
• Handles large CSV files (chunked processing)    • Fast Mode: 60-80% speed improvement
• Machine Learning anomaly detection               • Memory Efficient: 1000 records per batch
• Rule-based filtering with whitelist support     • Scalable: SQLite → PostgreSQL ready
• Real-time analytics and case management         • Session Persistence: Resume analysis
• Multi-action workflow (Clear/Escalate/Investigate) • Background Processing: Non-blocking UI

┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                Data Flow Summary:                                      │
│ CSV Upload → Validation → Chunked Processing → Rule Engine → Whitelist Filter →       │
│ ML Analysis → Case Generation → Review → Action                                       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

## Process Flow Details

### Phase 1: Data Ingestion
- **CSV Upload**: Tessian email export files up to 500MB
- **Data Validation**: Column mapping with case-insensitive field matching
- **Chunked Processing**: 1000 records per batch for memory efficiency

### Phase 2: Analysis Pipeline
- **Rule Engine**: Exclusion and security rules with AND/OR logic
- **Whitelist Filter**: Domain trust scoring and auto-clearance
- **ML Analysis**: Isolation Forest anomaly detection with risk scoring

### Phase 3: Case Management
- **Case Generation**: Risk-based prioritization (Critical/High/Medium/Low)
- **Case Management**: Review queue with investigative tools
- **Action Workflow**: Clear/Escalate/Investigate paths

### Phase 4: Outputs
- **Dashboard**: Real-time analytics and visualizations
- **Data Storage**: Session persistence with audit trails
- **Reporting**: Statistics and compliance reporting

## Current Implementation Status

✅ **Completed Components:**
- CSV file upload and validation
- Chunked data processing (1000 records/batch)
- Rule engine with complex conditions
- Domain whitelist management
- ML risk scoring with Isolation Forest
- Case management system
- Real-time dashboard with Chart.js
- Session persistence and cleanup

✅ **Advanced Features:**
- Sender behavior analysis
- Temporal pattern detection
- Attachment risk assessment
- Advanced ML insights
- Administrative interfaces
- API endpoints for real-time updates

## Technical Specifications

**Processing Engine:**
- Chunk Size: 1000 records (configurable)
- ML Estimators: 50 (fast mode)
- Progress Updates: Every 500 records
- Memory Optimization: Batch commits

**Database Architecture:**
- SQLite for development
- PostgreSQL-ready design
- Session-based data isolation
- Automatic compression for large datasets

**Web Interface:**
- Flask with Bootstrap 5
- AJAX real-time updates
- Responsive design
- Chart.js visualizations
