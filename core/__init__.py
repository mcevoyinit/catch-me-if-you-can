"""
Core module for Catch Me If You Can Protocol
Handles EV calculations, risk scoring, and decision logic
"""

from .calculator import EVCalculator
from .models import Strategy, RiskProfile, Decision
from .risk_scorer import RiskScorer

__all__ = ['EVCalculator', 'Strategy', 'RiskProfile', 'Decision', 'RiskScorer']