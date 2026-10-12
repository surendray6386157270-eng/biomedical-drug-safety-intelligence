from __future__ import annotations

from collections import Counter
from typing import Any


def analyze_drug_reactions(
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Analyze observed reaction patterns in normalized evidence.

    This is descriptive analysis only. It does not establish
    causation, incidence, clinical risk, or safety.
    """

    if not evidence:
        return {
            "total_records": 0,
            "unique_reactions": 0,
            "top_reactions": [],
            "limitations": [
                "No evidence records were available for analysis."
            ],
        }

    reactions = [
        str(item["reaction"]).strip()
        for item in evidence
        if item.get("reaction")
        and str(item["reaction"]).strip()
    ]

    counts = Counter(reactions)
    total = len(evidence)

    top_reactions = []

    for reaction, count in counts.most_common(10):
        top_reactions.append(
            {
                "reaction": reaction,
                "count": count,
                "proportion": round(count / total, 4),
            }
        )

    return {
        "total_records": total,
        "unique_reactions": len(counts),
        "top_reactions": top_reactions,
        "limitations": [
            "This analysis describes patterns in the acquired "
            "FAERS evidence.",
            "Report frequency is not incidence.",
            "The analysis does not establish causation.",
            "The analysis does not determine whether a drug "
            "is safe or unsafe.",
        ],
    }