from app.analytics.drug_reaction import analyze_drug_reactions


def test_analyze_drug_reactions():
    evidence = [
        {
            "drug_name": "ASPIRIN",
            "reaction": "Headache",
        },
        {
            "drug_name": "ASPIRIN",
            "reaction": "Headache",
        },
        {
            "drug_name": "ASPIRIN",
            "reaction": "Nausea",
        },
    ]

    result = analyze_drug_reactions(evidence)

    assert result["total_records"] == 3
    assert result["unique_reactions"] == 2

    assert result["top_reactions"][0]["reaction"] == "Headache"
    assert result["top_reactions"][0]["count"] == 2
    assert result["top_reactions"][0]["proportion"] == 0.6667


def test_empty_evidence():
    result = analyze_drug_reactions([])

    assert result["total_records"] == 0
    assert result["unique_reactions"] == 0
    assert result["top_reactions"] == []
    assert len(result["limitations"]) > 0
