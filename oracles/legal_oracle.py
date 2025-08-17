"""
Legal Context Oracle
Uses LLM integration to interpret legal text and regulatory requirements
For hackathon: Simulates LLM responses with predefined templates
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import hashlib


@dataclass
class LegalContext:
    """Legal interpretation and context for a strategy"""
    jurisdiction: str
    regulation_summary: str
    key_requirements: List[str]
    gray_areas: List[str]
    precedents: List[str]
    risk_factors: List[str]
    compliance_path: Optional[str]


class LegalOracle:
    """
    Oracle that provides legal context and interpretation
    In production, this would integrate with LLMs for real-time analysis
    """
    
    def __init__(self):
        self.legal_templates = self._initialize_legal_templates()
        self.cache = {}  # Cache LLM responses
    
    def _initialize_legal_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize legal context templates for different scenarios
        Simulates LLM responses for hackathon demo
        """
        return {
            "digital_nomad_tax": {
                "summary": "Tax optimization for remote workers across jurisdictions",
                "requirements": [
                    "Establish tax residency in favorable jurisdiction",
                    "Maintain compliance with source country regulations",
                    "Document days spent in each jurisdiction",
                    "Report foreign income appropriately"
                ],
                "gray_areas": [
                    "Definition of 'permanent establishment' for remote work",
                    "Tax treaty interpretation for digital services",
                    "Nexus rules for online businesses"
                ],
                "precedents": [
                    "2023 EU Digital Nomad Visa frameworks",
                    "US State nexus rules for remote workers",
                    "OECD guidance on digital economy taxation"
                ],
                "risk_factors": [
                    "Changing tax treaty interpretations",
                    "Increased enforcement on digital nomads",
                    "Social security contribution requirements"
                ]
            },
            "fintech_sandbox": {
                "summary": "Regulatory sandbox participation for innovative financial services",
                "requirements": [
                    "Meet innovation criteria for sandbox entry",
                    "Limited customer base during testing phase",
                    "Regular reporting to regulatory authority",
                    "Exit strategy and full compliance path"
                ],
                "gray_areas": [
                    "Definition of 'innovative' for sandbox qualification",
                    "Scope of activities permitted in sandbox",
                    "Data sharing requirements with regulators"
                ],
                "precedents": [
                    "Singapore MAS Fintech Regulatory Sandbox",
                    "UK FCA Regulatory Sandbox outcomes",
                    "Hong Kong HKMA Fintech Supervisory Sandbox"
                ],
                "risk_factors": [
                    "Sandbox graduation requirements",
                    "Limited operational scope",
                    "Regulatory changes during sandbox period"
                ]
            },
            "cross_border_payments": {
                "summary": "International money transfer and payment processing regulations",
                "requirements": [
                    "Money transmitter licenses in operating jurisdictions",
                    "AML/KYC compliance procedures",
                    "Transaction reporting requirements",
                    "Capital adequacy requirements"
                ],
                "gray_areas": [
                    "Cryptocurrency classification and treatment",
                    "Embedded finance partnership structures",
                    "Agent vs principal determination"
                ],
                "precedents": [
                    "Wise (TransferWise) multi-jurisdiction model",
                    "PayPal regulatory settlements",
                    "Stripe Treasury partner bank model"
                ],
                "risk_factors": [
                    "Rapid regulatory changes in crypto",
                    "Varying AML standards across jurisdictions",
                    "Banking partner stability"
                ]
            }
        }
    
    def analyze_legal_context(self,
                             strategy_description: str,
                             jurisdiction: str,
                             strategy_type: str) -> LegalContext:
        """
        Analyze legal context for a proposed strategy
        In production, this would call an LLM for analysis
        """
        
        # Generate cache key
        cache_key = self._generate_cache_key(strategy_description, jurisdiction)
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Simulate LLM analysis with template matching
        template_key = self._match_template(strategy_type, strategy_description)
        template = self.legal_templates.get(template_key, self._get_default_template())
        
        # Create legal context
        context = LegalContext(
            jurisdiction=jurisdiction,
            regulation_summary=template["summary"],
            key_requirements=template["requirements"],
            gray_areas=template["gray_areas"],
            precedents=template["precedents"],
            risk_factors=template["risk_factors"],
            compliance_path=self._generate_compliance_path(strategy_type, jurisdiction)
        )
        
        # Cache the result
        self.cache[cache_key] = context
        
        return context
    
    def _match_template(self, strategy_type: str, description: str) -> str:
        """
        Match strategy to appropriate template
        """
        # Simple keyword matching for demo
        description_lower = description.lower()
        
        if "tax" in description_lower or "nomad" in description_lower:
            return "digital_nomad_tax"
        elif "sandbox" in description_lower or "fintech" in description_lower:
            return "fintech_sandbox"
        elif "payment" in description_lower or "transfer" in description_lower:
            return "cross_border_payments"
        else:
            return "default"
    
    def _get_default_template(self) -> Dict[str, Any]:
        """
        Default template for unmatched strategies
        """
        return {
            "summary": "General regulatory compliance requirements",
            "requirements": [
                "Obtain necessary business licenses",
                "Comply with local regulations",
                "Maintain proper documentation",
                "Regular compliance reporting"
            ],
            "gray_areas": [
                "Regulatory interpretation variations",
                "Cross-jurisdiction operations",
                "Emerging technology regulations"
            ],
            "precedents": [
                "Industry standard practices",
                "Recent regulatory guidance",
                "Comparable business models"
            ],
            "risk_factors": [
                "Regulatory uncertainty",
                "Enforcement variations",
                "Compliance costs"
            ]
        }
    
    def _generate_compliance_path(self, strategy_type: str, jurisdiction: str) -> str:
        """
        Generate recommended compliance path
        """
        paths = {
            "fintech": f"1. Apply for {jurisdiction} sandbox program\n2. Develop MVP with limited users\n3. Iterate based on regulatory feedback\n4. Apply for full license",
            "tax_optimization": f"1. Establish tax residency in {jurisdiction}\n2. Structure operations for compliance\n3. Implement transfer pricing documentation\n4. Regular tax planning reviews",
            "cross_border": f"1. Obtain money transmitter licenses\n2. Establish banking partnerships\n3. Implement AML/KYC systems\n4. Scale operations gradually"
        }
        
        return paths.get(strategy_type, f"1. Research {jurisdiction} requirements\n2. Engage legal counsel\n3. Implement compliance framework\n4. Monitor regulatory changes")
    
    def _generate_cache_key(self, description: str, jurisdiction: str) -> str:
        """
        Generate cache key for legal analysis
        """
        content = f"{description}:{jurisdiction}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_regulatory_updates(self, jurisdiction: str) -> List[str]:
        """
        Get recent regulatory updates for a jurisdiction
        For demo: Returns mock updates
        """
        updates = {
            "US": [
                "SEC proposes new rules for digital asset custody (Jan 2024)",
                "IRS clarifies remote work tax obligations (Dec 2023)",
                "FinCEN updates beneficial ownership requirements (Nov 2023)"
            ],
            "EU": [
                "MiCA regulation enters into force (Jan 2024)",
                "Updated GDPR guidance on AI systems (Dec 2023)",
                "Digital Services Act compliance deadline (Nov 2023)"
            ],
            "SG": [
                "MAS expands fintech regulatory sandbox (Jan 2024)",
                "New guidelines for digital payment tokens (Dec 2023)",
                "Variable capital company framework updates (Nov 2023)"
            ],
            "UK": [
                "FCA consultation on AI in financial services (Jan 2024)",
                "Updated cryptoasset financial promotions rules (Dec 2023)",
                "Online Safety Bill implementation (Nov 2023)"
            ]
        }
        
        return updates.get(jurisdiction, ["No recent updates available"])
    
    def assess_legal_innovation(self, strategy_description: str) -> float:
        """
        Assess how innovative a strategy is from legal perspective
        Returns innovation score from 0.0 to 1.0
        """
        # Simple keyword-based scoring for demo
        innovation_keywords = [
            "blockchain", "defi", "ai", "machine learning",
            "autonomous", "decentralized", "tokenization",
            "smart contract", "dao", "nft", "metaverse"
        ]
        
        description_lower = strategy_description.lower()
        innovation_count = sum(1 for keyword in innovation_keywords if keyword in description_lower)
        
        # Normalize to 0-1 scale
        innovation_score = min(innovation_count / 3, 1.0)
        
        return innovation_score