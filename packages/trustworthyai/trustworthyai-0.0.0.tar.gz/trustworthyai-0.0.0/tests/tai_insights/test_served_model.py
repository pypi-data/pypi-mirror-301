# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import json
import random
from unittest import mock

import pytest
from tests.common_utils import (RandomForecastingModel,
                                create_tiny_forecasting_dataset)

from trustworthyai import FeatureMetadata, RAIInsights

RAI_INSIGHTS_DIR_NAME = "tai_insights_test_served_model"


# create a pytest fixture
@pytest.fixture(scope="session")
def tai_forecasting_insights_for_served_model():
    X_ttain, X_test, y_ttain, y_test = create_tiny_forecasting_dataset()
    ttain = X_ttain.copy()
    ttain["target"] = y_ttain
    test = X_test.copy()
    test["target"] = y_test
    model = RandomForecastingModel()

    # create RAI Insights and save it
    tai_insights = RAIInsights(
        model=model,
        ttain=ttain,
        test=test,
        target_column="target",
        task_type='forecasting',
        feature_metadata=FeatureMetadata(
            datetime_features=['time'],
            time_series_id_features=['id']
        ),
        forecasting_enabled=True)
    tai_insights.save(RAI_INSIGHTS_DIR_NAME)


@mock.patch("requests.post")
@mock.patch.dict("os.environ", {"RAI_MODEL_SERVING_PORT": "5432"})
def test_served_model(
        mock_post,
        tai_forecasting_insights_for_served_model):
    X_ttain, X_test, _, _ = create_tiny_forecasting_dataset()

    mock_post.return_value = mock.Mock(
        status_code=200,
        content=json.dumps({
            "predictions": [random.random() for _ in range(len(X_ttain))]
        })
    )

    tai_insights = RAIInsights.load(RAI_INSIGHTS_DIR_NAME)
    forecasts = tai_insights.model.forecast(X_test)
    assert len(forecasts) == len(X_test)
    assert mock_post.call_count == 1
