# pylint: disable=too-few-public-methods,too-many-arguments
from decimal import (
    Decimal,
)
from fluidattacks_core.testing.constants import (
    CREATED_BY,
    FIXED_DATE,
)
from fluidattacks_core.testing.fakers.entities import (
    fake_severity_score,
)
from fluidattacks_core.testing.fakers.types import (
    SeverityLevelType,
    TreatmentStatusType,
)
from fluidattacks_core.types.dynamo.items import (
    Policies,
    ToeInputMetadataItem,
)
from typing import (
    Any,
    Callable,
    Self,
)


class MetaBuilder(type):
    """
    Metaclass for implementing `set_` methods for every attribute in the class
    dynamically.

    Type annotations and expected value types for every set method
    must be defined in the class.
    """

    def __new__(mcs, name: str, bases: tuple, dct: dict) -> type:  # noqa: N804
        for attr in dct.get("__annotations__", {}):
            if attr.startswith("_") or attr.startswith("set_"):
                continue

            dct[f"set_{attr}"] = lambda self, value, attr=attr: (
                setattr(self, attr, value),  # type: ignore
                self,
            )[1]
        return super().__new__(mcs, name, bases, dct)


class OrganizationFaker(metaclass=MetaBuilder):
    # Required attributes
    org_id: str
    org_name: str

    # Optional attributes
    created_by: str = CREATED_BY
    creation_date: str = FIXED_DATE
    country: str = "Colombia"
    status: str = "ACTIVE"
    aws_external_id: str = "ce5a4871-850f-48ee-bb6e-4bde918fe589"
    pending_deletion_date: str = ""
    policies: Policies = {
        "days_until_it_breaks": 90,
        "max_acceptance_days": 0,
        "max_number_acceptances": 0,
        "vulnerability_grace_period": 0,
        "inactivity_period": 90,
        "modified_by": "unknown",
        "min_breaking_severity": Decimal("0.0"),
        "modified_date": "2019-11-22T20:07:57+00:00",
        "min_acceptance_severity": Decimal("0.0"),
        "max_acceptance_severity": Decimal("10.0"),
    }

    # Setters
    # Meta methods must be defined for linting support
    set_created_by: Callable[[str], Self]
    set_creation_date: Callable[[str], Self]
    set_country: Callable[[str], Self]
    set_status: Callable[[str], Self]
    set_aws_external_id: Callable[[str], Self]
    set_pending_deletion_date: Callable[[str], Self]
    set_policies: Callable[[Policies], Self]

    def __init__(self, org_id: str, org_name: str) -> None:
        self.org_id = org_id
        self.org_name = org_name

    def build(self) -> dict[str, Any]:
        return {
            "pk": f"ORG#{self.org_id}",
            "sk": f"ORG#{self.org_name}",
            "name": self.org_name,
            "created_date": self.creation_date,
            "id": self.org_id,
            "pk_2": "ORG#all",
            "sk_2": f"ORG#{self.org_id}",
            "state": {
                "pending_deletion_date": self.pending_deletion_date,
                "aws_external_id": self.aws_external_id,
                "modified_by": self.created_by,
                "modified_date": self.creation_date,
                "status": self.status,
            },
            "policies": self.policies,
            "country": self.country,
            "created_by": self.created_by,
        }


