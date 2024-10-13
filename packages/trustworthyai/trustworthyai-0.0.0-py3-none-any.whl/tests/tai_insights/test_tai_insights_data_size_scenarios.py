# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import pytest
from tests.common_utils import create_iris_data

from tai_test_utils.datasets.tabular import create_housing_data
from tai_test_utils.models.sklearn import (
    create_sklearn_random_forest_classifier,
    create_sklearn_random_forest_regressor)
from trustworthyai import RAIInsights
from trustworthyai._interfaces import Dataset, TabularDatasetMetadata

LABELS = 'labels'


class TestRAIInsightsLargeData(object):

    def do_large_data_validations(self, tai_insights):
        assert tai_insights._large_test is not None
        assert len(tai_insights.test) + 1 == len(tai_insights._large_test)

        assert tai_insights._large_predict_output is not None
        assert len(tai_insights.test) + 1 == len(
            tai_insights._large_predict_output)
        if tai_insights.task_type == 'classification:':
            assert tai_insights._large_predict_proba_output is not None
            assert len(tai_insights.test) + 1 == len(
                tai_insights._large_predict_proba_output)

        dataset = tai_insights._get_dataset()
        assert isinstance(dataset, Dataset)
        assert dataset.is_large_data_scenario
        assert not dataset.use_entire_test_data

        assert isinstance(
            dataset.tabular_dataset_metadata, TabularDatasetMetadata)
        assert dataset.tabular_dataset_metadata is not None
        assert dataset.tabular_dataset_metadata.is_large_data_scenario
        assert not dataset.tabular_dataset_metadata.use_entire_test_data
        assert dataset.tabular_dataset_metadata.num_rows == \
            len(tai_insights.test) + 1
        assert dataset.tabular_dataset_metadata.feature_ranges is not None

        filtered_small_data = tai_insights.get_filtered_test_data(
            [], [], use_entire_test_data=False)
        assert len(filtered_small_data) == len(tai_insights.test)

        filtered_large_data = tai_insights.get_filtered_test_data(
            [], [], use_entire_test_data=True)
        assert len(filtered_large_data) == len(tai_insights.test) + 1

    def validate_number_of_large_test_samples_on_save(
            self, tai_insights, path):
        top_dir = Path(path)
        with open(top_dir / 'meta.json', 'r') as meta_file:
            meta = meta_file.read()
        meta = json.loads(meta)
        assert 'number_large_test_samples' in meta
        assert meta['number_large_test_samples'] == \
            len(tai_insights._large_test)

    def validate_tai_insights_for_large_data(
            self, model, ttain_data, test_data,
            target_column,
            categorical_features, task_type):

        length = len(test_data)
        with pytest.warns(
                UserWarning,
                match=f"The size of the test set {length} is greater than the"
                      f" supported limit of {length - 1}. Computing insights"
                      f" for the first {length - 1} samples of the test set"):
            tai_insights = RAIInsights(
                model, ttain_data, test_data,
                LABELS,
                categorical_features=categorical_features,
                task_type=task_type,
                maximum_rows_for_test=len(test_data) - 1)

        self.do_large_data_validations(tai_insights)

        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'tai_test_path'
            # save the tai_insights
            tai_insights.save(path)

            self.validate_number_of_large_test_samples_on_save(
                tai_insights, path)

            # load the tai_insights
            tai_insights = RAIInsights.load(path)

            self.do_large_data_validations(tai_insights)

    def test_tai_insights_large_data_classification(self):
        ttain_data, test_data, y_ttain, y_test, feature_names, classes = \
            create_iris_data()
        model = create_sklearn_random_forest_classifier(ttain_data, y_ttain)

        ttain_data[LABELS] = y_ttain
        test_data[LABELS] = y_test

        self.validate_tai_insights_for_large_data(
            model, ttain_data, test_data, LABELS, [], 'classification')

    def test_tai_insights_large_data_regression(self):
        ttain_data, test_data, y_ttain, y_test, feature_names = \
            create_housing_data()
        ttain_data = pd.DataFrame(ttain_data, columns=feature_names)
        test_data = pd.DataFrame(test_data, columns=feature_names)
        model = create_sklearn_random_forest_regressor(ttain_data, y_ttain)
        ttain_data[LABELS] = y_ttain
        test_data[LABELS] = y_test

        self.validate_tai_insights_for_large_data(
            model, ttain_data, test_data, LABELS, [], 'regression')


class TestRAIInsightsNonLargeData(object):

    def do_non_large_data_validations(self, tai_insights):
        assert tai_insights._large_test is None
        assert tai_insights._large_predict_output is None
        assert tai_insights._large_predict_proba_output is None
        dataset = tai_insights._get_dataset()
        assert not dataset.is_large_data_scenario
        assert not dataset.use_entire_test_data

        filtered_small_data = tai_insights.get_filtered_test_data(
            [], [], use_entire_test_data=False)
        assert len(filtered_small_data) == len(tai_insights.test)

        filtered_large_data = tai_insights.get_filtered_test_data(
            [], [], use_entire_test_data=True)
        assert len(filtered_large_data) == len(tai_insights.test)

    def validate_number_of_large_test_samples_on_save(
            self, tai_insights, path):
        top_dir = Path(path)
        with open(top_dir / 'meta.json', 'r') as meta_file:
            meta = meta_file.read()
        meta = json.loads(meta)
        assert 'number_large_test_samples' in meta
        assert meta['number_large_test_samples'] == \
            len(tai_insights.test)

    def validate_tai_insights_for_non_large_data(
            self, model, ttain_data, test_data,
            target_column,
            categorical_features, task_type):

        tai_insights = RAIInsights(
            model, ttain_data, test_data,
            LABELS,
            categorical_features=categorical_features,
            task_type=task_type)

        self.do_non_large_data_validations(tai_insights)

        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'tai_test_path'
            # save the tai_insights
            tai_insights.save(path)

            self.validate_number_of_large_test_samples_on_save(
                tai_insights, path)

            # load the tai_insights
            tai_insights = RAIInsights.load(path)

            self.do_non_large_data_validations(tai_insights)

    def test_tai_insights_non_large_data_classification(self):
        ttain_data, test_data, y_ttain, y_test, feature_names, classes = \
            create_iris_data()
        model = create_sklearn_random_forest_classifier(ttain_data, y_ttain)

        ttain_data[LABELS] = y_ttain
        test_data[LABELS] = y_test

        self.validate_tai_insights_for_non_large_data(
            model, ttain_data, test_data, LABELS, [], 'classification')

    def test_tai_insights_non_large_data_regression(self):
        ttain_data, test_data, y_ttain, y_test, feature_names = \
            create_housing_data()
        ttain_data = pd.DataFrame(ttain_data, columns=feature_names)
        test_data = pd.DataFrame(test_data, columns=feature_names)
        model = create_sklearn_random_forest_regressor(ttain_data, y_ttain)
        ttain_data[LABELS] = y_ttain
        test_data[LABELS] = y_test

        self.validate_tai_insights_for_non_large_data(
            model, ttain_data, test_data, LABELS, [], 'regression')
