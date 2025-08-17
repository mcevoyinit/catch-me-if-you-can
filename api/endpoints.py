"""
REST API endpoints for ArbiLens Protocol
Flask-based API for hackathon demo
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import Dict, Any
import uuid

from core import EVCalculator, Strategy, RiskProfile, RiskScorer
from core.models import StrategyType, Actor
from oracles import EnforcementOracle, LegalOracle, MarketOracle
from attestation import TEESimulator, BlockchainLogger


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    CORS(app)
    
    # Initialize components
    app.calculator = EVCalculator()
    app.risk_scorer = RiskScorer()
    app.enforcement_oracle = EnforcementOracle()
    app.legal_oracle = LegalOracle()
    app.market_oracle = MarketOracle()
    app.tee = TEESimulator()
    app.blockchain = BlockchainLogger()
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({"status": "healthy", "service": "Catch Me If You Can Protocol"})
    
    @app.route('/evaluate', methods=['POST'])
    def evaluate_strategy():
        """
        Evaluate a compliant business strategy across jurisdictions
        
        Expected JSON payload:
        {
            "description": "Strategy description",
            "jurisdiction": "US/EU/UK/SG",
            "type": "tax_optimization/market_entry/product_launch/etc",
            "profit_potential": 1000000,
            "implementation_cost": 100000,
            "time_horizon_months": 12
        }
        """
        try:
            data = request.json
            
            # Create strategy
            strategy = Strategy(
                id=str(uuid.uuid4()),
                type=StrategyType(data.get('type', 'market_entry')),
                description=data['description'],
                jurisdiction=data['jurisdiction'],
                profit_potential=data['profit_potential'],
                implementation_cost=data['implementation_cost'],
                time_horizon_months=data['time_horizon_months']
            )
            
            # Get legal context
            legal_context = app.legal_oracle.analyze_legal_context(
                strategy.description,
                strategy.jurisdiction,
                strategy.type.value
            )
            
            # Get enforcement data
            enforcement_data = app.enforcement_oracle.get_enforcement_data(
                strategy.jurisdiction,
                strategy.type.value
            )
            
            # Get market assessment
            market_assessment = app.market_oracle.assess_market_opportunity(
                strategy.type.value,
                strategy.profit_potential,
                strategy.time_horizon_months
            )
            
            # Create risk profile
            if enforcement_data:
                enforcement_prob = enforcement_data.enforcement_probability
                penalty = enforcement_data.average_penalty_usd
            else:
                enforcement_prob = 0.15
                penalty = strategy.profit_potential * 0.2
            
            risk_profile = RiskProfile(
                strategy_id=strategy.id,
                enforcement_probability=enforcement_prob,
                penalty_amount=penalty,
                reputational_damage=strategy.profit_potential * 0.1,
                opportunity_cost=strategy.profit_potential * 0.05,
                audit_latency_months=12,
                compliance_burden=strategy.implementation_cost * 0.1
            )
            
            # Calculate EV
            ev_result = app.calculator.calculate_ev(strategy, risk_profile)
            
            # Score risk
            risk_score, risk_zone, risk_breakdown = app.risk_scorer.score_risk(
                strategy, risk_profile
            )
            
            # Create attestation
            attestation = app.tee.attest_computation(
                "ev_calculation",
                inputs={
                    "strategy": strategy.id,
                    "jurisdiction": strategy.jurisdiction,
                    "type": strategy.type.value
                },
                outputs={
                    "expected_value": ev_result.expected_value,
                    "decision": ev_result.decision.value,
                    "risk_score": risk_score
                }
            )
            
            # Log to blockchain  
            full_report = {
                "strategy": strategy.__dict__,
                "risk_profile": risk_profile.__dict__,
                "ev_result": ev_result.to_dict(),
                "legal_context": legal_context.__dict__,
                "market_assessment": market_assessment,
                "risk_analysis": {
                    "score": risk_score,
                    "zone": risk_zone.value,
                    "breakdown": risk_breakdown
                }
            }
            
            tx = app.blockchain.log_compliance_evaluation(
                strategy.id,
                attestation.attestation_id,
                ev_result.expected_value,
                ev_result.decision.value,
                strategy.jurisdiction,
                full_report
            )
            
            # Prepare response
            response = {
                "success": True,
                "strategy_id": strategy.id,
                "expected_value": ev_result.expected_value,
                "decision": ev_result.decision.value,
                "confidence_score": ev_result.confidence_score,
                "risk_zone": risk_zone.value,
                "breakdown": ev_result.breakdown,
                "attestation": {
                    "id": attestation.attestation_id,
                    "hash": attestation.computation_hash[:16] + "...",
                    "timestamp": attestation.timestamp
                },
                "blockchain": {
                    "tx_hash": tx.tx_hash,
                    "block_number": tx.block_number,
                    "ipfs_cid": full_report.get("ipfs_cid")
                },
                "recommendations": app.risk_scorer.get_risk_mitigation_suggestions(risk_breakdown)
            }
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400
    
    @app.route('/transparency', methods=['GET'])
    def transparency_dashboard():
        """Get transparency dashboard data"""
        dashboard = app.blockchain.get_transparency_dashboard()
        return jsonify(dashboard)
    
    @app.route('/regulatory-insights', methods=['GET'])
    def regulatory_insights():
        """Get insights for regulators"""
        insights = app.blockchain.simulate_regulatory_query()
        return jsonify(insights)
    
    @app.route('/market-trends', methods=['GET'])
    def market_trends():
        """Get current market trends"""
        trends = app.market_oracle.get_market_trends()
        conditions = app.market_oracle.simulate_market_conditions()
        return jsonify({
            "trends": trends,
            "current_conditions": conditions
        })
    
    @app.route('/attestation-status', methods=['GET'])
    def attestation_status():
        """Get TEE attestation status"""
        remote_attestation = app.tee.simulate_remote_attestation()
        summary = app.tee.get_attestation_summary()
        return jsonify({
            "remote_attestation": remote_attestation,
            "summary": summary
        })
    
    @app.route('/jurisdictions', methods=['GET'])
    def list_jurisdictions():
        """List supported jurisdictions"""
        return jsonify({
            "jurisdictions": ["US", "EU", "UK", "SG", "AE", "PT", "JP"],
            "total": 7
        })
    
    @app.route('/strategy-types', methods=['GET'])
    def list_strategy_types():
        """List available strategy types"""
        from core.models import StrategyType
        return jsonify({
            "types": [t.value for t in StrategyType],
            "total": len(StrategyType)
        })
    
    return app