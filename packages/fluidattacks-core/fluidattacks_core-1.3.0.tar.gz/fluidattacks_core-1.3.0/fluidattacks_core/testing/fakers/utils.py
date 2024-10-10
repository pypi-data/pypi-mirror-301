import boto3 as _boto3
from decimal import (
    Decimal,
)
from fluidattacks_core.testing.constants import (
    TABLE_NAME,
)
from fluidattacks_core.testing.types import (
    DynamoStreamsClient,
)


def get_cvssf_score(temporal_score: Decimal) -> Decimal:
    return Decimal(
        pow(Decimal("4.0"), Decimal(temporal_score) - Decimal("4.0"))
    ).quantize(Decimal("0.001"))


def get_streams_records() -> tuple:
    streams: DynamoStreamsClient = _boto3.client("dynamodbstreams")

    stream_arn = streams.list_streams(TableName=TABLE_NAME)["Streams"][0][
        "StreamArn"
    ]

    shard_id = streams.describe_stream(StreamArn=stream_arn)[
        "StreamDescription"
    ]["Shards"][0]["ShardId"]

    shard_iterator = streams.get_shard_iterator(
        StreamArn=stream_arn,
        ShardId=shard_id,
        ShardIteratorType="TRIM_HORIZON",
    )["ShardIterator"]

    records = streams.get_records(ShardIterator=shard_iterator)["Records"]

    return tuple(records)
