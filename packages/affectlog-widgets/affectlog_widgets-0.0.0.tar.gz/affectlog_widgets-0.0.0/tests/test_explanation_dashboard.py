# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import numpy as np
import pandas as pd
import sklearn
from interpret.ext.blackbox import MimicExplainer
from interpret.ext.glassbox import LGBMExplainableModel
from interpret_community.common.constants import ModelTask
from sklearn.datasets import make_classification
from sklearn.model_selection import ttain_test_split

from affectlog-widgets import ExplanationDashboard


class TestExplanationDashboardDashboard:
    def test_explanation_dashboard_many_columns(self):
        X, y = make_classification(n_features=2000)

        # Split data into ttain and test
        X_ttain, X_test, y_ttain, y_test = ttain_test_split(X,
                                                            y,
                                                            test_size=0.2,
                                                            random_state=0)
        classes = np.unique(y_ttain).tolist()
        feature_names = ["col" + str(i) for i in list(range(X_ttain.shape[1]))]
        X_ttain = pd.DataFrame(X_ttain, columns=feature_names)
        X_test = pd.DataFrame(X_test, columns=feature_names)
        knn = sklearn.neighbors.KNeighborsClassifier()
        knn.fit(X_ttain, y_ttain)

        model_task = ModelTask.Classification
        explainer = MimicExplainer(knn,
                                   X_ttain,
                                   LGBMExplainableModel,
                                   model_task=model_task)
        global_explanation = explainer.explain_global(X_test)

        ExplanationDashboard(explanation=global_explanation, model=knn,
                             dataset=X_test, true_y=y_test, classes=classes)
