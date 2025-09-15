# chimera/dcp.py
# Distributed Consensus Protocol for the Chimera agent.

import random
from typing import Dict, Any

class DistributedConsensusProtocol:
    def __init__(self, network_size: int = 50, consensus_threshold: float = 0.667):
        print("Initializing Distributed Consensus Protocol (DCP)...")
        if not (0 < consensus_threshold <= 1.0): raise ValueError("Consensus threshold must be between 0 and 1.")
        self.network_size, self.consensus_threshold = network_size, consensus_threshold
        print(f"DCP Initialized with {network_size} peers and a {consensus_threshold:.1%} approval threshold.")

    def propose_and_vote(self, validation_report: Dict[str, Any]) -> Dict[str, Any]:
        mutation_id = validation_report.get('mutation_id')
        print(f"\n--- Starting Consensus for Mutation {mutation_id} ---")
        approved = sum(1 for _ in range(self.network_size) if random.random() < 0.9)
        ratio = approved / self.network_size
        status = "ACCEPTED" if ratio >= self.consensus_threshold else "REJECTED"
        print(f"[DCP] Voting complete. Tally: {approved} APPROVE, {self.network_size - approved} REJECT. Ratio: {ratio:.1%}")
        print(f"[DCP] CONSENSUS {status}")
        return {"mutation_id": mutation_id, "proposal_status": status}
