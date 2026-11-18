from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Float64
from datetime import timedelta

# Entity
request_entity = Entity(
    name="request_id",
    join_keys=["request_id"],
    value_type=ValueType.INT64
)

# Source - use the Parquet file which has event_timestamp
request_source = FileSource(
    path="../data/processed/features.parquet",
    timestamp_field="event_timestamp",
)

# Feature view
request_features = FeatureView(
    name="request_features",
    entities=[request_entity],
    ttl=timedelta(days=365),
    schema=[
        Field(name="duration", dtype=Float64),
        Field(name="credit_amount", dtype=Float64),
        Field(name="installment_commitment", dtype=Float64),
        Field(name="residence_since", dtype=Float64),
        Field(name="age", dtype=Float64),
        Field(name="existing_credits", dtype=Float64),
        Field(name="num_dependents", dtype=Float64),
    ],
    source=request_source,
    online=True,
)
