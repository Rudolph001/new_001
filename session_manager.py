import json
import os
import gzip
import logging
from datetime import datetime
from models import ProcessingSession, EmailRecord
from app import db

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages session data persistence and compression"""

    def __init__(self):
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)

    def save_session_data(self, session_id, data):
        """Save session data with automatic compression for large files"""
        try:
            json_data = json.dumps(data, indent=2)
            data_size = len(json_data.encode('utf-8'))

            # Compress if larger than 5MB
            if data_size > 5 * 1024 * 1024:
                filepath = os.path.join(self.data_dir, f"{session_id}.json.gz")
                with gzip.open(filepath, 'wt', encoding='utf-8') as f:
                    f.write(json_data)
                is_compressed = True
            else:
                filepath = os.path.join(self.data_dir, f"{session_id}.json")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(json_data)
                is_compressed = False

            # Update session record
            session = ProcessingSession.query.get(session_id)
            if session:
                session.data_path = filepath
                session.is_compressed = is_compressed
                db.session.commit()

            logger.info(f"Session data saved for {session_id}, compressed: {is_compressed}")
            return filepath

        except Exception as e:
            logger.error(f"Error saving session data for {session_id}: {str(e)}")
            raise

    def load_session_data(self, session_id):
        """Load session data with decompression support"""
        try:
            session = ProcessingSession.query.get(session_id)
            if not session or not session.data_path:
                return None

            if not os.path.exists(session.data_path):
                logger.warning(f"Session data file not found: {session.data_path}")
                return None

            if session.is_compressed:
                with gzip.open(session.data_path, 'rt', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                with open(session.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

            return data

        except Exception as e:
            logger.error(f"Error loading session data for {session_id}: {str(e)}")
            return None

    def get_processing_stats(self, session_id):
        """Get processing statistics for a session"""
        try:
            from models import ProcessingSession, EmailRecord

            session = ProcessingSession.query.get(session_id)
            if not session:
                return {'error': 'Session not found'}

            # Get basic session info
            session_info = {
                'status': session.status,
                'total_records': session.total_records or 0,
                'processed_records': session.processed_records or 0,
                'current_chunk': session.current_chunk or 0,
                'total_chunks': session.total_chunks or 0
            }

            # Get email record counts
            total_emails = EmailRecord.query.filter_by(session_id=session_id).count()
            analyzed_emails = EmailRecord.query.filter(
                EmailRecord.session_id == session_id,
                EmailRecord.ml_risk_score.isnot(None)
            ).count()

            return {
                'session_info': session_info,
                'total_emails': total_emails,
                'analyzed_emails': analyzed_emails,
                'analysis_complete': analyzed_emails > 0
            }

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error getting processing stats for session {session_id}: {str(e)}")
            return {
                'error': str(e),
                'session_info': {'status': 'error'},
                'total_emails': 0,
                'analyzed_emails': 0,
                'analysis_complete': False
            }

    def create_session_checkpoint(self, session_id, stage, data):
        """Create checkpoint for session recovery"""
        try:
            checkpoint_data = {
                'session_id': session_id,
                'stage': stage,
                'timestamp': datetime.utcnow().isoformat(),
                'data': data
            }

            checkpoint_path = os.path.join(self.data_dir, f"{session_id}_checkpoint_{stage}.json")
            with open(checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, indent=2)

            logger.info(f"Checkpoint created for {session_id} at stage {stage}")
            return checkpoint_path

        except Exception as e:
            logger.error(f"Error creating checkpoint for {session_id}: {str(e)}")
            raise

    def recover_from_checkpoint(self, session_id, stage):
        """Recover session from checkpoint"""
        try:
            checkpoint_path = os.path.join(self.data_dir, f"{session_id}_checkpoint_{stage}.json")
            if not os.path.exists(checkpoint_path):
                return None

            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                checkpoint_data = json.load(f)

            logger.info(f"Recovered checkpoint for {session_id} from stage {stage}")
            return checkpoint_data['data']

        except Exception as e:
            logger.error(f"Error recovering checkpoint for {session_id}: {str(e)}")
            return None

    def cleanup_session(self, session_id):
        """Clean up session files and data"""
        try:
            session = ProcessingSession.query.get(session_id)
            if session:
                # Remove data file
                if session.data_path and os.path.exists(session.data_path):
                    os.remove(session.data_path)

                # Remove checkpoints
                checkpoint_pattern = f"{session_id}_checkpoint_"
                for filename in os.listdir(self.data_dir):
                    if filename.startswith(checkpoint_pattern):
                        os.remove(os.path.join(self.data_dir, filename))

                # Remove uploaded file
                upload_pattern = f"{session_id}_"
                uploads_dir = 'uploads'
                if os.path.exists(uploads_dir):
                    for filename in os.listdir(uploads_dir):
                        if filename.startswith(upload_pattern):
                            os.remove(os.path.join(uploads_dir, filename))

                # Remove database records
                EmailRecord.query.filter_by(session_id=session_id).delete()
                db.session.delete(session)
                db.session.commit()

                logger.info(f"Session {session_id} cleaned up successfully")
                return True

        except Exception as e:
            logger.error(f"Error cleaning up session {session_id}: {str(e)}")
            return False

    def export_session(self, session_id, include_ml_data=True):
        """Export complete session data for external use"""
        try:
            session = ProcessingSession.query.get(session_id)
            if not session:
                return None

            # Get all email records
            records = EmailRecord.query.filter_by(session_id=session_id).all()

            export_data = {
                'session_info': {
                    'id': session.id,
                    'filename': session.filename,
                    'upload_time': session.upload_time.isoformat() if session.upload_time else None,
                    'total_records': session.total_records,
                    'processed_records': session.processed_records,
                    'status': session.status
                },
                'records': []
            }

            for record in records:
                record_data = {
                    'record_id': record.record_id,
                    'sender': record.sender,
                    'subject': record.subject,
                    'recipients': record.recipients,
                    'recipients_email_domain': record.recipients_email_domain,
                    'time': record.time,
                    'attachments': record.attachments,
                    'risk_level': record.risk_level,
                    'case_status': record.case_status
                }

                if include_ml_data:
                    record_data.update({
                        'ml_risk_score': record.ml_risk_score,
                        'ml_anomaly_score': record.ml_anomaly_score,
                        'ml_explanation': record.ml_explanation,
                        'rule_matches': json.loads(record.rule_matches) if record.rule_matches else []
                    })

                export_data['records'].append(record_data)

            return export_data

        except Exception as e:
            logger.error(f"Error exporting session {session_id}: {str(e)}")
            return None