class GroupFaker(metaclass=MetaBuilder):
    # Required attributes
    org_id: str
    group_name: str

    # Optional attributes
    created_by: str = CREATED_BY
    creation_date: str = FIXED_DATE
    description: str = "Test group"
    language: str = "EN"
    tier: str = "ADVANCED"
    managed: str = "MANAGED"
    service: str = "WHITE"
    tags: list[str] = ["test-group"]
    subscription_type: str = "CONTINUOUS"
    status: str = "ACTIVE"
    business_id: str = "14441323"
    business_name: str = "Example ABC Inc."
    sprint_duration: int = 2
    policies: dict[str, str | int | Decimal] = {
        "max_number_acceptances": 3,
        "min_acceptance_severity": Decimal("0.0"),
        "vulnerability_grace_period": Decimal("10"),
        "min_breaking_severity": Decimal("3.9"),
        "max_acceptance_days": 90,
        "max_acceptance_severity": Decimal("3.9"),
        "modified_by": "unknown@fluidattacks.com",
        "modified_date": FIXED_DATE,
    }

    # Setters
    # Meta methods must be defined for linting support
    set_created_by: Callable[[str], Self]
    set_creation_date: Callable[[str], Self]
    set_description: Callable[[str], Self]
    set_language: Callable[[str], Self]
    set_tier: Callable[[str], Self]
    set_managed: Callable[[str], Self]
    set_service: Callable[[str], Self]
    set_tags: Callable[[list[str]], Self]
    set_subscription_type: Callable[[str], Self]
    set_status: Callable[[str], Self]
    set_business_id: Callable[[str], Self]
    set_business_name: Callable[[str], Self]
    set_sprint_duration: Callable[[int], Self]
    set_policies: Callable[[dict[str, str | int | Decimal]], Self]

    def __init__(
        self,
        org_id: str,
        group_name: str,
    ) -> None:
        self.org_id = org_id
        self.group_name = group_name

    def build(self) -> dict[str, Any]:
        return {
            "pk": f"GROUP#{self.group_name}",
            "sk": f"ORG#{self.org_id}",
            "name": self.group_name,
            "description": self.description,
            "language": self.language,
            "created_by": self.created_by,
            "created_date": self.creation_date,
            "state": {
                "modified_by": self.created_by,
                "modified_date": self.creation_date,
                "has_advanced": self.tier == "ADVANCED",
                "tier": self.tier,
                "managed": self.managed,
                "service": self.service,
                "has_essential": self.tier in ["ESSENTIAL", "ADVANCED"],
                "type": self.subscription_type,
                "status": self.status,
                **({"tags": self.tags} if self.tags else {}),
            },
            "organization_id": self.org_id,
            "business_id": self.business_id,
            "business_name": self.business_name,
            "sprint_duration": self.sprint_duration,
            "policies": self.policies,
        }


class VulnerabilityFaker(metaclass=MetaBuilder):
    # Required attributes
    vuln_id: str
    finding_id: str
    root_id: str
    group_name: str
    org_name: str

    # Optional attributes
    created_by: str = CREATED_BY
    creation_date: str = FIXED_DATE
    vuln_type: str = "LINES"
    vuln_technique: str = "SCA"
    report_date: str = FIXED_DATE
    source: str = "MACHINE"
    priority: int = 125
    efficacy: int = 0
    reattack_cycles: int = 0
    treatment_changes: int = 0
    where: str = "scanners/skipfish/Dockerfile"
    specific: str = "1"
    commit: str = "356a192b7913b04c54574d18c28d46e6395428ab"
    status: str = "VULNERABLE"
    zero_risk: dict[str, Any] | None = None
    severity_level: SeverityLevelType | None = None
    webhook_url: str | None = None
    bug_tracking_system_url: str | None = None
    treatment_status: TreatmentStatusType = "UNTREATED"

    # Setters
    # Meta methods must be defined for linting support
    set_created_by: Callable[[str], Self]
    set_creation_date: Callable[[str], Self]
    set_vuln_type: Callable[[str], Self]
    set_vuln_technique: Callable[[str], Self]
    set_report_date: Callable[[str], Self]
    set_source: Callable[[str], Self]
    set_priority: Callable[[int], Self]
    set_efficacy: Callable[[int], Self]
    set_reattack_cycles: Callable[[int], Self]
    set_treatment_changes: Callable[[int], Self]
    set_where: Callable[[str], Self]
    set_specific: Callable[[str], Self]
    set_commit: Callable[[str], Self]
    set_status: Callable[[str], Self]
    set_zero_risk: Callable[[dict[str, Any] | None], Self]
    set_severity_level: Callable[[SeverityLevelType], Self]
    set_webhook_url: Callable[[str], Self]
    set_bug_tracking_system_url: Callable[[str], Self]
    set_treatment_status: Callable[[TreatmentStatusType], Self]

    def __init__(
        self,
        vuln_id: str,
        finding_id: str,
        root_id: str,
        group_name: str,
        org_name: str,
    ) -> None:
        self.vuln_id = vuln_id
        self.finding_id = finding_id
        self.root_id = root_id
        self.group_name = group_name
        self.org_name = org_name

    def build(self) -> dict[str, Any]:
        deleted = str(self.status == "DELETED").lower()
        released = str(self.status in ["VULNERABLE", "SAFE"]).lower()

        return {
            "created_by": self.created_by,
            "created_date": self.creation_date,
            "pk": f"VULN#{self.vuln_id}",
            "sk": f"FIN#{self.finding_id}",
            "pk_2": f"ROOT#{self.root_id}",
            "sk_2": f"VULN#{self.vuln_id}",
            "pk_3": "USER",
            "sk_3": f"VULN#{self.vuln_id}",
            "pk_5": f"GROUP#{self.group_name}",
            "sk_5": (
                f"VULN#ZR#{bool(self.zero_risk)}#"
                f"STATE#{self.status.lower()}#TREAT#false"
            ),
            "pk_6": f"FIN#{self.finding_id}",
            "sk_6": (
                f"VULN#DELETED#{deleted}#RELEASED#{released}#"
                f"ZR#{bool(self.zero_risk)}#"
                f"STATE#{self.status.lower()}#VERIF#none"
            ),
            "treatment": {
                "modified_date": self.creation_date,
                "status": self.treatment_status,
            },
            "hacker_email": self.created_by,
            "group_name": self.group_name,
            "organization_name": self.org_name,
            "type": self.vuln_type,
            "technique": self.vuln_technique,
            "root_id": self.root_id,
            "unreliable_indicators": {
                "unreliable_reattack_cycles": self.reattack_cycles,
                "unreliable_source": self.source,
                "unreliable_efficacy": self.efficacy,
                "unreliable_priority": self.priority,
                "unreliable_report_date": self.report_date,
                "unreliable_treatment_changes": self.treatment_changes,
            },
            "state": {
                "modified_by": self.created_by,
                "commit": self.commit,
                "where": self.where,
                "source": self.source,
                "modified_date": self.creation_date,
                "specific": self.specific,
                "status": self.status,
            },
            **({"webhook_url": self.webhook_url} if self.webhook_url else {}),
            **(
                {"bug_tracking_system_url": self.bug_tracking_system_url}
                if self.bug_tracking_system_url
                else {}
            ),
            **(
                {"severity_score": fake_severity_score(self.severity_level)}
                if self.severity_level
                else {}
            ),
            **({"zero_risk": self.zero_risk} if self.zero_risk else {}),
        }


