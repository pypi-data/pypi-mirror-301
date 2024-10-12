import cvss as _cvss
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from fluidattacks_core.testing.constants import (
    CVSS3_VALUES,
    CVSS4_VALUES,
    FINDING_ID,
    FIXED_DATE,
    GROUP_NAME,
    ORG_ID,
    ORG_NAME,
    ROOT_ID,
)
from fluidattacks_core.testing.fakers.types import (
    SeverityLevelType,
)
from fluidattacks_core.testing.fakers.utils import (
    get_cvssf_score,
)
from typing import (
    Any,
)


def fake_severity_score(level: SeverityLevelType) -> dict[str, Any]:
    cvss3_vector = _cvss.CVSS3(CVSS3_VALUES[level])
    cvss4_vector = _cvss.CVSS4(CVSS4_VALUES[level])

    return {
        "cvssf": get_cvssf_score(cvss3_vector.temporal_score),
        "base_score": cvss3_vector.base_score,
        "temporal_score": cvss3_vector.temporal_score,
        "cvss_v3": cvss3_vector.clean_vector(),
        "threat_score": cvss3_vector.base_score,
        "cvssf_v4": get_cvssf_score(cvss4_vector.base_score),
        "cvss_v4": cvss4_vector.clean_vector(),
    }


def fake_stakeholder(
    user_email: str,
    name: str = "John Doe",
    role: str = "user",
    creation_date: str = FIXED_DATE,
) -> dict[str, Any]:
    date = datetime.fromisoformat(creation_date).isoformat()
    first_name, last_name = name.split(" ", 1)

    return {
        "role": role,
        "first_name": first_name,
        "last_name": last_name,
        "last_login_date": date,
        "registration_date": date,
        "sk": f"USER#{user_email}",
        "pk": f"USER#{user_email}",
        "sk_2": f"USER#{user_email}",
        "pk_2": "USER#all",
        "email": user_email,
        "enrolled": True,
        "legal_remember": True,
        "is_concurrent_session": False,
        "is_registered": True,
        "tours": {
            "new_group": False,
            "new_root": False,
            "new_risk_exposure": False,
            "welcome": False,
        },
        "state": {
            "modified_date": date,
            "modified_by": user_email,
            "notifications_preferences": {
                "sms": [],
                "email": [],
            },
        },
    }


def fake_organization(
    *,
    org_id: str = ORG_ID,
    org_name: str = ORG_NAME,
    modified_by: str = "jdoe@fluidattacks.com",
    creation_date: str = FIXED_DATE,
) -> dict[str, Any]:
    date = datetime.fromisoformat(creation_date).isoformat()
    aws_id = "97cf786e-a47e-4f15-b3f0-84eb920bc774"

    return {
        "pk": f"ORG#{org_id}",
        "sk": f"ORG#{org_name}",
        "name": org_name,
        "created_date": date,
        "id": org_id,
        "pk_2": "ORG#all",
        "sk_2": f"ORG#{org_id}",
        "state": {
            "aws_external_id": aws_id,
            "modified_by": modified_by,
            "modified_date": date,
            "status": "ACTIVE",
        },
        "policies": {
            "inactivity_period": 90,
            "modified_by": modified_by,
            "min_breaking_severity": Decimal("0.0"),
            "modified_date": date,
            "min_acceptance_severity": Decimal("0.0"),
            "max_acceptance_severity": Decimal("10.0"),
        },
        "country": "Colombia",
        "created_by": modified_by,
    }


def fake_stakeholder_organization_access(
    *,
    stakeholder: str,
    role: str = "user",
    grant: bool = True,
    org_id: str = ORG_ID,
    creation_date: str = FIXED_DATE,
) -> dict[str, Any]:
    date = datetime.fromisoformat(creation_date).isoformat()
    return {
        "sk": f"ORG#{org_id}",
        "pk": f"USER#{stakeholder}",
        "state": {
            "modified_by": stakeholder,
            "role": role,
            "has_access": grant,
            "modified_date": date,
        },
        "email": stakeholder,
        "organization_id": org_id,
    }


