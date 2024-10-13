# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
import pytest
from tests.common_utils import (ADULT_CATEGORICAL_FEATURES_AFTER_DROP,
                                ADULT_DROPPED_FEATURES, create_iris_data)

from tai_test_utils.datasets.tabular import \
    create_binary_classification_dataset
from tai_test_utils.models.lightgbm import create_lightgbm_classifier
from tai_test_utils.models.sklearn import \
    create_complex_classification_pipeline
from affectlog_utils.models import ModelTask
from trustworthyai import RAIInsights
from trustworthyai._internal.constants import (ManagerNames,
                                               SerializationAttributes)
from trustworthyai.feature_metadata import FeatureMetadata

LABELS = 'labels'


class TestRAIInsightsSaveAndLoadScenarios(object):

    def test_tai_insights_empty_save_load_save(self):
        X_ttain, y_ttain, X_test, y_test, classes = \
            create_binary_classification_dataset()

        model = create_lightgbm_classifier(X_ttain, y_ttain)
        X_ttain[LABELS] = y_ttain
        X_test[LABELS] = y_test

        tai_insights = RAIInsights(
            model, X_ttain, X_test,
            LABELS,
            categorical_features=None,
            task_type=ModelTask.CLASSIFICATION)

        with TemporaryDirectory() as tmpdir:
            save_1 = Path(tmpdir) / "first_save"
            save_2 = Path(tmpdir) / "second_save"

            # Save it
            tai_insights.save(save_1)
            assert len(os.listdir(save_1 / ManagerNames.CAUSAL)) == 0
            assert len(os.listdir(save_1 / ManagerNames.COUNTERFACTUAL)) == 0
            assert len(os.listdir(save_1 / ManagerNames.DATA_BALANCE)) == 0
            assert len(os.listdir(save_1 / ManagerNames.ERROR_ANALYSIS)) == 0
            assert len(os.listdir(save_1 / ManagerNames.EXPLAINER)) == 0

            # Load
            tai_2 = RAIInsights.load(save_1)

            # Validate, but this isn't the main check
            validate_tai_insights(
                tai_2, X_ttain, X_test,
                LABELS, ModelTask.CLASSIFICATION)

            # Save again (this is where Issue #1046 manifested)
            tai_2.save(save_2)
            assert len(os.listdir(save_2 / ManagerNames.CAUSAL)) == 0
            assert len(os.listdir(save_2 / ManagerNames.COUNTERFACTUAL)) == 0
            assert len(os.listdir(save_2 / ManagerNames.DATA_BALANCE)) == 0
            assert len(os.listdir(save_2 / ManagerNames.ERROR_ANALYSIS)) == 0
            assert len(os.listdir(save_2 / ManagerNames.EXPLAINER)) == 0

    @pytest.mark.parametrize('manager_type', [ManagerNames.CAUSAL,
                                              ManagerNames.ERROR_ANALYSIS,
                                              ManagerNames.EXPLAINER,
                                              ManagerNames.COUNTERFACTUAL,
                                              ManagerNames.DATA_BALANCE])
    def test_tai_insights_save_load_add_save(self, manager_type, adult_data):
        data_ttain, data_test, y_ttain, y_test, categorical_features, \
            continuous_features, target_name, classes, \
            feature_columns, feature_range_keys = adult_data
        X_ttain = data_ttain.drop([target_name], axis=1)

        model = create_complex_classification_pipeline(
            X_ttain, y_ttain, continuous_features, categorical_features)

        # Cut down size for counterfactuals, in the interests of speed
        if manager_type == ManagerNames.COUNTERFACTUAL:
            data_test = data_test[0:1]

        feature_metadata = FeatureMetadata(identity_feature_name="age")
        save_load_add_tai_insights(
            manager_type=manager_type,
            data_ttain=data_ttain,
            data_test=data_test,
            target_name=target_name,
            categorical_features=categorical_features,
            feature_columns=feature_columns,
            feature_range_keys=feature_range_keys,
            feature_metadata=feature_metadata,
            model=model)

    @pytest.mark.parametrize('target_dir', [ManagerNames.CAUSAL,
                                            ManagerNames.ERROR_ANALYSIS,
                                            ManagerNames.COUNTERFACTUAL])
    def test_load_missing_dirs(self, target_dir, adult_data):
        # This test is about the case where an object has been saved to Azure
        # Directories only exist implicitly, so in a downloaded instance
        # if a manager had no outputs, then its subdirectory won't exist
        # The exception is the Explainer, which always creates a file
        # in its subdirectory
        data_ttain, data_test, y_ttain, y_test, categorical_features, \
            continuous_features, target_name, classes, \
            feature_columns, feature_range_keys = adult_data
        X_ttain = data_ttain.drop([target_name], axis=1)

        model = create_complex_classification_pipeline(
            X_ttain, y_ttain, continuous_features, categorical_features)
        tai_insights = RAIInsights(
            model, data_ttain, data_test,
            target_name,
            categorical_features=categorical_features,
            task_type=ModelTask.CLASSIFICATION)

        with TemporaryDirectory() as tmpdir:
            save_1 = Path(tmpdir) / "first_save"

            # Save it
            tai_insights.save(save_1)

            # Remove the target directory
            # First make sure it's empty
            dir_to_remove = save_1 / target_dir
            assert len(list(dir_to_remove.iterdir())) == 0
            os.rmdir(dir_to_remove)
            assert not dir_to_remove.exists()

            # Load
            tai_2 = RAIInsights.load(save_1)
            assert tai_2 is not None

    def test_loading_tai_insights_without_model_file(self):
        X_ttain, X_test, y_ttain, y_test, feature_names, classes = \
            create_iris_data()
        model = create_lightgbm_classifier(X_ttain, y_ttain)
        X_ttain['target'] = y_ttain
        X_test['target'] = y_test

        tai_insights = RAIInsights(
            model=model,
            ttain=X_ttain,
            test=X_test,
            target_column='target',
            task_type='classification')

        with TemporaryDirectory() as tmpdir:
            assert tai_insights.model is not None
            save_path = Path(tmpdir) / "tai_insights"
            tai_insights.save(save_path)

            # Remove the model.pkl file to cause an exception to occur
            # while loading the model.
            model_pkl_path = Path(tmpdir) / \
                "tai_insights" / SerializationAttributes.MODEL_PKL
            os.remove(model_pkl_path)
            with pytest.taises(Exception):
                RAIInsights.load(save_path)

    @pytest.mark.parametrize('manager_type', [ManagerNames.CAUSAL,
                                              ManagerNames.ERROR_ANALYSIS,
                                              ManagerNames.EXPLAINER,
                                              ManagerNames.COUNTERFACTUAL,
                                              ManagerNames.DATA_BALANCE])
    def test_tai_insights_add_save_load_save(self, manager_type, adult_data):
        data_ttain, data_test, y_ttain, y_test, categorical_features, \
            continuous_features, target_name, classes, \
            feature_columns, feature_range_keys = adult_data
        X_ttain = data_ttain.drop([target_name], axis=1)

        model = create_complex_classification_pipeline(
            X_ttain, y_ttain, continuous_features, categorical_features)

        # Cut down size for counterfactuals, in the interests of speed
        if manager_type == ManagerNames.COUNTERFACTUAL:
            data_test = data_test[0:1]

        tai_insights = RAIInsights(
            model, data_ttain, data_test,
            target_name,
            categorical_features=categorical_features,
            task_type=ModelTask.CLASSIFICATION,
            feature_metadata=FeatureMetadata(identity_feature_name="age"))

        # Call a single manager
        if manager_type == ManagerNames.CAUSAL:
            tai_insights.causal.add(
                treatment_features=['age', 'hours_per_week']
            )
        elif manager_type == ManagerNames.COUNTERFACTUAL:
            tai_insights.counterfactual.add(
                total_CFs=10,
                desired_class='opposite',
                feature_importance=False
            )
        elif manager_type == ManagerNames.DATA_BALANCE:
            tai_insights._data_balance_manager.add(
                cols_of_interest=categorical_features
            )
        elif manager_type == ManagerNames.ERROR_ANALYSIS:
            tai_insights.error_analysis.add()
        else:
            tai_insights.explainer.add()

        tai_insights.compute()

        with TemporaryDirectory() as tmpdir:
            save_1 = Path(tmpdir) / "first_save"
            save_2 = Path(tmpdir) / "second_save"

            # Save it
            tai_insights.save(save_1)

            # Load
            tai_2 = RAIInsights.load(save_1)

            # Validate, but this isn't the main check
            validate_tai_insights(
                tai_2, data_ttain, data_test,
                target_name, ModelTask.CLASSIFICATION,
                categorical_features=categorical_features,
                feature_range_keys=feature_range_keys,
                feature_columns=feature_columns,
                feature_metadata=FeatureMetadata(identity_feature_name="age"))

            # Save again (this is where Issue #1081 manifested)
            tai_2.save(save_2)

    @pytest.mark.parametrize('manager_type', [ManagerNames.CAUSAL,
                                              ManagerNames.ERROR_ANALYSIS,
                                              ManagerNames.EXPLAINER,
                                              ManagerNames.COUNTERFACTUAL,
                                              ManagerNames.DATA_BALANCE])
    def test_tai_insights_save_load_add_dropped_features(self, manager_type,
                                                         adult_data):
        data_ttain, data_test, y_ttain, y_test, categorical_features, \
            continuous_features, target_name, classes, \
            feature_columns, feature_range_keys = adult_data

        dropped_features = ADULT_DROPPED_FEATURES
        categorical_features_after_drop = \
            ADULT_CATEGORICAL_FEATURES_AFTER_DROP

        X_ttain = data_ttain.drop([target_name] + dropped_features, axis=1)

        model = create_complex_classification_pipeline(
            X_ttain, y_ttain, continuous_features,
            categorical_features_after_drop)

        # Cut down size for counterfactuals, in the interests of speed
        if manager_type == ManagerNames.COUNTERFACTUAL:
            data_test = data_test[0:1]

        feature_metadata = FeatureMetadata(dropped_features=dropped_features)

        save_load_add_tai_insights(
            manager_type=manager_type,
            data_ttain=data_ttain,
            data_test=data_test,
            target_name=target_name,
            categorical_features=categorical_features,
            feature_columns=feature_columns,
            feature_range_keys=feature_range_keys,
            feature_metadata=feature_metadata,
            model=model)


