import numpy as np
import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from models import EmailRecord, WhitelistDomain
from app import db
import re

logger = logging.getLogger(__name__)

class AdvancedMLEngine:
    """Advanced ML analytics for deep insights and pattern recognition"""
    
    def __init__(self):
        self.business_hours = (8, 18)  # 8 AM to 6 PM
        self.business_days = [0, 1, 2, 3, 4]  # Monday to Friday
    
    def analyze_bau_patterns(self, session_id):
        """Analyze Business As Usual communication patterns"""
        try:
            # Check if we've already analyzed this session recently
            if hasattr(self, '_bau_cache') and session_id in self._bau_cache:
                return self._bau_cache[session_id]
                
            logger.info(f"Analyzing BAU patterns for session {session_id}")
            
            # Get all records for the session
            records = EmailRecord.query.filter_by(session_id=session_id).all()
            
            if not records:
                return {'error': 'No records found'}
            
            # Analyze sender-recipient domain patterns
            domain_patterns = self._analyze_domain_patterns(records)
            
            # Identify high-volume communications
            high_volume_pairs = self._identify_high_volume_communications(domain_patterns)
            
            # Generate whitelist recommendations
            whitelist_recommendations = self._generate_whitelist_recommendations(high_volume_pairs, records)
            
            # Analyze communication frequency
            frequency_analysis = self._analyze_communication_frequency(records)
            
            analysis = {
                'total_records_analyzed': len(records),
                'unique_sender_domains': len(set(self._extract_domain(r.sender) for r in records if r.sender)),
                'unique_recipient_domains': len(set(r.recipients_email_domain for r in records if r.recipients_email_domain)),
                'domain_patterns': domain_patterns,
                'high_volume_pairs': high_volume_pairs,
                'whitelist_recommendations': whitelist_recommendations,
                'frequency_analysis': frequency_analysis,
                'bau_statistics': self._calculate_bau_statistics(records)
            }
            
            # Cache the result
            if not hasattr(self, '_bau_cache'):
                self._bau_cache = {}
            self._bau_cache[session_id] = analysis
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing BAU patterns: {str(e)}")
            return {'error': str(e)}
    
    def analyze_attachment_risks(self, session_id):
        """Comprehensive attachment risk analysis"""
        try:
            # Check if we've already analyzed this session recently
            if hasattr(self, '_attachment_cache') and session_id in self._attachment_cache:
                return self._attachment_cache[session_id]
                
            logger.info(f"Analyzing attachment risks for session {session_id}")
            
            records_with_attachments = EmailRecord.query.filter(
                EmailRecord.session_id == session_id,
                EmailRecord.attachments.isnot(None),
                EmailRecord.attachments != ''
            ).all()
            
            if not records_with_attachments:
                return {'message': 'No attachments found in session'}
            
            # Risk categorization
            risk_categories = self._categorize_attachment_risks(records_with_attachments)
            
            # Malware indicators
            malware_indicators = self._detect_malware_indicators(records_with_attachments)
            
            # Data exfiltration patterns
            exfiltration_patterns = self._detect_exfiltration_patterns(records_with_attachments)
            
            # Risk scoring distribution
            risk_distribution = self._analyze_attachment_risk_distribution(records_with_attachments)
            
            analysis = {
                'total_attachments': len(records_with_attachments),
                'risk_categories': risk_categories,
                'malware_indicators': malware_indicators,
                'exfiltration_patterns': exfiltration_patterns,
                'risk_distribution': risk_distribution,
                'top_risk_attachments': self._get_top_risk_attachments(records_with_attachments),
                'recommendations': self._generate_attachment_recommendations(records_with_attachments)
            }
            
            # Cache the result
            if not hasattr(self, '_attachment_cache'):
                self._attachment_cache = {}
            self._attachment_cache[session_id] = analysis
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing attachment risks: {str(e)}")
            return {'error': str(e)}
    
    def analyze_sender_behavior(self, session_id):
        """Comprehensive sender behavior analysis with advanced metrics"""
        try:
            records = EmailRecord.query.filter_by(session_id=session_id).all()
            
            sender_analysis = defaultdict(lambda: {
                'total_emails': 0,
                'external_emails': 0,
                'internal_emails': 0,
                'high_risk_emails': 0,
                'critical_risk_emails': 0,
                'medium_risk_emails': 0,
                'low_risk_emails': 0,
                'attachments_sent': 0,
                'attachment_types': {},
                'risk_score_avg': 0,
                'risk_score_max': 0,
                'risk_score_min': 1.0,
                'risk_scores': [],
                'domains_contacted': set(),
                'domain_risk_scores': {},
                'time_patterns': [],
                'communication_frequency': defaultdict(int),
                'behavior_flags': [],
                'data_volume_score': 0,
                'leaver_emails': 0,
                'business_hours_emails': 0,
                'after_hours_emails': 0,
                'weekend_emails': 0,
                'subject_keywords': defaultdict(int),
                'justification_patterns': defaultdict(int),
                'recipient_spread': 0,
                'anomaly_indicators': [],
                'behavioral_score': 0,
                'trust_score': 0,
                'first_seen': None,
                'last_seen': None,
                'communication_velocity': 0,
                'risk_trend': 'stable'
            })
            
            for record in records:
                if not record.sender:
                    continue
                
                sender = record.sender.lower()
                analysis = sender_analysis[sender]
                
                analysis['total_emails'] += 1
                
                # Track first and last communication
                if record.time:
                    if analysis['first_seen'] is None or record.time < analysis['first_seen']:
                        analysis['first_seen'] = record.time
                    if analysis['last_seen'] is None or record.time > analysis['last_seen']:
                        analysis['last_seen'] = record.time
                    analysis['time_patterns'].append(record.time)
                    
                    # Time-based analysis
                    time_str = str(record.time).lower()
                    if any(day in time_str for day in ['saturday', 'sunday', 'sat', 'sun']):
                        analysis['weekend_emails'] += 1
                    elif any(hour in time_str for hour in ['22:', '23:', '00:', '01:', '02:', '03:', '04:', '05:', '06:', '07:']):
                        analysis['after_hours_emails'] += 1
                    else:
                        analysis['business_hours_emails'] += 1
                
                # Enhanced external communication analysis
                if record.recipients_email_domain:
                    domain = record.recipients_email_domain.lower()
                    analysis['domains_contacted'].add(domain)
                    
                    # Track risk scores per domain
                    if record.ml_risk_score:
                        if domain not in analysis['domain_risk_scores']:
                            analysis['domain_risk_scores'][domain] = []
                        analysis['domain_risk_scores'][domain].append(record.ml_risk_score)
                    
                    if self._is_external_domain(record.recipients_email_domain):
                        analysis['external_emails'] += 1
                    else:
                        analysis['internal_emails'] += 1
                
                # Enhanced risk analysis
                if record.ml_risk_score:
                    analysis['risk_scores'].append(record.ml_risk_score)
                    analysis['risk_score_avg'] += record.ml_risk_score
                    analysis['risk_score_max'] = max(analysis['risk_score_max'], record.ml_risk_score)
                    analysis['risk_score_min'] = min(analysis['risk_score_min'], record.ml_risk_score)
                    
                    # Risk level categorization
                    if record.risk_level == 'Critical' or record.ml_risk_score > 0.8:
                        analysis['critical_risk_emails'] += 1
                    elif record.risk_level == 'High' or record.ml_risk_score > 0.6:
                        analysis['high_risk_emails'] += 1
                    elif record.risk_level == 'Medium' or record.ml_risk_score > 0.4:
                        analysis['medium_risk_emails'] += 1
                    else:
                        analysis['low_risk_emails'] += 1
                
                # Enhanced attachment analysis
                if record.attachments:
                    analysis['attachments_sent'] += 1
                    
                    # Analyze attachment types
                    attachments_lower = record.attachments.lower()
                    for ext in ['.exe', '.zip', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.txt', '.csv']:
                        if ext in attachments_lower:
                            analysis['attachment_types'][ext] = analysis['attachment_types'].get(ext, 0) + 1
                    
                    # Calculate data volume score based on attachment presence
                    analysis['data_volume_score'] += 1
                
                # Leaver analysis
                if record.leaver and record.leaver.lower() in ['yes', 'true', '1']:
                    analysis['leaver_emails'] += 1
                
                # Subject keyword analysis
                if record.subject:
                    subject_words = record.subject.lower().split()
                    for word in subject_words[:5]:  # Top 5 words
                        if len(word) > 3:  # Skip short words
                            analysis['subject_keywords'][word] += 1
                
                # Justification pattern analysis
                if record.justification:
                    justification_lower = record.justification.lower()
                    for pattern in ['urgent', 'mistake', 'personal', 'business', 'legitimate', 'error', 'wrong']:
                        if pattern in justification_lower:
                            analysis['justification_patterns'][pattern] += 1
                
                # Communication frequency (daily)
                if record.time:
                    day_key = str(record.time)[:10] if len(str(record.time)) > 10 else str(record.time)
                    analysis['communication_frequency'][day_key] += 1
            
            # Post-process analysis with advanced calculations
            for sender, data in sender_analysis.items():
                if data['total_emails'] > 0:
                    # Basic ratios
                    data['risk_score_avg'] /= data['total_emails']
                    data['external_ratio'] = data['external_emails'] / data['total_emails']
                    data['internal_ratio'] = data['internal_emails'] / data['total_emails']
                    data['attachment_ratio'] = data['attachments_sent'] / data['total_emails']
                    data['high_risk_ratio'] = data['high_risk_emails'] / data['total_emails']
                    data['critical_risk_ratio'] = data['critical_risk_emails'] / data['total_emails']
                    
                    # Convert sets to lists
                    data['domains_contacted'] = list(data['domains_contacted'])
                    data['recipient_spread'] = len(data['domains_contacted'])
                    
                    # Calculate risk variance and consistency
                    if len(data['risk_scores']) > 1:
                        data['risk_variance'] = float(np.var(data['risk_scores']))
                        data['risk_consistency'] = 1 / (1 + data['risk_variance'])  # Higher = more consistent
                    else:
                        data['risk_variance'] = 0
                        data['risk_consistency'] = 1
                    
                    # Calculate communication velocity (emails per day)
                    if data['first_seen'] and data['last_seen'] and data['first_seen'] != data['last_seen']:
                        try:
                            # Simple day calculation
                            unique_days = len(set(data['communication_frequency'].keys()))
                            data['communication_velocity'] = data['total_emails'] / max(unique_days, 1)
                        except:
                            data['communication_velocity'] = data['total_emails']
                    else:
                        data['communication_velocity'] = data['total_emails']
                    
                    # Calculate behavioral score (0-100)
                    behavioral_factors = []
                    
                    # Risk factor (weight: 40%)
                    risk_factor = (1 - data['risk_score_avg']) * 40
                    behavioral_factors.append(risk_factor)
                    
                    # Communication pattern factor (weight: 30%)
                    pattern_factor = 30
                    if data['external_ratio'] > 0.8:
                        pattern_factor -= 15  # High external communication penalty
                    if data['after_hours_emails'] / data['total_emails'] > 0.3:
                        pattern_factor -= 10  # After hours penalty
                    if data['weekend_emails'] > 0:
                        pattern_factor -= 5   # Weekend penalty
                    behavioral_factors.append(max(0, pattern_factor))
                    
                    # Consistency factor (weight: 20%)
                    consistency_factor = data['risk_consistency'] * 20
                    behavioral_factors.append(consistency_factor)
                    
                    # Volume factor (weight: 10%)
                    volume_factor = min(10, data['total_emails'] / 10 * 10)  # Cap at 10
                    behavioral_factors.append(volume_factor)
                    
                    data['behavioral_score'] = sum(behavioral_factors)
                    
                    # Calculate trust score (inverse of risk indicators)
                    trust_penalties = 0
                    if data['critical_risk_emails'] > 0:
                        trust_penalties += 30
                    if data['high_risk_emails'] > 0:
                        trust_penalties += 20
                    if data['external_ratio'] > 0.9:
                        trust_penalties += 15
                    if data['leaver_emails'] > 0:
                        trust_penalties += 25
                    if data['after_hours_emails'] / data['total_emails'] > 0.5:
                        trust_penalties += 10
                    
                    data['trust_score'] = max(0, 100 - trust_penalties)
                    
                    # Calculate risk trend
                    if len(data['risk_scores']) >= 3:
                        recent_scores = data['risk_scores'][-3:]
                        older_scores = data['risk_scores'][:-3] if len(data['risk_scores']) > 3 else data['risk_scores'][:1]
                        
                        recent_avg = np.mean(recent_scores)
                        older_avg = np.mean(older_scores)
                        
                        if recent_avg > older_avg + 0.1:
                            data['risk_trend'] = 'increasing'
                        elif recent_avg < older_avg - 0.1:
                            data['risk_trend'] = 'decreasing'
                        else:
                            data['risk_trend'] = 'stable'
                    
                    # Generate anomaly indicators
                    data['anomaly_indicators'] = self._detect_sender_anomalies(data)
                    
                    # Generate enhanced behavior flags
                    data['behavior_flags'] = self._generate_enhanced_behavior_flags(data)
            
            # Sort by behavioral score (descending - higher score = better behavior)
            # But for security dashboard, we want to see risky senders first
            sorted_senders = sorted(sender_analysis.items(), 
                                  key=lambda x: (x[1]['risk_score_avg'], -x[1]['behavioral_score']), 
                                  reverse=True)
            
            return {
                'total_senders': len(sender_analysis),
                'sender_profiles': dict(sorted_senders[:100]) if sorted_senders else {},  # Top 100 for detailed analysis
                'summary_statistics': self._calculate_enhanced_sender_summary_stats(sender_analysis),
                'behavioral_insights': self._generate_behavioral_insights(sender_analysis),
                'risk_patterns': self._analyze_sender_risk_patterns(sender_analysis),
                'anomaly_summary': self._generate_anomaly_summary(sender_analysis),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error in sender behavior analysis: {str(e)}")
            return {
                'error': str(e),
                'total_senders': 0,
                'sender_profiles': {},
                'summary_statistics': {
                    'high_risk_senders': 0,
                    'external_focused_senders': 0,
                    'attachment_senders': 0,
                    'avg_emails_per_sender': 0,
                    'critical_risk_senders': 0,
                    'avg_trust_score': 0,
                    'total_anomalies': 0,
                    'multi_domain_senders': 0
                },
                'behavioral_insights': {
                    'communication_patterns': {
                        'external_heavy': 0,
                        'internal_heavy': 0
                    },
                    'risk_profiles': {
                        'consistently_risky': 0,
                        'low_risk_stable': 0
                    },
                    'trust_distribution': {
                        'high_trust': 0,
                        'medium_trust': 0,
                        'low_trust': 0
                    },
                    'temporal_patterns': {
                        'business_hours_only': 0,
                        'after_hours_active': 0,
                        'weekend_active': 0
                    }
                },
                'risk_patterns': {
                    'high_risk_external': 0,
                    'high_risk_attachments': 0,
                    'high_risk_volume': 0,
                    'high_risk_after_hours': 0,
                    'leaver_risk_correlation': 0
                },
                'anomaly_summary': {
                    'top_anomalies': {}
                }
            }

    def _detect_sender_anomalies(self, sender_data):
        """Detect anomalies in sender behavior"""
        anomalies = []
        
        # High external ratio anomaly
        if sender_data.get('external_ratio', 0) > 0.9:
            anomalies.append("🔴 Primarily external communication")
        
        # High risk variance anomaly
        if sender_data.get('risk_variance', 0) > 0.3:
            anomalies.append("⚠️ Inconsistent risk patterns")
        
        # High volume with low trust
        if sender_data.get('total_emails', 0) > 20 and sender_data.get('trust_score', 100) < 50:
            anomalies.append("🟡 High volume with low trust")
        
        # After hours activity
        if sender_data.get('after_hours_emails', 0) > 5:
            anomalies.append("🌙 Significant after-hours activity")
        
        # Multiple domain contacts
        if sender_data.get('recipient_spread', 0) > 15:
            anomalies.append("🌐 Contacts many external domains")
        
        return anomalies

    def _generate_enhanced_behavior_flags(self, sender_data):
        """Generate enhanced behavior flags for sender"""
        flags = []
        
        # Risk-based flags
        if sender_data.get('critical_risk_emails', 0) > 0:
            flags.append("🔴 Critical risk emails")
        
        if sender_data.get('high_risk_emails', 0) > 3:
            flags.append("⚠️ Multiple high-risk emails")
        
        # Communication pattern flags
        if sender_data.get('external_ratio', 0) > 0.8:
            flags.append("📤 External communication heavy")
        
        if sender_data.get('attachment_ratio', 0) > 0.5:
            flags.append("📎 Frequent attachment sender")
        
        # Temporal flags
        if sender_data.get('weekend_emails', 0) > 2:
            flags.append("📅 Weekend activity")
        
        if sender_data.get('after_hours_emails', 0) > 3:
            flags.append("🌙 After-hours activity")
        
        # Trust and behavioral flags
        if sender_data.get('trust_score', 100) < 40:
            flags.append("⚠️ Low trust score")
        
        if sender_data.get('behavioral_score', 100) < 50:
            flags.append("🔍 Concerning behavior pattern")
        
        # Leaver flag
        if sender_data.get('leaver_emails', 0) > 0:
            flags.append("🚪 Leaver communication detected")
        
        return flags

    def _calculate_enhanced_sender_summary_stats(self, sender_analysis):
        """Calculate enhanced summary statistics for sender analysis"""
        if not sender_analysis:
            return {
                'high_risk_senders': 0,
                'external_focused_senders': 0,
                'attachment_senders': 0,
                'avg_emails_per_sender': 0,
                'critical_risk_senders': 0,
                'avg_trust_score': 0,
                'total_anomalies': 0,
                'multi_domain_senders': 0
            }
        
        high_risk_senders = sum(1 for data in sender_analysis.values() 
                               if data.get('risk_score_avg', 0) > 0.7)
        
        external_focused = sum(1 for data in sender_analysis.values() 
                              if data.get('external_ratio', 0) > 0.8)
        
        attachment_senders = sum(1 for data in sender_analysis.values() 
                                if data.get('attachments_sent', 0) > 0)
        
        critical_risk_senders = sum(1 for data in sender_analysis.values() 
                                   if data.get('critical_risk_emails', 0) > 0)
        
        multi_domain_senders = sum(1 for data in sender_analysis.values() 
                                  if data.get('recipient_spread', 0) > 10)
        
        total_emails = sum(data.get('total_emails', 0) for data in sender_analysis.values())
        avg_emails_per_sender = total_emails / len(sender_analysis) if sender_analysis else 0
        
        trust_scores = [data.get('trust_score', 0) for data in sender_analysis.values() 
                       if data.get('trust_score', 0) > 0]
        avg_trust_score = sum(trust_scores) / len(trust_scores) if trust_scores else 0
        
        total_anomalies = sum(len(data.get('anomaly_indicators', [])) 
                             for data in sender_analysis.values())
        
        return {
            'high_risk_senders': high_risk_senders,
            'external_focused_senders': external_focused,
            'attachment_senders': attachment_senders,
            'avg_emails_per_sender': avg_emails_per_sender,
            'critical_risk_senders': critical_risk_senders,
            'avg_trust_score': avg_trust_score,
            'total_anomalies': total_anomalies,
            'multi_domain_senders': multi_domain_senders
        }

    def _generate_behavioral_insights(self, sender_analysis):
        """Generate behavioral insights from sender analysis"""
        if not sender_analysis:
            return {
                'communication_patterns': {'external_heavy': 0, 'internal_heavy': 0},
                'risk_profiles': {'consistently_risky': 0, 'low_risk_stable': 0},
                'trust_distribution': {'high_trust': 0, 'medium_trust': 0, 'low_trust': 0},
                'temporal_patterns': {'business_hours_only': 0, 'after_hours_active': 0, 'weekend_active': 0}
            }
        
        # Communication patterns
        external_heavy = sum(1 for data in sender_analysis.values() 
                            if data.get('external_ratio', 0) > 0.7)
        internal_heavy = sum(1 for data in sender_analysis.values() 
                            if data.get('external_ratio', 0) < 0.3)
        
        # Risk profiles
        consistently_risky = sum(1 for data in sender_analysis.values() 
                                if data.get('risk_score_avg', 0) > 0.6 and 
                                   data.get('risk_variance', 1) < 0.2)
        low_risk_stable = sum(1 for data in sender_analysis.values() 
                             if data.get('risk_score_avg', 0) < 0.3 and 
                                data.get('risk_variance', 1) < 0.2)
        
        # Trust distribution
        high_trust = sum(1 for data in sender_analysis.values() 
                        if data.get('trust_score', 0) >= 80)
        medium_trust = sum(1 for data in sender_analysis.values() 
                          if 50 <= data.get('trust_score', 0) < 80)
        low_trust = sum(1 for data in sender_analysis.values() 
                       if data.get('trust_score', 0) < 50)
        
        # Temporal patterns
        business_hours_only = sum(1 for data in sender_analysis.values() 
                                 if data.get('after_hours_emails', 0) == 0 and 
                                    data.get('weekend_emails', 0) == 0)
        after_hours_active = sum(1 for data in sender_analysis.values() 
                                if data.get('after_hours_emails', 0) > 0)
        weekend_active = sum(1 for data in sender_analysis.values() 
                            if data.get('weekend_emails', 0) > 0)
        
        return {
            'communication_patterns': {
                'external_heavy': external_heavy,
                'internal_heavy': internal_heavy
            },
            'risk_profiles': {
                'consistently_risky': consistently_risky,
                'low_risk_stable': low_risk_stable
            },
            'trust_distribution': {
                'high_trust': high_trust,
                'medium_trust': medium_trust,
                'low_trust': low_trust
            },
            'temporal_patterns': {
                'business_hours_only': business_hours_only,
                'after_hours_active': after_hours_active,
                'weekend_active': weekend_active
            }
        }

    def _analyze_sender_risk_patterns(self, sender_analysis):
        """Analyze risk patterns across senders"""
        if not sender_analysis:
            return {
                'high_risk_external': 0,
                'high_risk_attachments': 0,
                'high_risk_volume': 0,
                'high_risk_after_hours': 0,
                'leaver_risk_correlation': 0
            }
        
        high_risk_external = sum(1 for data in sender_analysis.values() 
                                if data.get('risk_score_avg', 0) > 0.7 and 
                                   data.get('external_ratio', 0) > 0.7)
        
        high_risk_attachments = sum(1 for data in sender_analysis.values() 
                                   if data.get('risk_score_avg', 0) > 0.7 and 
                                      data.get('attachments_sent', 0) > 0)
        
        high_risk_volume = sum(1 for data in sender_analysis.values() 
                              if data.get('risk_score_avg', 0) > 0.7 and 
                                 data.get('total_emails', 0) > 10)
        
        high_risk_after_hours = sum(1 for data in sender_analysis.values() 
                                   if data.get('risk_score_avg', 0) > 0.7 and 
                                      data.get('after_hours_emails', 0) > 0)
        
        leaver_risk_correlation = sum(1 for data in sender_analysis.values() 
                                     if data.get('leaver_emails', 0) > 0 and 
                                        data.get('risk_score_avg', 0) > 0.5)
        
        return {
            'high_risk_external': high_risk_external,
            'high_risk_attachments': high_risk_attachments,
            'high_risk_volume': high_risk_volume,
            'high_risk_after_hours': high_risk_after_hours,
            'leaver_risk_correlation': leaver_risk_correlation
        }

    def _generate_anomaly_summary(self, sender_analysis):
        """Generate anomaly summary from sender analysis"""
        if not sender_analysis:
            return {'top_anomalies': {}}
        
        anomaly_counts = {}
        for data in sender_analysis.values():
            for anomaly in data.get('anomaly_indicators', []):
                anomaly_counts[anomaly] = anomaly_counts.get(anomaly, 0) + 1
        
        # Get top 5 anomalies
        top_anomalies = dict(sorted(anomaly_counts.items(), 
                                   key=lambda x: x[1], reverse=True)[:5])
        
        return {
            'top_anomalies': top_anomalies
        }
            
        except Exception as e:
            logger.error(f"Error analyzing sender behavior: {str(e)}")
            return {'error': str(e)}
    
    def analyze_temporal_patterns(self, session_id):
        """Analyze temporal patterns and detect anomalies"""
        try:
            records = EmailRecord.query.filter_by(session_id=session_id).all()
            
            time_analysis = {
                'hourly_distribution': defaultdict(int),
                'daily_distribution': defaultdict(int),
                'weekend_activity': 0,
                'after_hours_activity': 0,
                'temporal_anomalies': [],
                'business_hours_ratio': 0
            }
            
            total_with_time = 0
            business_hours_count = 0
            
            for record in records:
                if not record.time:
                    continue
                
                total_with_time += 1
                
                # Basic time parsing (enhance based on actual time format)
                try:
                    # This is a simplified approach - enhance based on actual timestamp format
                    time_str = str(record.time).lower()
                    
                    # Extract hour if possible
                    hour_match = re.search(r'(\d{1,2}):(\d{2})', time_str)
                    if hour_match:
                        hour = int(hour_match.group(1))
                        time_analysis['hourly_distribution'][hour] += 1
                        
                        # Check if business hours
                        if self.business_hours[0] <= hour <= self.business_hours[1]:
                            business_hours_count += 1
                        else:
                            time_analysis['after_hours_activity'] += 1
                    
                    # Check for weekend indicators
                    if any(day in time_str for day in ['saturday', 'sunday', 'sat', 'sun']):
                        time_analysis['weekend_activity'] += 1
                        
                        # Flag as temporal anomaly if high risk
                        if record.ml_risk_score and record.ml_risk_score > 0.7:
                            time_analysis['temporal_anomalies'].append({
                                'record_id': record.record_id,
                                'sender': record.sender,
                                'time': record.time,
                                'risk_score': record.ml_risk_score,
                                'anomaly_type': 'weekend_high_risk'
                            })
                
                except Exception as e:
                    logger.debug(f"Error parsing time for record {record.record_id}: {str(e)}")
                    continue
            
            if total_with_time > 0:
                time_analysis['business_hours_ratio'] = business_hours_count / total_with_time
            
            # Identify unusual time patterns
            time_analysis['unusual_patterns'] = self._identify_unusual_time_patterns(time_analysis)
            
            return time_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing temporal patterns: {str(e)}")
            return {'error': str(e)}
    
    def get_advanced_insights(self, session_id):
        """Get comprehensive advanced ML insights"""
        try:
            insights = {
                'network_analysis': self._analyze_communication_networks(session_id),
                'justification_analysis': self._analyze_justifications(session_id),
                'pattern_clusters': self._identify_pattern_clusters(session_id),
                'risk_correlation': self._analyze_risk_correlations(session_id),
                'behavioral_anomalies': self._detect_behavioral_anomalies(session_id)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting advanced insights: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_domain_patterns(self, records):
        """Analyze sender-recipient domain communication patterns"""
        patterns = defaultdict(int)
        
        for record in records:
            sender_domain = self._extract_domain(record.sender)
            recipient_domain = record.recipients_email_domain
            
            if sender_domain and recipient_domain:
                pattern_key = f"{sender_domain} -> {recipient_domain.lower()}"
                patterns[pattern_key] += 1
        
        # Sort by frequency
        return dict(sorted(patterns.items(), key=lambda x: x[1], reverse=True))
    
    def _extract_domain(self, email):
        """Extract domain from email address"""
        if not email or '@' not in email:
            return None
        return email.split('@')[-1].lower()
    
    def _identify_high_volume_communications(self, domain_patterns):
        """Identify high-volume communication pairs"""
        # Consider patterns with more than 5 communications as high-volume
        threshold = 5
        return {pattern: count for pattern, count in domain_patterns.items() if count >= threshold}
    
    def _generate_whitelist_recommendations(self, high_volume_pairs, records):
        """Generate domain whitelist recommendations based on BAU analysis"""
        recommendations = []
        
        # Get currently whitelisted domains
        current_whitelist = set(domain.domain.lower() for domain in 
                              WhitelistDomain.query.filter_by(is_active=True).all())
        
        for pattern, count in high_volume_pairs.items():
            if ' -> ' in pattern:
                sender_domain, recipient_domain = pattern.split(' -> ')
                
                # Check if recipient domain is not already whitelisted
                if recipient_domain not in current_whitelist:
                    # Analyze risk profile for this domain
                    domain_records = [r for r in records if 
                                    r.recipients_email_domain and 
                                    r.recipients_email_domain.lower() == recipient_domain]
                    
                    if domain_records:
                        avg_risk = np.mean([r.ml_risk_score or 0 for r in domain_records])
                        high_risk_count = sum(1 for r in domain_records if r.ml_risk_score and r.ml_risk_score > 0.6)
                        
                        recommendation = {
                            'domain': recipient_domain,
                            'communication_count': count,
                            'average_risk_score': float(avg_risk),
                            'high_risk_communications': high_risk_count,
                            'recommendation_confidence': 'High' if avg_risk < 0.3 and high_risk_count == 0 else 'Medium',
                            'recommended_action': 'Add to whitelist' if avg_risk < 0.3 else 'Review before whitelisting'
                        }
                        
                        recommendations.append(recommendation)
        
        return sorted(recommendations, key=lambda x: x['communication_count'], reverse=True)
    
    def _analyze_communication_frequency(self, records):
        """Analyze communication frequency patterns"""
        sender_frequency = defaultdict(int)
        domain_frequency = defaultdict(int)
        
        for record in records:
            if record.sender:
                sender_frequency[record.sender.lower()] += 1
            if record.recipients_email_domain:
                domain_frequency[record.recipients_email_domain.lower()] += 1
        
        return {
            'top_senders': dict(sorted(sender_frequency.items(), key=lambda x: x[1], reverse=True)[:10]),
            'top_recipient_domains': dict(sorted(domain_frequency.items(), key=lambda x: x[1], reverse=True)[:10]),
            'frequency_distribution': {
                'high_frequency_senders': len([s for s, count in sender_frequency.items() if count > 10]),
                'medium_frequency_senders': len([s for s, count in sender_frequency.items() if 3 <= count <= 10]),
                'low_frequency_senders': len([s for s, count in sender_frequency.items() if count < 3])
            }
        }
    
    def _calculate_bau_statistics(self, records):
        """Calculate Business As Usual statistics"""
        total_records = len(records)
        if total_records == 0:
            return {}
        
        external_communications = sum(1 for r in records if self._is_external_domain(r.recipients_email_domain))
        with_attachments = sum(1 for r in records if r.attachments)
        high_risk = sum(1 for r in records if r.ml_risk_score and r.ml_risk_score > 0.6)
        
        return {
            'total_communications': total_records,
            'external_ratio': external_communications / total_records,
            'attachment_ratio': with_attachments / total_records,
            'high_risk_ratio': high_risk / total_records,
            'bau_score': self._calculate_bau_score(records)
        }
    
    def _calculate_bau_score(self, records):
        """Calculate overall BAU score (0-100, higher = more routine)"""
        if not records:
            return 0
        
        # Factors that indicate BAU
        total_score = 0
        factors = 0
        
        # Low average risk score
        avg_risk = np.mean([r.ml_risk_score or 0 for r in records])
        if avg_risk < 0.3:
            total_score += 25
        factors += 1
        
        # High volume of repeated patterns
        domain_patterns = self._analyze_domain_patterns(records)
        repeated_patterns = sum(1 for count in domain_patterns.values() if count > 3)
        if repeated_patterns > len(domain_patterns) * 0.3:
            total_score += 25
        factors += 1
        
        # Low proportion of high-risk communications
        high_risk_ratio = sum(1 for r in records if r.ml_risk_score and r.ml_risk_score > 0.6) / len(records)
        if high_risk_ratio < 0.1:
            total_score += 25
        factors += 1
        
        # Consistent sender patterns
        sender_counts = defaultdict(int)
        for record in records:
            if record.sender:
                sender_counts[record.sender.lower()] += 1
        
        regular_senders = sum(1 for count in sender_counts.values() if count > 2)
        if regular_senders > len(sender_counts) * 0.5:
            total_score += 25
        factors += 1
        
        return total_score / factors if factors > 0 else 0
    
    def _categorize_attachment_risks(self, records):
        """Categorize attachment risks"""
        categories = {
            'executable': 0,
            'archive': 0,
            'document': 0,
            'image': 0,
            'other': 0,
            'suspicious_naming': 0
        }
        
        for record in records:
            attachments_lower = record.attachments.lower()
            
            # Executable files
            if any(ext in attachments_lower for ext in ['.exe', '.scr', '.bat', '.cmd', '.com']):
                categories['executable'] += 1
            
            # Archive files
            elif any(ext in attachments_lower for ext in ['.zip', '.rar', '.7z', '.tar']):
                categories['archive'] += 1
            
            # Document files
            elif any(ext in attachments_lower for ext in ['.doc', '.docx', '.pdf', '.xls', '.xlsx']):
                categories['document'] += 1
            
            # Image files
            elif any(ext in attachments_lower for ext in ['.jpg', '.png', '.gif', '.bmp']):
                categories['image'] += 1
            
            else:
                categories['other'] += 1
            
            # Suspicious naming patterns
            if any(pattern in attachments_lower for pattern in ['urgent', 'confidential', 'invoice', 'payment']):
                categories['suspicious_naming'] += 1
        
        return categories
    
    def _detect_malware_indicators(self, records):
        """Detect potential malware indicators"""
        indicators = {
            'double_extensions': 0,
            'executable_files': 0,
            'suspicious_names': 0,
            'large_files': 0
        }
        
        suspicious_names = ['invoice', 'receipt', 'urgent', 'payment', 'statement', 'document']
        
        for record in records:
            attachments_lower = record.attachments.lower()
            
            # Double extensions
            if re.search(r'\.\w+\.\w+', attachments_lower):
                indicators['double_extensions'] += 1
            
            # Executable files
            if any(ext in attachments_lower for ext in ['.exe', '.scr', '.bat', '.cmd']):
                indicators['executable_files'] += 1
            
            # Suspicious names
            if any(name in attachments_lower for name in suspicious_names):
                indicators['suspicious_names'] += 1
            
            # Large files (if size information available)
            if 'large' in attachments_lower or 'mb' in attachments_lower:
                indicators['large_files'] += 1
        
        return indicators
    
    def _detect_exfiltration_patterns(self, records):
        """Detect potential data exfiltration patterns"""
        patterns = {
            'bulk_data_transfers': 0,
            'sensitive_file_types': 0,
            'external_personal_domains': 0,
            'off_hours_transfers': 0
        }
        
        sensitive_types = ['database', 'backup', 'export', 'dump', 'customer', 'employee']
        personal_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        
        for record in records:
            attachments_lower = record.attachments.lower()
            
            # Bulk transfers (multiple files or large files)
            if ',' in record.attachments or 'multiple' in attachments_lower:
                patterns['bulk_data_transfers'] += 1
            
            # Sensitive file types
            if any(stype in attachments_lower for stype in sensitive_types):
                patterns['sensitive_file_types'] += 1
            
            # External personal domains
            if record.recipients_email_domain and any(domain in record.recipients_email_domain.lower() 
                                                     for domain in personal_domains):
                patterns['external_personal_domains'] += 1
            
            # Off-hours (basic detection)
            if record.time and any(indicator in record.time.lower() 
                                 for indicator in ['night', 'weekend', 'holiday']):
                patterns['off_hours_transfers'] += 1
        
        return patterns
    
    def _analyze_attachment_risk_distribution(self, records):
        """Analyze the distribution of attachment risk scores"""
        risk_scores = []
        
        for record in records:
            # Calculate attachment-specific risk score
            risk_score = self._calculate_detailed_attachment_risk(record.attachments)
            risk_scores.append(risk_score)
        
        if not risk_scores:
            return {}
        
        return {
            'mean_risk': float(np.mean(risk_scores)),
            'median_risk': float(np.median(risk_scores)),
            'std_risk': float(np.std(risk_scores)),
            'high_risk_count': sum(1 for score in risk_scores if score > 0.7),
            'medium_risk_count': sum(1 for score in risk_scores if 0.4 <= score <= 0.7),
            'low_risk_count': sum(1 for score in risk_scores if score < 0.4)
        }
    
    def _calculate_detailed_attachment_risk(self, attachments):
        """Calculate detailed attachment risk score"""
        if not attachments:
            return 0.0
        
        attachments_lower = attachments.lower()
        risk_score = 0.0
        
        # File extension risks
        if any(ext in attachments_lower for ext in ['.exe', '.scr', '.bat']):
            risk_score += 0.8
        elif any(ext in attachments_lower for ext in ['.zip', '.rar']):
            risk_score += 0.4
        elif any(ext in attachments_lower for ext in ['.doc', '.pdf']):
            risk_score += 0.2
        
        # Naming patterns
        if any(pattern in attachments_lower for pattern in ['urgent', 'confidential', 'invoice']):
            risk_score += 0.3
        
        # Size indicators
        if any(size in attachments_lower for size in ['large', 'big', 'huge']):
            risk_score += 0.2
        
        return min(risk_score, 1.0)
    
    def _get_top_risk_attachments(self, records):
        """Get top risky attachments with details"""
        attachment_risks = []
        
        for record in records:
            risk_score = self._calculate_detailed_attachment_risk(record.attachments)
            if risk_score > 0.5:
                attachment_risks.append({
                    'record_id': record.record_id,
                    'sender': record.sender,
                    'recipient_domain': record.recipients_email_domain,
                    'attachments': record.attachments,
                    'risk_score': risk_score,
                    'overall_risk_level': record.risk_level
                })
        
        return sorted(attachment_risks, key=lambda x: x['risk_score'], reverse=True)[:20]
    
    def _generate_attachment_recommendations(self, records):
        """Generate recommendations based on attachment analysis"""
        recommendations = []
        
        # Count high-risk attachments
        high_risk_count = sum(1 for r in records 
                            if self._calculate_detailed_attachment_risk(r.attachments) > 0.7)
        
        if high_risk_count > 0:
            recommendations.append(f"Immediately review {high_risk_count} high-risk attachments")
        
        # Executable file recommendations
        exe_count = sum(1 for r in records 
                      if any(ext in r.attachments.lower() for ext in ['.exe', '.scr', '.bat']))
        if exe_count > 0:
            recommendations.append(f"Block or quarantine {exe_count} executable files")
        
        # Archive file recommendations
        archive_count = sum(1 for r in records 
                          if any(ext in r.attachments.lower() for ext in ['.zip', '.rar']))
        if archive_count > 5:
            recommendations.append(f"Implement additional scanning for {archive_count} archive files")
        
        return recommendations
    
    def _is_external_domain(self, domain):
        """Check if domain is external (not corporate)"""
        if not domain:
            return False
        
        domain_lower = domain.lower()
        # This would typically check against known corporate domains
        corporate_indicators = ['company.com', 'corp.com', 'internal']
        return not any(indicator in domain_lower for indicator in corporate_indicators)
    
    def _generate_behavior_flags(self, sender_data):
        """Generate behavior flags for sender analysis"""
        flags = []
        
        if sender_data['external_ratio'] > 0.8:
            flags.append('High external communication')
        
        if sender_data['risk_score_avg'] > 0.6:
            flags.append('High average risk score')
        
        if sender_data['high_risk_emails'] > 0:
            flags.append(f'{sender_data["high_risk_emails"]} high-risk communications')
        
        if len(sender_data['domains_contacted']) > 10:
            flags.append('Contacts many external domains')
        
        return flags
    
    def _generate_enhanced_behavior_flags(self, sender_data):
        """Generate enhanced behavior flags with detailed analysis"""
        flags = []
        
        # Risk-based flags
        if sender_data['critical_risk_emails'] > 0:
            flags.append(f'🔴 {sender_data["critical_risk_emails"]} critical risk communications')
        
        if sender_data['risk_score_avg'] > 0.7:
            flags.append(f'⚠️ High average risk score ({sender_data["risk_score_avg"]:.3f})')
        elif sender_data['risk_score_avg'] > 0.5:
            flags.append(f'🟡 Medium average risk score ({sender_data["risk_score_avg"]:.3f})')
        
        # Communication pattern flags
        if sender_data['external_ratio'] > 0.9:
            flags.append(f'🌐 Extreme external focus ({sender_data["external_ratio"]:.1%})')
        elif sender_data['external_ratio'] > 0.7:
            flags.append(f'📤 High external communication ({sender_data["external_ratio"]:.1%})')
        
        # Volume and spread flags
        if sender_data['recipient_spread'] > 20:
            flags.append(f'📊 Wide recipient spread ({sender_data["recipient_spread"]} domains)')
        elif sender_data['recipient_spread'] > 10:
            flags.append(f'📈 Multiple domains contacted ({sender_data["recipient_spread"]})')
        
        # Temporal pattern flags
        if sender_data['after_hours_emails'] > 0:
            after_hours_ratio = sender_data['after_hours_emails'] / sender_data['total_emails']
            if after_hours_ratio > 0.5:
                flags.append(f'🌙 Primarily after-hours activity ({after_hours_ratio:.1%})')
            elif after_hours_ratio > 0.2:
                flags.append(f'🕐 Significant after-hours activity ({after_hours_ratio:.1%})')
        
        if sender_data['weekend_emails'] > 0:
            weekend_ratio = sender_data['weekend_emails'] / sender_data['total_emails']
            if weekend_ratio > 0.3:
                flags.append(f'📅 High weekend activity ({weekend_ratio:.1%})')
            elif weekend_ratio > 0.1:
                flags.append(f'🗓️ Some weekend activity ({weekend_ratio:.1%})')
        
        # Attachment flags
        if sender_data['attachment_ratio'] > 0.8:
            flags.append(f'📎 High attachment usage ({sender_data["attachment_ratio"]:.1%})')
        
        # Velocity flags
        if sender_data['communication_velocity'] > 10:
            flags.append(f'⚡ High communication velocity ({sender_data["communication_velocity"]:.1f} emails/day)')
        elif sender_data['communication_velocity'] > 5:
            flags.append(f'📨 Moderate communication velocity ({sender_data["communication_velocity"]:.1f} emails/day)')
        
        # Trust score flags
        if sender_data['trust_score'] < 30:
            flags.append(f'❌ Low trust score ({sender_data["trust_score"]:.0f}/100)')
        elif sender_data['trust_score'] < 60:
            flags.append(f'⚠️ Medium trust score ({sender_data["trust_score"]:.0f}/100)')
        else:
            flags.append(f'✅ High trust score ({sender_data["trust_score"]:.0f}/100)')
        
        # Leaver flags
        if sender_data['leaver_emails'] > 0:
            flags.append(f'🚨 Leaver status detected ({sender_data["leaver_emails"]} emails)')
        
        # Risk trend flags
        if sender_data['risk_trend'] == 'increasing':
            flags.append('📈 Risk trend: Increasing')
        elif sender_data['risk_trend'] == 'decreasing':
            flags.append('📉 Risk trend: Decreasing')
        
        return flags
    
    def _detect_sender_anomalies(self, sender_data):
        """Detect anomalous patterns in sender behavior"""
        anomalies = []
        
        # Risk-based anomalies
        if sender_data['risk_variance'] > 0.5:
            anomalies.append('Highly inconsistent risk scores')
        
        # Volume anomalies
        if sender_data['total_emails'] > 100:
            anomalies.append('Unusually high email volume')
        
        # Temporal anomalies
        if sender_data['weekend_emails'] / sender_data['total_emails'] > 0.4:
            anomalies.append('Excessive weekend activity')
        
        if sender_data['after_hours_emails'] / sender_data['total_emails'] > 0.6:
            anomalies.append('Primarily after-hours communication')
        
        # Communication pattern anomalies
        if sender_data['external_ratio'] > 0.95:
            anomalies.append('Almost exclusively external communication')
        
        if sender_data['recipient_spread'] > 50:
            anomalies.append('Contacts unusually many domains')
        
        # Attachment anomalies
        if sender_data['attachment_ratio'] > 0.9:
            anomalies.append('Almost all emails contain attachments')
        
        return anomalies
    
    def _calculate_enhanced_sender_summary_stats(self, sender_analysis):
        """Calculate enhanced summary statistics for sender analysis"""
        if not sender_analysis:
            return {}
        
        all_senders = list(sender_analysis.values())
        
        return {
            'total_senders': len(all_senders),
            'avg_emails_per_sender': float(np.mean([s['total_emails'] for s in all_senders])),
            'median_emails_per_sender': float(np.median([s['total_emails'] for s in all_senders])),
            'high_risk_senders': len([s for s in all_senders if s['risk_score_avg'] > 0.6]),
            'critical_risk_senders': len([s for s in all_senders if s['critical_risk_emails'] > 0]),
            'external_focused_senders': len([s for s in all_senders if s['external_ratio'] > 0.7]),
            'attachment_senders': len([s for s in all_senders if s['attachments_sent'] > 0]),
            'high_volume_senders': len([s for s in all_senders if s['total_emails'] > 20]),
            'low_trust_senders': len([s for s in all_senders if s['trust_score'] < 50]),
            'after_hours_senders': len([s for s in all_senders if s['after_hours_emails'] > 0]),
            'weekend_senders': len([s for s in all_senders if s['weekend_emails'] > 0]),
            'multi_domain_senders': len([s for s in all_senders if s['recipient_spread'] > 5]),
            'leaver_senders': len([s for s in all_senders if s['leaver_emails'] > 0]),
            'avg_behavioral_score': float(np.mean([s['behavioral_score'] for s in all_senders])),
            'avg_trust_score': float(np.mean([s['trust_score'] for s in all_senders])),
            'avg_risk_variance': float(np.mean([s['risk_variance'] for s in all_senders])),
            'total_anomalies': sum(len(s['anomaly_indicators']) for s in all_senders)
        }
    
    def _generate_behavioral_insights(self, sender_analysis):
        """Generate behavioral insights from sender analysis"""
        if not sender_analysis:
            return {}
        
        all_senders = list(sender_analysis.values())
        
        insights = {
            'communication_patterns': {
                'external_heavy': len([s for s in all_senders if s['external_ratio'] > 0.8]),
                'internal_heavy': len([s for s in all_senders if s['internal_ratio'] > 0.8]),
                'balanced': len([s for s in all_senders if 0.3 <= s['external_ratio'] <= 0.7])
            },
            'risk_profiles': {
                'consistently_risky': len([s for s in all_senders if s['risk_score_avg'] > 0.6 and s['risk_variance'] < 0.2]),
                'inconsistent_risk': len([s for s in all_senders if s['risk_variance'] > 0.4]),
                'low_risk_stable': len([s for s in all_senders if s['risk_score_avg'] < 0.3 and s['risk_variance'] < 0.1])
            },
            'temporal_patterns': {
                'business_hours_only': len([s for s in all_senders if s['after_hours_emails'] == 0 and s['weekend_emails'] == 0]),
                'after_hours_active': len([s for s in all_senders if s['after_hours_emails'] > 0]),
                'weekend_active': len([s for s in all_senders if s['weekend_emails'] > 0])
            },
            'trust_distribution': {
                'high_trust': len([s for s in all_senders if s['trust_score'] >= 80]),
                'medium_trust': len([s for s in all_senders if 50 <= s['trust_score'] < 80]),
                'low_trust': len([s for s in all_senders if s['trust_score'] < 50])
            }
        }
        
        return insights
    
    def _analyze_sender_risk_patterns(self, sender_analysis):
        """Analyze risk patterns across senders"""
        if not sender_analysis:
            return {}
        
        all_senders = list(sender_analysis.values())
        
        # Identify common risk patterns
        patterns = {
            'high_risk_external': len([s for s in all_senders if s['risk_score_avg'] > 0.6 and s['external_ratio'] > 0.7]),
            'high_risk_attachments': len([s for s in all_senders if s['risk_score_avg'] > 0.6 and s['attachment_ratio'] > 0.5]),
            'high_risk_volume': len([s for s in all_senders if s['risk_score_avg'] > 0.6 and s['total_emails'] > 20]),
            'high_risk_after_hours': len([s for s in all_senders if s['risk_score_avg'] > 0.6 and s['after_hours_emails'] > 0]),
            'leaver_risk_correlation': len([s for s in all_senders if s['leaver_emails'] > 0 and s['risk_score_avg'] > 0.5])
        }
        
        return patterns
    
    def _summarize_sender_anomalies(self, sender_analysis):
        """Summarize anomalies found across all senders"""
        if not sender_analysis:
            return {}
        
        all_anomalies = []
        for sender_data in sender_analysis.values():
            all_anomalies.extend(sender_data['anomaly_indicators'])
        
        # Count anomaly types
        anomaly_counts = defaultdict(int)
        for anomaly in all_anomalies:
            anomaly_counts[anomaly] += 1
        
        return {
            'total_anomalies': len(all_anomalies),
            'unique_anomaly_types': len(anomaly_counts),
            'top_anomalies': dict(sorted(anomaly_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            'senders_with_anomalies': len([s for s in sender_analysis.values() if s['anomaly_indicators']])
        }
    
    def _calculate_sender_summary_stats(self, sender_analysis):
        """Calculate summary statistics for sender analysis"""
        if not sender_analysis:
            return {}
        
        all_senders = list(sender_analysis.values())
        
        return {
            'total_senders': len(all_senders),
            'avg_emails_per_sender': np.mean([s['total_emails'] for s in all_senders]),
            'high_risk_senders': len([s for s in all_senders if s['risk_score_avg'] > 0.6]),
            'external_focused_senders': len([s for s in all_senders if s['external_ratio'] > 0.5]),
            'attachment_senders': len([s for s in all_senders if s['attachments_sent'] > 0])
        }
    
    def _identify_unusual_time_patterns(self, time_analysis):
        """Identify unusual temporal patterns"""
        patterns = []
        
        # High after-hours activity
        if time_analysis['after_hours_activity'] > 10:
            patterns.append(f"High after-hours activity: {time_analysis['after_hours_activity']} communications")
        
        # Weekend activity
        if time_analysis['weekend_activity'] > 5:
            patterns.append(f"Weekend activity detected: {time_analysis['weekend_activity']} communications")
        
        # Low business hours ratio
        if time_analysis['business_hours_ratio'] < 0.6:
            patterns.append("Low business hours communication ratio")
        
        return patterns
    
    def _analyze_communication_networks(self, session_id):
        """Analyze communication networks and relationships"""
        # Simplified network analysis
        records = EmailRecord.query.filter_by(session_id=session_id).all()
        
        sender_network = defaultdict(set)
        for record in records:
            if record.sender and record.recipients_email_domain:
                sender_network[record.sender].add(record.recipients_email_domain)
        
        network_stats = {
            'total_nodes': len(sender_network),
            'highly_connected_senders': len([s for s, domains in sender_network.items() if len(domains) > 5]),
            'network_density': sum(len(domains) for domains in sender_network.values()) / len(sender_network) if sender_network else 0
        }
        
        return network_stats
    
    def _analyze_justifications(self, session_id):
        """Analyze email justifications for sentiment and patterns"""
        records = EmailRecord.query.filter(
            EmailRecord.session_id == session_id,
            EmailRecord.justification.isnot(None),
            EmailRecord.justification != ''
        ).all()
        
        if not records:
            return {'message': 'No justifications found'}
        
        # Simple sentiment analysis
        positive_terms = ['appropriate', 'legitimate', 'business', 'approved', 'authorized']
        negative_terms = ['mistake', 'error', 'unauthorized', 'personal', 'wrong']
        
        sentiment_scores = []
        for record in records:
            justification_lower = record.justification.lower()
            positive_count = sum(1 for term in positive_terms if term in justification_lower)
            negative_count = sum(1 for term in negative_terms if term in justification_lower)
            
            if positive_count > negative_count:
                sentiment_scores.append(1)  # Positive
            elif negative_count > positive_count:
                sentiment_scores.append(-1)  # Negative
            else:
                sentiment_scores.append(0)  # Neutral
        
        return {
            'total_justifications': len(records),
            'positive_sentiment': sentiment_scores.count(1),
            'negative_sentiment': sentiment_scores.count(-1),
            'neutral_sentiment': sentiment_scores.count(0)
        }
    
    def _identify_pattern_clusters(self, session_id):
        """Identify clusters of similar communication patterns"""
        # Simplified clustering based on communication characteristics
        records = EmailRecord.query.filter_by(session_id=session_id).all()
        
        clusters = {
            'high_risk_cluster': len([r for r in records if r.ml_risk_score and r.ml_risk_score > 0.7]),
            'external_communication_cluster': len([r for r in records if self._is_external_domain(r.recipients_email_domain)]),
            'attachment_cluster': len([r for r in records if r.attachments]),
            'leaver_cluster': len([r for r in records if r.leaver and r.leaver.lower() in ['yes', 'true']])
        }
        
        return clusters
    
    def _analyze_risk_correlations(self, session_id):
        """Analyze correlations between different risk factors"""
        records = EmailRecord.query.filter_by(session_id=session_id).all()
        
        correlations = {
            'attachment_risk_correlation': 0,
            'external_domain_risk_correlation': 0,
            'leaver_risk_correlation': 0
        }
        
        # Calculate simple correlations
        records_with_risk = [r for r in records if r.ml_risk_score is not None]
        
        if records_with_risk:
            # Attachment correlation
            attachment_risks = [1 if r.attachments else 0 for r in records_with_risk]
            risk_scores = [r.ml_risk_score for r in records_with_risk]
            
            if len(set(attachment_risks)) > 1:
                correlations['attachment_risk_correlation'] = np.corrcoef(attachment_risks, risk_scores)[0, 1]
        
        return correlations
    
    def _detect_behavioral_anomalies(self, session_id):
        """Detect behavioral anomalies at the session level"""
        records = EmailRecord.query.filter_by(session_id=session_id).all()
        
        anomalies = []
        
        # Unusual volume of high-risk communications
        high_risk_count = sum(1 for r in records if r.ml_risk_score and r.ml_risk_score > 0.7)
        if high_risk_count > len(records) * 0.2:
            anomalies.append(f"Unusually high proportion of risky communications: {high_risk_count}/{len(records)}")
        
        # Unusual external communication patterns
        external_count = sum(1 for r in records if self._is_external_domain(r.recipients_email_domain))
        if external_count > len(records) * 0.8:
            anomalies.append(f"Unusually high external communication: {external_count}/{len(records)}")
        
        return anomalies
