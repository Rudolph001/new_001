# Email Guardian - Process Flow (Current Implementation)

```
                            Email Guardian - Actual Process Flow

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ CSV Upload  │───▶│ Data Valid. │───▶│ Chunked Proc│───▶│ Dashboard   │
    │ File Upload │    │ Column Map  │    │ 1000 Records│    │ Real-time   │
    │ Session ID  │    │ Structure   │    │ Memory Eff. │    │ Analytics   │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
           │                                       │                   ▲
           ▼                                       ▼                   │
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Rule Engine │───▶│ Whitelist   │───▶│ ML Analysis │───▶│ Case Gen.   │
    │ Exclusion   │    │ Filter      │    │ Isolation   │    │ Risk Assess │
    │ AND/OR Logic│    │ Domain Trust│    │ Forest Algo │    │ Status Track│
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
           │                                                         │
           ▼                                                         ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Case Mgmt   │    │ Sender      │    │ Admin Panel │    │ Data Store  │
    │ Review      │    │ Analysis    │    │ System Cfg  │    │ SQLite DB   │
    │ Escalation  │    │ Behavior    │    │ Rule Mgmt   │    │ Session     │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Currently Implemented Features:

✅ **CSV Upload & Processing**
- File upload with validation
- Background processing threads
- Chunked processing (1000 records/batch)
- Progress tracking

✅ **Data Validation**
- Case-insensitive column mapping
- CSV structure validation
- Record counting

✅ **4-Stage Workflow**
1. **Rule Engine**: Exclusion rules with AND/OR logic
2. **Whitelist Filter**: Domain-based filtering
3. **ML Analysis**: Isolation Forest anomaly detection
4. **Case Generation**: Risk scoring and classification

✅ **Dashboard & Analytics**
- Real-time statistics
- Animated counters
- Risk distribution charts
- Processing status

✅ **Case Management**
- Status tracking (Active/Cleared/Escalated)
- Bulk operations
- Case details modal
- Filtering and search

✅ **Sender Analysis**
- Behavior pattern analysis
- Risk profiling
- Communication statistics

✅ **Administrative Interface**
- Rule management
- Whitelist domain management
- Session cleanup
- System statistics

## Performance Configuration:
- Fast Mode: Enabled (60-80% speed improvement)
- Chunk Size: 1000 records
- ML Records: 5000 max for analysis
- Database: SQLite with optimized queries