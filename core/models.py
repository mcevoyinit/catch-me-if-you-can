"""
Data models for the Regulatory Navigation Protocol
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime


class Decision(Enum):
    """Decision recommendations based on EV calculation"""
    EXECUTE = "EXECUTE"  # Green zone - favorable compliant opportunity
    CAUTION = "CAUTION"  # Yellow zone - proceed with additional compliance review
    AVOID = "AVOID"      # Red zone - high compliance burden or regulatory uncertainty


class StrategyType(Enum):
    """Types of regulatory strategies"""
    TAX_OPTIMIZATION = "tax_optimization"
    MARKET_ENTRY = "market_entry"
    PRODUCT_LAUNCH = "product_launch"
    REGULATORY_SANDBOX = "regulatory_sandbox"
    CROSS_BORDER = "cross_border"
    COMPLIANCE_OPTIMIZATION = "compliance_optimization"


@dataclass
class Strategy:
    """
    Represents a proposed regulatory strategy
    """
    id: str
    type: StrategyType
    description: str
    jurisdiction: str
    profit_potential: float  # Expected profit in USD
    implementation_cost: float  # Cost to implement strategy
    time_horizon_months: int  # Expected duration
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class RiskProfile:
    """
    Compliance and risk assessment for a strategy
    """
    strategy_id: str
    enforcement_probability: float  # 0.0 to 1.0 - regulatory clarity/uncertainty
    penalty_amount: float  # Compliance costs and regulatory fees in USD
    reputational_damage: float  # Estimated reputation impact in USD
    opportunity_cost: float  # Cost of missed opportunities
    audit_latency_months: int  # Time to achieve regulatory clarity
    compliance_burden: float  # Ongoing compliance maintenance costs
    
    @property
    def total_risk(self) -> float:
        """Calculate total risk-adjusted cost"""
        enforcement_cost = self.penalty_amount * self.enforcement_probability
        return (enforcement_cost + 
                self.reputational_damage + 
                self.opportunity_cost + 
                self.compliance_burden)


@dataclass
class EVResult:
    """
    Expected Value calculation result
    """
    strategy: Strategy
    risk_profile: RiskProfile
    expected_value: float
    decision: Decision
    confidence_score: float  # 0.0 to 1.0
    breakdown: Dict[str, float]
    attestation_hash: Optional[str] = None
    
    @property
    def risk_reward_ratio(self) -> float:
        """Calculate risk/reward ratio"""
        if self.risk_profile.total_risk == 0:
            return float('inf')
        return self.strategy.profit_potential / self.risk_profile.total_risk
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response"""
        return {
            "strategy_id": self.strategy.id,
            "expected_value": self.expected_value,
            "decision": self.decision.value,
            "confidence_score": self.confidence_score,
            "risk_reward_ratio": self.risk_reward_ratio,
            "profit_potential": self.strategy.profit_potential,
            "total_risk": self.risk_profile.total_risk,
            "breakdown": self.breakdown,
            "attestation_hash": self.attestation_hash
        }


@dataclass
class Actor:
    """
    Represents an entity using the protocol
    """
    id: str
    type: str  # individual, small_business, startup, corporation
    jurisdiction: str
    risk_tolerance: float  # 0.0 (conservative) to 1.0 (aggressive)
    capital_available: float
    reputation_sensitivity: float  # 0.0 to 1.0
    
    def can_afford_strategy(self, strategy: Strategy) -> bool:
        """Check if actor can afford to implement strategy"""
        return self.capital_available >= strategy.implementation_cost