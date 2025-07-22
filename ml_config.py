# ML Risk Scoring Configuration
# This file contains all configurable ML risk scoring parameters

class MLRiskConfig:
    """Configuration class for ML risk scoring parameters"""
    
    # Risk Level Thresholds (0.0 - 1.0)
    RISK_THRESHOLDS = {
        'critical': 0.8,
        'high': 0.6,
        'medium': 0.4,
        'low': 0.0
    }
    
    # Rule-based Factor Weights (max scores for each factor)
    RULE_BASED_FACTORS = {
        'leaver_status': 0.3,          # Employee leaving organization
        'external_domain': 0.2,        # Public email domains (Gmail, Yahoo, etc.)
        'attachment_risk': 0.3,        # File type and suspicious patterns
        'wordlist_matches': 0.2,       # Suspicious keywords in subject/attachment
        'time_based_risk': 0.1,        # Weekend/after-hours activity
        'justification_analysis': 0.1  # Suspicious terms in explanations
    }
    
    # Attachment Risk Scoring
    HIGH_RISK_EXTENSIONS = [
        '.exe', '.scr', '.bat', '.cmd', '.com', '.pif', 
        '.vbs', '.js', '.jar', '.msi', '.dll', '.sys'
    ]
    HIGH_RISK_SCORE = 0.8
    
    MEDIUM_RISK_EXTENSIONS = [
        '.zip', '.rar', '.7z', '.tar', '.gz',
        '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.pdf', '.rtf', '.odt', '.ods', '.odp'
    ]
    MEDIUM_RISK_SCORE = 0.3
    
    # Suspicious attachment patterns
    SUSPICIOUS_PATTERNS = [
        'double extension', 'hidden', 'confidential', 'urgent', 
        'invoice', 'payment', 'refund', 'winner', 'prize'
    ]
    PATTERN_SCORE = 0.2
    
    # External Domain Patterns (scored as risky)
    PUBLIC_DOMAINS = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'aol.com', 'icloud.com', 'live.com', 'msn.com',
        'ymail.com', 'mail.com', 'protonmail.com'
    ]
    
    # Time-based Risk Patterns
    RISKY_TIME_PATTERNS = [
        'weekend', 'saturday', 'sunday',
        '22:', '23:', '00:', '01:', '02:', '03:', '04:', '05:'  # After hours
    ]
    
    # Suspicious Justification Terms
    SUSPICIOUS_JUSTIFICATION_TERMS = [
        'urgent', 'confidential', 'personal', 'mistake', 'wrong',
        'emergency', 'immediate', 'asap', 'critical', 'secret',
        'private', 'sensitive', 'restricted', 'classified'
    ]
    
    # Wordlist Categories and Risk Scores
    WORDLIST_CATEGORIES = {
        'financial': {
            'keywords': ['bank', 'account', 'credit', 'payment', 'invoice', 'money', 'salary', 'bonus'],
            'risk_score': 0.15
        },
        'sensitive_data': {
            'keywords': ['password', 'ssn', 'social security', 'confidential', 'proprietary', 'trade secret'],
            'risk_score': 0.2
        },
        'personal_info': {
            'keywords': ['address', 'phone', 'personal', 'family', 'medical', 'health'],
            'risk_score': 0.1
        },
        'business_critical': {
            'keywords': ['merger', 'acquisition', 'layoff', 'restructure', 'strategic', 'competition'],
            'risk_score': 0.18
        }
    }
    
    # Algorithm Weights
    ANOMALY_DETECTION_WEIGHT = 0.4  # 40%
    RULE_BASED_WEIGHT = 0.6         # 60%
    
    @classmethod
    def get_config_dict(cls):
        """Return configuration as dictionary for API/UI display"""
        return {
            'risk_thresholds': cls.RISK_THRESHOLDS,
            'rule_based_factors': cls.RULE_BASED_FACTORS,
            'attachment_scoring': {
                'high_risk_extensions': cls.HIGH_RISK_EXTENSIONS,
                'high_risk_score': cls.HIGH_RISK_SCORE,
                'medium_risk_extensions': cls.MEDIUM_RISK_EXTENSIONS,
                'medium_risk_score': cls.MEDIUM_RISK_SCORE,
                'suspicious_patterns': cls.SUSPICIOUS_PATTERNS,
                'pattern_score': cls.PATTERN_SCORE
            },
            'public_domains': cls.PUBLIC_DOMAINS,
            'time_patterns': cls.RISKY_TIME_PATTERNS,
            'justification_terms': cls.SUSPICIOUS_JUSTIFICATION_TERMS,
            'wordlist_categories': cls.WORDLIST_CATEGORIES,
            'algorithm_weights': {
                'anomaly_detection': cls.ANOMALY_DETECTION_WEIGHT,
                'rule_based': cls.RULE_BASED_WEIGHT
            }
        }
    
    @classmethod
    def update_config(cls, config_updates):
        """Update configuration values (for future admin interface)"""
        for key, value in config_updates.items():
            if hasattr(cls, key.upper()):
                setattr(cls, key.upper(), value)