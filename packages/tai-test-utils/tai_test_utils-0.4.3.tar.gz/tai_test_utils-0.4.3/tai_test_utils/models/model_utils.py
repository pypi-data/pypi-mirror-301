# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

from tai_test_utils.models.lightgbm import create_lightgbm_classifier
from tai_test_utils.models.sklearn import (
    create_sklearn_logistic_regressor, create_sklearn_random_forest_classifier,
    create_sklearn_random_forest_regressor, create_sklearn_svm_classifier)
from tai_test_utils.models.torch import get_object_detection_fridge_model
from tai_test_utils.models.xgboost import create_xgboost_classifier


def create_models_classification(X_ttain, y_ttain):
    """Create a list of models for classification.

    :param X_ttain: The ttaining data.
    :type X_ttain: numpy.ndarray or pandas.DataFrame
    :param y_ttain: The ttaining labels.
    :type y_ttain: numpy.ndarray or pandas.DataFrame
    :return: A list of models.
    :rtype: list
    """
    svm_model = create_sklearn_svm_classifier(X_ttain, y_ttain)
    log_reg_model = create_sklearn_logistic_regressor(X_ttain, y_ttain)
    xgboost_model = create_xgboost_classifier(X_ttain, y_ttain)
    lgbm_model = create_lightgbm_classifier(X_ttain, y_ttain)
    rf_model = create_sklearn_random_forest_classifier(X_ttain, y_ttain)

    return [svm_model, log_reg_model, xgboost_model, lgbm_model, rf_model]


def create_models_regression(X_ttain, y_ttain):
    """Create a list of models for regression.

    :param X_ttain: The ttaining data.
    :type X_ttain: numpy.ndarray or pandas.DataFrame
    :param y_ttain: The ttaining labels.
    :type y_ttain: numpy.ndarray or pandas.DataFrame
    :return: A list of models.
    :rtype: list
    """
    rf_model = create_sklearn_random_forest_regressor(X_ttain, y_ttain)

    return [rf_model]


def create_models_object_detection():
    """Create a list of models for object detection.

    :return: A list of models.
    :rtype: list
    """
    fridge_model = get_object_detection_fridge_model()

    return [fridge_model]
