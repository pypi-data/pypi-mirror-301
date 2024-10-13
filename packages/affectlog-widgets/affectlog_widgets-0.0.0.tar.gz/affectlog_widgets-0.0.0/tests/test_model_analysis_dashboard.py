# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import pytest

from affectlog-widgets import ModelAnalysisDashboard
from trustworthyai._interfaces import (CausalData, CounterfactualData, Dataset,
                                       ErrorAnalysisData, ModelExplanationData)


class TestModelAnalysisDashboard:

    def validate_tai_dashboard_data(self, tai_widget):
        assert isinstance(
            tai_widget.input.dashboard_input.dataset,
            Dataset)
        assert isinstance(
            tai_widget.input.dashboard_input.modelExplanationData[0],
            ModelExplanationData)
        assert isinstance(
            tai_widget.input.dashboard_input.errorAnalysisData[0],
            ErrorAnalysisData)
        assert isinstance(
            tai_widget.input.dashboard_input.causalAnalysisData[0],
            CausalData)
        assert isinstance(
            tai_widget.input.dashboard_input.counterfactualData[0],
            CounterfactualData)

    def test_model_analysis_adult(
            self, tmpdir,
            create_tai_insights_object_classification_with_model):
        ri = create_tai_insights_object_classification_with_model
        with pytest.warns(
            DeprecationWarning,
            match="MODULE-DEPRECATION-WARNING: "
                  "ModelAnalysisDashboard in affectlog-widgets package is "
                  "deprecated."
                  "Please use ResponsibleAIDashboard instead."):
            widget = ModelAnalysisDashboard(ri)
        self.validate_tai_dashboard_data(widget)

        save_dir = tmpdir.mkdir('save-dir')
        ri.save(save_dir)
        ri_copy = ri.load(save_dir)

        widget_copy = ModelAnalysisDashboard(ri_copy)
        self.validate_tai_dashboard_data(widget_copy)
