"""
Market Data Oracle
Provides market opportunity and profit potential data
For hackathon: Uses mock market data and trends
"""

from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import random


@dataclass
class MarketOpportunity:
    """Market opportunity assessment"""
    market_size_usd: float
    growth_rate_annual: float
    competition_level: str  # low, medium, high
    entry_barriers: List[str]
    profit_margins: Dict[str, float]  # industry averages
    time_to_profitability_months: int
    market_maturity: str  # emerging, growing, mature, declining


class MarketOracle:
    """
    Oracle that provides market data and opportunity assessment
    In production, this would connect to market research APIs and databases
    """
    
    def __init__(self):
        self.market_data = self._initialize_market_data()
        self.trend_data = self._initialize_trend_data()
    
    def _initialize_market_data(self) -> Dict[str, MarketOpportunity]:
        """
        Initialize mock market data for different opportunities
        """
        return {
            "digital_nomad_services": MarketOpportunity(
                market_size_usd=50_000_000_000,
                growth_rate_annual=0.25,
                competition_level="medium",
                entry_barriers=["Regulatory compliance", "Trust building", "Multi-currency operations"],
                profit_margins={"gross": 0.70, "operating": 0.30, "net": 0.20},
                time_to_profitability_months=18,
                market_maturity="growing"
            ),
            "cross_border_payments": MarketOpportunity(
                market_size_usd=150_000_000_000,
                growth_rate_annual=0.15,
                competition_level="high",
                entry_barriers=["Licensing requirements", "Banking partnerships", "Capital requirements"],
                profit_margins={"gross": 0.40, "operating": 0.15, "net": 0.08},
                time_to_profitability_months=36,
                market_maturity="mature"
            ),
            "regulatory_tech": MarketOpportunity(
                market_size_usd=20_000_000_000,
                growth_rate_annual=0.30,
                competition_level="low",
                entry_barriers=["Technical expertise", "Data access", "Regulatory knowledge"],
                profit_margins={"gross": 0.80, "operating": 0.40, "net": 0.25},
                time_to_profitability_months=24,
                market_maturity="emerging"
            ),
            "defi_services": MarketOpportunity(
                market_size_usd=80_000_000_000,
                growth_rate_annual=0.40,
                competition_level="medium",
                entry_barriers=["Technical complexity", "Security requirements", "Regulatory uncertainty"],
                profit_margins={"gross": 0.85, "operating": 0.50, "net": 0.35},
                time_to_profitability_months=12,
                market_maturity="emerging"
            ),
            "embedded_finance": MarketOpportunity(
                market_size_usd=100_000_000_000,
                growth_rate_annual=0.35,
                competition_level="medium",
                entry_barriers=["Partnership requirements", "Technical integration", "Compliance"],
                profit_margins={"gross": 0.60, "operating": 0.25, "net": 0.15},
                time_to_profitability_months=24,
                market_maturity="growing"
            )
        }
    
    def _initialize_trend_data(self) -> Dict[str, List[str]]:
        """
        Initialize market trend data
        """
        return {
            "hot_markets": [
                "AI-powered compliance tools",
                "Cross-border remote work solutions",
                "Regulatory sandbox platforms",
                "Digital identity verification",
                "Embedded tax optimization"
            ],
            "cooling_markets": [
                "Traditional remittance",
                "Manual compliance consulting",
                "Single-jurisdiction solutions"
            ],
            "emerging_opportunities": [
                "Quantum-resistant financial infrastructure",
                "Regulatory arbitrage transparency tools",
                "Decentralized compliance networks"
            ]
        }
    
    def assess_market_opportunity(self,
                                 market_type: str,
                                 target_revenue: float,
                                 timeframe_months: int) -> Dict[str, Any]:
        """
        Assess market opportunity for a strategy
        """
        # Find closest matching market data
        market = self._find_best_market_match(market_type)
        
        if not market:
            # Default conservative estimates
            return {
                "feasibility_score": 0.3,
                "addressable_market": target_revenue * 100,
                "capture_probability": 0.05,
                "competitive_advantage_needed": "high",
                "recommended_approach": "niche focus"
            }
        
        # Calculate feasibility based on market conditions
        feasibility = self._calculate_feasibility(market, target_revenue, timeframe_months)
        
        # Calculate addressable market
        addressable_market = market.market_size_usd * 0.01  # Assume 1% is addressable
        
        # Estimate capture probability
        capture_probability = self._estimate_capture_probability(
            market.competition_level,
            market.market_maturity,
            timeframe_months
        )
        
        return {
            "feasibility_score": feasibility,
            "addressable_market": addressable_market,
            "capture_probability": capture_probability,
            "market_growth_rate": market.growth_rate_annual,
            "profit_margins": market.profit_margins,
            "competitive_landscape": market.competition_level,
            "entry_barriers": market.entry_barriers,
            "time_to_profitability": market.time_to_profitability_months,
            "recommended_approach": self._recommend_approach(market, feasibility)
        }
    
    def _find_best_market_match(self, market_type: str) -> Optional[MarketOpportunity]:
        """
        Find best matching market data based on type
        """
        # Simple keyword matching for demo
        market_type_lower = market_type.lower()
        
        if "nomad" in market_type_lower or "remote" in market_type_lower:
            return self.market_data["digital_nomad_services"]
        elif "payment" in market_type_lower or "transfer" in market_type_lower:
            return self.market_data["cross_border_payments"]
        elif "regulatory" in market_type_lower or "compliance" in market_type_lower:
            return self.market_data["regulatory_tech"]
        elif "defi" in market_type_lower or "blockchain" in market_type_lower:
            return self.market_data["defi_services"]
        elif "embedded" in market_type_lower or "fintech" in market_type_lower:
            return self.market_data["embedded_finance"]
        
        return None
    
    def _calculate_feasibility(self,
                              market: MarketOpportunity,
                              target_revenue: float,
                              timeframe_months: int) -> float:
        """
        Calculate feasibility score (0.0 to 1.0)
        """
        score = 0.5  # Base score
        
        # Adjust for market size
        if target_revenue < market.market_size_usd * 0.001:
            score += 0.2  # Very achievable target
        elif target_revenue < market.market_size_usd * 0.01:
            score += 0.1  # Achievable target
        else:
            score -= 0.2  # Ambitious target
        
        # Adjust for timeframe
        if timeframe_months >= market.time_to_profitability_months * 1.5:
            score += 0.15  # Sufficient time
        elif timeframe_months >= market.time_to_profitability_months:
            score += 0.05  # Adequate time
        else:
            score -= 0.15  # Tight timeline
        
        # Adjust for market maturity
        maturity_adjustments = {
            "emerging": 0.1,    # High potential
            "growing": 0.05,    # Good potential
            "mature": -0.05,    # Harder to enter
            "declining": -0.2   # Avoid
        }
        score += maturity_adjustments.get(market.market_maturity, 0)
        
        # Adjust for competition
        competition_adjustments = {
            "low": 0.15,
            "medium": 0,
            "high": -0.15
        }
        score += competition_adjustments.get(market.competition_level, 0)
        
        return max(0.0, min(1.0, score))
    
    def _estimate_capture_probability(self,
                                     competition: str,
                                     maturity: str,
                                     timeframe_months: int) -> float:
        """
        Estimate probability of capturing market share
        """
        base_probability = {
            "low": 0.15,
            "medium": 0.08,
            "high": 0.03
        }.get(competition, 0.05)
        
        # Adjust for market maturity
        if maturity == "emerging":
            base_probability *= 1.5
        elif maturity == "growing":
            base_probability *= 1.2
        elif maturity == "declining":
            base_probability *= 0.5
        
        # Adjust for timeframe
        if timeframe_months > 36:
            base_probability *= 1.3
        elif timeframe_months < 12:
            base_probability *= 0.7
        
        return min(base_probability, 0.25)  # Cap at 25%
    
    def _recommend_approach(self, market: MarketOpportunity, feasibility: float) -> str:
        """
        Recommend market entry approach
        """
        if feasibility >= 0.7:
            if market.competition_level == "low":
                return "aggressive expansion - first mover advantage"
            else:
                return "rapid scaling - strong market opportunity"
        elif feasibility >= 0.4:
            if market.market_maturity == "emerging":
                return "measured growth - focus on product-market fit"
            else:
                return "niche focus - differentiate from competitors"
        else:
            if market.growth_rate_annual > 0.25:
                return "wait and watch - market still developing"
            else:
                return "pivot recommended - challenging market conditions"
    
    def get_profit_potential(self,
                            market_type: str,
                            investment: float,
                            timeframe_months: int) -> Dict[str, float]:
        """
        Estimate profit potential for an investment
        """
        market = self._find_best_market_match(market_type)
        
        if not market:
            # Conservative default
            return {
                "pessimistic": investment * 0.5,
                "expected": investment * 1.2,
                "optimistic": investment * 2.0
            }
        
        # Calculate based on market margins and growth
        months_factor = timeframe_months / 12
        growth_factor = (1 + market.growth_rate_annual) ** months_factor
        
        # Base return on margins
        base_return = investment * (1 + market.profit_margins["net"]) * growth_factor
        
        return {
            "pessimistic": base_return * 0.6,
            "expected": base_return,
            "optimistic": base_return * 1.8
        }
    
    def get_market_trends(self) -> Dict[str, List[str]]:
        """
        Get current market trends
        """
        return self.trend_data
    
    def simulate_market_conditions(self, volatility: str = "medium") -> Dict[str, float]:
        """
        Simulate current market conditions for demo
        """
        base_conditions = {
            "risk_appetite": 0.5,
            "regulatory_clarity": 0.4,
            "innovation_index": 0.7,
            "funding_availability": 0.6,
            "competitive_intensity": 0.65
        }
        
        # Add volatility
        volatility_factor = {"low": 0.05, "medium": 0.1, "high": 0.2}.get(volatility, 0.1)
        
        for key in base_conditions:
            adjustment = (random.random() - 0.5) * volatility_factor
            base_conditions[key] = max(0, min(1, base_conditions[key] + adjustment))
        
        return base_conditions