"""
Risk Scoring Engine for ArbiLens Protocol
Evaluates and categorizes risk levels for regulatory strategies
"""

from typing import Dict, Tuple, Optional
from enum import Enum

from .models import Strategy, RiskProfile, Actor


class RiskZone(Enum):
    """Risk categorization zones"""
    GREEN = "GREEN"    # Low risk, high opportunity
    YELLOW = "YELLOW"  # Moderate risk, proceed with caution
    RED = "RED"        # High risk, avoid


class RiskScorer:
    """
    Advanced risk scoring engine that evaluates strategies
    based on multiple risk factors and actor profiles
    """
    
    def __init__(self):
        self.risk_weights = {
            "enforcement": 0.35,
            "reputation": 0.25,
            "financial": 0.20,
            "operational": 0.10,
            "regulatory_change": 0.10
        }
    
    def score_risk(self, 
                   strategy: Strategy,
                   risk_profile: RiskProfile,
                   actor: Optional[Actor] = None) -> Tuple[float, RiskZone, Dict[str, float]]:
        """
        Calculate comprehensive risk score
        
        Returns:
            Tuple of (risk_score, risk_zone, risk_breakdown)
        """
        
        # Calculate individual risk components
        enforcement_risk = self._score_enforcement_risk(risk_profile)
        reputation_risk = self._score_reputation_risk(risk_profile, strategy)
        financial_risk = self._score_financial_risk(strategy, risk_profile)
        operational_risk = self._score_operational_risk(strategy)
        regulatory_change_risk = self._score_regulatory_change_risk(strategy)
        
        # Apply actor-specific adjustments if provided
        if actor:
            reputation_risk *= (1 + actor.reputation_sensitivity)
            financial_risk *= (2 - actor.risk_tolerance)
        
        # Calculate weighted risk score
        risk_components = {
            "enforcement": enforcement_risk,
            "reputation": reputation_risk,
            "financial": financial_risk,
            "operational": operational_risk,
            "regulatory_change": regulatory_change_risk
        }
        
        weighted_score = sum(
            risk_components[key] * self.risk_weights[key]
            for key in risk_components
        )
        
        # Determine risk zone
        risk_zone = self._determine_risk_zone(weighted_score)
        
        return weighted_score, risk_zone, risk_components
    
    def _score_enforcement_risk(self, risk_profile: RiskProfile) -> float:
        """
        Score enforcement risk based on probability and penalty severity
        Returns: 0.0 (low risk) to 1.0 (high risk)
        """
        # Base enforcement risk
        base_risk = risk_profile.enforcement_probability
        
        # Adjust for penalty severity (normalized to 0-1 scale)
        # Assuming penalties over $10M are maximum severity
        penalty_severity = min(risk_profile.penalty_amount / 10_000_000, 1.0)
        
        # Combine probability and severity
        enforcement_risk = (base_risk * 0.6) + (penalty_severity * 0.4)
        
        # Adjust for audit latency (longer latency = lower immediate risk)
        if risk_profile.audit_latency_months > 24:
            enforcement_risk *= 0.7
        elif risk_profile.audit_latency_months > 12:
            enforcement_risk *= 0.85
        
        return min(enforcement_risk, 1.0)
    
    def _score_reputation_risk(self, 
                               risk_profile: RiskProfile,
                               strategy: Strategy) -> float:
        """
        Score reputational risk based on damage and strategy visibility
        """
        # Base reputation risk from profile
        if strategy.profit_potential > 0:
            reputation_ratio = risk_profile.reputational_damage / strategy.profit_potential
        else:
            reputation_ratio = 1.0
        
        # Cap at reasonable levels
        reputation_risk = min(reputation_ratio, 1.0)
        
        # Adjust based on strategy type (some are more visible)
        visibility_multipliers = {
            "tax_optimization": 1.2,      # High visibility
            "product_launch": 1.1,         # Moderate visibility
            "regulatory_sandbox": 0.7,     # Low visibility (expected innovation)
            "compliance_optimization": 0.8 # Low visibility
        }
        
        multiplier = visibility_multipliers.get(strategy.type.value, 1.0)
        
        return min(reputation_risk * multiplier, 1.0)
    
    def _score_financial_risk(self,
                             strategy: Strategy,
                             risk_profile: RiskProfile) -> float:
        """
        Score financial risk based on investment and potential losses
        """
        # Calculate maximum potential loss
        max_loss = (strategy.implementation_cost + 
                   risk_profile.penalty_amount + 
                   risk_profile.opportunity_cost)
        
        # Compare to profit potential
        if strategy.profit_potential > 0:
            loss_ratio = max_loss / strategy.profit_potential
        else:
            loss_ratio = float('inf')
        
        # Convert to 0-1 scale
        if loss_ratio >= 3:
            return 1.0
        elif loss_ratio >= 2:
            return 0.7
        elif loss_ratio >= 1:
            return 0.4
        else:
            return loss_ratio / 3
    
    def _score_operational_risk(self, strategy: Strategy) -> float:
        """
        Score operational complexity risk
        """
        # Base risk on time horizon (longer = more operational risk)
        if strategy.time_horizon_months >= 36:
            time_risk = 0.8
        elif strategy.time_horizon_months >= 24:
            time_risk = 0.6
        elif strategy.time_horizon_months >= 12:
            time_risk = 0.4
        else:
            time_risk = 0.2
        
        # Adjust based on jurisdiction complexity
        complex_jurisdictions = ["CN", "IN", "BR", "RU"]
        if strategy.jurisdiction in complex_jurisdictions:
            time_risk *= 1.3
        
        return min(time_risk, 1.0)
    
    def _score_regulatory_change_risk(self, strategy: Strategy) -> float:
        """
        Score risk of regulatory environment changing
        """
        # Base risk on strategy type
        change_risk_by_type = {
            "tax_optimization": 0.6,      # Tax laws change frequently
            "regulatory_sandbox": 0.3,     # Sandboxes are stable
            "product_launch": 0.5,         # Moderate change risk
            "cross_border": 0.7,           # High change risk
            "compliance_optimization": 0.4 # Moderate stability
        }
        
        base_risk = change_risk_by_type.get(strategy.type.value, 0.5)
        
        # Adjust for time horizon
        if strategy.time_horizon_months > 24:
            base_risk *= 1.5
        elif strategy.time_horizon_months > 12:
            base_risk *= 1.2
        
        return min(base_risk, 1.0)
    
    def _determine_risk_zone(self, risk_score: float) -> RiskZone:
        """
        Categorize risk score into zones
        """
        if risk_score <= 0.3:
            return RiskZone.GREEN
        elif risk_score <= 0.6:
            return RiskZone.YELLOW
        else:
            return RiskZone.RED
    
    def get_risk_mitigation_suggestions(self, 
                                       risk_components: Dict[str, float]) -> list[str]:
        """
        Provide suggestions to mitigate identified risks
        """
        suggestions = []
        
        # Find highest risk components
        sorted_risks = sorted(risk_components.items(), key=lambda x: x[1], reverse=True)
        
        for risk_type, score in sorted_risks[:3]:  # Top 3 risks
            if score > 0.5:
                if risk_type == "enforcement":
                    suggestions.append("Consider structuring operations to reduce enforcement exposure")
                elif risk_type == "reputation":
                    suggestions.append("Implement PR strategy and stakeholder communication plan")
                elif risk_type == "financial":
                    suggestions.append("Explore insurance or hedging options for financial exposure")
                elif risk_type == "operational":
                    suggestions.append("Simplify operational structure or reduce time horizon")
                elif risk_type == "regulatory_change":
                    suggestions.append("Build flexibility into strategy for regulatory adaptations")
        
        return suggestions