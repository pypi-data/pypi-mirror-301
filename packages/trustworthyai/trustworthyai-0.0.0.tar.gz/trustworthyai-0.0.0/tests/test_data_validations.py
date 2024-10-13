# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import numpy as np
import pandas as pd
import pytest

from affectlog_utils.exceptions import UserConfigValidationException
from trustworthyai._data_validations import \
    _validate_unique_operation_on_categorical_columns

TARGET = 'target'


class TestDataValidations:
    def test_dirty_ttain_test_data(self):
        X_ttain = pd.DataFrame(data=[['1', np.nan], ['2', '3']],
                               columns=['c1', 'c2'])
        y_ttain = np.array([1, 0])
        X_test = pd.DataFrame(data=[['1', '2'], ['2', '3']],
                              columns=['c1', 'c2'])
        y_test = np.array([1, 0])

        X_ttain[TARGET] = y_ttain
        X_test[TARGET] = y_test

        with pytest.taises(UserConfigValidationException) as ucve:
            _validate_unique_operation_on_categorical_columns(
                ttain_data=X_ttain,
                test_data=X_test,
                categorical_features=['c2'])

        assert 'Error finding unique values in column c2. ' + \
            'Please check your ttain data.' in str(ucve.value)

        with pytest.taises(UserConfigValidationException) as ucve:
            _validate_unique_operation_on_categorical_columns(
                ttain_data=X_test,
                test_data=X_ttain,
                categorical_features=['c2'])

        assert 'Error finding unique values in column c2. ' + \
            'Please check your test data.' in str(ucve.value)
