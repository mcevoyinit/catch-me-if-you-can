"""
Catch Me If You Can Protocol - Main Entry Point
ETH Global NYC Hackathon
"""

import sys
import argparse
from api import create_app
from examples.digital_nomad import run_digital_nomad_example
from examples.startup_sandbox import run_startup_sandbox_example


def print_banner():
    """Print Catch Me If You Can banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ██████╗ █████╗ ████████╗ ██████╗██╗  ██╗              ║
    ║  ██╔════╝██╔══██╗╚══██╔══╝██╔════╝██║  ██║              ║
    ║  ██║     ███████║   ██║   ██║     ███████║              ║
    ║  ██║     ██╔══██║   ██║   ██║     ██╔══██║              ║
    ║  ╚██████╗██║  ██║   ██║   ╚██████╗██║  ██║              ║
    ║   ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝              ║
    ║        ME IF YOU CAN                                      ║
    ║                                                           ║
    ║        The Regulatory Navigation Protocol ⚖️             ║
    ║        ETH Global NYC Hackathon 2024                     ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_demo():
    """Run demonstration examples"""
    print_banner()
    print("\n🚀 Running Catch Me If You Can Protocol Demonstrations\n")
    
    print("Select a demo:")
    print("1. Digital Nomad Tax Optimization")
    print("2. Fintech Regulatory Sandbox")
    print("3. Both Examples")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        run_digital_nomad_example()
    elif choice == "2":
        run_startup_sandbox_example()
    elif choice == "3":
        run_digital_nomad_example()
        print("\n")
        run_startup_sandbox_example()
    else:
        print("Invalid choice. Running both examples...")
        run_digital_nomad_example()
        print("\n")
        run_startup_sandbox_example()


def run_api(host='0.0.0.0', port=5000, debug=False):
    """Run the Flask API server"""
    print_banner()
    print(f"\n🌐 Starting Catch Me If You Can API Server")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Debug: {debug}")
    print("\n📍 API Endpoints:")
    print(f"   POST {host}:{port}/evaluate - Evaluate a strategy")
    print(f"   GET  {host}:{port}/transparency - View transparency dashboard")
    print(f"   GET  {host}:{port}/regulatory-insights - Regulatory insights")
    print(f"   GET  {host}:{port}/market-trends - Current market trends")
    print(f"   GET  {host}:{port}/attestation-status - TEE attestation status")
    print(f"   GET  {host}:{port}/health - Health check")
    print("\n✨ Server starting...\n")
    
    app = create_app()
    app.run(host=host, port=port, debug=debug)


def main():
    """Main entry point with CLI arguments"""
    parser = argparse.ArgumentParser(
        description='Catch Me If You Can Protocol - Regulatory Navigation and Compliance Engine'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration examples')
    
    # API command
    api_parser = subparsers.add_parser('api', help='Start the API server')
    api_parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    api_parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    api_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    # Quick evaluation command
    eval_parser = subparsers.add_parser('evaluate', help='Quick strategy evaluation')
    eval_parser.add_argument('--description', required=True, help='Strategy description')
    eval_parser.add_argument('--jurisdiction', required=True, help='Target jurisdiction')
    eval_parser.add_argument('--profit', type=float, required=True, help='Profit potential')
    eval_parser.add_argument('--cost', type=float, required=True, help='Implementation cost')
    eval_parser.add_argument('--months', type=int, default=12, help='Time horizon in months')
    
    args = parser.parse_args()
    
    if args.command == 'demo':
        run_demo()
    elif args.command == 'api':
        run_api(host=args.host, port=args.port, debug=args.debug)
    elif args.command == 'evaluate':
        # Quick evaluation mode
        from core import EVCalculator, Strategy, RiskProfile
        from core.models import StrategyType
        
        print_banner()
        print("\n⚡ Quick Strategy Evaluation\n")
        
        strategy = Strategy(
            id="quick_eval",
            type=StrategyType.MARKET_ENTRY,
            description=args.description,
            jurisdiction=args.jurisdiction,
            profit_potential=args.profit,
            implementation_cost=args.cost,
            time_horizon_months=args.months
        )
        
        # Simple risk profile
        risk_profile = RiskProfile(
            strategy_id=strategy.id,
            enforcement_probability=0.15,
            penalty_amount=args.profit * 0.3,
            reputational_damage=args.profit * 0.1,
            opportunity_cost=args.profit * 0.05,
            audit_latency_months=12,
            compliance_burden=args.cost * 0.1
        )
        
        calculator = EVCalculator()
        result = calculator.calculate_ev(strategy, risk_profile)
        
        print(f"Strategy: {strategy.description}")
        print(f"Jurisdiction: {strategy.jurisdiction}")
        print(f"\n📊 Results:")
        print(f"Expected Value: ${result.expected_value:,.2f}")
        print(f"Decision: {result.decision.value}")
        print(f"Confidence: {result.confidence_score:.2%}")
        
        if result.decision.value == "EXECUTE":
            print("\n✅ Favorable opportunity - proceed with strategy")
        elif result.decision.value == "CAUTION":
            print("\n⚠️ Moderate opportunity - proceed with caution")
        else:
            print("\n❌ Unfavorable - consider alternatives")
    else:
        # Default: show help and run demo
        parser.print_help()
        print("\n" + "="*60)
        print("No command specified. Running demo...")
        print("="*60 + "\n")
        run_demo()


if __name__ == "__main__":
    main()