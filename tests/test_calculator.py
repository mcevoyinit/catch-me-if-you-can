"""
Tests for EV Calculator
"""

import unittest
from core import EVCalculator, Strategy, RiskProfile
from core.models import StrategyType, Decision


class TestEVCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calculator = EVCalculator()
    
    def test_positive_ev_calculation(self):
        """Test calculation with positive expected value"""
        strategy = Strategy(
            id="test_001",
            type=StrategyType.MARKET_ENTRY,
            description="Test strategy",
            jurisdiction="US",
            profit_potential=100000,
            implementation_cost=10000,
            time_horizon_months=12
        )
        
        risk_profile = RiskProfile(
            strategy_id="test_001",
            enforcement_probability=0.1,
            penalty_amount=5000,
            reputational_damage=1000,
            opportunity_cost=2000,
            audit_latency_months=6,
            compliance_burden=1000
        )
        
        result = self.calculator.calculate_ev(strategy, risk_profile)
        
        self.assertGreater(result.expected_value, 0)
        self.assertEqual(result.decision, Decision.EXECUTE)
    
    def test_negative_ev_calculation(self):
        """Test calculation with negative expected value"""
        strategy = Strategy(
            id="test_002",
            type=StrategyType.MARKET_ENTRY,
            description="High risk strategy",
            jurisdiction="US",
            profit_potential=10000,
            implementation_cost=8000,
            time_horizon_months=12
        )
        
        risk_profile = RiskProfile(
            strategy_id="test_002",
            enforcement_probability=0.9,
            penalty_amount=50000,
            reputational_damage=10000,
            opportunity_cost=5000,
            audit_latency_months=3,
            compliance_burden=5000
        )
        
        result = self.calculator.calculate_ev(strategy, risk_profile)
        
        self.assertLess(result.expected_value, 0)
        self.assertEqual(result.decision, Decision.AVOID)


if __name__ == '__main__':
    unittest.main()