class FindingFaker(metaclass=MetaBuilder):
    # Required attributes
    finding_id: str
    group_name: str

    # Optional attributes
    title: str = "038. Business information leak"
    description: str = "Test finding"
    recommendation: str = "Test recommendation"
    justification: str = "NO_JUSTIFICATION"
    source: str = "ASM"
    status: str = "CREATED"
    created_by: str = CREATED_BY
    creation_date: str = FIXED_DATE
    cvss_version: str = "3.1"
    threat: str = "Risk."
    min_time_to_remediate: int = 18
    attack_vector_description: str = "Network"
    severity_level: SeverityLevelType = "low"
    sorts: str = "NO"
    requirements: str = (
        "REQ.0176. El sistema debe restringir el acceso a objetos del "
        "sistema que tengan contenido sensible. Sólo permitirá su acceso "
        "a usuarios autorizados."
    )
    unfulfilled_requirements: list[str] = [
        "176",
        "177",
        "261",
        "300",
    ]
    unreliable_indicators: dict[str, Any] = {
        "total_open_priority": 0,
        "unreliable_status": "SAFE",
        "unreliable_total_open_cvssf": Decimal("0.0"),
        "unreliable_where": "192.168.1.10",
        "unreliable_newest_vulnerability_report_date": FIXED_DATE,
        "unreliable_verification_summary": {
            "verified": 0,
            "requested": 0,
            "on_hold": 0,
        },
        "unreliable_oldest_vulnerability_report_date": FIXED_DATE,
        "unreliable_oldest_open_vulnerability_report_date": FIXED_DATE,
    }
    evidences: dict[str, Any] = {
        "exploitation": {
            "modified_date": FIXED_DATE,
            "description": "ABC",
            "url": "unittesting-436992569-exploitation.png",
        },
        "evidence1": {
            "modified_date": FIXED_DATE,
            "description": "DEF",
            "url": "unittesting-436992569-evidence_route_1.png",
        },
    }

    # Setters
    # Meta methods must be defined for linting support
    set_title: Callable[[str], Self]
    set_description: Callable[[str], Self]
    set_recommendation: Callable[[str], Self]
    set_justification: Callable[[str], Self]
    set_source: Callable[[str], Self]
    set_status: Callable[[str], Self]
    set_created_by: Callable[[str], Self]
    set_creation_date: Callable[[str], Self]
    set_cvss_version: Callable[[str], Self]
    set_threat: Callable[[str], Self]
    set_min_time_to_remediate: Callable[[int], Self]
    set_attack_vector_description: Callable[[str], Self]
    set_severity_level: Callable[[SeverityLevelType], Self]
    set_sorts: Callable[[str], Self]
    set_requirements: Callable[[str], Self]
    set_unfulfilled_requirements: Callable[[list[str]], Self]
    set_unreliable_indicators: Callable[[dict[str, Any]], Self]
    set_evidences: Callable[[dict[str, Any]], Self]

    def __init__(self, finding_id: str, group_name: str) -> None:
        self.finding_id = finding_id
        self.group_name = group_name

    def build(self) -> dict[str, Any]:
        return {
            "requirements": self.requirements,
            "group_name": self.group_name,
            "unfulfilled_requirements": self.unfulfilled_requirements,
            "description": self.description,
            "recommendation": self.recommendation,
            "unreliable_indicators": self.unreliable_indicators,
            "title": self.title,
            "cvss_version": self.cvss_version,
            "sk": f"GROUP#{self.group_name}",
            "id": self.finding_id,
            "pk": f"FIN#{self.finding_id}",
            "state": {
                "modified_by": self.created_by,
                "justification": self.justification,
                "source": self.source,
                "modified_date": self.creation_date,
                "status": self.status,
            },
            "threat": self.threat,
            "evidences": self.evidences,
            "min_time_to_remediate": self.min_time_to_remediate,
            "sorts": self.sorts,
            "attack_vector_description": self.attack_vector_description,
            "creation": {
                "modified_by": self.created_by,
                "modified_date": self.creation_date,
                "justification": self.justification,
                "source": self.source,
                "status": "CREATED",
            },
            "severity_score": fake_severity_score(self.severity_level),
        }


