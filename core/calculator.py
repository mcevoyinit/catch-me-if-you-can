"""
Expected Value (EV) Calculator for Regulatory Navigation
Core engine that quantifies compliant business opportunities across jurisdictions
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
import hashlib
import json
from datetime import datetime

from .models import Strategy, RiskProfile, EVResult, Decision


class EVCalculator:
    """
    Deterministic engine for calculating Expected Value of regulatory strategies
    """
    
    # Decision thresholds
    EXECUTE_THRESHOLD = 0.3  # EV/Investment ratio above this = EXECUTE
    CAUTION_THRESHOLD = 0.1  # Between this and EXECUTE = CAUTION
    
    def __init__(self, 
                 risk_multiplier: float = 1.0,
                 time_discount_rate: float = 0.05):
        """
        Initialize calculator with configurable parameters
        
        Args:
            risk_multiplier: Global risk adjustment factor
            time_discount_rate: Monthly discount rate for future costs
        """
        self.risk_multiplier = risk_multiplier
        self.time_discount_rate = time_discount_rate
    
    def calculate_ev(self, 
                     strategy: Strategy, 
                     risk_profile: RiskProfile,
                     multi_jurisdiction_costs: Optional[float] = None) -> EVResult:
        """
        Calculate Expected Value using the Catch Me If You Can formula:
        EV = Profit - ComplianceCosts - RegulatoryRisks - OpportunityCost - TimeDelayCost
        
        Args:
            strategy: The proposed regulatory strategy
            risk_profile: Risk assessment for the strategy
            multi_jurisdiction_costs: Additional compliance costs from multi-jurisdiction operations
        
        Returns:
            EVResult with calculation breakdown and decision
        """
        
        # Core profit calculation
        gross_profit = strategy.profit_potential - strategy.implementation_cost
        
        # Risk-adjusted penalty
        expected_penalty = risk_profile.penalty_amount * risk_profile.enforcement_probability
        
        # Audit latency discount (penalties in the future are less costly)
        latency_discount = self._calculate_latency_discount(
            risk_profile.audit_latency_months
        )
        discounted_penalty = expected_penalty * latency_discount
        
        # Multi-jurisdiction considerations
        multi_jurisdiction_cost = multi_jurisdiction_costs or 0
        
        # Total costs
        total_costs = (
            discounted_penalty * self.risk_multiplier +
            risk_profile.reputational_damage +
            risk_profile.opportunity_cost +
            risk_profile.compliance_burden +
            multi_jurisdiction_cost
        )
        
        # Final EV calculation
        expected_value = gross_profit - total_costs
        
        # Confidence score based on data quality
        confidence_score = self._calculate_confidence(strategy, risk_profile)
        
        # Decision logic
        decision = self._make_decision(
            expected_value, 
            strategy.implementation_cost,
            confidence_score
        )
        
        # Create breakdown for transparency
        breakdown = {
            "gross_profit": gross_profit,
            "profit_potential": strategy.profit_potential,
            "implementation_cost": -strategy.implementation_cost,
            "expected_penalty": -expected_penalty,
            "latency_discount_factor": latency_discount,
            "discounted_penalty": -discounted_penalty,
            "reputational_damage": -risk_profile.reputational_damage,
            "opportunity_cost": -risk_profile.opportunity_cost,
            "compliance_burden": -risk_profile.compliance_burden,
            "multi_jurisdiction_cost": -multi_jurisdiction_cost,
            "total_costs": -total_costs,
            "final_ev": expected_value
        }
        
        # Generate attestation hash
        attestation_hash = self._generate_attestation_hash(
            strategy, risk_profile, breakdown
        )
        
        return EVResult(
            strategy=strategy,
            risk_profile=risk_profile,
            expected_value=expected_value,
            decision=decision,
            confidence_score=confidence_score,
            breakdown=breakdown,
            attestation_hash=attestation_hash
        )
    
    def _calculate_latency_discount(self, months: int) -> float:
        """
        Calculate discount factor for delayed enforcement
        Penalties in the future are worth less than immediate penalties
        """
        if months <= 0:
            return 1.0
        return 1 / ((1 + self.time_discount_rate) ** months)
    
    def _calculate_confidence(self, 
                             strategy: Strategy, 
                             risk_profile: RiskProfile) -> float:
        """
        Calculate confidence score based on data quality and certainty
        """
        confidence = 0.5  # Base confidence
        
        # Adjust based on enforcement probability certainty
        if 0.1 <= risk_profile.enforcement_probability <= 0.9:
            confidence += 0.2  # Not extreme probability = more reliable
        
        # Adjust based on time horizon
        if strategy.time_horizon_months <= 12:
            confidence += 0.2  # Shorter timeframe = more predictable
        
        # Adjust based on jurisdiction
        known_jurisdictions = ["US", "EU", "UK", "SG", "JP"]
        if strategy.jurisdiction in known_jurisdictions:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _make_decision(self, 
                      expected_value: float, 
                      investment: float,
                      confidence: float) -> Decision:
        """
        Make execution decision based on EV and confidence
        """
        if investment <= 0:
            return Decision.AVOID
        
        # Calculate return on investment ratio
        roi_ratio = expected_value / investment
        
        # Adjust thresholds based on confidence
        execute_threshold = self.EXECUTE_THRESHOLD * (2 - confidence)
        caution_threshold = self.CAUTION_THRESHOLD * (2 - confidence)
        
        if roi_ratio >= execute_threshold and expected_value > 0:
            return Decision.EXECUTE
        elif roi_ratio >= caution_threshold and expected_value > 0:
            return Decision.CAUTION
        else:
            return Decision.AVOID
    
    def _generate_attestation_hash(self,
                                   strategy: Strategy,
                                   risk_profile: RiskProfile,
                                   breakdown: Dict[str, float]) -> str:
        """
        Generate cryptographic hash for attestation
        This would be signed in a TEE in production
        """
        attestation_data = {
            "timestamp": datetime.now().isoformat(),
            "strategy_id": strategy.id,
            "strategy_type": strategy.type.value,
            "jurisdiction": strategy.jurisdiction,
            "profit_potential": strategy.profit_potential,
            "enforcement_probability": risk_profile.enforcement_probability,
            "penalty_amount": risk_profile.penalty_amount,
            "expected_value": breakdown["final_ev"],
            "breakdown": breakdown
        }
        
        # Create deterministic hash
        data_str = json.dumps(attestation_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def calculate_multi_jurisdiction_penalty(self,
                                            strategies: list[Strategy],
                                            correlation_matrix: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate additional penalties from operating in multiple jurisdictions
        Some penalties stack, others substitute
        
        Args:
            strategies: List of strategies across jurisdictions
            correlation_matrix: How penalties correlate between jurisdictions
        
        Returns:
            Additional penalty amount
        """
        if len(strategies) <= 1:
            return 0.0
        
        additional_penalty = 0.0
        jurisdictions = [s.jurisdiction for s in strategies]
        
        for i, j1 in enumerate(jurisdictions):
            for j2 in jurisdictions[i+1:]:
                if j1 in correlation_matrix and j2 in correlation_matrix[j1]:
                    # Correlation factor determines if penalties stack (1.0) or substitute (0.0)
                    correlation = correlation_matrix[j1][j2]
                    additional_penalty += strategies[i].profit_potential * 0.1 * correlation
        
        return additional_penalty