from __future__ import annotations

from typing import Any

from app.analytics.drug_reaction import analyze_drug_reactions
from app.services.search import search_drug_evidence


def analyze_drug(
    drug_name: str,
    limit: int = 100,
) -> dict[str, Any]:
    """Run drug-reaction analysis over stored evidence."""

    evidence = search_drug_evidence(
        drug_name=drug_name,
        limit=limit,
    )

    analysis = analyze_drug_reactions(evidence)

    return {
        "drug_name": drug_name.strip(),
        "analysis_type": "descriptive_drug_reaction_analysis",
        "input_evidence_count": len(evidence),
        "analysis": analysis,
        "evidence": evidence,
        "source": "FDA FAERS / openFDA",
    }