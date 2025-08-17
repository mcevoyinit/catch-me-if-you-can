"""
Enforcement Data Oracle
Provides real-world enforcement statistics and probabilities
For hackathon: Uses mock data simulating multiple jurisdictions
"""

import json
from typing import Dict, Optional, Any
from dataclasses import dataclass
import random


@dataclass
class EnforcementData:
    """Enforcement statistics for a specific regulation"""
    jurisdiction: str
    regulation_type: str
    enforcement_probability: float
    average_penalty_usd: float
    max_penalty_usd: float
    average_audit_latency_months: int
    last_updated: str
    cases_last_year: int
    success_rate: float  # Rate of successful prosecutions


class EnforcementOracle:
    """
    Oracle that provides enforcement statistics from multiple jurisdictions
    In production, this would connect to real regulatory databases
    """
    
    def __init__(self):
        self.mock_data = self._initialize_mock_data()
        self.correlation_matrix = self._initialize_correlation_matrix()
    
    def _initialize_mock_data(self) -> Dict[str, Dict[str, EnforcementData]]:
        """
        Initialize mock enforcement data for demonstration
        Structure: {jurisdiction: {regulation_type: EnforcementData}}
        """
        return {
            "US": {
                "tax_optimization": EnforcementData(
                    jurisdiction="US",
                    regulation_type="tax_optimization",
                    enforcement_probability=0.15,
                    average_penalty_usd=500_000,
                    max_penalty_usd=10_000_000,
                    average_audit_latency_months=18,
                    last_updated="2024-01-15",
                    cases_last_year=1250,
                    success_rate=0.78
                ),
                "securities": EnforcementData(
                    jurisdiction="US",
                    regulation_type="securities",
                    enforcement_probability=0.25,
                    average_penalty_usd=2_000_000,
                    max_penalty_usd=50_000_000,
                    average_audit_latency_months=12,
                    last_updated="2024-01-15",
                    cases_last_year=450,
                    success_rate=0.82
                ),
                "data_privacy": EnforcementData(
                    jurisdiction="US",
                    regulation_type="data_privacy",
                    enforcement_probability=0.08,
                    average_penalty_usd=250_000,
                    max_penalty_usd=5_000_000,
                    average_audit_latency_months=24,
                    last_updated="2024-01-15",
                    cases_last_year=320,
                    success_rate=0.65
                )
            },
            "EU": {
                "tax_optimization": EnforcementData(
                    jurisdiction="EU",
                    regulation_type="tax_optimization",
                    enforcement_probability=0.20,
                    average_penalty_usd=750_000,
                    max_penalty_usd=15_000_000,
                    average_audit_latency_months=24,
                    last_updated="2024-01-15",
                    cases_last_year=890,
                    success_rate=0.71
                ),
                "data_privacy": EnforcementData(
                    jurisdiction="EU",
                    regulation_type="data_privacy",
                    enforcement_probability=0.30,  # GDPR is heavily enforced
                    average_penalty_usd=1_500_000,
                    max_penalty_usd=20_000_000,
                    average_audit_latency_months=9,
                    last_updated="2024-01-15",
                    cases_last_year=580,
                    success_rate=0.88
                ),
                "environmental": EnforcementData(
                    jurisdiction="EU",
                    regulation_type="environmental",
                    enforcement_probability=0.18,
                    average_penalty_usd=400_000,
                    max_penalty_usd=8_000_000,
                    average_audit_latency_months=15,
                    last_updated="2024-01-15",
                    cases_last_year=210,
                    success_rate=0.75
                )
            },
            "SG": {
                "tax_optimization": EnforcementData(
                    jurisdiction="SG",
                    regulation_type="tax_optimization",
                    enforcement_probability=0.10,
                    average_penalty_usd=300_000,
                    max_penalty_usd=5_000_000,
                    average_audit_latency_months=12,
                    last_updated="2024-01-15",
                    cases_last_year=120,
                    success_rate=0.85
                ),
                "fintech": EnforcementData(
                    jurisdiction="SG",
                    regulation_type="fintech",
                    enforcement_probability=0.05,  # Sandbox-friendly
                    average_penalty_usd=100_000,
                    max_penalty_usd=2_000_000,
                    average_audit_latency_months=6,
                    last_updated="2024-01-15",
                    cases_last_year=45,
                    success_rate=0.60
                )
            },
            "UK": {
                "tax_optimization": EnforcementData(
                    jurisdiction="UK",
                    regulation_type="tax_optimization",
                    enforcement_probability=0.18,
                    average_penalty_usd=600_000,
                    max_penalty_usd=12_000_000,
                    average_audit_latency_months=20,
                    last_updated="2024-01-15",
                    cases_last_year=780,
                    success_rate=0.74
                ),
                "financial_services": EnforcementData(
                    jurisdiction="UK",
                    regulation_type="financial_services",
                    enforcement_probability=0.22,
                    average_penalty_usd=1_800_000,
                    max_penalty_usd=30_000_000,
                    average_audit_latency_months=14,
                    last_updated="2024-01-15",
                    cases_last_year=340,
                    success_rate=0.79
                )
            }
        }
    
    def _initialize_correlation_matrix(self) -> Dict[str, Dict[str, float]]:
        """
        Initialize correlation matrix for multi-jurisdiction penalties
        1.0 = penalties stack completely
        0.0 = penalties substitute (only pay highest)
        """
        return {
            "US": {"EU": 0.7, "UK": 0.8, "SG": 0.5},
            "EU": {"US": 0.7, "UK": 0.9, "SG": 0.4},
            "UK": {"US": 0.8, "EU": 0.9, "SG": 0.6},
            "SG": {"US": 0.5, "EU": 0.4, "UK": 0.6}
        }
    
    def get_enforcement_data(self, 
                            jurisdiction: str,
                            regulation_type: str) -> Optional[EnforcementData]:
        """
        Retrieve enforcement data for specific jurisdiction and regulation
        """
        if jurisdiction in self.mock_data:
            return self.mock_data[jurisdiction].get(regulation_type)
        return None
    
    def estimate_enforcement_probability(self,
                                        jurisdiction: str,
                                        regulation_type: str,
                                        violation_severity: str = "medium") -> float:
        """
        Estimate enforcement probability with severity adjustment
        
        Args:
            jurisdiction: Target jurisdiction
            regulation_type: Type of regulation
            violation_severity: low, medium, or high
        """
        base_data = self.get_enforcement_data(jurisdiction, regulation_type)
        
        if not base_data:
            # Default conservative estimate if no data
            return 0.25
        
        # Adjust based on severity
        severity_multipliers = {
            "low": 0.5,
            "medium": 1.0,
            "high": 1.8
        }
        
        multiplier = severity_multipliers.get(violation_severity, 1.0)
        adjusted_probability = base_data.enforcement_probability * multiplier
        
        # Cap at reasonable maximum
        return min(adjusted_probability, 0.95)
    
    def get_penalty_estimate(self,
                            jurisdiction: str,
                            regulation_type: str,
                            violation_amount: float) -> Dict[str, float]:
        """
        Estimate penalty based on violation amount
        """
        base_data = self.get_enforcement_data(jurisdiction, regulation_type)
        
        if not base_data:
            # Conservative default
            return {
                "expected": violation_amount * 0.2,
                "minimum": violation_amount * 0.05,
                "maximum": violation_amount * 0.5
            }
        
        # Scale penalty based on violation amount
        scale_factor = min(violation_amount / 1_000_000, 10)  # Cap at 10x
        
        return {
            "expected": base_data.average_penalty_usd * (1 + scale_factor * 0.1),
            "minimum": base_data.average_penalty_usd * 0.2,
            "maximum": min(base_data.max_penalty_usd, violation_amount * 2)
        }
    
    def get_jurisdiction_correlation(self,
                                    jurisdiction1: str,
                                    jurisdiction2: str) -> float:
        """
        Get correlation factor between two jurisdictions
        """
        if jurisdiction1 == jurisdiction2:
            return 1.0
        
        if jurisdiction1 in self.correlation_matrix:
            return self.correlation_matrix[jurisdiction1].get(jurisdiction2, 0.5)
        
        return 0.5  # Default moderate correlation
    
    def simulate_enforcement_update(self, jurisdiction: str, regulation_type: str):
        """
        Simulate real-time enforcement data updates (for demo purposes)
        """
        if jurisdiction in self.mock_data and regulation_type in self.mock_data[jurisdiction]:
            data = self.mock_data[jurisdiction][regulation_type]
            # Add some random variation to simulate real updates
            data.enforcement_probability *= (0.95 + random.random() * 0.1)
            data.cases_last_year = int(data.cases_last_year * (0.9 + random.random() * 0.2))
            return data
        return None