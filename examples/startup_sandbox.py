"""
Example: Fintech Startup Regulatory Sandbox
Shows how a startup can evaluate entering a regulatory sandbox
"""

from core import EVCalculator, Strategy, RiskProfile, RiskScorer
from core.models import StrategyType
from oracles import EnforcementOracle, MarketOracle
from attestation import TEESimulator, BlockchainLogger


def run_startup_sandbox_example():
    """
    Example: Fintech startup considering Singapore's regulatory sandbox
    for a new cross-border payment solution
    """
    
    print("=" * 60)
    print("EXAMPLE: Fintech Regulatory Sandbox Entry")
    print("=" * 60)
    
    # Initialize components
    calculator = EVCalculator()
    risk_scorer = RiskScorer()
    market_oracle = MarketOracle()
    enforcement_oracle = EnforcementOracle()
    tee = TEESimulator()
    blockchain = BlockchainLogger()
    
    # Define the strategy
    strategy = Strategy(
        id="sg_sandbox_fintech_2024",
        type=StrategyType.REGULATORY_SANDBOX,
        description="Enter Singapore MAS Fintech Regulatory Sandbox for blockchain-based remittance platform",
        jurisdiction="SG",
        profit_potential=2000000,  # Expected revenue in sandbox period
        implementation_cost=250000,  # Development and compliance costs
        time_horizon_months=18,  # Sandbox duration
        metadata={
            "target_customers": 10000,
            "transaction_volume": 50000000,
            "innovation_score": 0.8
        }
    )
    
    print(f"\nStrategy: {strategy.description}")
    print(f"Market Opportunity: ${strategy.profit_potential:,.0f}")
    print(f"Investment Required: ${strategy.implementation_cost:,.0f}")
    print(f"Sandbox Duration: {strategy.time_horizon_months} months")
    
    # Get market assessment
    market_assessment = market_oracle.assess_market_opportunity(
        "fintech remittance blockchain",
        strategy.profit_potential,
        strategy.time_horizon_months
    )
    
    print(f"\n📈 MARKET ASSESSMENT:")
    print(f"Feasibility Score: {market_assessment['feasibility_score']:.2%}")
    print(f"Market Growth Rate: {market_assessment['market_growth_rate']:.1%}")
    print(f"Competitive Landscape: {market_assessment['competitive_landscape']}")
    
    # Get enforcement data for sandbox
    enforcement_data = enforcement_oracle.get_enforcement_data("SG", "fintech")
    
    # Create risk profile (sandbox has lower risks)
    risk_profile = RiskProfile(
        strategy_id=strategy.id,
        enforcement_probability=0.05,  # Very low in sandbox
        penalty_amount=50000,  # Limited penalties in sandbox
        reputational_damage=20000,  # Low reputation risk
        opportunity_cost=100000,  # Cost of not pursuing other markets
        audit_latency_months=3,  # Quick feedback in sandbox
        compliance_burden=50000  # Sandbox reporting requirements
    )
    
    # Calculate Expected Value
    ev_result = calculator.calculate_ev(strategy, risk_profile)
    
    print(f"\n📊 EXPECTED VALUE CALCULATION:")
    print(f"Expected Value: ${ev_result.expected_value:,.2f}")
    print(f"Decision: {ev_result.decision.value}")
    print(f"Risk/Reward Ratio: {ev_result.risk_reward_ratio:.2f}")
    
    # Risk scoring
    risk_score, risk_zone, risk_breakdown = risk_scorer.score_risk(
        strategy, risk_profile
    )
    
    print(f"\n⚠️ RISK ANALYSIS:")
    print(f"Overall Risk Score: {risk_score:.2%}")
    print(f"Risk Zone: {risk_zone.value}")
    print("\nRisk Components:")
    for component, score in risk_breakdown.items():
        print(f"  {component}: {score:.2%}")
    
    # Get mitigation suggestions
    suggestions = risk_scorer.get_risk_mitigation_suggestions(risk_breakdown)
    if suggestions:
        print("\n💡 Risk Mitigation Suggestions:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
    
    # Create attestation
    attestation = tee.attest_computation(
        "sandbox_evaluation",
        inputs={
            "strategy": strategy.id,
            "jurisdiction": "SG",
            "innovation_type": "blockchain_remittance"
        },
        outputs={
            "expected_value": ev_result.expected_value,
            "decision": ev_result.decision.value,
            "risk_score": risk_score
        }
    )
    
    # Log to blockchain
    tx = blockchain.log_compliance_evaluation(
        strategy.id,
        attestation.attestation_id,
        ev_result.expected_value,
        ev_result.decision.value,
        strategy.jurisdiction,
        {
            "strategy": strategy.__dict__,
            "market": market_assessment,
            "risk": {"score": risk_score, "zone": risk_zone.value}
        }
    )
    
    print(f"\n⛓️ TRANSPARENCY RECORD:")
    print(f"Transaction Hash: {tx.tx_hash[:32]}...")
    print(f"Attestation ID: {attestation.attestation_id}")
    print(f"On-chain verification available for regulators")
    
    print(f"\n✅ SANDBOX ENTRY RECOMMENDATION:")
    if ev_result.decision.value == "EXECUTE":
        print("Strong opportunity! The Singapore sandbox offers:")
        print("• Low regulatory risk during testing phase")
        print("• Access to Asian remittance markets")
        print("• Path to full licensing after successful pilot")
        print("\nNext Steps:")
        print("1. Submit sandbox application to MAS")
        print("2. Prepare technical documentation")
        print("3. Establish local partnerships")
    elif ev_result.decision.value == "CAUTION":
        print("Proceed with careful planning:")
        print("• Ensure product-market fit before entry")
        print("• Build strong compliance framework")
        print("• Consider phased approach")
    else:
        print("Reconsider strategy:")
        print("• Market conditions may not be favorable")
        print("• Alternative jurisdictions might be better")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_startup_sandbox_example()