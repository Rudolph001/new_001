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
        """Analyze sender behavior patterns and risk profiles"""
        try:
            # Get all email records for this session
            records = EmailRecord.query.filter_by(session_id=session_id).all()

            if not records:
                logger.warning(f"No records found for session {session_id}")
                return {}

            # Sender analysis
            sender_profiles = {}

            for record in records:
                sender = record.sender or 'Unknown'

                if sender not in sender_profiles:
                    sender_profiles[sender] = {
                        'total_emails': 0,
                        'risk_scores': [],
                        'external_communications': 0,
                        'internal_communications': 0,
                        'attachment_count': 0,
                        'high_risk_count': 0,
                        'unique_recipients': set(),
                        'time_patterns': []
                    }

                profile = sender_profiles[sender]
                profile['total_emails'] += 1

                # Risk analysis
                if record.ml_risk_score is not None:
                    profile['risk_scores'].append(record.ml_risk_score)

                if record.risk_level in ['High', 'Critical']:
                    profile['high_risk_count'] += 1

                # Communication patterns
                if record.recipients_email_domain:
                    # Check if external (non-corporate) domain
                    if any(ext in record.recipients_email_domain.lower() for ext in 
                          ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']):
                        profile['external_communications'] += 1
                    else:
                        profile['internal_communications'] += 1

                # Attachments
                if record.attachments:
                    profile['attachment_count'] += 1

                # Recipients
                if record.recipients:
                    profile['unique_recipients'].add(record.recipients)

                # Time patterns
                if record.time:
                    try:
                        if isinstance(record.time, str):
                            time_obj = datetime.fromisoformat(record.time.replace('Z', '+00:00'))
                        else:
                            time_obj = record.time
                        profile['time_patterns'].append(time_obj)
                    except:
                        pass

            # Calculate derived metrics for each sender
            for sender, profile in sender_profiles.items():
                # Risk metrics
                if profile['risk_scores']:
                    profile['risk_score_avg'] = sum(profile['risk_scores']) / len(profile['risk_scores'])
                    profile['risk_score_max'] = max(profile['risk_scores'])
                else:
                    profile['risk_score_avg'] = 0.0
                    profile['risk_score_max'] = 0.0

                # Communication ratios
                total_comms = profile['external_communications'] + profile['internal_communications']
                if total_comms > 0:
                    profile['external_ratio'] = profile['external_communications'] / total_comms
                    profile['internal_ratio'] = profile['internal_communications'] / total_comms
                else:
                    profile['external_ratio'] = 0.0
                    profile['internal_ratio'] = 0.0

                # Convert set to count
                profile['unique_recipients'] = len(profile['unique_recipients'])

                # Calculate attachment ratio
                if profile['total_emails'] > 0:
                    profile['attachment_ratio'] = profile['attachment_count'] / profile['total_emails']
                else:
                    profile['attachment_ratio'] = 0.0

            # Summary statistics
            total_senders = len(sender_profiles)
            high_risk_senders = sum(1 for p in sender_profiles.values() if p['high_risk_count'] > 0)
            external_focused_senders = sum(1 for p in sender_profiles.values() if p['external_ratio'] > 0.5)
            attachment_senders = sum(1 for p in sender_profiles.values() if p['attachment_count'] > 0)

            avg_emails_per_sender = sum(p['total_emails'] for p in sender_profiles.values()) / total_senders if total_senders > 0 else 0

            # Find top risk senders
            top_risk_senders = sorted(
                [(sender, profile) for sender, profile in sender_profiles.items()],
                key=lambda x: x[1]['risk_score_avg'],
                reverse=True
            )[:10]

            # Find communication anomalies
            top_anomalies = []
            for sender, profile in sender_profiles.items():
                if profile['total_emails'] > avg_emails_per_sender * 2:  # High volume
                    top_anomalies.append({
                        'sender': sender,
                        'anomaly_type': 'High Volume',
                        'details': f"{profile['total_emails']} emails (avg: {avg_emails_per_sender:.1f})"
                    })

                if profile['external_ratio'] > 0.8 and profile['total_emails'] > 5:  # Mostly external
                    top_anomalies.append({
                        'sender': sender,
                        'anomaly_type': 'External Focus',
                        'details': f"{profile['external_ratio']:.1%} external communications"
                    })

            return {
                'total_senders': total_senders,
                'sender_profiles': dict(list(sender_profiles.items())[:50]),  # Limit for performance
                'summary_statistics': {
                    'high_risk_senders': high_risk_senders,
                    'external_focused_senders': external_focused_senders,
                    'attachment_senders': attachment_senders,
                    'avg_emails_per_sender': avg_emails_per_sender
                },
                'top_risk_senders': top_risk_senders,
                'top_anomalies': top_anomalies
            }

        except Exception as e:
            logger.error(f"Error analyzing sender behavior: {str(e)}")
            return {'error': str(e)}

    def _detect_sender_anomalies(self, sender_data):
        """Detect anomalies in sender behavior"""
        anomalies = []

        # High suspicious domain ratio anomaly (replaces external ratio check)
        if sender_data.get('suspicious_domain_ratio', 0) > 0.3:
            anomalies.append("🔴 High suspicious/temporary domain usage")

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

        # Communication pattern flags - adjusted for all-external scenario
        if sender_data.get('suspicious_domain_ratio', 0) > 0.2:
            flags.append("⚠️ High suspicious domain usage")
        if sender_data.get('public_domain_ratio', 0) > 0.8:
            flags.append("📤 High public domain usage")

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

    def _identify_unusual_time_patterns(self, time_analysis):
        """Identify unusual temporal patterns"""
        patterns = []
        
        # High after-hours activity
        if time_analysis.get('after_hours_activity', 0) > 10:
            patterns.append(f"High after-hours activity: {time_analysis['after_hours_activity']} communications")
        
        # Weekend activity
        if time_analysis.get('weekend_activity', 0) > 5:
            patterns.append(f"Weekend activity detected: {time_analysis['weekend_activity']} communications")
        
        # Low business hours ratio
        if time_analysis.get('business_hours_ratio', 1) < 0.6:
            patterns.append("Low business hours communication ratio")
        
        return patterns

    def _analyze_communication_networks(self, session_id):
        """Analyze communication networks and relationships"""
        from collections import defaultdict
        from models import EmailRecord
        
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
        from models import EmailRecord
        
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
        from models import EmailRecord
        
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
        from models import EmailRecord
        import numpy as np
        
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
        from models import EmailRecord
        
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