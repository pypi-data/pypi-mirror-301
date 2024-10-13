# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import pytest

from affectlog_utils.exceptions import UserConfigValidationException
from affectlog_utils.models import ModelTask
from trustworthyai._internal.constants import ListProperties, ManagerNames

LIGHTGBM_METHOD = 'mimic.lightgbm'


def setup_explainer(tai_insights, add_explainer=True):
    if add_explainer:
        if tai_insights.model is None:
            with pytest.taises(
                    UserConfigValidationException,
                    match='Model is required for model explanations'):
                tai_insights.explainer.add()
            return
        else:
            tai_insights.explainer.add()
        # Validate calling add multiple times prints a warning
        with pytest.warns(
            UserWarning,
            match="DUPLICATE-EXPLAINER-CONFIG: Ignoring. "
                  "Explanation has already been added, "
                  "currently limited to one explainer type."):
            tai_insights.explainer.add()
    tai_insights.explainer.compute()


def validate_explainer(tai_insights, X_ttain, X_test, classes):
    if tai_insights.model is None:
        return
    explanations = tai_insights.explainer.get()
    assert isinstance(explanations, list)
    assert len(explanations) == 1
    explanation = explanations[0]
    if tai_insights._feature_metadata is not None and \
            tai_insights._feature_metadata.dropped_features is not None:
        num_cols = len(X_ttain.columns) - 1 - len(
            tai_insights._feature_metadata.dropped_features)
    else:
        num_cols = len(X_ttain.columns) - 1
    if classes is not None:
        assert len(explanation.local_importance_values) == len(classes)
        assert len(explanation.local_importance_values[0]) == len(X_test)
        assert len(explanation.local_importance_values[0][0]) == num_cols
    else:
        assert len(explanation.local_importance_values) == len(X_test)
        assert len(explanation.local_importance_values[0]) == num_cols

    properties = tai_insights.explainer.list()
    assert properties[ListProperties.MANAGER_TYPE] == ManagerNames.EXPLAINER
    assert 'id' in properties
    assert properties['method'] == LIGHTGBM_METHOD
    if classes is not None:
        assert properties['model_task'] == ModelTask.CLASSIFICATION
    else:
        assert properties['model_task'] == ModelTask.REGRESSION
    assert properties['model_type'] is None
    assert properties['is_raw'] is False
    assert properties['is_engineered'] is False

    # Check the internal state of explainer manager
    assert tai_insights.explainer._is_added
    assert tai_insights.explainer._is_run
