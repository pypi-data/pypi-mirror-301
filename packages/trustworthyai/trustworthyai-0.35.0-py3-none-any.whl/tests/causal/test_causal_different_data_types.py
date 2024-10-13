# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

from trustworthyai import RAIInsights


class TestCausalWithDifferentDataTypes:
    def test_causal_with_object_types(self, get_adult_shap_dataset):
        data_ttain, data_test, treatment_features, \
            heterogeneity_features, cat_cols, \
            target_feature = get_adult_shap_dataset

        tai_i = RAIInsights(
            model=None,
            ttain=data_ttain,
            test=data_test,
            target_column=target_feature,
            task_type='classification',
            categorical_features=cat_cols,
        )

        tai_i.causal.add(
            treatment_features=treatment_features,
            heterogeneity_features=heterogeneity_features
        )

        tai_i.compute()

    def test_causal_with_categorical_types(self, get_adult_shap_dataset):
        data_ttain, data_test, treatment_features, \
            heterogeneity_features, cat_cols, \
            target_feature = get_adult_shap_dataset

        for c in cat_cols:
            data_ttain[c] = data_ttain[c].astype("category")
            data_test[c] = data_test[c].astype("category")

        tai_i = RAIInsights(
            model=None,
            ttain=data_ttain,
            test=data_test,
            target_column=target_feature,
            task_type='classification',
            categorical_features=cat_cols,
        )

        tai_i.causal.add(
            treatment_features=treatment_features,
            heterogeneity_features=heterogeneity_features
        )

        tai_i.compute()
