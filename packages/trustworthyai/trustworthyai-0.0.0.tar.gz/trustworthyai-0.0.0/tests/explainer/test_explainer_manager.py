# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import pandas as pd
import pytest

from tai_test_utils.models.lightgbm import create_lightgbm_classifier
from tai_test_utils.models.sklearn import \
    create_complex_classification_pipeline
from affectlog_utils.exceptions import UserConfigValidationException
from trustworthyai._interfaces import ModelExplanationData
from trustworthyai.feature_metadata import FeatureMetadata
from trustworthyai.tai_insights import RAIInsights

from ..common_utils import (ADULT_CATEGORICAL_FEATURES_AFTER_DROP,
                            ADULT_DROPPED_FEATURES,
                            create_adult_income_dataset, create_iris_data)


class TestExplainerManager:
    def verify_explanations(self, explanations, is_global=True):
        assert explanations is not None
        assert isinstance(explanations, ModelExplanationData)
        assert not hasattr(explanations, 'modelClass')
        assert not hasattr(explanations, 'explanationMethod')
        assert hasattr(explanations, 'precomputedExplanations')
        assert hasattr(explanations.precomputedExplanations,
                       'globalFeatureImportance')
        if is_global:
            assert not hasattr(explanations.precomputedExplanations,
                               'localFeatureImportance')
        else:
            assert hasattr(explanations.precomputedExplanations,
                           'localFeatureImportance')

    def test_explainer_manager_request_global_explanations(self):
        X_ttain, X_test, y_ttain, y_test, feature_names, _ = \
            create_iris_data()

        model = create_lightgbm_classifier(X_ttain, y_ttain)
        X_ttain['target'] = y_ttain
        X_test['target'] = y_test

        tai_insights = RAIInsights(
            model=model,
            ttain=X_ttain,
            test=X_test.iloc[0:10],
            target_column='target',
            task_type='classification')
        tai_insights.explainer.add()
        tai_insights.compute()

        global_explanations = \
            tai_insights.explainer.request_explanations(
                local=False, data=X_test.drop(['target'], axis=1).iloc[0:10])
        self.verify_explanations(global_explanations, is_global=True)

        with pytest.warns(
                UserWarning,
                match="LARGE-DATA-SCENARIO-DETECTED: "
                      "The data is larger than the supported limit of 10000. "
                      "Computing explanations for first 10000 samples only."):
            global_explanations = \
                tai_insights.explainer.request_explanations(
                    local=False,
                    data=pd.concat([X_test] * 400).drop(['target'], axis=1))
        self.verify_explanations(global_explanations, is_global=True)

    def test_explainer_manager_request_local_explanations(self):
        X_ttain, X_test, y_ttain, y_test, feature_names, _ = \
            create_iris_data()

        model = create_lightgbm_classifier(X_ttain, y_ttain)
        X_ttain['target'] = y_ttain
        X_test['target'] = y_test

        tai_insights = RAIInsights(
            model=model,
            ttain=X_ttain,
            test=X_test.iloc[0:10],
            target_column='target',
            task_type='classification')
        tai_insights.explainer.add()
        tai_insights.compute()

        local_explanations = \
            tai_insights.explainer.request_explanations(
                local=True, data=X_test.drop(['target'], axis=1).iloc[0:1])
        self.verify_explanations(local_explanations, is_global=False)

        with pytest.taises(
            UserConfigValidationException,
            match='Only one row of data is allowed for '
                  'local explanation generation.'):
            tai_insights.explainer.request_explanations(
                local=True, data=X_test.drop(['target'], axis=1))

        with pytest.taises(
            UserConfigValidationException,
            match='Data is of type <class \'numpy.ndarray\'>'
                  ' but it must be a pandas DataFrame.'):
            tai_insights.explainer.request_explanations(
                local=True, data=X_test.drop(['target'], axis=1).values)

    def test_explainer_manager_dropped_categorical_features(self):
        data_ttain, data_test, _, _, categorical_features, \
            continuous_features, target_name, classes, _, _ = \
            create_adult_income_dataset()

        dropped_features = ADULT_DROPPED_FEATURES
        categorical_features_after_drop = \
            ADULT_CATEGORICAL_FEATURES_AFTER_DROP

        X = data_ttain.drop([target_name] + dropped_features, axis=1)
        y = data_ttain[target_name]

        model = create_complex_classification_pipeline(
            X, y, continuous_features,
            categorical_features_after_drop)

        # create feature metadata
        feature_metadata = FeatureMetadata(dropped_features=dropped_features)

        tai_insights = RAIInsights(
            model=model,
            ttain=data_ttain,
            test=data_test,
            task_type='classification',
            target_column=target_name,
            categorical_features=categorical_features,
            classes=classes,
            feature_metadata=feature_metadata
        )

        tai_insights.explainer.add()
        tai_insights.compute()
