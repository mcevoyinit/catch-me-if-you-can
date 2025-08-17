"""
Oracles module for ArbiLens Protocol
Provides data feeds for enforcement statistics, legal context, and market data
"""

from .enforcement_oracle import EnforcementOracle
from .legal_oracle import LegalOracle
from .market_oracle import MarketOracle

__all__ = ['EnforcementOracle', 'LegalOracle', 'MarketOracle']