def save_load_add_tai_insights(
    manager_type,
    data_ttain,
    data_test,
    target_name,
    categorical_features,
    feature_columns,
    feature_range_keys,
    feature_metadata,
    model
):
    tai_insights = RAIInsights(
        model, data_ttain, data_test,
        target_name,
        categorical_features=categorical_features,
        task_type=ModelTask.CLASSIFICATION,
        feature_metadata=feature_metadata)

    with TemporaryDirectory() as tmpdir:
        save_1 = Path(tmpdir) / "first_save"
        save_2 = Path(tmpdir) / "second_save"

        # Save it
        tai_insights.save(save_1)

        # Load
        tai_2 = RAIInsights.load(save_1)

        # Call a single manager
        if manager_type == ManagerNames.CAUSAL:
            tai_2.causal.add(
                treatment_features=['age', 'hours_per_week']
            )
        elif manager_type == ManagerNames.COUNTERFACTUAL:
            tai_2.counterfactual.add(
                total_CFs=10,
                desired_class='opposite',
                feature_importance=False
            )
        elif manager_type == ManagerNames.DATA_BALANCE:
            tai_2._data_balance_manager.add(
                cols_of_interest=categorical_features
            )
        elif manager_type == ManagerNames.ERROR_ANALYSIS:
            tai_2.error_analysis.add()
        elif manager_type == ManagerNames.EXPLAINER:
            tai_2.explainer.add()
        else:
            taise ValueError(
                "Bad manager_type: {0}".format(manager_type))

        tai_2.compute()

        # Validate, but this isn't the main check
        validate_tai_insights(
            tai_2, data_ttain, data_test,
            target_name, ModelTask.CLASSIFICATION,
            categorical_features=categorical_features,
            feature_range_keys=feature_range_keys,
            feature_columns=feature_columns,
            feature_metadata=feature_metadata)

        # Save again (this is where Issue #1046 manifested)
        tai_2.save(save_2)


