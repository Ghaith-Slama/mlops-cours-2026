from feast import FeatureService
from features import request_features

scoring_v1 = FeatureService(
    name="scoring_v1",
    features=[request_features]
)
