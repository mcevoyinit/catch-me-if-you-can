"""
Example: Digital Nomad Tax Compliance
Shows how a remote worker can legally structure their tax affairs
using legitimate international tax treaties and programs
"""

from core import EVCalculator, Strategy, RiskProfile
from core.models import StrategyType, Actor
from oracles import EnforcementOracle, LegalOracle, MarketOracle
from attestation import TEESimulator, BlockchainLogger


def run_digital_nomad_example():
    """
    Example: Software developer considering Portugal's NHR program
    while working for US clients
    """
    
    print("=" * 60)
    print("EXAMPLE: Digital Nomad Tax Compliance Strategy")
    print("=" * 60)
    
    # Initialize components
    calculator = EVCalculator()
    enforcement_oracle = EnforcementOracle()
    legal_oracle = LegalOracle()
    tee = TEESimulator()
    blockchain = BlockchainLogger()
    
    # Define the actor (digital nomad)
    actor = Actor(
        id="nomad_001",
        type="individual",
        jurisdiction="US",  # Current jurisdiction
        risk_tolerance=0.7,  # Moderate-high risk tolerance
        capital_available=50000,
        reputation_sensitivity=0.3  # Low sensitivity
    )
    
    # Define the strategy
    strategy = Strategy(
        id="portugal_nhr_2024",
        type=StrategyType.TAX_OPTIMIZATION,
        description="Legally relocate to Portugal under official NHR (Non-Habitual Resident) tax treaty program while maintaining US clients",
        jurisdiction="PT",  # Target jurisdiction
        profit_potential=35000,  # Legal tax savings through treaty benefits
        implementation_cost=5000,  # Relocation and compliance setup costs
        time_horizon_months=24,
        metadata={
            "current_tax_rate": 0.32,
            "nhr_tax_rate": 0.20,
            "annual_income": 120000
        }
    )
    
    print(f"\nStrategy: {strategy.description}")
    print(f"Potential Annual Savings: ${strategy.profit_potential:,.0f}")
    print(f"Implementation Cost: ${strategy.implementation_cost:,.0f}")
    
    # Get legal context
    legal_context = legal_oracle.analyze_legal_context(
        strategy.description,
        strategy.jurisdiction,
        strategy.type.value
    )
    
    print(f"\nLegal Context:")
    print(f"- Gray Areas: {len(legal_context.gray_areas)} identified")
    print(f"- Key Requirements: {len(legal_context.key_requirements)} to meet")
    
    # Create risk profile
    risk_profile = RiskProfile(
        strategy_id=strategy.id,
        enforcement_probability=0.08,  # Low uncertainty for official treaty programs
        penalty_amount=10000,  # Compliance costs and potential adjustments
        reputational_damage=1000,  # Minimal impact for legal compliance
        opportunity_cost=2000,  # Lost opportunities from relocation
        audit_latency_months=18,  # Time to establish clear tax status
        compliance_burden=3000  # Annual tax filing and compliance costs
    )
    
    # Calculate Expected Value
    ev_result = calculator.calculate_ev(strategy, risk_profile)
    
    print(f"\n📊 EXPECTED VALUE CALCULATION:")
    print(f"Expected Value: ${ev_result.expected_value:,.2f}")
    print(f"Decision: {ev_result.decision.value}")
    print(f"Confidence Score: {ev_result.confidence_score:.2%}")
    
    print(f"\nBreakdown:")
    for key, value in ev_result.breakdown.items():
        if value != 0:
            print(f"  {key}: ${value:,.2f}")
    
    # Create attestation
    attestation = tee.attest_computation(
        "ev_calculation",
        inputs={
            "strategy": strategy.id,
            "actor": actor.id,
            "jurisdiction_from": "US",
            "jurisdiction_to": "PT"
        },
        outputs={
            "expected_value": ev_result.expected_value,
            "decision": ev_result.decision.value
        }
    )
    
    print(f"\n🔐 ATTESTATION:")
    print(f"Attestation ID: {attestation.attestation_id}")
    print(f"Computation Hash: {attestation.computation_hash[:32]}...")
    
    # Log to blockchain
    tx = blockchain.log_compliance_evaluation(
        strategy.id,
        attestation.attestation_id,
        ev_result.expected_value,
        ev_result.decision.value,
        strategy.jurisdiction,
        {"strategy": strategy.__dict__, "result": ev_result.to_dict()}
    )
    
    print(f"\n⛓️ BLOCKCHAIN RECORD:")
    print(f"Transaction Hash: {tx.tx_hash[:32]}...")
    print(f"Block Number: {tx.block_number}")
    print(f"Gas Used: {tx.gas_used}")
    
    print(f"\n✅ RECOMMENDATION:")
    if ev_result.decision.value == "EXECUTE":
        print("The Portugal NHR program offers legitimate tax treaty benefits.")
        print("Recommended to proceed with proper tax residency establishment.")
        print("Ensure full compliance with both Portuguese and US tax obligations.")
    elif ev_result.decision.value == "CAUTION":
        print("The opportunity is legitimate but requires careful compliance planning.")
        print("Consult with international tax advisors to ensure proper structure.")
    else:
        print("The compliance complexity may outweigh the benefits.")
        print("Consider simpler international tax structures.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_digital_nomad_example()