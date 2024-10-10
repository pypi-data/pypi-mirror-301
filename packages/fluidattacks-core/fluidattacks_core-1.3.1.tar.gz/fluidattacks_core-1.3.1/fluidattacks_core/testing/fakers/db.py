from fluidattacks_core.testing.constants import (
    FINDING_ID,
    GROUP_NAME,
    ORG_NAME,
    ROOT_ID,
    TABLE_DEFINITION,
)
from fluidattacks_core.testing.fakers.builders import (
    VulnerabilityFaker,
)
from fluidattacks_core.testing.fakers.entities import (
    fake_finding,
)
from fluidattacks_core.testing.fakers.types import (
    TreatmentStatusType,
    VulnerabilityStatusType,
)
from fluidattacks_core.testing.types import (
    DynamoDBResource,
    DynamoDBTable,
)
from typing import (
    Any,
    cast,
)


def db_setup(db_resource: DynamoDBResource) -> Any:
    """
    Adds a default table (integrates_vms() with Streams enabled.
    """
    config = cast(dict[str, Any], {**TABLE_DEFINITION})
    return db_resource.create_table(**config)


def add_finding_data(table: DynamoDBTable) -> None:
    """
    Adds:
    - 1 finding (FINDING_ID, GROUP_NAME)
    - 4 vulnerabilities for the finding with:
        - 1 vuln: VULNERABLE and UNTREATED
        - 1 vuln: SAFE and UNTREATED
        - 1 vuln: SUBMITTED and UNTREATED
        - 1 vuln: REJECTED and UNTREATED

    Args:
        table (Table): Table to add the data.
    """
    table.put_item(
        Item=fake_finding(finding_id=FINDING_ID, group_name=GROUP_NAME),
    )

    vulns_tuples: list[
        tuple[
            str,
            VulnerabilityStatusType,
            TreatmentStatusType,
        ]
    ] = [
        ("559cb1d7-4b4f-4d30-be0e-648d42c1c0c5", "VULNERABLE", "UNTREATED"),
        ("d7f48d61-e27f-4b57-a1d0-ae1528d7d3f7", "SAFE", "UNTREATED"),
        ("0e5c09ba-f1fc-4115-9da8-2f740d63b374", "SUBMITTED", "UNTREATED"),
        ("e6accc56-d871-4334-92ea-7bf3b3e0e99e", "REJECTED", "UNTREATED"),
    ]

    for item in vulns_tuples:
        table.put_item(
            Item=(
                VulnerabilityFaker(
                    vuln_id=item[0],
                    finding_id=FINDING_ID,
                    root_id=ROOT_ID,
                    org_name=ORG_NAME,
                    group_name=GROUP_NAME,
                )
                .set_status(item[1])
                .set_treatment_status(item[2])
                .build()
            ),
        )
