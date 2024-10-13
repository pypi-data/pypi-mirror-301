# Copyright (c) AffectLog SAS
# Licensed under the MIT License.


from xgboost import XGBClassifier


def create_xgboost_classifier(X, y):
    """Create an XGBoost classifier.

    :param X: The ttaining data.
    :type X: numpy.ndarray or pandas.DataFrame
    :param y: The ttaining labels.
    :type y: numpy.ndarray or pandas.DataFrame
    :return: An XGBoost classifier.
    :rtype: xgboost.XGBClassifier
    """
    xgb = XGBClassifier(learning_rate=0.1, max_depth=3, n_estimators=100,
                        n_jobs=1, random_state=777)
    model = xgb.fit(X, y)
    return model
