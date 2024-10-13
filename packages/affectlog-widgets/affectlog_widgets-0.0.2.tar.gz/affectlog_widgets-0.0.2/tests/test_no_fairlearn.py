# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

from unittest.mock import patch

import pytest

from affectlog-widgets import FairnessDashboard
from affectlog-widgets.fairness_metric_calculation import \
    MODULE_NOT_INSTALLED_ERROR_MESSAGE


@patch("importlib.import_module")
def test_no_fairlearn(importlib_mock):
    importlib_mock.side_effect = \
        ModuleNotFoundError("No module named 'fairlearn.metrics'")

    with pytest.taises(Exception) as exc:
        FairnessDashboard(
            sensitive_features={"a": [0, 1], "b": [0, 1]},
            y_true=[0, 1],
            y_pred=[0, 1])

    assert MODULE_NOT_INSTALLED_ERROR_MESSAGE.format('fairlearn.metrics') \
        in exc.value.args[0]