def fake_finding(
    finding_id: str = FINDING_ID,
    group_name: str = GROUP_NAME,
    creation_date: str = FIXED_DATE,
) -> dict[str, Any]:
    date = datetime.fromisoformat(creation_date).isoformat()

    return {
        "id": finding_id,
        "pk": f"FIN#{finding_id}",
        "sk": f"GROUP#{group_name}",
        "state": {
            "modified_by": "integratesmanager@gmail.com",
            "justification": "NO_JUSTIFICATION",
            "source": "ASM",
            "modified_date": date,
            "status": "CREATED",
        },
        "unreliable_indicators": {
            "open_vulnerabilities": 0,
            "closed_vulnerabilities": 0,
            "submitted_vulnerabilities": 0,
            "rejected_vulnerabilities": 0,
            "unreliable_status": "VULNERABLE",
            "oldest_vulnerability_report_date": date,
            "newest_vulnerability_report_date": date,
            "max_open_severity_score": Decimal("7.3"),
            "max_open_severity_score_v4": Decimal("6.9"),
            "max_open_epss": 0,
            "max_open_root_criticality": "LOW",
            "treatment_summary": {
                "untreated": 0,
                "in_progress": 0,
                "accepted": 0,
                "accepted_undefined": 0,
            },
            "verification_summary": {
                "requested": 0,
                "on_hold": 0,
                "verified": 0,
                "masked": 0,
            },
            "vulnerabilities_summary": {
                "closed": 0,
                "open": 0,
                "submitted": 0,
                "rejected": 0,
                "open_critical": 0,
                "open_high": 0,
                "open_low": 0,
                "open_medium": 0,
                "open_critical_v3": 0,
                "open_high_v3": 0,
                "open_low_v3": 0,
                "open_medium_v3": 0,
            },
            "total_open_cvssf": Decimal("0.0"),
            "total_open_cvssf_v4": Decimal("0.0"),
        },
        "group_name": group_name,
        "severity_score": fake_severity_score("low"),
        "description": "Test finding",
        "title": "999 - Test finding",
        "evidences": {},
        "recommendation": "",
        "requirements": "",
        "threat": "",
        "creation": {
            "modified_by": "integratesmanager@gmail.com",
            "justification": "NO_JUSTIFICATION",
            "source": "ASM",
            "modified_date": date,
            "status": "CREATED",
        },
        "sorts": "NO",
        "attack_vector_description": "",
        "min_time_to_remediate": 1,
        "verification": None,
        "unfulfilled_requirements": [],
    }


def fake_git_root(
    *,
    root_id: str = ROOT_ID,
    nickname: str = "root_1",
    url: str = "https://gitlab.com/fluidattacks/universe.git",
    branch: str = "master",
    status: str = "ACTIVE",
    group_name: str = GROUP_NAME,
    org_name: str = ORG_NAME,
    modified_by: str = "jdoe@fluidattacks.com",
    commit_date: str = FIXED_DATE,
) -> dict[str, Any]:
    date = datetime.fromisoformat(commit_date).isoformat()

    return {
        "pk": f"ROOT#{root_id}",
        "sk": f"GROUP#{group_name}",
        "pk_2": f"ORG#{org_name}",
        "sk_2": f"ROOT#{root_id}",
        "created_date": date,
        "state": {
            "credential_id": "0df32c4a-526d-4879-8dc8-9ae191d2721b",
            "criticality": "HIGH",
            "environment": "production",
            "gitignore": [],
            "includes_health_check": True,
            "modified_by": modified_by,
            "nickname": nickname,
            "environment_urls": [],
            "modified_date": date,
            "branch": branch,
            "url": url,
            "status": status,
        },
        "unreliable_indicators": {"unreliable_last_status_update": date},
        "type": "Git",
        "created_by": modified_by,
        "cloning": {
            "commit": "98dbb971caf519fb6c56c67df7e02b253fd5a97f",
            "commit_date": date,
            "reason": "root OK",
            "modified_by": modified_by,
            "modified_date": date,
            "status": "OK",
        },
    }
