"""
Blockchain Logger for ArbiLens Protocol
Simulates on-chain logging of attestations and arbitrage records
For hackathon: Mock blockchain with local storage
"""

import json
import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class BlockchainTransaction:
    """Represents a blockchain transaction"""
    tx_hash: str
    block_number: int
    timestamp: str
    from_address: str
    to_address: str
    data: Dict[str, Any]
    gas_used: int
    status: str  # success, failed, pending


@dataclass
class ComplianceRecord:
    """On-chain record of a compliance evaluation"""
    record_id: str
    strategy_id: str
    attestation_hash: str
    expected_value: float
    decision: str
    jurisdiction: str
    timestamp: str
    ipfs_cid: Optional[str] = None


class BlockchainLogger:
    """
    Simulates blockchain logging for transparency
    In production, this would interact with actual smart contracts
    """
    
    def __init__(self, chain_id: int = 1):
        self.chain_id = chain_id
        self.current_block = 1000000  # Starting block number
        self.contract_address = "0x" + "a" * 40  # Mock contract address
        self.transactions = []
        self.compliance_records = {}
        self.ipfs_store = {}  # Simulated IPFS storage
    
    def log_compliance_evaluation(self,
                                strategy_id: str,
                                attestation_hash: str,
                                expected_value: float,
                                decision: str,
                                jurisdiction: str,
                                full_report: Dict[str, Any]) -> BlockchainTransaction:
        """
        Log compliance evaluation on-chain
        
        Args:
            strategy_id: Unique strategy identifier
            attestation_hash: Hash from TEE attestation
            expected_value: Calculated EV
            decision: EXECUTE/CAUTION/AVOID
            jurisdiction: Target jurisdiction
            full_report: Complete evaluation report
        
        Returns:
            Blockchain transaction record
        """
        
        # Store full report in "IPFS"
        ipfs_cid = self._store_to_ipfs(full_report)
        
        # Create on-chain record (minimal data to save gas)
        record = ComplianceRecord(
            record_id=f"COMP-{uuid.uuid4().hex[:8]}",
            strategy_id=strategy_id,
            attestation_hash=attestation_hash,
            expected_value=expected_value,
            decision=decision,
            jurisdiction=jurisdiction,
            timestamp=datetime.now().isoformat(),
            ipfs_cid=ipfs_cid
        )
        
        # Create transaction
        tx = self._create_transaction(
            method="logCompliance",
            params=asdict(record)
        )
        
        # Store record
        self.compliance_records[record.record_id] = record
        
        return tx
    
    def _store_to_ipfs(self, data: Dict[str, Any]) -> str:
        """
        Simulate IPFS storage
        Returns CID (Content Identifier)
        """
        # Create deterministic CID based on content
        content = json.dumps(data, sort_keys=True, default=str)
        cid = "Qm" + hashlib.sha256(content.encode()).hexdigest()[:44]
        
        # Store in simulated IPFS
        self.ipfs_store[cid] = data
        
        return cid
    
    def retrieve_from_ipfs(self, cid: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from simulated IPFS
        """
        return self.ipfs_store.get(cid)
    
    def _create_transaction(self,
                           method: str,
                           params: Dict[str, Any]) -> BlockchainTransaction:
        """
        Create a blockchain transaction
        """
        # Increment block number
        self.current_block += 1
        
        # Create transaction hash
        tx_data = f"{method}:{json.dumps(params, sort_keys=True)}"
        tx_hash = "0x" + hashlib.sha256(tx_data.encode()).hexdigest()
        
        # Create transaction
        tx = BlockchainTransaction(
            tx_hash=tx_hash,
            block_number=self.current_block,
            timestamp=datetime.now().isoformat(),
            from_address="0x" + "f" * 40,  # Mock user address
            to_address=self.contract_address,
            data={"method": method, "params": params},
            gas_used=50000 + len(json.dumps(params)) * 10,  # Mock gas calculation
            status="success"
        )
        
        # Store transaction
        self.transactions.append(tx)
        
        return tx
    
    def query_compliance_records(self,
                               jurisdiction: Optional[str] = None,
                               decision: Optional[str] = None,
                               min_value: Optional[float] = None) -> List[ComplianceRecord]:
        """
        Query on-chain compliance records with filters
        """
        records = list(self.compliance_records.values())
        
        # Apply filters
        if jurisdiction:
            records = [r for r in records if r.jurisdiction == jurisdiction]
        
        if decision:
            records = [r for r in records if r.decision == decision]
        
        if min_value is not None:
            records = [r for r in records if r.expected_value >= min_value]
        
        # Sort by timestamp (newest first)
        records.sort(key=lambda r: r.timestamp, reverse=True)
        
        return records
    
    def get_transparency_dashboard(self) -> Dict[str, Any]:
        """
        Generate transparency dashboard data
        Shows aggregate statistics of compliance evaluations
        """
        records = list(self.compliance_records.values())
        
        if not records:
            return {
                "total_evaluations": 0,
                "jurisdictions": {},
                "decisions": {},
                "average_ev": 0,
                "total_gas_used": 0
            }
        
        # Aggregate by jurisdiction
        jurisdictions = {}
        for record in records:
            if record.jurisdiction not in jurisdictions:
                jurisdictions[record.jurisdiction] = {"count": 0, "total_ev": 0}
            jurisdictions[record.jurisdiction]["count"] += 1
            jurisdictions[record.jurisdiction]["total_ev"] += record.expected_value
        
        # Aggregate by decision
        decisions = {"EXECUTE": 0, "CAUTION": 0, "AVOID": 0}
        for record in records:
            if record.decision in decisions:
                decisions[record.decision] += 1
        
        # Calculate averages
        total_ev = sum(r.expected_value for r in records)
        average_ev = total_ev / len(records) if records else 0
        
        # Total gas used
        total_gas = sum(tx.gas_used for tx in self.transactions)
        
        return {
            "total_evaluations": len(records),
            "jurisdictions": jurisdictions,
            "decisions": decisions,
            "average_ev": average_ev,
            "total_ev": total_ev,
            "total_gas_used": total_gas,
            "latest_block": self.current_block,
            "contract_address": self.contract_address
        }
    
    def simulate_regulatory_query(self) -> Dict[str, Any]:
        """
        Simulate a regulator querying the system
        Returns aggregated compliance insights
        """
        records = list(self.compliance_records.values())
        
        # Find successful compliant strategies (high EV with EXECUTE decisions)
        successful_strategies = [
            r for r in records 
            if r.decision == "EXECUTE" and r.expected_value > 100000
        ]
        
        # Group by jurisdiction
        jurisdiction_risks = {}
        for record in records:
            if record.jurisdiction not in jurisdiction_risks:
                jurisdiction_risks[record.jurisdiction] = {
                    "high_risk_count": 0,
                    "total_count": 0,
                    "average_ev": 0
                }
            
            jurisdiction_risks[record.jurisdiction]["total_count"] += 1
            
            if record.decision == "EXECUTE" and record.expected_value > 50000:
                jurisdiction_risks[record.jurisdiction]["high_risk_count"] += 1
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_strategies_evaluated": len(records),
            "successful_strategies": len(successful_strategies),
            "jurisdiction_activity_map": jurisdiction_risks,
            "high_value_opportunities": [
                {
                    "record_id": r.record_id,
                    "jurisdiction": r.jurisdiction,
                    "expected_value": r.expected_value,
                    "ipfs_cid": r.ipfs_cid
                }
                for r in successful_strategies[:10]  # Top 10
            ],
            "recommendation": "Review successful strategies to understand compliant market opportunities"
        }
    
    def export_attestation_log(self) -> List[Dict[str, Any]]:
        """
        Export all attestations for audit
        """
        return [
            {
                "tx_hash": tx.tx_hash,
                "block_number": tx.block_number,
                "timestamp": tx.timestamp,
                "method": tx.data["method"],
                "gas_used": tx.gas_used,
                "status": tx.status
            }
            for tx in self.transactions
        ]