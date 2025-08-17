"""
Configuration settings for Catch Me If You Can Protocol
"""

import os
from typing import Dict, Any


class Config:
    """Base configuration"""
    
    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Blockchain Settings
    CHAIN_ID = int(os.getenv('CHAIN_ID', 1))
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '0x' + 'a' * 40)
    
    # TEE Settings
    TEE_ENABLED = os.getenv('TEE_ENABLED', 'False').lower() == 'true'
    TEE_TYPE = os.getenv('TEE_TYPE', 'SGX_SIMULATED')
    
    # Oracle Settings
    ORACLE_REFRESH_INTERVAL = int(os.getenv('ORACLE_REFRESH_INTERVAL', 3600))
    
    # Risk Parameters
    RISK_MULTIPLIER = float(os.getenv('RISK_MULTIPLIER', 1.0))
    TIME_DISCOUNT_RATE = float(os.getenv('TIME_DISCOUNT_RATE', 0.05))
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('_') and not callable(value)
        }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TEE_ENABLED = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TEE_ENABLED = True


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('ENVIRONMENT', 'development')
    return config.get(env, config['default'])