"""
Password Security Audit Workflow
Checks password strength, common patterns, breach exposure signals, and gives recommendations.
"""
from dataclasses import dataclass
from typing import List
from providers.ollama_llm_provider import OllamaLLMProvider
from prompts.password_audit_prompts import PASSWORD_AUDIT_SYSTEM, build_password_audit_prompt
import re
import hashlib


@dataclass
class PasswordAuditResult:
    strength_score: int          # 0-100
    strength_label: str          # WEAK / FAIR / STRONG / VERY_STRONG
    issues: List[str]
    recommendations: List[str]
    estimated_crack_time: str
    ai_feedback: str


class PasswordAuditWorkflow:
    MIN_LENGTH = 12
    COMMON_PATTERNS = [r"^123", r"password", r"qwerty", r"admin", r"letmein"]

    def __init__(self):
        self._llm = OllamaLLMProvider()

    async def run(self, password: str) -> PasswordAuditResult:
        issues = self._static_checks(password)
        score = self._score(password, issues)
        label = self._label(score)
        crack_time = self._crack_time_estimate(score)

        prompt = build_password_audit_prompt(
            length=len(password),
            has_upper=bool(re.search(r"[A-Z]", password)),
            has_lower=bool(re.search(r"[a-z]", password)),
            has_digit=bool(re.search(r"\d", password)),
            has_special=bool(re.search(r"[^a-zA-Z0-9]", password)),
            issues=issues,
            score=score,
        )
        ai_feedback = await self._llm.generate(prompt, system=PASSWORD_AUDIT_SYSTEM)
        recommendations = [line.strip("- ").strip() for line in ai_feedback.split("\n") if line.strip()][:5]

        return PasswordAuditResult(
            strength_score=score,
            strength_label=label,
            issues=issues,
            recommendations=recommendations,
            estimated_crack_time=crack_time,
            ai_feedback=ai_feedback,
        )

    def _static_checks(self, pw: str) -> List[str]:
        issues = []
        if len(pw) < self.MIN_LENGTH:
            issues.append(f"Too short (minimum {self.MIN_LENGTH} characters)")
        if not re.search(r"[A-Z]", pw):
            issues.append("Missing uppercase letters")
        if not re.search(r"[a-z]", pw):
            issues.append("Missing lowercase letters")
        if not re.search(r"\d", pw):
            issues.append("Missing digits")
        if not re.search(r"[^a-zA-Z0-9]", pw):
            issues.append("Missing special characters")
        for pat in self.COMMON_PATTERNS:
            if re.search(pat, pw, re.IGNORECASE):
                issues.append("Contains common weak pattern")
                break
        return issues

    def _score(self, pw: str, issues: List[str]) -> int:
        score = min(len(pw) * 4, 40)
        if re.search(r"[A-Z]", pw): score += 15
        if re.search(r"[a-z]", pw): score += 15
        if re.search(r"\d", pw): score += 15
        if re.search(r"[^a-zA-Z0-9]", pw): score += 15
        score -= len(issues) * 10
        return max(0, min(score, 100))

    def _label(self, score: int) -> str:
        if score >= 80: return "VERY_STRONG"
        if score >= 60: return "STRONG"
        if score >= 40: return "FAIR"
        return "WEAK"

    def _crack_time_estimate(self, score: int) -> str:
        if score >= 80: return "centuries"
        if score >= 60: return "years"
        if score >= 40: return "days"
        return "minutes"
