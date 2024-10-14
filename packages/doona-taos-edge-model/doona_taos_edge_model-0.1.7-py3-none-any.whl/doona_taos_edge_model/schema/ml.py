from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class MlModelType(str, Enum):
    regression = "regression"
    classification = "classification"


class MlScalerType(str, Enum):
    standard_scaler = "standard_scaler"
    min_max_scaler = "min_max_scaler"
    max_abs_scaler = "max_abs_scaler"
    robust_scaler = "robust_scaler"


class RegressionModel(str, Enum):
    decision_tree_regression = "decision_tree_regression"
    elastic_net_regression = "elastic_net_regression"
    gradient_boosting_regression = "gradient_boosting_regression"
    lasso_regression = "lasso_regression"
    random_forest_regression = "random_forest_regression"
    ridge_regression = "ridge_regression"
    svm_regression = "svm_regression"


class ClassificationModel(str, Enum):
    ada_boost_classification = "ada_boost_classification"
    decision_tree_classification = "decision_tree_classification"
    gradient_boosting_classification = "gradient_boosting_classification"
    kneighbors_classification = "kneighbors_classification"
    lightgbm_classification = "lightgbm_classification"
    svm_classification = "svm_classification"
    xgboost_classification = "xgboost_classification"


class ScoringType(str, Enum):
    r2 = "r2"
    accuracy = "accuracy"


class ScikitClassificationReport(BaseModel):
    precision: float
    recall: float
    f1_score: float
    support: int


class MlModelTrainResult(BaseModel):
    model: Optional[str] = Field(None)
    best_params: Optional[dict] = Field(None)
    best_score: Optional[float] = Field(None)
    score_test: Optional[float] = Field(None)
    score_train: Optional[float] = Field(None)
    plot_url: Optional[str] = Field(None)
    train_duration: Optional[str] = Field(None)

    # regression
    r2_score: Optional[float] = Field(None)
    mse: Optional[float] = Field(None)
    mse_train: Optional[float] = Field(None)
    rmse: Optional[float] = Field(None)
    rmse_train: Optional[float] = Field(None)

    # classification
    accuracy_score: Optional[float] = Field(None)
    confusion_matrix: Optional[List[List[int]]] = Field(None)
    classification_report: Optional[Dict[str, ScikitClassificationReport]] = Field(None)