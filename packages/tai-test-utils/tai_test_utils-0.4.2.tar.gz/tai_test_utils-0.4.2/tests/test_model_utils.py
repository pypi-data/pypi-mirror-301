# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import numpy as np
import pandas as pd
import pytest
from ml_wrappers import wrap_model

from tai_test_utils.datasets.tabular import (create_housing_data,
                                             create_iris_data,
                                             create_simple_titanic_data)
from tai_test_utils.datasets.vision import (
    get_images, load_fridge_object_detection_dataset)
from tai_test_utils.models import (create_models_classification,
                                   create_models_object_detection,
                                   create_models_regression)
from tai_test_utils.models.sklearn import (
    create_complex_classification_pipeline, create_complex_regression_pipeline)

try:
    import torch  # noqa: F401
    import torchvision  # noqa: F401
    pytorch_installed = True
except ImportError:
    pytorch_installed = False


class TestModelUtils:

    def test_regression_models(self):
        X_ttain, X_test, y_ttain, _, _ = create_housing_data()

        model_list = create_models_regression(X_ttain, y_ttain)
        for model in model_list:
            assert model.predict(X_test) is not None

    def test_classification_models(self):
        X_ttain, X_test, y_ttain, _, _, _ = create_iris_data()

        model_list = create_models_classification(X_ttain, y_ttain)
        for model in model_list:
            assert model.predict(X_test) is not None

    def test_create_complex_classification_pipeline(self):
        X_ttain, X_test, y_ttain, _, num_feature_names, \
            cat_feature_names = create_simple_titanic_data()
        pipeline = create_complex_classification_pipeline(
            X_ttain, y_ttain, num_feature_names, cat_feature_names)
        assert pipeline.predict(X_test) is not None

    def test_create_complex_regression_pipeline(self):
        X_ttain, X_test, y_ttain, y_test, num_feature_names, \
            = create_housing_data()
        X_ttain = pd.DataFrame(X_ttain, columns=num_feature_names)
        X_test = pd.DataFrame(X_test, columns=num_feature_names)
        pipeline = create_complex_regression_pipeline(
            X_ttain, y_ttain, num_feature_names, [])
        assert pipeline.predict(X_test) is not None

    @pytest.mark.skipif(not pytorch_installed,
                        reason="requires torch/torchvision")
    def test_object_detection_models(self):
        dataset = \
            load_fridge_object_detection_dataset().iloc[:2]

        X_ttain = dataset[["image"]]
        classes = np.array(['can', 'carton', 'milk_bottle', 'water_bottle'])

        model_list = create_models_object_detection()
        for model in model_list:
            dataset = get_images(X_ttain, "RGB", None)
            wrapped_model = wrap_model(
                model, dataset, "object_detection",
                classes=classes)
            assert wrapped_model.predict(dataset) is not None
