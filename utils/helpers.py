"""
Helper functions for data processing and validation
"""

from typing import Dict, Any, Optional
import hashlib
import json
from datetime import datetime


def generate_strategy_id() -> str:
    """Generate unique strategy ID"""
    timestamp = datetime.now().isoformat()
    return hashlib.md5(timestamp.encode()).hexdigest()[:12]


def validate_jurisdiction(jurisdiction: str) -> bool:
    """Validate if jurisdiction is supported"""
    from .constants import SUPPORTED_JURISDICTIONS
    return jurisdiction in SUPPORTED_JURISDICTIONS


def format_currency(amount: float) -> str:
    """Format amount as currency string"""
    return f"${amount:,.2f}"


def calculate_roi(profit: float, investment: float) -> float:
    """Calculate return on investment"""
    if investment <= 0:
        return 0.0
    return (profit - investment) / investment


def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize user input data"""
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = value.strip()
        elif isinstance(value, (int, float)):
            sanitized[key] = abs(value)
        else:
            sanitized[key] = value
    return sanitized