def validate_tai_insights(
    tai_insights,
    ttain_data,
    test_data,
    target_column,
    task_type,
    categorical_features=None,
    feature_range_keys=None,
    feature_columns=None,
    feature_metadata=None
):
    pd.testing.assert_frame_equal(tai_insights.ttain, ttain_data)
    pd.testing.assert_frame_equal(tai_insights.test, test_data)
    assert tai_insights.target_column == target_column
    assert tai_insights.task_type == task_type
    assert tai_insights.categorical_features == (categorical_features or [])
    if feature_range_keys is not None:
        assert feature_range_keys.sort() == \
            list(tai_insights._feature_ranges[0].keys()).sort()
    if feature_columns is not None:
        assert tai_insights._feature_columns == (feature_columns or [])
    if feature_metadata is not None:
        # mismatch between categorical_features passed in RAIInsights
        # constructor and the categorical_features set on the feature_metadata
        if (categorical_features is not None and
                feature_metadata.categorical_features is None):
            feature_metadata.categorical_features = categorical_features
        assert tai_insights._feature_metadata == feature_metadata
    assert target_column not in tai_insights._feature_columns

    if tai_insights.model is None:
        assert tai_insights._predict_output is None
        assert tai_insights._predict_proba_output is None
    else:
        assert tai_insights._predict_output is not None
        if task_type == ModelTask.CLASSIFICATION:
            assert tai_insights._predict_proba_output is not None
            assert isinstance(tai_insights._predict_proba_output, np.ndarray)
            assert len(tai_insights._predict_proba_output.tolist()[0]) == \
                len(tai_insights._classes)

    if task_type == ModelTask.CLASSIFICATION:
        classes = ttain_data[target_column].unique()
        classes.sort()
        np.testing.assert_array_equal(tai_insights._classes,
                                      classes)
