import pytest
from domain.entities.threat import Threat
from domain.enums.threat_level import ThreatLevel
from domain.enums.threat_status import ThreatStatus
from domain.services.threat_scorer import ThreatScorerService

def make_threat(level: ThreatLevel) -> Threat:
    return Threat(
        id="test-1",
        source_ip="10.0.0.1",
        threat_type="malware",
        level=level,
        status=ThreatStatus.DETECTED,
        description="Test threat description for scoring.",
    )

def test_critical_threat_scores_above_90():
    scorer = ThreatScorerService()
    threat = make_threat(ThreatLevel.CRITICAL)
    score = scorer.calculate_risk_score(threat)
    assert score >= 90.0

def test_low_threat_scores_below_20():
    scorer = ThreatScorerService()
    threat = make_threat(ThreatLevel.LOW)
    score = scorer.calculate_risk_score(threat)
    assert score < 20.0

def test_score_never_exceeds_100():
    scorer = ThreatScorerService()
    threat = make_threat(ThreatLevel.CRITICAL)
    threat.description = "x" * 10000
    score = scorer.calculate_risk_score(threat)
    assert score <= 100.0
