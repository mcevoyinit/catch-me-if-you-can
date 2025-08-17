"""
Trusted Execution Environment (TEE) Simulator
Simulates attestation and secure computation for hackathon demo
In production, this would use actual TEE hardware (Intel SGX, ARM TrustZone, etc.)
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import hmac
import secrets


@dataclass
class Attestation:
    """Attestation record for a computation"""
    attestation_id: str
    timestamp: str
    computation_hash: str
    input_hash: str
    output_hash: str
    tee_signature: str
    metadata: Dict[str, Any]


class TEESimulator:
    """
    Simulates TEE functionality for secure computation attestation
    """
    
    def __init__(self):
        # Generate simulated TEE keys
        self.tee_private_key = secrets.token_hex(32)
        self.tee_public_key = hashlib.sha256(self.tee_private_key.encode()).hexdigest()
        self.attestation_counter = 0
        self.attestation_log = []
    
    def attest_computation(self,
                          computation_type: str,
                          inputs: Dict[str, Any],
                          outputs: Dict[str, Any],
                          metadata: Optional[Dict[str, Any]] = None) -> Attestation:
        """
        Create attestation for a computation
        
        Args:
            computation_type: Type of computation (e.g., "ev_calculation")
            inputs: Input parameters to the computation
            outputs: Results of the computation
            metadata: Additional metadata
        
        Returns:
            Attestation record
        """
        
        # Generate attestation ID
        self.attestation_counter += 1
        attestation_id = f"ATT-{self.attestation_counter:06d}-{secrets.token_hex(4)}"
        
        # Create hashes
        input_hash = self._hash_data(inputs)
        output_hash = self._hash_data(outputs)
        computation_hash = self._hash_computation(computation_type, input_hash, output_hash)
        
        # Create signature
        signature = self._sign_attestation(computation_hash)
        
        # Build attestation
        attestation = Attestation(
            attestation_id=attestation_id,
            timestamp=datetime.now().isoformat(),
            computation_hash=computation_hash,
            input_hash=input_hash,
            output_hash=output_hash,
            tee_signature=signature,
            metadata=metadata or {}
        )
        
        # Log attestation
        self.attestation_log.append(attestation)
        
        return attestation
    
    def verify_attestation(self, attestation: Attestation) -> bool:
        """
        Verify an attestation signature
        """
        expected_signature = self._sign_attestation(attestation.computation_hash)
        return hmac.compare_digest(attestation.tee_signature, expected_signature)
    
    def _hash_data(self, data: Dict[str, Any]) -> str:
        """
        Create deterministic hash of data
        """
        # Sort keys for deterministic hashing
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def _hash_computation(self, 
                         computation_type: str,
                         input_hash: str,
                         output_hash: str) -> str:
        """
        Create hash of the entire computation
        """
        computation_data = f"{computation_type}:{input_hash}:{output_hash}"
        return hashlib.sha256(computation_data.encode()).hexdigest()
    
    def _sign_attestation(self, computation_hash: str) -> str:
        """
        Sign attestation with TEE private key
        """
        return hmac.new(
            self.tee_private_key.encode(),
            computation_hash.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def export_attestation_proof(self, attestation: Attestation) -> Dict[str, Any]:
        """
        Export attestation in a format suitable for blockchain storage
        """
        return {
            "version": "1.0",
            "attestation_id": attestation.attestation_id,
            "timestamp": attestation.timestamp,
            "computation_hash": attestation.computation_hash,
            "tee_public_key": self.tee_public_key,
            "signature": attestation.tee_signature,
            "metadata": attestation.metadata
        }
    
    def generate_eip712_message(self, attestation: Attestation) -> Dict[str, Any]:
        """
        Generate EIP-712 formatted message for Ethereum signing
        """
        return {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"}
                ],
                "Attestation": [
                    {"name": "attestationId", "type": "string"},
                    {"name": "timestamp", "type": "string"},
                    {"name": "computationHash", "type": "bytes32"},
                    {"name": "inputHash", "type": "bytes32"},
                    {"name": "outputHash", "type": "bytes32"}
                ]
            },
            "primaryType": "Attestation",
            "domain": {
                "name": "ArbiLens Protocol",
                "version": "1",
                "chainId": 1  # Ethereum mainnet
            },
            "message": {
                "attestationId": attestation.attestation_id,
                "timestamp": attestation.timestamp,
                "computationHash": f"0x{attestation.computation_hash}",
                "inputHash": f"0x{attestation.input_hash}",
                "outputHash": f"0x{attestation.output_hash}"
            }
        }
    
    def get_attestation_summary(self) -> Dict[str, Any]:
        """
        Get summary of all attestations
        """
        return {
            "total_attestations": len(self.attestation_log),
            "tee_public_key": self.tee_public_key,
            "latest_attestations": [
                {
                    "id": att.attestation_id,
                    "timestamp": att.timestamp,
                    "computation_hash": att.computation_hash[:16] + "..."
                }
                for att in self.attestation_log[-5:]  # Last 5
            ]
        }
    
    def simulate_remote_attestation(self) -> Dict[str, Any]:
        """
        Simulate remote attestation protocol
        Returns TEE identity and security properties
        """
        return {
            "tee_type": "Simulated SGX",
            "security_version": "2.0",
            "attestation_type": "EPID",
            "enclave_hash": hashlib.sha256(f"enclave_{time.time()}".encode()).hexdigest(),
            "platform_info": {
                "cpu_svn": "01020304050607080900010203040506",
                "pce_id": "0000",
                "sgx_enabled": True,
                "trusted_computing_base": "valid"
            },
            "quote": {
                "version": 3,
                "sign_type": 2,
                "epid_group_id": secrets.token_hex(4),
                "qe_svn": 7,
                "pce_svn": 10
            },
            "timestamp": datetime.now().isoformat(),
            "tee_public_key": self.tee_public_key
        }