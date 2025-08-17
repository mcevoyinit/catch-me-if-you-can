"""
Attestation module for ArbiLens Protocol
Handles TEE simulation and blockchain logging for transparency
"""

from .tee_simulator import TEESimulator
from .blockchain_logger import BlockchainLogger

__all__ = ['TEESimulator', 'BlockchainLogger']