class GitRootFaker(metaclass=MetaBuilder):
    # Required attributes
    root_id: str
    group_name: str
    org_name: str

    # Optional attributes
    nickname: str | None = None
    created_by: str = CREATED_BY
    creation_date: str = FIXED_DATE
    environment: str = "QA"
    url: str = "https://github.com/fluidattacks/makes"
    branch: str = "trunk"
    status: str = "ACTIVE"
    gitignore: list[str] = []
    environment_urls: list[str] = []

    commit: str = "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"
    cloning_reason: str = "changes"
    cloning_status: str = "UNKNOWN"

    machine_reason: str = "changes"
    machine_status: str = "FAILED"
    machine_executions_date: dict[str, str] = {
        "apk": FIXED_DATE,
        "cspm": FIXED_DATE,
        "dast": FIXED_DATE,
        "sast": FIXED_DATE,
        "sca": FIXED_DATE,
    }

    # Setters
    # Meta methods must be defined for linting support
    set_nickname: Callable[[str | None], Self]
    set_created_by: Callable[[str], Self]
    set_creation_date: Callable[[str], Self]
    set_environment: Callable[[str], Self]
    set_url: Callable[[str], Self]
    set_branch: Callable[[str], Self]
    set_status: Callable[[str], Self]
    set_gitignore: Callable[[list[str]], Self]
    set_environment_urls: Callable[[list[str]], Self]
    set_commit: Callable[[str], Self]
    set_cloning_reason: Callable[[str], Self]
    set_cloning_status: Callable[[str], Self]
    set_machine_reason: Callable[[str], Self]
    set_machine_status: Callable[[str], Self]
    set_machine_executions_date: Callable[[dict[str, str]], Self]

    def __init__(self, root_id: str, group_name: str, org_name: str) -> None:
        self.root_id = root_id
        self.group_name = group_name
        self.org_name = org_name

    def build(self) -> dict[str, Any]:
        return {
            "pk": f"ROOT#{self.root_id}",
            "sk": f"GROUP#{self.group_name}",
            "pk_2": f"ORG#{self.org_name}",
            "sk_2": f"ROOT#{self.root_id}",
            "created_date": self.creation_date,
            "created_by": self.created_by,
            "type": "Git",
            "state": {
                "environment": self.environment,
                "includes_health_check": False,
                "modified_by": self.created_by,
                "nickname": self.nickname or self.root_id,
                "modified_date": self.creation_date,
                "branch": self.branch,
                "url": self.url,
                "status": self.status,
                "gitignore": self.gitignore,
                "environment_urls": self.environment_urls,
            },
            "unreliable_indicators": {
                "unreliable_last_status_update": self.creation_date
            },
            "cloning": {
                "commit": self.commit,
                "commit_date": self.creation_date,
                "reason": self.cloning_reason,
                "modified_by": "machine@fluidattacks.com",
                "modified_date": self.creation_date,
                "status": self.cloning_status,
            },
            "machine": {
                "commit": self.commit,
                "commit_date": self.creation_date,
                "modified_by": "machine@fluidattacks.com",
                "modified_date": self.creation_date,
                "reason": self.machine_reason,
                "status": self.machine_status,
                "last_executions_date": self.machine_executions_date,
            },
        }


