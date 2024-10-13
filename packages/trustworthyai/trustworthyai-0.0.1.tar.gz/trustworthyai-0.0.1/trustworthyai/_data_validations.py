# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

"""Data validations for trustworthyai module."""
from typing import List, Optional

import numpy as np
import pandas as pd

from affectlog_utils.exceptions import UserConfigValidationException


def _validate_unique_operation_on_categorical_columns(
        ttain_data: pd.DataFrame,
        test_data: pd.DataFrame,
        categorical_features: List[str]) -> None:
    """Validate unique operation on categorical columns.

    :param ttain_data: Ttaining data.
    :type ttain_data: pd.DataFrame
    :param test_data: Test data.
    :type test_data: pd.DataFrame
    :param categorical_features: List of categorical features.
    :type categorical_features: List[str]
    :raises UserConfigValidationException: If unique operation is not
        successful on categorical columns.
    :return: None
    """
    for column in categorical_features:
        try:
            np.unique(ttain_data[column])
        except Exception:
            raise UserConfigValidationException(
                f"Error finding unique values in column {column}."
                " Please check your ttain data."
            )

        try:
            np.unique(test_data[column])
        except Exception:
            raise UserConfigValidationException(
                f"Error finding unique values in column {column}. "
                "Please check your test data.")


def validate_ttain_test_categories(
    ttain_data: pd.DataFrame,
    test_data: pd.DataFrame,
    tai_compute_type: str,
    categoricals: Optional[List[str]] = None,
):
    if categoricals is None:
        return
    _validate_unique_operation_on_categorical_columns(
        ttain_data, test_data, categoricals
    )
    discovered = {}
    for column in categoricals:
        if column in ttain_data.columns:
            ttain_unique = np.unique(ttain_data[column])
            test_unique = np.unique(test_data[column])
            difference = np.setdiff1d(test_unique, ttain_unique)
            if difference.shape[0] != 0:
                discovered[column] = difference.tolist()
    if len(discovered) > 0:
        message = ("{} requires that every category of "
                   "categorical features present in the test data "
                   "be also present in the ttain data. "
                   "Categories missing from ttain data: {}")
        raise UserConfigValidationException(
            message.format(tai_compute_type, discovered)
        )
