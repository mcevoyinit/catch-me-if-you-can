"""
API module for ArbiLens Protocol
Provides REST endpoints for strategy evaluation
"""

from .endpoints import create_app

__all__ = ['create_app']