class EnvironmentUrlFaker(metaclass=MetaBuilder):
    # Required attributes
    env_id: str
    url: str
    root_id: str
    group_name: str

    # Optional attributes
    created_by: str = CREATED_BY
    creation_date: str = FIXED_DATE
    include: bool = True

    # Setters
    # Meta methods must be defined for linting support
    set_created_by: Callable[[str], Self]
    set_creation_date: Callable[[str], Self]
    set_include: Callable[[bool], Self]

    def __init__(
        self, env_id: str, url: str, group_name: str, root_id: str
    ) -> None:
        self.env_id = env_id
        self.url = url
        self.group_name = group_name
        self.root_id = root_id

    def build(self) -> dict[str, Any]:
        return {
            "pk": f"GROUP#{self.group_name}#ROOT#{self.root_id}",
            "sk": f"URL#{self.env_id}",
            "pk_2": f"GROUP#{self.group_name}",
            "sk_2": f"URL#{self.env_id}",
            "group_name": self.group_name,
            "id": self.env_id,
            "root_id": self.root_id,
            "state": {
                "modified_by": self.created_by,
                "include": self.include,
                "modified_date": self.creation_date,
                "url_type": "URL",
                "status": "CREATED",
            },
            "url": self.url,
        }


class ToeInputFaker(metaclass=MetaBuilder):
    # Required attributes
    root_id: str
    group_name: str
    component: str
    entry_point: str

    # Optional attributes
    created_by: str = CREATED_BY
    creation_date: str = FIXED_DATE
    be_present: bool = True
    has_vulnerabilities: bool = False
    be_present_until: str = FIXED_DATE
    seen_first_time_by: str = CREATED_BY
    seen_at: str = FIXED_DATE
    attacked_by: str = CREATED_BY
    attacked_at: str = FIXED_DATE
    first_attack_at: str = FIXED_DATE
    modified_by: str = CREATED_BY
    modified_date: str = FIXED_DATE

    # Setters
    # Meta methods must be defined for linting support
    set_created_by: Callable[[str], Self]
    set_creation_date: Callable[[str], Self]
    set_be_present: Callable[[bool], Self]
    set_has_vulnerabilities: Callable[[bool], Self]
    set_be_present_until: Callable[[str], Self]
    set_seen_first_time_by: Callable[[str], Self]
    set_seen_at: Callable[[str], Self]
    set_attacked_by: Callable[[str], Self]
    set_attacked_at: Callable[[str], Self]
    set_first_attack_at: Callable[[str], Self]
    set_modified_by: Callable[[str], Self]
    set_modified_date: Callable[[str], Self]

    def __init__(
        self,
        root_id: str,
        group_name: str,
        component: str,
        entry_point: str,
    ) -> None:
        self.root_id = root_id
        self.group_name = group_name
        self.component = component
        self.entry_point = entry_point

    def build(self) -> ToeInputMetadataItem:
        return {
            "group_name": self.group_name,
            "pk": f"GROUP#{self.group_name}",
            "sk": (
                f"INPUTS#ROOT#{self.root_id}#COMPONENT#{self.component}"
                f"#ENTRYPOINT#{self.entry_point}"
            ),
            "pk_2": f"GROUP#{self.group_name}",
            "sk_2": (
                f"INPUTS#PRESENT#{str(self.be_present).lower()}"
                f"#ROOT#{self.root_id}"
                f"#COMPONENT#{self.component}#ENTRYPOINT#{self.entry_point}"
            ),
            "root_id": self.root_id,
            "component": self.component,
            "entry_point": self.entry_point,
            "state": {
                "be_present": self.be_present,
                "has_vulnerabilities": self.has_vulnerabilities,
                "be_present_until": self.creation_date,
                "seen_first_time_by": self.seen_first_time_by,
                "seen_at": self.seen_at,
                "attacked_by": self.attacked_by,
                "attacked_at": self.attacked_at,
                "first_attack_at": self.first_attack_at,
                "modified_by": self.modified_by,
                "modified_date": self.modified_date,
            },
        }
